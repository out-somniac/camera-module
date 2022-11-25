import os
from camera import Camera
from image_utils import saveImage
from time import sleep, process_time


def testInstance(id, resolution_main, resolution_backup, frequency, is_recording, is_saved, frames_total=100):
    sleep_interval = 1 / frequency
    os.mkdir("test_{}".format(id))
    os.mkdir("test_{}/images".format(id))

    camera = Camera(resolution_main, resolution_backup)
    begin = process_time()

    if is_recording:
        camera.startRecording("test_{}/video_test.h264".format(id))

    for curr_frame in range(frames_total):
        image = camera.getFrame()
        if is_saved:
            saveImage("test_{}/images/frame{}.jpg".format(id, curr_frame))
        sleep(sleep_interval)

    if is_recording:
        camera.stopRecording()

    end = process_time()
    return end - begin


def test():
    time = testInstance(0, (1920, 1080), (640, 480), 10, True, True)
    print(time)
