from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

from threading import Lock


class Camera():
    # Note that the Camera is a thread safe Singleton. This prevents Picamera2 from being initialized twice.
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            with cls._lock():
                if cls._instance == None:
                    cls._instance = super().__new__(
                        cls, *args, **kwargs)
        return cls._instance

    def __init__(self, main_resolution, backup_resolution):
        self._camera = Picamera2()

        self.verifyResolution(main_resolution)
        self.verifyResolution(backup_resolution)

        self._configuration = self.__createConfig(
            main_resolution, backup_resolution)
        self._camera.configure(self._configuration)
        # TODO: Add other encoders. For example the null encored to capture raw data
        self._encoder = H264Encoder()

    def startBackupRecording(self, filepath):
        self._camera.start_recording(self._encoder, filepath, Quality.MEDIUM)

    def stop(self):
        self._camera.stop_recording()

    def pollCurrent(self):
        request = self._camera.capture_request()
        result = request.make_array("main")
        request.release()
        return result

    def is_running(self):
        return self._camera.started

    def __createConfig(self, main_resolution, backup_resolution):
        # This configures the camera so that the backup stream with backup_resolution can be recorded,
        # but at any point a still image of resolution main_resolution can be taken.
        return self._camera.create_video_configuration(
            {"size": main_resolution}, {"size": backup_resolution}, encode="lores")

    def __verifyResolution(self, resolution):
        if resolution[0] > self._camera.sensor_resolution[0] or resolution[1] > self._camera.sensor_resolution[1]:
            raise ValueError("Given resolution is too large!")
        elif resolution[0] < 64 or resolution[1] < 64:
            raise ValueError("Given resolution is too small!")
