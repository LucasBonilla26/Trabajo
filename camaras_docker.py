import cv2
from yolov7_package import Yolov7Detector
import sched, time
from datetime import datetime

# Camera url list
cam_list = [
    "rtsp://guest:smpt00@10.253.247.25:88/videoMain", # TIC hall
    "http://admin:xtrem$@10.253.247.40:5900/mjpg/video.mjpghttp://admin:xtrem$@10.253.247.40:5900/mjpg/video.mjpg", # I1 classroom (Does not work)
    "http://admin:xtrem$@10.253.246.37/snapshot.cgi", # Norba classroom camera_1
    "http://admin:xtrem$@10.253.246.38/snapshot.cgi", # Norba classroom camera_2
    "http://admin:xtrem$@10.253.246.35/snapshot.cgi", # Novell classroom camera_1 (Does not work)
    "http://admin:xtrem$@10.253.246.36/snapshot.cgi", # Novell classroom camera_2 (Does not work)
    "rtsp://estudiante:DuRa2020@10.253.246.230/axis-media/media.amp?camera=1", # C7 classroom teacher camera
    "rtsp://guest:smpt00@10.253.246.23:88/videoMain", # AT Hall
    "rtsp://robolab1:0pticalflow@158.49.247.195:88/videoMain"
    ]

s = sched.scheduler(time.time,time.sleep)

def get_camera_dir_from_URL(cam_url):
    """
    Returns ip address or dns from complete address of the camera
    """
    ret = cam_url.split("@")[1].split("/")[0]
    return ret

def show_video():
    """
    Show the video of the camera specificar in the cam_list variable
    """
    # Get the current camera frame from the address and a boolean value if exists
    print(cam_list[8])
    capture = cv2.VideoCapture(cam_list[8])
    print("1")

    if capture.isOpened():
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

def get_yolo_items(sc):
    """
    Print the items id of the ones identified by YOLO
    """
    # Get the current camera frame from the address and a boolean value if exists
    capture = cv2.VideoCapture(cam_list[8], cv2.CAP_FFMPEG)

    if capture.isOpened():
        validate, camera_frame = capture.read()

        if validate:
            # cv2.imshow('camera frame', camera_frame)
            # cv2.waitKey(0)
            det = Yolov7Detector(traced=False)
            classes, boxes, scores = det.detect(camera_frame) 
            #Person_id = 0
            print(classes)
            print(classes[0].count(0))
    else:
        print("Error opening camera!")
    
    capture.release()   
    sc.enter(60, 1, get_yolo_items, (sc,)) #Throw the event each 60 seconds

if __name__ == "__main__":
    
    # while(True):
        # camera_address = get_camera_dir_from_URL(cam_list[0])
        # n_people = get_yolo_items().count("0")
        # print(n_people)
    show_video()
    now = datetime.now()

    # current_time = now.strftime("%H:%M:%S")
    # print("Current Time =", current_time)
    # s.enter(60, 1, get_yolo_items, (s,)) #Throw the event each 60 seconds
    # s.run()
    #insert in data base

