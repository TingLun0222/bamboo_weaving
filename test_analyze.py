import cv2
import sys
import numpy as np
import json

#Ans_img
input_Ans_img='url.jpg'  #Ans
Original_Ans_img = cv2.imread(input_Ans_img)
Ans_img = cv2.resize(Original_Ans_img, (360, 360), interpolation=cv2.INTER_AREA)
Ans_imgHSV = cv2.cvtColor(Ans_img,cv2.COLOR_BGR2HSV)

#test_data
input_test_img='1-1.PNG'
input_test_img='exam/'+input_test_img
Original_test_img = cv2.imread(input_test_img)
test_img = cv2.resize(Original_test_img, (360, 360), interpolation=cv2.INTER_AREA)
test_imgHSV = cv2.cvtColor(test_img,cv2.COLOR_BGR2HSV)

#zoom
x_size = 6
y_size = 6
area_size = x_size * y_size
uint_x_len = Ans_img.shape[0]/x_size
uint_y_len = Ans_img.shape[1]/y_size
Original_uint_x_len = Original_Ans_img.shape[0]/x_size
Original_uint_y_len = Original_Ans_img.shape[1]/y_size
unit_area = uint_x_len*uint_y_len

#eps
hue_eps = 10
area_eps = 0.75
search_eps = 5
#wrong record
wrong_area = []
wrong_times = 0

def hue_check(Uint_test_imgHSV,Uint_Ans_imgHSV):
    temp_area=0
    for i in range(search_eps,uint_x_len-search_eps):
        for j in range(search_eps,uint_y_len-search_eps):
            if Uint_test_imgHSV[i][j][0]+hue_eps>=Uint_Ans_imgHSV[i][j][0] and Uint_test_imgHSV[i][j][0]-hue_eps<=Uint_Ans_imgHSV[i][j][0]:
                temp_area+=1
    if temp_area<=(unit_area-(search_eps*search_eps))*area_eps:
        return True
    else:
        return False

def mark_error(i,j):
    cv2.rectangle(Original_Ans_img, (j * Original_uint_y_len + 5, i * Original_uint_x_len + 5), 
                                    ((j + 1) * Original_uint_y_len - 5, (i + 1) * Original_uint_x_len - 5),
                                    [150, 0, 0], 3)
#check_unit
def check_unit():
    global wrong_times,wrong_area
    for i in range(x_size):
        for j in range(y_size):
            if not hue_check(test_imgHSV[i*uint_x_len:(i-1)*uint_x_len][j*uint_y_len:(j-1)*uint_y_len], 
                             Ans_imgHSV[i*uint_x_len:(i-1)*uint_x_len][j*uint_y_len:(j-1)*uint_y_len]):
                mark_error(i, j)
                wrong_area += [i, j]
                wrong_times += 1

percent = ((area_size-wrong_times)/area_size)*100
jsonStr = { 
    "percent": percent/100, 
    "number": wrong_times, 
    "wrong_area": wrong_area
    }
return_data = json.dumps(jsonStr)
cv2.imwrite(input_Ans_img, Original_Ans_img)
with open('return_data.json', 'w') as f:
    f.write(return_data)
