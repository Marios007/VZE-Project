import cv2

class imagesProcessing():

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
            vidcap = cv2.VideoCapture(videopath)
            success,image = vidcap.read()
            if success:
                cv2.imwrite("./frame.jpg", image)     # save frame as JPEG file
            vidcap.release()
            return image

    def createGraphicsScene(self, filepath):
        pixmap = QtGui.QPixmap(filepath)
        pixmap_scaled = pixmap.scaled(790, 410)
        graphicsScene = QtWidgets.QGraphicsScene(self)
        graphicsScene.addPixmap(pixmap_scaled)
        return graphicsScene