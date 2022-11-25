import cv2


def saveImage(filepath, image):
    cv2.imwrite(filepath, image)
