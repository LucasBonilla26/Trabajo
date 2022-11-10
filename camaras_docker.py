import cv2
from yolov7_package import Yolov7Detector
import time

# Camera url list
cam_list = [
    "rtsp://guest:smpt00@10.253.247.25:88/videoMain"
    ]

def get_camera_dir_from_URL(cam_url):
    """
    Returns ip address or dns from complete address of the camera
    """
    ret = cam_url.split("@")[1].split("/")[0]
    return ret

def show_video():
    # Get the current camera frame from the address and a boolean value if exists
    capture = cv2.VideoCapture(cam_list[0])
    
    if not capture.isOpened():
        print("Error opening video stream or file")

    while(capture.isOpened()):
        validate, camera_frame = capture.read()
        if validate:
            cv2.imshow('Frame',camera_frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            print("Error in validation!")
            break

    capture.release()    

def get_yolo_items():
    # Get the current camera frame from the address and a boolean value if exists
    capture = cv2.VideoCapture(cam_list[0])

    if capture.isOpened():
        validate, camera_frame = capture.read()

        if validate:
            cv2.imshow('camera frame', camera_frame)
            cv2.waitKey(0)
            det = Yolov7Detector(traced=False)
            classes, boxes, scores = det.detect(camera_frame) 
            #Maybe person id = 0
            print(classes)
    else:
        print("Error opening camera!")
    
    capture.release()    

if __name__ == "__main__":
    camera_address = get_camera_dir_from_URL(cam_list[0])
    print(camera_address)
    
    if __debug__:
        print('Debug ON')
    else:
        print('Debug OFF')

    show_video()
