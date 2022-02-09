import cv2
import mediapipe
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os
import random as r
from PIL import Image
import glob, os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# The correct coordinates of the puzzle pieces
puzzle_coor = [
    (69, 107), (358, 107), (600, 107), (790, 107), (944, 107),
    (69, 182), (358, 182), (600, 182), (790, 182), (944, 182),
    (69, 278), (358, 278), (600, 278), (790, 278), (944, 278),
    (69, 405), (358, 405), (600, 405), (790, 405), (944, 405),
]
#

"""
# convert confetti_old to png
files = glob.glob("Images/confetti_old/*.gif")

for imageFile in files:
    filepath, filename = os.path.split(imageFile)
    filterame, exts = os.path.splitext(filename)
    print("Processing: " + imageFile, filterame)
    im = Image.open(imageFile)
    im.save('Images/confetti/' + filterame[:8] + '.png', 'PNG')
"""

detector = HandDetector(detectionCon=0.8)


class DragImg():
    def __init__(self, path, posOrigin, imgType, posFinal=(0,0), scale=None):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.posFinal = posFinal
        self.path = path
        self.inPlace = False
        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        if scale:
            self.img = cv2.resize(self.img, (0, 0), None, scale, scale)

        self.size = self.img.shape[:2]

    def __str__(self):
        return f'current: {self.posOrigin}, final:{self.posFinal}, {self.path}'

    def resize(self, scale):
        self.img = cv2.resize(self.img, (0, 0), None, scale, scale)

    def update(self, cursor):
        ox, oy = self.posOrigin
        cx, cy = cursor
        fx, fy = self.posFinal
        h, w = self.size

        # Check if cursor over it
        if not self.inPlace and ox < cx < ox + w and oy < cy < oy + h:
            self.posOrigin = cx - w // 2, cy - h // 2
            # Check if in right spot
            if abs(ox - fx) < 50 and abs(oy - fy) < 50:
                self.posOrigin = fx, fy
                self.inPlace = True
            return True

        return False


# Successfully solved the puzzle
def party():
    # TODO: do something cool
    print("congrats! you got the puzzle")
    message = DragImg("Images/message.png", (400, 400), "png")
    print(message)
    for ilfdsfl in range(3):
        for img_ in listConf:
            sus, image = cap.read()
            image = cv2.flip(image, 1)
            image = cvzone.overlayPNG(image, message.img, [message.posOrigin[0], message.posOrigin[1]])
            image = cvzone.overlayPNG(image, img_.img, [img_.posOrigin[0], img_.posOrigin[1]])
            cv2.imshow("Image", image)
            cv2.waitKey(10)
        print(f"round {ilfdsfl}")
    quit(0)


path_puzzle = "Images/puzzle"
img_files = os.listdir(path_puzzle)
path_confetti = "Images/confetti"
confetti_files = os.listdir(path_confetti)

# save puzzle images
listImg = []
for x, pathImg in enumerate(img_files):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(
        DragImg(f'{path_puzzle}/{pathImg}', (r.randint(100, 1000), r.randint(100, 500)), imgType=imgType, posFinal=puzzle_coor[int(pathImg[1:-4])], scale=0.25))
    # print(listImg[-1])

    #
# save confetti images
listConf = []
for x, pathConf in enumerate(confetti_files):
    if 'png' in pathConf:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listConf.append(
        DragImg(f'{path_confetti}/{pathConf}', [0, 0], imgType, scale=1.5))
    # print(listConf[-1])


#""""""
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, img = detector.findDistance(lmList[8], lmList[12], img)

        # party()
        if length < 60:
            cursor = lmList[8]
            # print(cursor)

            pieces_left = len(listImg)
            for imgObject in listImg:
                if imgObject.inPlace:
                    pieces_left -= 1
                # only move one image at a time
                # update returns true if image is moved
                if imgObject.update(cursor):
                    break

            if pieces_left == 0:
                party()
                cv2.waitKey(100)
                break

    try:

        for imgObject in listImg:

            # Draw for JPG image
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                img = cvzone.overlayPNG(img, imgObject.img, [ox, oy])
            else:
                img[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)

#"""
