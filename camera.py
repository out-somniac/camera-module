from picamera2 import Picamera2
from picamera2.encoders import H264Encode


class Camera:
    def __init__(self):
        self.m_camera = Picamera2()

    def startRecording(self, filepath):
        video_config = self.m_camera.create_video_configuration()
        self.m_camera.configure(video_config)
        encoder = H264Encoder(10000000)
        self.m_camera.start_recording(encoder, filepath)

    def stopRecording(self):
        self.m_camera.stop_recording()
