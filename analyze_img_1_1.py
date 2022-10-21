import cv2
import sys
import numpy as np
import json

#input_data=input("input_data:")
input_data=sys.argv[1]
#input_data="101894.jpg"
OriginalImg = cv2.imread(input_data)
img = cv2.resize(OriginalImg, (360, 360), interpolation=cv2.INTER_AREA)
imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
color_array = np.zeros((5, 5))
wrong_area = []

def Hue(hue):
    if hue >= 72 and hue < 92:#Green
        return 1
    elif hue >= 98 and hue < 113:#Blue
        return 2
    elif hue >= 125 and hue <  180:#Red
        return 3
    else:return 0#unkown

def Color_Detect(colortemp):
    #print(colortemp)
    return int(np.where(colortemp==max(colortemp))[0])

def Unit_Color(img,i,j):
    colortemp = np.array([0, 0, 0, 0])
    for x in range(10, img.shape[0]-10):
        for y in range(10, img.shape[1]-10):
            colortemp[Hue(np.array(img[x][y])[0])]+=1
            #colortemp =  colortemp + np.array(img[x][y])
    color_array[i][j]=Color_Detect(colortemp)

def Sqare_Color(img, size = 5):
    temp_x=0
    for x in range(0, img.shape[0], int(img.shape[0] / size)):
        temp_y=0
        for y in range(0, img.shape[1], int(img.shape[1]/size)):
            Unit_Color(img[x:x+int(img.shape[0] / size), y:y+int(img.shape[1] / size)], temp_x, temp_y)
            #cv2.rectangle(img, (y+30,x+30), (y+int(img.shape[1] / size)-30, x+int(img.shape[0] / size)-30),
            #              [150, 0, 0], 3)
            #cv2.rectangle(img, (y , x), (y + int(img.shape[1] / size) , x + int(img.shape[0] / size) ),
            #              [0, 0, 150], 2)
            temp_y+=1
        temp_x+=1

def Detect_row(data,_i,_j,num=5,array=color_array):
    times=0
    for i in range(_i,num,2):
        for j in range(_j,num,2):
            if array[i][j] != data:
                times+=1
    return times

def Detect_error(maxdata,mindata):
    error_times=0
    error_times+=Detect_row(maxdata, 0, 0)
    error_times+=Detect_row(maxdata, 1, 1)
    error_times+=Detect_row(mindata, 0, 1)
    error_times+=Detect_row(mindata, 1, 0)
    return [error_times,maxdata,mindata]

def Mark_row(data,_i,_j,num=5,array=color_array):
    uint_x=int(OriginalImg.shape[0]/num)
    uint_y=int(OriginalImg.shape[1]/num)
    for i in range(_i,num,2):
        for j in range(_j,num,2):
            if array[i][j] != data:
                cv2.rectangle(OriginalImg, (j * uint_y + 5, i * uint_x + 5), ((j + 1) * uint_y - 5, (i + 1) * uint_x - 5),
                              [150, 0, 0], 3)
                wrong_area.append((i,j))

# def Mark_error():
#     Mark_row(min_error[1], 0, 0)
#     Mark_row(min_error[1], 1, 1)
#     Mark_row(min_error[2], 0, 1)
#     Mark_row(min_error[2], 1, 0)

# def Detect():
#     vals, counts = np.unique(color_array, return_counts=True)
#     for i in range(vals.size):
#         for j in range(i,vals.size):
#             temp_error = Detect_error(vals[i], vals[j])
#             if temp_error[0]< min_error[0]:
#                 min_error = temp_error
#             temp_error = Detect_error(vals[j], vals[i])
#             if temp_error[0]< min_error[0]:
#                 min_error = temp_error
#     Mark_error()
def Mark_error(maxdata,mindata):
    Mark_row(maxdata, 0, 0)
    Mark_row(maxdata, 1, 1)
    Mark_row(mindata, 0, 1)
    Mark_row(mindata, 1, 0)

def Detect():
    min_error = [25,0,0]
    vals, counts = np.unique(color_array, return_counts=True)
    for i in range(vals.size):
        for j in range(i,vals.size):
            temp_error = Detect_error(vals[i], vals[j])
            if temp_error[0]< min_error[0]:
                min_error = temp_error
            temp_error = Detect_error(vals[j], vals[i])
            if temp_error[0]< min_error[0]:
                min_error = temp_error
    Mark_error(min_error[1],min_error[2])
    return min_error[0]
    
#input_data=input("input_data:")
#if __name__ == "__main__" :

Sqare_Color(imgHSV)
number = Detect()
percent = ((25-number)/25)*100
jsonStr = { 
    "percent": percent/100, 
    "number": number, 
    "wrong_area": wrong_area
    }
return_data = json.dumps(jsonStr)
#print(return_data)
# cv2.imshow("ORI",OriginalImg)
# cv2.imshow("img",img)
# print(color_array)
# cv2.waitKey(0)
cv2.imwrite(input_data, OriginalImg)
with open('return_data.json', 'w') as f:
    f.write(return_data)