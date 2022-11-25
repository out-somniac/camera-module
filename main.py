from camera import Camera
import time
import image_utils


def main():
    camera = Camera(main_resolution=(1920, 1080), backup_resolution=(640, 480))
    camera.startRecording("hello_world.h264")
    image = camera.getFrame()
    time.sleep(10)
    camera.stopRecording()
    image_utils.saveImage("check.jpg", image)


if __name__ == "__main__":
    main()
