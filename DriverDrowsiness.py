import cv2
import numpy as np
import dlib
from imutils import face_utils
from pygame import mixer
import time
from tkinter import *

# Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\\Study Material\\3rd year\\5th sem\\Mini Project\\shape_predictor_68_face_landmarks.dat")

def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0

def update_count_text(text_widget, count_value):
    text_widget.delete("1.0", END)
    text_widget.insert(END, count_value)

def main():
    cap = cv2.VideoCapture("E:\\Study Material\\3rd year\\5th sem\\Mini Project\\Video.mp4")
    sleep, drowsy, active, status, color, count = 0, 0, 0, "", (0, 0, 0), 0

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if left_blink == 0 or right_blink == 0:
                sleep += 1
                drowsy, active = 0, 0
                if sleep > 6:
                    count += 1
                    status = "SLEEPING !!!"
                    color = (255, 0, 0)
                    mixer.init()
                    mixer.music.load(r"E:\\Study Material\\3rd year\\5th sem\\Mini Project\\alarm1.wav")
                    cv2.imwrite("dataset/frame_yawn%d.jpg" % sleep, frame)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(1)
            elif 0 < left_blink == right_blink < 2:
                sleep, active = 0, 0
                drowsy += 1
                if drowsy > 6:
                    count += 1
                    status = "Drowsy !"
                    color = (0, 0, 255)
                    mixer.init()
                    mixer.music.load(r"E:\\Study Material\\3rd year\\5th sem\\Mini Project\\alarm2.wav")
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(1)
            else:
                drowsy, sleep = 0, 0
                active += 1
                if active > 6:
                    status = "Active :)"
                    color = (0, 255, 0)

            cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            update_count_text(t3, count)
            break

def camera():
    cap = cv2.VideoCapture(0)
    sleep, drowsy, active, status, color, count = 0, 0, 0, "", (0, 0, 0), 0

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if left_blink == 0 or right_blink == 0:
                sleep += 1
                drowsy, active = 0, 0
                if sleep > 6:
                    count += 1
                    status = "SLEEPING !!!"
                    color = (255, 0, 0)
                    mixer.init()
                    mixer.music.load(r"E:\\Study Material\\3rd year\\5th sem\\Mini Project\\alarm1.wav")
                    cv2.imwrite("dataset/frame_yawn%d.jpg" % sleep, frame)
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(1)
            elif 0 < left_blink == right_blink < 2:
                sleep, active = 0, 0
                drowsy += 1
                if drowsy > 6:
                    status = "Drowsy !"
                    color = (0, 0, 255)
                    mixer.init()
                    mixer.music.load(r"E:\\Study Material\\3rd year\\5th sem\\Mini Project\\alarm2.wav")
                    mixer.music.play()
                    while mixer.music.get_busy():
                        time.sleep(1)
            else:
                drowsy, sleep = 0, 0
                active += 1
                if active > 6:
                    status = "Active :)"
                    color = (0, 255, 0)

            cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            for n in range(0, 68):
                (x, y) = landmarks[n]

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            update_count_text(t4, count)
            break

root = Tk()
root.title("Driver Drowsiness Detection made by PRAKHAR KUKREJA BCA V SEM SEC C")

label1 = Label(root)
label1.place(x=0, y=0)

w2 = Label(root, justify=LEFT, text="Driver Drowsiness Detection")
w2.config(font=("Times", 30), background="white")
w2.grid(row=2, column=0, columnspan=2, padx=100, pady=10)

lr_video = Button(root, text="Video", height=2, width=10, command=main)
lr_video.config(font=("Times", 17), background="lightgreen")
lr_video.grid(row=15, column=0, pady=10)

lr_camera = Button(root, text="Camera", height=2, width=10, command=camera)
lr_camera.config(font=("Times", 17), background="lightgreen")
lr_camera.grid(row=16, column=0, pady=10)

NameLb = Label(root, text="Predict using:")
NameLb.config(font=("Times", 15), background="lightblue")
NameLb.grid(row=13, column=0, pady=20)

# Adding Text widgets for displaying counts
t3 = Text(root, height=2, width=15)
t3.config(font=("Times", 15))
t3.grid(row=15, column=1, padx=60)

t4 = Text(root, height=2, width=15)
t4.config(font=("Times", 15))
t4.grid(row=16, column=1, padx=60)


# Adding a Quit button to gracefully exit the application
quit_button = Button(root, text="Quit", command=root.destroy)
quit_button.config(font=("Times", 17), background="lightcoral")
quit_button.grid(row=17, column=0, pady=10)

root.mainloop()