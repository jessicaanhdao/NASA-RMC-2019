<<<<<<< HEAD
from cscore import CameraServer
import numpy as np
import cv2
from pipeline import Pipeline
from grip import GripPipeline

from networktables import NetworkTables
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)

    # connect to the RoboRIO
    NetworkTables.initialize(server='localhost')
    sd = NetworkTables.getTable('/SmartDashboard')

    sd.putNumber('y', 1)
    sd.putNumber('rot', .5)
    
    cs = CameraServer.getInstance()
    cs.enableLogging()
 #   pip = Pipeline()
    grip = GripPipeline()
    '''usb1 = cs.startAutomaticCapture(dev=0)
    usb2 = cs.startAutomaticCapture(dev=1)'''
  #  image_file = cv2.imread('pig.jpg',1)
   # cv2.imshow("Pig",image_file)

    #cv2.waitForever()
     # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource (a stream). This will send images/videos back to the Dashboard
    #outputStream is a openCV stream
    outputStream = cs.putVideo("Blob test", 320, 240)

    '''show on server
    mjpegServer = cs.MjpegServer("httpserver", 8081)
    mjpegServer.setSource(camera)

    print("mjpg server listening at http://0.0.0.0:8081")
    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    cvMjpegServer = cs.MjpegServer("cvhttpserver", 8082)
    cvMjpegServer.setSource(cvSource)'''


    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    img_flip = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    pig = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue
        print("got frame at time", time, img.shape)

        #
        # Insert your image processing logic here!
        #       
#        pip.process(img)
        grip.process(img)
  #      print("blobs length: ",len(pip.find_blobs_output))
        print("blobs length: ",len(grip.filter_contours_output))

      #  print(pip.find_blobs_output.size())
        if (len(grip.filter_contours_output) > 0):
            sd.putBoolean('ObjectFound', True)
        else:
            sd.putBoolean('ObjectFound', False)
      #  img_with_keypoints = cv2.drawKeypoints(pip.mask_output, pip.find_blobs_output,pig,(0, 0, 255))
        cv2.drawContours(img,grip.filter_contours_output,-1,(0,255,0),1)

        #cv2.flip(img, flipCode=0, dst=img_flip)


        # (optional) send some image back to the dashboard
        outputStream.putFrame(img)

if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    

    
=======
from cscore import CameraServer
import numpy as np
import cv2
from pipeline import Pipeline
from grip import GripPipeline

from networktables import NetworkTables
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)

    # connect to the RoboRIO
    NetworkTables.initialize(server='localhost')
    sd = NetworkTables.getTable('/SmartDashboard')

    sd.putNumber('y', 1)
    sd.putNumber('rot', .5)
    
    cs = CameraServer.getInstance()
    cs.enableLogging()
 #   pip = Pipeline()
    grip = GripPipeline()
    '''usb1 = cs.startAutomaticCapture(dev=0)
    usb2 = cs.startAutomaticCapture(dev=1)'''
  #  image_file = cv2.imread('pig.jpg',1)
   # cv2.imshow("Pig",image_file)

    #cv2.waitForever()
     # Capture from the first USB Camera on the system
    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240)

    

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    # (optional) Setup a CvSource (a stream). This will send images/videos back to the Dashboard
    #outputStream is a openCV stream
    outputStream = cs.putVideo("Blob test", 320, 240)

    '''show on server
    mjpegServer = cs.MjpegServer("httpserver", 8081)
    mjpegServer.setSource(camera)

    print("mjpg server listening at http://0.0.0.0:8081")
    cvSource = cs.CvSource("cvsource", cs.VideoMode.PixelFormat.kMJPEG, 320, 240, 30)
    cvMjpegServer = cs.MjpegServer("cvhttpserver", 8082)
    cvMjpegServer.setSource(cvSource)'''


    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    img_flip = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
    pig = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue
        print("got frame at time", time, img.shape)

        #
        # Insert your image processing logic here!
        #       
#        pip.process(img)
        grip.process(img)
  #      print("blobs length: ",len(pip.find_blobs_output))
        print("blobs length: ",len(grip.filter_contours_output))

      #  print(pip.find_blobs_output.size())
        if (len(grip.filter_contours_output) > 0):
            sd.putBoolean('ObjectFound', True)
        else:
            sd.putBoolean('ObjectFound', False)
      #  img_with_keypoints = cv2.drawKeypoints(pip.mask_output, pip.find_blobs_output,pig,(0, 0, 255))
        cv2.drawContours(img,grip.filter_contours_output,-1,(0,255,0),1)

        #cv2.flip(img, flipCode=0, dst=img_flip)


        # (optional) send some image back to the dashboard
        outputStream.putFrame(img)

if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    

    
>>>>>>> remotes/origin/master
    main()