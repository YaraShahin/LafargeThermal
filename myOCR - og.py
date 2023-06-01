import cv2
import pytesseract as tess
import numpy as np
import csv
import os
import datetime as dt

def show(frame):
    cv2.imshow("frame", frame)
    #cv2.waitKey()

def process_text(str):
    num = ""
    nums = []
    for ch in str:
        if (ch=='1' or ch=='2' or ch=='3' or ch=='4' or ch=='5' or ch=='6' or ch=='7' or ch=='8' or ch=='9' or ch=='0'):
            if (len(num)<3):
                num+=ch
        else:
            if(ch=='.' and len(num)<4):
                print(num)
                nums.append(num)
            num = ""
    return nums

def process_frame(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    show(img)
    img = img[:,0:185]
    text = tess.image_to_string(img, lang = 'eng', config='--psm 11')
    text = text.strip()
    return text

if __name__ == "__main__":
    tess.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    os.chdir("C:\\Users\\Lafarge-LCE\\Downloads\\Lafarge-ws\\ocr")

    file = open("data.csv", 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(["Time stamp", "Box 1", "Box 2", "Box 3", "Box 4", "Box 5", "Box 6", "Box 7", "Box 8", "Box 9", "Box 10", "Box 11", "Box 12", "Box 13", "Box 14", "Box 15", "Box 16", "Box 17", "Box 18", "Box 19", "Box 20", "Box 21"])

    video = cv2.VideoCapture("rtsp://admin:Lafarge@2020@192.168.0.108:554/Streaming/Channels/101")
    counter = 0
    while True:
        ret, frame = video.read()
        if (not ret):
            print("No more frames")
            break
        counter+=1
        if counter%100==0:
            txt = process_frame(frame)
            nums = process_text(txt)
            row = [dt.datetime.now()]
            row.extend(nums)
            writer.writerow(row)
            print("-------------------")
        cv2.waitKey(1)
    video.release()
    cv2.destroyAllWindows()