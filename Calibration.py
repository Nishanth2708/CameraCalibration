import numpy as np
import cv2
import glob,os


#!/usr/bin/env python
# coding:utf-8
"""
Name     : Calibration.py
Author   : Nishanth Reddy Vanipenta
Contact  : nishanthv@zdmetalproducts.com
Time     : 07/02/2021 8:00 A.M
Desc     : Functions: Calibration and UnDistortion of frames

"""


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


if not os.path.isdir('camera_data'):

    os.mkdir('camera_data')

else:

    pass

savedir="camera_data/"

def calibrate (width=9, height=6):



    """ Apply camera calibration operation for images in the given directory path. """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)

    print(" [INFO]: Calibration Started.......")
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    # objp = objp * square_size

    # print(objp)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob('./SavedImages/*.png')
    # print(images)

    count =0
    for fname in images:

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:

            count += 1
            print("[INFO]: Found corners on image {}".format(count))
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11),
                                        (-1, -1), criteria)
            imgpoints.append(corners2)

            print(corners2)


            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
            cv2.imshow('img',img)
            cv2.waitKey(1)

    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                       gray.shape[::-1],
                                                       None, None )

    mean_error = 0

    for i in range(len(objpoints)):

        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        mean_error += error

    print("total error: {}".format(mean_error / len(objpoints)))

    np.save(savedir + 'imagepoints.npy', imgpoints)
    np.save(savedir + 'worldpoints.npy', objpoints)

    print("[INFO]: Saved all the Data into the Directory.")
    return [ret, mtx, dist, rvecs, tvecs,imgpoints, objpoints]


def save_coefficients ( mtx, dist, path ):

    """ Save the camera matrix and the distortion coefficients to given path/file. """

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)
    cv_file.write("K", mtx)
    cv_file.write("D", dist)

    # cv_file.write("newcammat", newcameramtx)
    # cv_file.write("roi", roi)

    # note you *release* you don't close() a FileStorage object

    cv_file.release()

def load_coefficients ( path ):

    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ

    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix

    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    # new_camera_matrix = cv_file.getNode("newcammat").mat()
    # roi =   cv_file.getNode("roi").mat()

    cv_file.release()

    return [camera_matrix, dist_matrix]

def undistort ( path, storage_file =0 ):

    print("[INFO]: Undistorting Started...")

    mtx,dist = load_coefficients(path)

    print("[INFO]: Loaded image...")
    img = cv2.imread('SavedImages/saved_frame_0.png')
    h, w = img.shape[:2]

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]

    print(dst.shape)

    np.save(savedir+'newcam_mtx.npy', newcameramtx)
    np.save(savedir+'roi.npy', roi)

    cv2.imwrite('SavedImages/calibrated.png', dst)

    cv2.imshow('distorted image', img)
    cv2.imshow('undistorted image', dst)
    cv2.waitKey(0)

    return [newcameramtx,roi]


''' This function retrieves an image  with detected corners or edges 
    that can be used as a reference to observe the pixels per metric
    along the cartesian coordinate system. 
    
    The resolution of the image should be fixed all the time in order
    to observe the pixel per metric ratios
'''


def TextonImage ( path_image ):

    img = cv2.imread(path_image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

    imgpoints_one, objpoints_one = [], []


    # If found, add object points, image points (after refining them)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    print(ret)
    if ret == True:
        objpoints_one.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # print(corners2)
        imgpoints_one.append(corners2)
        # Draw and display the corners

        img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)


        for i in corners2:
            for j in corners2:
                for k in range(0, len(j)):
                    print(int(j[k][0]),int(j[k][1]))
                    cv2.putText(img, "{}".format(int(j[k][0])),
                                                (int(j[k][0]), int(j[k][1])),
                                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1
                                )

        np.save(savedir + 'imagepoints_one.npy', imgpoints_one)
        np.save(savedir + 'worldpoints_one.npy', objpoints_one)

        cv2.imshow('img', img)
        cv2.imwrite('chessboardcorners.png', img)