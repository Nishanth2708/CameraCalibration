import cv2
import matplotlib.pyplot as plt
import numpy as np

path = 'SavedImages/saved_frame_0.png'


def TextonImage(path_image='SavedImages/saved_frame_5.png'):

    img = cv2.imread(path_image)
    img = cv2.resize(img,(238,353))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    imgpoints_one, objpoints_one = [], []

    # If found, add object points, image points (after refining them)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    x, y = [],[]
    if ret == True:
        objpoints_one.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        print(corners2)
        # print(corners2)
        imgpoints_one.append(corners2)
        # Draw and display the corners

        img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)

        for i in corners2:
            for j in corners2:
                for k in range(0, len(j)):

                    cv2.putText(img, "{}".format(int(j[k][1])),
                                (int(j[k][0]), int(j[k][1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 125, 255), 1
                                )
        cv2.imshow('img', img)
        cv2.waitKey()



        # cv2.imshow('img', img)
        # cv2.waitKey(0)
        cv2.imwrite('chessboardcorners_resized.png', img)

        return x,y

# x,y = TextonImage()


import cv2

image = cv2.imread('ruler1.png')
image = cv2.resize(image,(238,353))
print(image.shape)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 130, 255, 1)

cnts = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
    cv2.drawContours(image,[c], 0, (0,255,0), 1)

cv2.imshow("result", image)
cv2.imwrite('result.png',image)
cv2.waitKey(0)

a = []
b = []

img = cv2.imread('ruler1.png')
img = cv2.resize(img,(238,353))

print(img.shape)
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=-1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("image", img)


cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)


