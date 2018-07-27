import numpy as np
import cv2
import time
import glob
import os

upFolder = 'up_cam/'
sideFolder = 'side_cam/'

def takePictures(camNum):
    dirPath = 'pics'+str(camNum)+'/'
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    cap = cv2.VideoCapture(camNum)
    cap.read()
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    for i in range(35):
        ret,frame = cap.read() # return a single frame in variable `frame`
        cv2.imwrite(dirPath+str(i)+'.png', frame)
        time.sleep(0.2)

#camNum - camera number
#folderPath - folder path to save calibration in (folder exists)
def calibrateCamera(camNum, folderPath):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6 * 9, 3), np.float32)
    objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)*1.8
    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    images = glob.glob('pics'+str(camNum)+'\*.png')
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (6, 9), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    dirPath = 'pics' + str(camNum) + '/'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    np.save(folderPath+'cam_mat', mtx)
    np.save(folderPath+'dist', dist)
    np.save(folderPath+'r vecs', rvecs)
    np.save(folderPath+'t vecs', tvecs)

def takePicsAndCalibrate(camNum, path):
    takePictures(camNum)
    calibrateCamera(camNum, path)
