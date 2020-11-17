import cv2

class imagesProcessing():
    def __init__(self):
        return
        
    # Important - openvc reads images in BGR
    def read_image(self, path):
        self.image = cv2.imread(path)
        # checkpoint
        # print("Image shape={0}".format(image.shape))
        return self.image

    def read_video(path):
        cap = cv2.VideoCapture(path)
        height, width = None, None
        return cap, height, width

    def get_dimensions(image):
        height, width = image.shape[:2]
        # checkpoint
        # print("height={0}, width={1}".format(height, width))
        return height, width

    def show_image(title, image):
        cv2.imshow(title, image)
        return

    def resize_image(image, scale):
        width = int(image.shape[1] * scale / 100)
        height = int(image.shape[0] * scale / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
        return resized