import cv2
import filetype

class imagesProcessing():
    def __init__(self):
        return
        
    # Important - openvc reads images in BGR
    def read_image(self, path):
        self.image = cv2.imread(path)
        # checkpoint
        # print("Image shape={0}".format(image.shape))
        return self.image

    def read_video(self, path):
        cap = cv2.VideoCapture(path)
        height, width = None, None
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
            #Create Thumbnail of video
            #vidcap = cv2.VideoCapture(videopath)
            #success,image = vidcap.read()
            #if success:
            #    cv2.imwrite("./frame.jpg", image)     # save frame as JPEG file
            #vidcap.release()
            #return image

    def check_File(self, filepath):
        #print("method check_file in preprocessor")
        #kind = filetype.guess('tests/fixtures/sample.jpg')
        #if kind is None:
        #    print('Cannot guess file type!')

        #print('File extension: %s' % kind.extension)
        #print('File MIME type: %s' % kind.mime)

        ##if video
        #vidcap=cv2.VideoCapture(filepath)
        #vidcap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
        #duration = vidcap.get(cv2.CAP_PROP_POS_MSEC)
        #width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        #height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        #n_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        #image = self.get_firstImage(filepath)


        ##wenn alles erfüllt, dann True zurückgeben
        return True