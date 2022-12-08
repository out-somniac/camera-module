from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Encoder


class Camera():
    def __init__(self, main_resolution, backup_resolution, no_encoding=False):
        '''
        Disclaimer: do not initialize twice
        '''
        self._camera = Picamera2()

        self.__verify_resolution(main_resolution)
        self.__verify_resolution(backup_resolution)

        self._configuration = self.__create_config(
            main_resolution, backup_resolution)
        self._camera.configure(self._configuration)
        if no_encoding:
            self._encoder = Encoder()
        else:
            self._encoder = H264Encoder()

    def set_log_output(self, output_path):
        '''
        Specifies the file to which to send the log output
        Parameters:
        output_path (string)- path to the file
        '''
        output_stream = open(output_path, mode='a')
        self._camera.set_logging(output=output_stream)

    def start_recording(self, filepath):
        '''
        Starts recording video to the file specified in the filepath
        Parameters:
        filepath (string) - path to the file
        '''
        self._camera.start_recording(self._encoder, filepath)

    def stop_recording(self):
        self._camera.stop_recording()

    def get_frame(self):
        '''
        Saves the current frame from the main stream
        Returns:
        np.ndarray - numpy array that represents the RGBA values
        '''
        request = self._camera.capture_request()
        result = request.make_array("main")
        request.release()
        return result

    def __create_config(self, main_resolution, backup_resolution):
        '''
        This configures the camera so that the backup stream with backup_resolution can be recorded,
        but at any point a still image of resolution main_resolution can be taken.
        Parameters:
        main_resolution (Tuple(int, int))- resolution for the main stream (pictures) (ex. (1920, 1080))
        backup_resolution (Tuple(int, int))- resolution for the backup stream (video) (ex. (1920, 1080))
        Returns:
        camera configuration
        '''
        return self._camera.create_video_configuration(
            {"size": main_resolution}, {"size": backup_resolution}, encode="lores")

    def __verify_resolution(self, resolution):
        '''
        Checks if the given resolution is acceptable
        if not raises ValueError
        '''
        if resolution[0] > self._camera.sensor_resolution[0] or resolution[1] > self._camera.sensor_resolution[1]:
            raise ValueError("Given resolution is too large!")
        elif resolution[0] < 64 or resolution[1] < 64:
            raise ValueError("Given resolution is too small!")

    def get_metadata(self):
        '''
        Returns:
        dictionary of information about conditions of the image capture
        ex. ExposureTime
        '''
        return self._camera.capture_metadata()

    def get_main_format(self):
        '''
        Returns:
        Format of the main stream (photos)
        '''
        return self._configuration['main']['format']

    def get_backup_format(self):
        '''
        Returns:
        Format of the backup stream (video)
        '''
        return self._configuration['lores']['format']

    def get_main_resolution(self):
        '''
        Returns:
        Resolution of the main stream (photos)
        '''
        return self._configuration['main']['size']

    def get_backup_resolution(self):
        '''
        Returns:
        Resolution of the backup stream (videos)
        '''
        return self._configuration['lores']['size']
