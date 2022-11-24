from camera import Camera
import time


def main():
    camera = Camera(main_resolution=(1920, 1080), backup_resolution=(640, 480))
    camera.startRecording("hello_world.h264")
    time.sleep(10)
    camera.stopRecording()


if __name__ == "__main__":
    main()
