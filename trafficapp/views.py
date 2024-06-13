from django.shortcuts import redirect, render
from django.contrib import messages
import cv2
import dlib
import time
import math
from trafficapp.models import *
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
# Create your views here.


def estimateSpeed(location1, location2):
        d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
        ppm = 8.8
        d_meters = d_pixels / ppm
        fps = 18
        speed = d_meters * fps * 3.6
        print('1')
        return speed

def dashboard(req):
    return render(req,'dashboard.html')

def login(req):
    admin_name = 'Admin'
    admin_pswd = '1234'
    if req.method == 'POST':
        admin_n = req.POST.get('a_name')
        admin_p = req.POST.get('a_pswd')
        if admin_name == admin_n and admin_pswd == admin_p:
            messages.success(req,'Login Successful')
            return redirect('dashboard')
        else:
            messages.warning(req,'Invalid Credentials')
            return redirect('login')
    return render(req,'login.html')

def speeddetection(req):
    if req.method == 'POST':
        video1 = req.FILES['vfile']
        print('video')
        Speed_Detection.objects.create(VIDEO = video1)
        
        #Classifier File
        carCascade = cv2.CascadeClassifier("overspeeding.xml")

        #Video file capture
        v = Speed_Detection.objects.last()
        video = cv2.VideoCapture(v.VIDEO.path)

        # Constant Declaration
        WIDTH =1280
        HEIGHT = 720

        #estimate speed function
     
        # estimateSpeed()
        #tracking multiple objects
        rectangleColor = (0, 255, 255)
        frameCounter = 0
        currentCarID = 0
        fps = 0

        carTracker = {}
        carNumbers = {}
        carLocation1 = {}
        carLocation2 = {}
        speed = [None] * 1000

        out = cv2.VideoWriter('outTraffic.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH, HEIGHT))

        while True:
            start_time = time.time()
            rc, image = video.read()
            if type(image) == type(None):
                break

            image = cv2.resize(image, (WIDTH, HEIGHT))
            resultImage = image.copy()

            frameCounter = frameCounter + 1
            carIDtoDelete = []

            for carID in carTracker.keys():
                trackingQuality = carTracker[carID].update(image)

                if trackingQuality < 7:
                    carIDtoDelete.append(carID)

            
            for carID in carIDtoDelete:
                print("Removing carID " + str(carID) + ' from list of trackers. ')
                print("Removing carID " + str(carID) + ' previous location. ')
                print("Removing carID " + str(carID) + ' current location. ')
                carTracker.pop(carID, None)
                carLocation1.pop(carID, None)
                carLocation2.pop(carID, None)

            
            if not (frameCounter % 10):
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

                for (_x, _y, _w, _h) in cars:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    x_bar = x + 0.5 * w
                    y_bar = y + 0.5 * h

                    matchCarID = None

                    for carID in carTracker.keys():
                        trackedPosition = carTracker[carID].get_position()

                        t_x = int(trackedPosition.left())
                        t_y = int(trackedPosition.top())
                        t_w = int(trackedPosition.width())
                        t_h = int(trackedPosition.height())

                        t_x_bar = t_x + 0.5 * t_w
                        t_y_bar = t_y + 0.5 * t_h

                        if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                            matchCarID = carID

                    if matchCarID is None:
                        print(' Creating new tracker' + str(currentCarID))

                        tracker = dlib.correlation_tracker()
                        tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                        carTracker[currentCarID] = tracker
                        carLocation1[currentCarID] = [x, y, w, h]

                        currentCarID = currentCarID + 1

            for carID in carTracker.keys():
                trackedPosition = carTracker[carID].get_position()

                t_x = int(trackedPosition.left())
                t_y = int(trackedPosition.top())
                t_w = int(trackedPosition.width())
                t_h = int(trackedPosition.height())

                cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

                carLocation2[carID] = [t_x, t_y, t_w, t_h]

            end_time = time.time()

            if not (end_time == start_time):
                fps = 1.0/(end_time - start_time)

            for i in carLocation1.keys():
                if frameCounter % 1 == 0:
                    [x1, y1, w1, h1] = carLocation1[i]
                    [x2, y2, w2, h2] = carLocation2[i]

                    carLocation1[i] = [x2, y2, w2, h2]

                    if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                        if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                            speed[i] = estimateSpeed([x1, y1, w1, h1], [x1, y2, w2, h2])

                        if speed[i] != None and y1 >= 180:
                            cv2.putText(resultImage, str(int(speed[i])) + "km/h", (int(x1 + w1/2), int(y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 100) ,2)

            cv2.imshow('result', resultImage)

            out.write(resultImage)

            if cv2.waitKey(15) & 0xFF == ord('q'):
                break

        
        cv2.destroyAllWindows()
        out.release()

    return render(req,'speedDetection.html')



def helmetdetection(req):

    return render(req, 'helmetDetection.html')

def helmetform(req):
    if req.method == 'POST':
        video1 = req.FILES['hfile']
        print('video')
        vid = Helmet_Detection.objects.create(VIDEO=video1)

    cascade_src = "helmet.xml"
    h = Helmet_Detection.objects.last()
    video_src = (h.VIDEO.path)
    cap = cv2.VideoCapture(video_src)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    car_cascade = cv2.CascadeClassifier(cascade_src)

    # Set up GUI
    window = tk.Tk()  # Makes main window
    window.wm_title("Digital Microscope")
    window.config(background="#FFFFFF")

    # Graphics window
    imageFrame = tk.Frame(window, width=600, height=500)
    imageFrame.grid(row=0, column=0, padx=10, pady=2)

    # Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)


    def show_frame():
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cars = car_cascade.detectMultiScale(gray, 1.59, 1)

        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 215), 2)
            cv2.putText(frame, "Helmet", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 215), 2)

        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(color)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)


    def close_window():
        cap.release()
        cv2.destroyAllWindows()
        window.destroy()


    # Slider window (slider controls stage position)
    sliderFrame = tk.Frame(window, width=600, height=100)
    sliderFrame.grid(row=600, column=0, padx=10, pady=2)

    # Bind the 'q' key press event to the close_window function
    window.bind('q', lambda event: close_window())

    show_frame()  # Display
    window.mainloop()  # Start GUI
    return render(req, 'helmetDetection.html')

def index(req):
    return render(req,'index.html')

def signaljumpdetection(req):
    return render(req,'signalJumpDetection.html')

def signaljumpform(req):
    if req.method == 'POST':
        video = req.FILES['jfile']
        SignalJump_Detection.objects.create(VIDEO = video)
    

    # Load pre-trained vehicle detection model (e.g., Haar cascades or deep learning models)
    car_cascade = cv2.CascadeClassifier("sj_haarcascade_car.xml")

    # Load pre-trained signal detection model or implement signal detection algorithm
    signal_cascade = cv2.CascadeClassifier("sj_cascade.xml")

    # Define color ranges for red, yellow, and green signals (adjust as per your requirements)
    red_lower = np.array([0, 0, 100], dtype=np.uint8)
    red_upper = np.array([20, 255, 255], dtype=np.uint8)
    yellow_lower = np.array([20, 0, 100], dtype=np.uint8)
    yellow_upper = np.array([40, 255, 255], dtype=np.uint8)
    green_lower = np.array([40, 0, 100], dtype=np.uint8)
    green_upper = np.array([70, 255, 255], dtype=np.uint8)

    # Define ROI coordinates (adjust as per your requirements)
    roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

    # Initialize video capture from a camera or video file
    j = SignalJump_Detection.objects.last()
    video_path = (j.VIDEO.path)
    cap = cv2.VideoCapture(video_path)

    while True:
        # Read the current frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Extract the ROI from the frame
        roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

        # Convert ROI to the HSV color space
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Perform color thresholding to detect red, yellow, and green signals
        mask_red = cv2.inRange(hsv_roi, red_lower, red_upper)
        mask_yellow = cv2.inRange(hsv_roi, yellow_lower, yellow_upper)
        mask_green = cv2.inRange(hsv_roi, green_lower, green_upper)

        # Count the number of non-zero pixels in each mask
        red_pixels = np.count_nonzero(mask_red)
        yellow_pixels = np.count_nonzero(mask_yellow)
        green_pixels = np.count_nonzero(mask_green)

        # Determine the signal state based on the number of pixels in each mask
        signal_state = None
        if red_pixels > yellow_pixels and red_pixels > green_pixels:
            signal_state = "Red"
        elif yellow_pixels > red_pixels and yellow_pixels > green_pixels:
            signal_state = "Yellow"
        elif green_pixels > red_pixels and green_pixels > yellow_pixels:
            signal_state = "Green"

        # Draw the signal state text on the frame
        cv2.putText(frame, f"Signal State: {signal_state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the frame with the ROI and signal state
        cv2.imshow('Signal State Analysis', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return render(req,'signalJumpDetection.html')


def tripleridedetection(req):
    return render(req,'tripleRideDetection.html')

def triplerideform(req):
    if req.method == 'POST':
        image = req.FILES['tview']
        print('image')
        Tripleride_Detection.objects.create(VIDEO = image)

    font = cv2.FONT_HERSHEY_SIMPLEX
    face_detector = cv2.CascadeClassifier("triple.xml")
    
    # Read the image
    a = Tripleride_Detection.objects.last()
    img = cv2.imread(a.VIDEO.path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Draw bounding boxes around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)
        cv2.putText(img, 'Face', (x, y), font, 2, (255, 0, 0), 5)

    # Display the image with bounding boxes and face count
    cv2.putText(img, 'Number of Faces: ' + str(len(faces)), (40, 40), font, 1, (255, 0, 0), 2)
    # print(cv2.putText(img, 'Number of Faces: ' + str(len(faces)), (40, 40), font, 1, (255, 0, 0), 2))
    cv2.imshow('Image', img)
    print(cv2.imshow('Image', img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return render(req,'tripleRideDetection.html')

def logout(req):
    messages.warning(req,"Logged Out")
    return render(req,'index.html')