import cv2
import pytesseract as tess
import csv
import os
import datetime as dt

def show(frame):
    cv2.imshow("frame", frame)
    cv2.waitKey()

def process_text(str):
    num = ""
    nums = []
    cnt = 0
    endcnt = -1
    for ch in str:
        if (ch in digits):
            num+=ch
            if (cnt == endcnt):
                num = ((7-len(num))*'0') + num + 'C'
                print(num)
                nums.append(num)
                num = ""
        else:
            if(ch=='.'):
                num+=ch
                endcnt = cnt+1
            else:
                num = ""
        cnt+=1
    return nums

def process_frame(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #show(img)
    img = img[:,0:185]
    text = tess.image_to_string(img, lang = 'eng', config='--psm 11')
    text = text.strip()
    return text

if __name__ == "__main__":
    #globals
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    bxs = ["Time stamp", "Box 1", "Box 2", "Box 3", "Box 4", "Box 5", "Box 6", "Box 7", "Box 8", "Box 9", "Box 10", "Box 11", "Box 12", "Box 13", "Box 14", "Box 15", "Box 16", "Box 17", "Box 18", "Box 19", "Box 20", "Box 21"]
    
    #OS paths
    tess.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    os.chdir("C:\\Users\\Lafarge-LCE\\Downloads\\Lafarge-ws\\ocr")

    #Initializing historical data file
    dataFile = open("data.csv", 'w', newline='')
    dataWriter = csv.writer(dataFile)
    dataWriter.writerow(bxs)

    video = cv2.VideoCapture("rtsp://admin:Lafarge@2020@192.168.0.108:554/Streaming/Channels/101")
    counter = 0
    while True:
        ret, frame = video.read()
        if (not ret):
            print("No more frames")
            break
        counter+=1
        if (counter==400):
            counter = 0
            
            txt = process_frame(frame)
            nums = process_text(txt)
            nums.extend(["0"]*(21-len(nums)))

            #formatting the temperatures array into the csv files
            timeStamp = str(dt.datetime.now())[0:10]+'_'+str(dt.datetime.now())[11:13]+'-'+str(dt.datetime.now())[14:16]
            row = [timeStamp]
            row.extend(nums)

            #reading per minute file
            readingName = "reading_" + timeStamp + ".csv"
            readingFile = open(readingName, 'x', newline='')
            readingWriter = csv.writer(readingFile)
            reading = zip(*[bxs, row])
            readingWriter.writerows(reading)
            readingFile.close()
			
			#historical data file
            dataWriter.writerow(row)
            
            print("-------------------")
        	
    video.release()
    cv2.destroyAllWindows()