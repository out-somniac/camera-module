import cv2


def save_image(filepath, image):
    cv2.imwrite(filepath, image)
