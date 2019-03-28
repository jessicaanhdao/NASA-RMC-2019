import numpy as np
import cv2, sys, time, math
#import cv2.aruco as aruco
from cv2 import aruco
#-- Font for the text in the image
font = cv2.FONT_HERSHEY_PLAIN

class ArucoTag:

    def __init__(self):
        #Define tag
        self.id_to_find = 72
        self.marker_size = 10 #cm
        
        #get camera calibration path
        self.calib_path = ""
        self.camera_matrix = np.loadtxt(self.calib_path+'cameraMatrix.txt',delimiter=',')
        self.camera_distortion = np.loadtxt(self.calib_path+'cameraDistortion.txt',delimiter=',')

        #180 deg rotation matrix around x axis
        self.R_flip = np.zeros((3,3), dtype=np.float32)
        self.R_flip[0,0] = 1.0 #x
        self.R_flip[1,1] = -1.0 #y img is flipped
        self.R_flip[2,2] = -1.0 #z img is flipped

        #define aruco dictionary
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = aruco.DetectorParameters_create()
    #------------------------------------------------------------------------------
    #------- ROTATIONS https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    #------------------------------------------------------------------------------
    # Checks if a matrix is a valid rotation matrix.
    def isRotationMatrix(self, R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6


    # Calculates rotation matrix to euler angles
    # The result is the same as MATLAB except the order
    # of the euler angles ( x and z are swapped ).
    def rotationMatrixToEulerAngles(self, R):
        assert (self.isRotationMatrix(R))

        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0

        return np.array([x, y, z])



        
    def process(self, frame):
        print("bish")
        #convert to gray scale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #find all aruco markers in the image (or read video)
        corners, ids, rejected = aruco.detectMarkers(image = gray, dictionary = self.aruco_dict, parameters = self. parameters,cameraMatrix =  self.camera_matrix, distCoeff = self.camera_distortion)

        if np.any(ids != None) and ids[0] == self.id_to_find:
            #-- ret = [rvec, tvec, ?]
            #-- array of rotation and position of each marker in camera frame
            #-- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame. this one is rotation vectors
            #-- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
            ret = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.camera_distortion)

            #-- Unpack the output, get only the first
            rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]

            #-- Draw the detected marker and put a reference frame over it
            aruco.drawDetectedMarkers(frame, corners)
            aruco.drawAxis(frame, self.camera_matrix, self.camera_distortion, rvec, tvec, 10)


            #-- Print the tag position in camera frame
            str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f"%(tvec[0], tvec[1], tvec[2])
            cv2.putText(frame, str_position, (0, 100), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            #-- Obtain the rotation matrix tag->camera
            #Rodrigues basically converts rot vectors to rot matrix. nothing cool kinda lame
            R_ct    = np.matrix(cv2.Rodrigues(rvec)[0])
            R_tc    = R_ct.T

            #-- Get the attitude in terms of euler 321 (Needs to be flipped first)
            roll_marker, pitch_marker, yaw_marker = self.rotationMatrixToEulerAngles(self.R_flip*R_tc)

            #-- Print the marker's attitude respect to camera frame
            str_attitude = "MARKER Attitude w/r/t CAMERA frame r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_marker),math.degrees(pitch_marker),
                                math.degrees(yaw_marker))
            cv2.putText(frame, str_attitude, (0, 150), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


            #-- Now get Position and attitude f the camera respect to the marker
            pos_camera = -R_tc*np.matrix(tvec).T

            str_position = "CAMERA Position x=%4.0f  y=%4.0f  z=%4.0f"%(pos_camera[0], pos_camera[1], pos_camera[2])
            cv2.putText(frame, str_position, (0, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            #-- Get the attitude of the camera respect to the frame
            roll_camera, pitch_camera, yaw_camera = self.rotationMatrixToEulerAngles(self.R_flip*R_tc)
            str_attitude = "CAMERA Attitude w/r/t MARKER frame r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_camera),math.degrees(pitch_camera),
                                math.degrees(yaw_camera))
            cv2.putText(frame, str_attitude, (0, 250), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return frame