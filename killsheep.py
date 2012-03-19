#!/usr/bin/python 

import sys
import cv
import time
import os
 
def detect(image):
    image_size = cv.GetSize(image)
 
    # create grayscale version
    grayscale = cv.CreateImage(image_size, 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
 
    # create storage
    storage = cv.CreateMemStorage(0)
 
    # equalize histogram
    cv.EqualizeHist(grayscale, grayscale)
 
    # detect objects
    cascade = cv.Load('haarcascade_frontalface_alt.xml')
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 0,  (20, 20))
 
    if faces:
        print 'face detected!'
        for (x,y,w,h),n in faces:
            cv.Rectangle(image, ( x, y), ((x + w), (y + h)), cv.RGB(0, 255, 0), 3, 8, 0)
        global _start
	_start = time.time() 
 
if __name__ == "__main__":
 
    print "Press ESC to exit ..."
 
    # create windows
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
 
    # create capture device
    device = 0 # assume we want first device
    capture = cv.CreateCameraCapture(0)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)    
 
    # check if capture device is OK
    if not capture:
        print "Error opening capture device"
        sys.exit(1)
 
    while 1:
        # do forever
 
        # capture the current frame
        frame = cv.QueryFrame(capture)
        if frame is None:
            break
 
        # mirror
        cv.Flip(frame, None, 1)
 
        # face detection
        detect(frame)

	_elapsed = (time.time() - _start) 
	if _elapsed > 5:
		os.system("xscreensaver-command -lock")

        # display webcam image
        cv.ShowImage('Camera', frame)
 
        # handle events
        k = cv.WaitKey(10)
 
        if k == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break
