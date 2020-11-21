import cv2
import filetype

class imageProcessing():
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
        # -1 zurückgeben, wenn Auflösung zu hoch, 
        # -2 zurückgeben, wenn Auflösung zu niedrig, 
        # 1 zurückgeben, wenn alles passt

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

        ##wenn alles erfüllt, dann True zurückgeben
        return 1

    def check_fileLength(self, filepath):
        # -1 zurückgeben, wenn Video zu lang ist
        #  1 zurückgeben, wenn alles passt

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

    def playVideoStream(self, path):
        """
        testmethod to play a video
        """
        print("play video " + str(path))
        self.video = cv2.VideoCapture(path)
        self.running = True
        while(self.video.isOpened()):
            read, frame = self.video.read()
            if not read:
                break
            cv2.imshow("test", frame)
            #self.ILogic.streaming(frame)
            #SL: Hier muss eigentlich nur die Methode showImageOnAnalyzeScreen der VzeGui aufgerufen werden. Weiß aber noch nicht wie.
            if cv2.waitKey(3) & 0xFF ==ord("q"):
                break
        self.video.release()
        cv2.destroyAllWindows()