import cv2
import numpy as np

lowThreshold = 28
ratio = 3
kernel_size = 3

input_image = 'img.jpg'
output_image = 'img-e.jpg'

img = cv2.imread(input_image)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

detected_edges = cv2.GaussianBlur(gray,(9,9),0)
detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)

des = cv2.bitwise_not(detected_edges)
cv2.imwrite(output_image, des)