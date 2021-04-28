import numpy as np
import cv2 as cv
roi = cv.imread('cropped.png')
hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)
target = cv.imread('abhiyaan_opencv_qn1.png')
hsvt = cv.cvtColor(target,cv.COLOR_BGR2HSV)

# calculating object histogram
roihist = cv.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )

# normalize histogram and apply backprojection
cv.normalize(roihist,roihist,0,255,cv.NORM_MINMAX)
dst = cv.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

disc = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
cv.filter2D(dst, -1, disc, dst) #dst is the matrix obtained after back projection

# threshold and binary AND
ret,thresh = cv.threshold(dst,100,180,0)
final = cv.merge((thresh,thresh,thresh))

#res = cv.bitwise_or(target,final)
#res = np.vstack((target,final,res))
cv.imwrite('binary_img.jpg',final)
#cv.imwrite('res.jpg',res)

img = cv.imread('binary_img.jpg')

# convert to grayscale
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# threshold
thresh = cv.threshold(gray,128,255,cv.THRESH_BINARY)[1]

# get contours
result = img.copy()
contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
for cntr in contours:
    x,y,w,h = cv.boundingRect(cntr)
    area = cv.contourArea(cntr)
    print(area)
    if area >= 50:
        cv.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #print("x,y,w,h:",x,y,w,h)
 
# save resulting image
#cv.imwrite('bounding_box.jpg',result)
res = cv.bitwise_or(target,result)
cv.imwrite('final_result.jpg',res)

# show thresh and result    
cv.imshow("bounding_box", result)
cv.waitKey(0)
cv.destroyAllWindows()