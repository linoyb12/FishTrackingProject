#!/usr/bin/env python

'''
TBD - enter output file name as arg
TBD - create templates
'''
# USAGE
# python scene_planner.py --video fish_video_example.mp4
# python scene_planner.py  # for use with camera

import argparse
import cv2
import random

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not

refPt = []
fish = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    global image, fish ,refPt

    # grab references to the global variables
    global refPt, cropping

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))

    # check to see if the left mouse button was released
    if(len(refPt)==4):
        # arrange points left-right up-down
        fish = {'1': refPt[0], '2-a': refPt[1], '3-b': refPt[2], '4': refPt[3]}

        for i in range(4):
            # draw a rectangle around the region of interest
            cv2.circle(image, refPt[i], 1, 4)
        cv2.imshow("image", image)

def SP_Main():
    global image, fish ,refPt
    refPt = []
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="Path to the image")
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    args = vars(ap.parse_args())

    # load the image, clone it, and setup the mouse callback function
    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        video_capture = cv2.VideoCapture(2)

        print video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

    # otherwise, grab a reference to the video file
    else:
        video_capture = cv2.VideoCapture(args["video"])

    video_capture.read()
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    ret, image = video_capture.read()

    if(image is None):#check for empty frames
        print 'No Image'


    # image = cv2.imread(args["image"])
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)

    # keep looping until the 'c' key is pressed
    while True:

        # Write Text
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(image, 'please mark your tanks',(50,50),font,fontScale,fontColor,lineType)
        cv2.putText(image, 'press "c" to finish and "r" to reset',(50,100),font,fontScale,fontColor,lineType)
        ''
        # display the image and wait for a keypress
        cv2.putText(image, 'please GDFHDSJs', (0, 0), font, fontScale, fontColor, lineType)
        #image = cv2.resize(image, (640, 480))
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        # 'r'=99            'c'=99
        # 'R'=82            'C'=67
        # 'heb(r)' = 248    'heb(c)=225

        #print key
        if (key == ord('r') or key == ord('R') or key == 248) :
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif (key == ord('c') or key == ord('C') or key == 225):
            break

    # if there are two reference points, then crop the region of interest
    # from the image and display it

    if len(refPt) == 4:
        print fish

    cv2.destroyAllWindows()

if __name__ == '__main__':
    SP_Main()