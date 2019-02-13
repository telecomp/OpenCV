# Thanks to Amir Hossein Daraie (https://github.com/Amirhosseindaraie)

import cv2
import numpy as np
import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
Mbox('سلام', '.لطفا جسم مورد نظرتان را با ماوس بالا سمت چپ به پایین سمت راست انتخاب کنید', 0)
Mbox('ادامه', 'سپس کلید روبه رو را فشار دید : s', 0) 
cropping = False
 
x_start, y_start, x_end, y_end = 0, 0, 0, 0
 
image = cv2.imread('sample_object.jpg')
oriImage = image.copy()
 
 
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
 
    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
 
    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
 
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished
 
        refPoint = [(x_start, y_start), (x_end, y_end)]
 
        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            cv2.imwrite("element.jpg", roi)

 
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
 
while True:
 
    i = image.copy()
 
    if not cropping:
        cv2.imshow("image", image)
 
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
 
    k = cv2.waitKey(0)
    if k == ord('s'):
        process = 1
    
    if process:
        break
 
Mbox('نتیجه', 'قسمت مورد نظر در تصویر جستجو میشود و اشیای مشابه در تصویر مشخص میشودند.', 0)
img_rgb = cv2.imread('sample_object.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

template = cv2.imread('element.jpg',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 
threshold = 0.5
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
# close all open windows
cv2.destroyAllWindows()
