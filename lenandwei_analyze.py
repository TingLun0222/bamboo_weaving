import cv2
import sys
import numpy as np
import json


class Image:
    def __init__(self, filepath: str, dimensions_filepath: str):
        self.original_img = cv2.imread(filepath)
        with open(dimensions_filepath, 'r') as file:
            dimensions = json.load(file)
        self.img = cv2.resize(self.original_img, (360, 360), interpolation=cv2.INTER_AREA)
        self.img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.x_size = int(dimensions['x_size'])
        self.y_size = int(dimensions['y_size'])
        self.uint_x_len = (int)(self.img.shape[0]/self.x_size)
        self.uint_y_len = (int)(self.img.shape[1]/self.y_size)

    def get_unit_hsv(self, x: int, y: int) -> np.ndarray:
        return self.img_hsv[x*self.uint_x_len:(x+1)*self.uint_x_len, y*self.uint_y_len:(y+1)*self.uint_y_len]


class ExamImage(Image):
    def __init__(self, filepath: str, dimensions_filepath: str):
        super().__init__(filepath, dimensions_filepath)
        self.area_size = self.x_size * self.y_size
        self.uint_x_len = (int)(self.img.shape[0]/self.x_size)
        self.uint_y_len = (int)(self.img.shape[1]/self.y_size)


class AnsImage(Image):
    def __init__(self, filepath: str, dimensions_filepath: str):
        super().__init__(filepath, dimensions_filepath)
        self.original_uint_x_len = (int)(self.original_img.shape[0]/self.x_size)
        self.original_uint_y_len = (int)(self.original_img.shape[1]/self.y_size)
        


    def mark_error(self, i: int, j: int):
        cv2.rectangle(self.original_img, (j * self.original_uint_y_len + 5, i * self.original_uint_x_len + 5),
                                ((j + 1) * self.original_uint_y_len - 5, (i + 1) * self.original_uint_x_len - 5),
                                [150, 0, 0], 5)

class Detector:
    def __init__(self, exam: ExamImage, hue_eps: int = 40, search_eps: int = 10, area_eps: float = 0.2):
        self.exam = exam
        self.hue_eps = hue_eps
        self.search_eps = search_eps
        self.area_eps = area_eps
        self.unit_area = (exam.uint_x_len - search_eps) * (exam.uint_y_len - search_eps)
        self.wrong_area = []

    def hue_search(self, exam_hue, ans_hue):
        pixel_hue_eps = min(180 - abs(ans_hue.astype(int) - exam_hue.astype(int)), abs(ans_hue.astype(int) - exam_hue.astype(int)))
        return pixel_hue_eps < self.hue_eps

    def check_unit(self, ans: AnsImage, x: int, y: int) -> bool:
        exam_unit_hsv = self.exam.get_unit_hsv(x, y)
        ans_unit_hsv = ans.get_unit_hsv(x, y)
        temp_area = 0
        for i in range(self.search_eps, self.exam.uint_x_len - self.search_eps):
            for j in range(self.search_eps, self.exam.uint_y_len - self.search_eps):
                if self.hue_search(exam_unit_hsv[i][j][0], ans_unit_hsv[i][j][0]):
                    temp_area += 1
        if temp_area < self.unit_area * self.area_eps:
            ans.mark_error(x, y)
            self.wrong_area.append((i, j))
        return temp_area >= self.unit_area * self.area_eps
    
    def run_detection(self, ans):
        wrong_times = 0
        for i in range(self.exam.x_size):
            for j in range(self.exam.y_size):
                wrong_times += not self.check_unit(ans, i, j)
        percent = ((self.exam.uint_x_len * self.exam.uint_y_len - wrong_times) / (self.exam.uint_x_len * self.exam.uint_y_len)) * 100
        jsonStr = {
            "percent": percent / 100,
            "number": wrong_times,
            "wrong_area": self.wrong_area
        }
        return json.dumps(jsonStr)
'''    
def mark_error_debug(img,i,j):
    cv2.rectangle(img, (j * (int)(img.shape[1]/6) + 5, i * (int)(img.shape[0]/6) + 5), 
                                    ((j + 1) * (int)(img.shape[1]/6) - 5, (i + 1) * (int)(img.shape[0]/6) - 5),
                                    [150, 0, 0], 3)
def debug(test_img, Ans_img):
    for i in range(6):
        for j in range(6):
            mark_error_debug(Ans_img, i, j)
            mark_error_debug(test_img, i, j)
'''
import os
if __name__ == "__main__":
    '''
    exam = ExamImage(sys.argv[1], sys.argv[2])
    ans = AnsImage("C:\\xampp\\htdocs\\url.jpg", sys.argv[2])
    '''
    exam = ExamImage("C:\\xampp\\htdocs\\exam\\1\\1\\answer.png", "C:\\xampp\\htdocs\\exam\\1\\1\\dimensions.json")
    ans = AnsImage("C:\\xampp\\htdocs\\url.jpg", "C:\\xampp\\htdocs\\exam\\1\\1\\dimensions.json")
    
    detector = Detector(exam)
    return_data = detector.run_detection(ans)
   
    with open('C:\\xampp\\htdocs\\return_data.json', 'w') as f:
        f.write(return_data)
    '''
    debug(exam.img, ans.img)
    cv2.imshow("Ans",ans.img)
    cv2.imshow("test",exam.img)
    cv2.imshow("real",ans.original_img)
    cv2.waitKey(0)
    '''