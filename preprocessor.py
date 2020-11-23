import cv2
import filetype
import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage, QPixmap

class ImageProcessing():
    def __init__(self, logicInterface, vzeController):
        self.ILogic = logicInterface
        self.vzeController = vzeController
        
    # Important - openvc reads images in BGR
    def read_image(self, path):
        self.image = cv2.imread(path)
        # checkpoint
        # print("Image shape={0}".format(image.shape))
        return self.image

    def read_video(self, path):
        cap = cv2.VideoCapture(path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return cap, height, width

    def get_dimensions(self, image):
        height, width = image.shape[:2]
        # checkpoint
        # print("height={0}, width={1}".format(height, width))
        return height, width

    def show_image(self, title, image):
        cv2.imshow(title, image)
        return

    def resize_image(self, image, scale):
        width = int(image.shape[1] * scale / 100)
        height = int(image.shape[0] * scale / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
        return resized

    def get_firstImage(self, videopath):
        #Create previewImage of video
        vidcap = cv2.VideoCapture(videopath)
        success,image = vidcap.read()

        if success:
            return image
        else:
            print("PreviewImage could not be created!")
            return None
        
        vidcap.release()
        
        

    def check_fileType(self, filepath):
        """
        method to check the fileType.
            returns -1 in case of error
            returns 1 if file is an image
            returns 2 if file is a video and creates the previewImage from it
        """
        print("method check_file in preprocessor")
        image = None
        kind = filetype.guess(filepath)

        if kind is None:
            print('Cannot guess file type!')
            return -1,None

        elif(str(kind.mime).startswith("image")):
            print("File is an image")
            image = self.read_image(filepath)
            return 1,image

        elif(str(kind.mime).startswith("video")):
            print("File is a video")
            image = self.get_firstImage(filepath)
            return 2,image

        else:
            print("Filetype unknown")
            return -1,None


    def check_fileResolution(self, fileType, filepath):
        """
        method to check the resolution of a file
            returns -1 if resolution is too high
            returns -2 if resolution is too low
            returns 1 if resolution is ok
        """

        if(fileType == 1):
            #File is an image
            print("Image-Resolution-Check")
            img = self.read_image(filepath)
            heigth, width = self.get_dimensions(img)

            print("ImageResolution: " + str(width) + "x" + str(heigth))

        elif(fileType == 2):
            #File is a video
            print("Video-Resolution-Check")
            
            vidcap,heigth,width = self.read_video(filepath)

            print("VideoResolution: " + str(width) + "x" + str(heigth))

        if(width < 800) or (heigth < 600):
            return -2
        elif(width > 1920) or (heigth > 1080):
            return -1                

        return 1

    def check_fileLength(self, filepath):
        """
        method to check the length of the video
            returns -1 if video is too long
            returns 1 if video is ok
        """

        max_duration = 600
        vidcap=cv2.VideoCapture(filepath)
        
        fps = vidcap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps
        
        vidcap.release()

        print("File has a length of " + str(duration) + " seconds")

        if(duration > max_duration):
            return -1
        else:
            return 1


class VideoThread(QThread):
    #changePixmap = pyqtSignal(QImage)
    img = None

    def __init__(self, path, gui, parent=None):
        QThread.__init__(self, parent)
        self.path = path
        self._run_flag = True
        self.gui = gui

    def run(self):
        print("play video " + str(self.path))
        self.cap = cv2.VideoCapture(self.path)
        while self._run_flag:
            read, frame = self.cap.read()
            if not read:
                break
                
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(800, 480, Qt.KeepAspectRatio)
            #self.changePixmap.emit(p)
            self.gui.setVideoImage(p)

            if cv2.waitKey(10) & 0xFF ==ord("q"):
                break
        print("done")
        self.cap.release()

    def stopVideo(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        self.cap.release()