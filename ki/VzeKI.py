import numpy as np
#import pandas as pd
from pandas import DataFrame
from pandas import read_csv

import cv2
import pickle
import filetype
from keras.models import load_model
from constants import *
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QImage
from pandas.core import frame
# for debugging inside thread
#import pydevd
from tensorflow.config import experimental
from tensorflow.python.client import device_lib


class VzeImageProcessing():
       
    def __init__(self, vzeController):
        self.vzeController = vzeController

    def read_video(self, path):
        cap = cv2.VideoCapture(path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return cap, height, width

    def read_image(self, path):
        self.image = cv2.imread(path)
        return self.image

    def get_dimensions(self, image):
        return image.shape[:2]

    def show_image(self, title, image):          
        return cv2.imshow(title, image)

    def resize_image(self, image, scale):
        # half FHD resolution
        width = int(960)
        height = int(540)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
        return resized

    def convert_grayscale(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def equalize_histogram(self, image):
        image = cv2.equalizeHist(image)
        return image
    
    def print_text_on_image(self, image, text, x_min, y_min, font_size, color, thickness):
        cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, [0,0,0], thickness+1)
        cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, color, thickness)
        return image

    def preprocessing_images(self, image):
        """
        maybe we should use variables instead of constants
        """
        image = cv2.resize(image, (32,32), interpolation = cv2.INTER_AREA) 
        image = self.convert_grayscale(image)
        image = self.equalize_histogram(image)
        image = image/255
        image = image.reshape(1,32,32,1)
        # checkpoint
        #print("shape for cnn: ", image.shape)
        return image


    def print_boxes_on_image(self, image, bounding_boxes_final, sign_names, probabilities):
        box_color = [0, 0, 255]
        text_color = [0, 255, 0]

        for i in range(len(bounding_boxes_final)):
            font_size = bounding_boxes_final[i,2]/90
            cv2.rectangle(image, (bounding_boxes_final[i,0], bounding_boxes_final[i,1]),
                                (bounding_boxes_final[i,0] + bounding_boxes_final[i,2],
                                bounding_boxes_final[i,1] + bounding_boxes_final[i,3]),
                                box_color, 2)
            self.print_text_on_image(image, (str(sign_names[i]) + " " + str(np.format_float_positional(probabilities[i,0],precision=2))),
                                bounding_boxes_final[i,0], bounding_boxes_final[i,1]-5, font_size, text_color, 1)

        return image

    def get_firstImage(self, videopath):
        #Create previewImage of video
        vidcap = cv2.VideoCapture(videopath)
        success,image = vidcap.read()

        if success:
            vidcap.release()
            return image
        else:
            print("PreviewImage could not be created!")
            vidcap.release()
            return None


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

        elif str(kind.mime).startswith("image"):
            print("File is an image")
            image = self.read_image(filepath)
            return 1,image

        elif str(kind.mime).startswith("video"):
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

        if fileType == 1:
            #File is an image
            print("Image-Resolution-Check")
            img = self.read_image(filepath)
            heigth, width = self.get_dimensions(img)

            print("ImageResolution: " + str(width) + "x" + str(heigth))

            if (width < IMAGE_MIN_WIDTH or heigth < IMAGE_MIN_HEIGTH):
                return -2
            elif (width > IMAGE_MAX_WIDTH or heigth > IMAGE_MAX_HEIGTH):
                return -1    


        elif fileType == 2:
            #File is a video
            print("Video-Resolution-Check")
            
            vidcap,heigth,width = self.read_video(filepath)

            print("VideoResolution: " + str(width) + "x" + str(heigth))

            if (width < VIDEO_MIN_WIDTH or heigth < VIDEO_MIN_HEIGTH):
                return -2
            elif (width > VIDEO_MAX_WIDTH or heigth > VIDEO_MAX_HEIGTH):
                return -1                

        return 1

    def check_fileLength(self, filepath):
        """
        method to check the length of the video
            returns -1 if video is too long
            returns 1 if video is ok
        """

        vidcap=cv2.VideoCapture(filepath)
        
        fps = vidcap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count/fps
        
        vidcap.release()

        print("File has a length of " + str(duration) + " seconds")

        if duration > VIDEO_MAX_DURATION:
            return -1
        else:
            return 1

class VzeKI:
    # Klassenkonstanten
    DNN_DIM = (416, 416)
    PROBABILITY_MINIMUM = 0.25
    THRESHOLD = 0.25
    BOX_SIZE_THRESHOLD = 20

    def __init__(self, videoPath: str):
        # Konstruktor lädt Labels, CNN-Model und YOLO-Modell
        # Definition Konstanten zur Initialisierung
        LABEL_PATH = "./ki/input/labels/signnames.csv"
        CNN_MODEL_PATH = "./ki/input/cnn/fit_gen"
        #CNN_MODEL_PATH = "./ki/input/cnn/test_model"
        YOLO_CONFIG_PATH = "./ki/input/yolo/yolov3_ts.cfg"
        YOLO_WEIGHTS_PATH = "./ki/input/yolo/yolov3_ts.weights"
        YOLO_MEAN_PICKLE = "./ki/input/yolo/mean_image_rgb.pickle"

        self.VzeIP = VzeImageProcessing(None)      
        self.videoPath = videoPath
        self.currentTime = 0
        self.previousTime = 0
        self.frames_count = 1

        physical_devices = experimental.list_physical_devices('GPU')
        #print("Num GPUs:", len(physical_devices))
        if len(physical_devices) > 0:
            experimental.set_memory_growth(physical_devices[0], True)


        # Labels laden
        #try:
        self.labels = read_csv(LABEL_PATH, sep=";", encoding="mac_latin2")
        #except expression as identifier:
        #    pass


        # CNN-Modell laden
        #try:
        self.model = load_model(CNN_MODEL_PATH)
        #except expression as identifier:
         #   pass

         
        # Pickle? Laden
        #try:
        self.mean = pickle.load(open(YOLO_MEAN_PICKLE, "rb"), encoding='latin1')
        #except expression as identifier:
        #   pass

        # YOLO-Network initialisieren
        self.yolo_network = cv2.dnn.readNetFromDarknet(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH)

        # Layer initialsieren
        self.layers_names_output = [self.yolo_network.getLayerNames()[i[0] - 1] for i in self.yolo_network.getUnconnectedOutLayers()]

        # set CUDA as the preferable backend and target
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            self.yolo_network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.yolo_network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
            print("FOUND GPU - USING GPU")
        else:
            print("NO GPU - USING CPU")


    ### KI-Methoden

    def yolo_detection(self, image):
        self.yolo_network.setInput(cv2.dnn.blobFromImage(image, 1 / 255.0, self.DNN_DIM, swapRB=True, crop=False))
        return self.yolo_network.forward(self.layers_names_output)


    def detect_signs(self, image, height, width):
        #only for debugging
        number_traffic_signs = 0
        results = []
        sign_names = np.array([])
        
        #for one anchor box: [tx, ty, tw, th, obj score, class probs.]
        output_from_yolo_network = self.yolo_detection(image)
        
        #create arrays out of list
        arr_output_layer1 = np.array(output_from_yolo_network[0], dtype=np.float32)
        arr_output_layer2 = np.array(output_from_yolo_network[1], dtype=np.float32)
        arr_output_layer3 = np.array(output_from_yolo_network[2], dtype=np.float32)
        # concetanate arrays
        arr_output_layers = np.vstack((arr_output_layer1,arr_output_layer2,arr_output_layer3))

        # create index array with indexes if probability is higher than the min value
        max_output_layers = np.argwhere(arr_output_layers[:,5:]>self.PROBABILITY_MINIMUM)

        # create array with the relevant detected boxes and confidences
        if max_output_layers.size == 0:
            returnObject = VzeObject(image)
        else:
            arr_output_layers_relevant = arr_output_layers[max_output_layers[:,0]]
            confidences = np.amax(arr_output_layers_relevant[:,5:], axis=1)

            box_current = arr_output_layers_relevant[:,:4] * np.array([width, height, width, height])
            # xmin, ymin, box_width, box_height
            min_point_offset = 0.998
            box_size_offset = 1.2

            bounding_boxes = np.array([(box_current[:,0]-(box_current[:,2]/2))*min_point_offset,
                                    (box_current[:,1]-(box_current[:,3]/2))*min_point_offset,
                                    box_current[:,2]*box_size_offset,
                                    box_current[:,3]*box_size_offset], dtype=int).T.clip(min=0) # to prevent negativ values after box calculation

            # get all bounding boxes and corresponding confidences with box_height and box_width grater than box_threshold
            min_size_bounding_boxes = np.argwhere(bounding_boxes[:,2:]>self.BOX_SIZE_THRESHOLD)
            if min_size_bounding_boxes.size == 0:
                returnObject = VzeObject(image)
            else:
                bounding_boxes = bounding_boxes[min_size_bounding_boxes[:,0]]
                confidences = confidences[min_size_bounding_boxes[:,0]]
                    
                # NMSBoxes dont accept an array
                bounding_boxes_list = np.ndarray.tolist(bounding_boxes)

                # non-maximum suppression of given bounding boxes, deletes duplicates, contains number of kept indicies
                results = cv2.dnn.NMSBoxes(bounding_boxes_list, confidences, self.PROBABILITY_MINIMUM, self.THRESHOLD)

                # only for fps analysis
                number_traffic_signs = len(results)

                bounding_boxes_final = bounding_boxes[results.flatten()]
                
                captured_signs_array = np.array([[[]]])

                #creating images of detected traffic signs
                for i in range(len(bounding_boxes_final)):
                    captured_sign = image[bounding_boxes_final[i,1]:bounding_boxes_final[i,1]+bounding_boxes_final[i,3],
                                        bounding_boxes_final[i,0]:bounding_boxes_final[i,0]+bounding_boxes_final[i,2],:]
                    # Checkpoint
                    #show_image("sign" + str(i), captured_sign)
                    captured_sign = self.VzeIP.preprocessing_images(captured_sign)
                    # Checkpoint
                    #show_image("sign" + str(i), captured_sign[0,:,:,0],)
                    #print("processing_done")
                    captured_signs_array = np.vstack([captured_signs_array,captured_sign]) if captured_signs_array.size else captured_sign
                    # Checkpoint
                    #print(captured_signs_array.shape)


                # Checkpoint
                # for i in range(len(captured_signs_array)):
                #     show_image("arr", captured_signs_array[i])
                #     cv2.waitKey(250)
        
                # feeding the images through the cnn (parallel processed)
                probabilities_all = self.model.predict(captured_signs_array)
                prediction = np.argmax(probabilities_all, axis = 1)
                sign_names = self.labels.iloc[prediction, 2]
                sign_names = np.array(sign_names)
                probabilities = probabilities_all[np.arange(probabilities_all.shape[0])[:, None],prediction.reshape(prediction.shape[0],1)[:]]*100

                # checkpoint
                #print("class: {0} - predict: {1} - probability: {2}".format(prediction, sign_names , probabilities))        
                #prediction ist ein Array der detektierten Schilder-IDs
                #probablity enthält die Wahrscheinlichkeit der einzelnen Schilder
                #bounding_boxes enthält die jeweiligen den XY-Wert der Box sowie Breite und Höhe der Box
                
                returnObject = VzeObject(self.VzeIP.print_boxes_on_image(image, bounding_boxes_final, sign_names, probabilities))
                for i in range(len(bounding_boxes_final)):
                    returnObject.addSign(TrafficSign(prediction[i],(bounding_boxes_final[i][2],bounding_boxes_final[i][3]),(bounding_boxes_final[i][0],bounding_boxes_final[i][1]),probabilities[i][0]))
                    print("SchildID: {0} - Wahrscheinlichkeit: {1} - X: {2} - Y: {3} - Breite x Höhe: {4} x {5}".format(prediction[i], probabilities[i][0], bounding_boxes_final[i][0],bounding_boxes_final[i][1],bounding_boxes_final[i][2],bounding_boxes_final[i][3]))
            
        return returnObject
    
    ### Hilfsmethoden

    def calculate_time(self, currentTime):
                
        timeDifference = (currentTime - self.previousTime)/cv2.getTickFrequency()
        if timeDifference != 0:
            fps = round(1/timeDifference, 1)
        else:
            fps = 1
        self.frames_count += 1
        self.previousTime = currentTime
        return timeDifference, fps

    def processFrame(self, frame, currentTime):

        frame = self.VzeIP.resize_image(frame, 50)           
        height, width = self.VzeIP.get_dimensions(frame)
        returnedObject = self.detect_signs(frame, height, width)
        self.estimated_time, fps = self.calculate_time(currentTime)
        text_info = "time {0:.3f} s - fps: {1}".format(self.estimated_time, fps)
        returnedObject.frame = self.VzeIP.print_text_on_image(returnedObject.frame, text_info, 20, 20, 0.5, [0,0,255], 2)
        returnedObject.frameId = self.frames_count
        returnedObject.convertQt()
        return returnedObject


class VideoThreadKI(QThread):
    """
    Thread for the AI processing and for putting the video (frames into the GUI)
    """
    def __init__(self, path, gui, parent=None):
        QThread.__init__(self, parent)
        self.path = path
        self._run_flag = True
        self.gui = gui
        self.ki = VzeKI(self.path)

    def run(self):
        print("play video " + str(self.path))
        self.cap = cv2.VideoCapture(self.path)
        while self._run_flag:
            currentTime = cv2.getTickCount()
            read, frame = self.cap.read()
            if not read:
                break
            currentObject = self.ki.processFrame(frame, currentTime)
            self.gui.processKIData(currentObject)

            if cv2.waitKey(10) & 0xFF ==ord("q"):
                break
        self.cap.release()
        self.gui.activateResultBtn()        
        print("done")
        

    def stopVideo(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
        self.cap.release()


class VzeObject:  
    """
    Class information for each frame
    frame = is the frame
    frameId = is a coutner starts with 1
    numDetectSigns = amount of detected signs in one frame
    detectedSigns = array of TrafficSign object
    """
    def __init__(self, processedFrame):
         self.frame = processedFrame
         self.frameId = 0
         self.numDetectSigns = 0
         self.detectedSigns = []

    def addSign(self, sign):
        self.numDetectSigns += 1
        self.detectedSigns.append(sign) 

    def convertQt(self):
        rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        #self.frame = convertToQtFormat.scaled(850, 480, Qt.KeepAspectRatio)
        self.frame = convertToQtFormat.scaled(ANALYZEIMAGE_WIDTH, ANALYZEIMAGE_HEIGTH, Qt.KeepAspectRatio)

class TrafficSign:
    """
    Class with information about a traffic sign
    prob = probapility
    SignId = is ID from csv
    box_W_H = Bounding Box size a Tuple
    coordinateXY = is coordinate of upper left corner of bounding box
    """
    def __init__(self, signID, box_W_H, coordinateXY, prob):
        self.prob = prob
        self.signID = signID
        self.box_W_H = box_W_H
        self.coordinateXY = coordinateXY


