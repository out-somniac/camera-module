from camera import Camera
import time


def main():
    camera = Camera()
    camera.startRecording("hello_world.h264")
    time.sleep(10)
    camera.stopRecording()


if __name__ == "__main__":
    main()
