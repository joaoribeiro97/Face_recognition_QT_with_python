from PIL import Image
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, qVersion
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QMessageBox
import os.path
from PIL import Image, ImageQt
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep


def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded


def unknown_image_encoded(img):
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]
    return encoding


def classify_face(im):
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    # img = img[:,:,::-1]

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            window.lb_result.setText("OK")
            window.lb_result.setStyleSheet("background-color: green;")
        else:
            window.lb_result.setText("NOK")
            window.lb_result.setStyleSheet("background-color: red;")

        face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left - 20, bottom - 15), (right + 20, bottom + 20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    # Display the resulting image
    while True:

        cv2.imshow('Classification', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return face_names


def path():
    fname = QFileDialog.getOpenFileName(window, 'Open Image', 'D:\\Python_examples\\QT_faces_recognition\\images',
                                        'Image files (*.jpg *.gif *.png)')
    path.imagePath = fname[0]
    print(fname[0])
    return path.imagePath


# LOAD IMAGE
def getImage():
    fname2 = path()
    pixmap = QPixmap(fname2)

    window.lb_images.setPixmap(QPixmap(pixmap))
    window.lb_images.setScaledContents(True)
    print(classify_face(fname2))


def save_image():
    simage = path.imagePath
    print(simage)

    image = cv2.imread(simage)
    #cv2.imwrite('D:\\Python_examples\\QT_faces_recognition\\x.jpg', image)
    dir = 'D:\\Python_examples\\QT_faces_recognition\\faces\\'
    cv2.imwrite(dir + window.line_save.text(), image)
    QMessageBox.about(window, "Alert", "Image successfully added!")
    print(window.line_save.text())


app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("qt_people.ui")
window.bt_image.clicked.connect(getImage)
window.bt_save.clicked.connect(save_image)

window.show()
app.exec()
