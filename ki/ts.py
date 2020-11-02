import numpy as np
import pandas as pd
import cv2
import pickle
from keras.models import load_model


# Important - openvc reads images in BGR
def read_image(path):
    image = cv2.imread(path)
    # checkpoint
    # print("Image shape={0}".format(image.shape))
    return image

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

def load_models(path_yolo_weights, path_yolo_config):
    labels = pd.read_csv("./input/labels/signnames.csv", sep=";")
    # checkpoint
    # print(labels.head())

    # pretrained cnn model
    model = load_model("./input/cnn/test_model")
    # mean image for preprocessing
    with open('./input/yolo/mean_image_rgb.pickle', 'rb') as f:
        mean = pickle.load(f, encoding='latin1')
    # checkpoint
    # print(mean['mean_image_rgb'].shape)  # (3, 32, 32)

    yolo_network = cv2.dnn.readNetFromDarknet(path_yolo_config, path_yolo_weights)
    return labels, model, yolo_network, mean

def get_layers(yolo_network):
    layers_all = yolo_network.getLayerNames()
    # checkpoint
    # print(layers_all)

    layers_names_output = [layers_all[i[0] - 1] for i in yolo_network.getUnconnectedOutLayers()]
    # checkpoint
    # print(layers_names_output)
    return layers_all, layers_names_output
    
def yolo_detection(image, dnn_dim, layers_names_output):
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, dnn_dim, swapRB=True, crop=False)
    yolo_network.setInput(blob)
    output_from_yolo_network = yolo_network.forward(layers_names_output)
    return output_from_yolo_network

def calculate_time(frames_count, start_time, end_time):
    estimated_time = (end_time - start_time)/cv2.getTickFrequency()
    fps = round((frames_count / estimated_time), 1)
    print("calculating time {0:.3f} seconds - FPS: {1}".format(estimated_time, fps))
    #print('FPS:', round((frames_count / estimated_time), 1))
    return estimated_time, fps

def print_text_on_image(image, text, x_min, y_min, font_size, color, thickness):
    cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, [0,0,0], thickness+1)
    cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, color, thickness)
    return image

def convert_grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def equalize_histogram(image):
    image = cv2.equalizeHist(image)
    return image

def preprocessing_images(image):
    """
    maybe we shpuld use variables instead of constants
    """
    image = cv2.resize(image, (32,32), interpolation = cv2.INTER_AREA) 
    image = convert_grayscale(image)
    image = equalize_histogram(image)
    image = image/255
    image = image.reshape(1,32,32,1)
    # checkpoint
    #print("shape for cnn: ", image.shape)
    return image

def detect_signs(image, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold):
    output_from_yolo_network = yolo_detection(image, dnn_dim, layers_names_output)

    bounding_boxes = []
    confidences = []
    
    # checkpoint
    #count=0

    for result in output_from_yolo_network:
        for detected_objects in result:
            # checkpoint
            # count+=1

            max_confidence = max(detected_objects[5:])

            # Eliminating weak predictions by minimum probability
            if max_confidence > probability_minimum:
                # Scaling bounding box coordinates to the initial frame size and get top left coordinates
                box_current = detected_objects[0:4] * np.array([width, height, width, height])
                x_center, y_center, box_width, box_height = box_current
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                # Adding results to lists
                bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                confidences.append(float(max_confidence))

                # checkpoint
                # print(max_confidence, x_min, y_min, box_current)

    # non-maximum suppression of given bounding boxes, deletes duplicates
    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)

    box_color = [0, 0, 255]
    text_color = [0, 255, 0]

    if len(results) > 0:
        for i in results.flatten():
            x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
            box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]
            
            """
            """
            # checkpoint for future cnn
            captured_sign = image[y_min:y_min+int(box_height), x_min:x_min+int(box_width), :]
            #checkpoint
            #show_image("estimated_sign", captured_sign)
            #print("captured_sign before processing: ", captured_sign.shape, captured_sign.dtype)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            #cv2.imwrite("captured_sign"+str(i)+".jpg", captured_sign)

            # preparation of captured signs for the cnn       
            if captured_sign.shape[:1] == (0,) or captured_sign.shape[1:2] == (0,):
                pass
            else:        
                captured_sign_pcd = preprocessing_images(captured_sign)

                # feeding th cnn and get prediction and probability
                probabilities = model.predict_proba(captured_sign_pcd)
                prediction = np.argmax(probabilities, axis = 1)
                name = labels.iat[int(prediction), 1]
                probability = probabilities[0,prediction]*100
                # checkpoint
                print("class: {0} - predict: {1} - probability: {2:.2f}%".format(prediction, name , float(probability)))
                print()

                # Preparing text with label and confidence for current bounding box
                text_box_sign = '{}: {:.2f}'.format(name, float(probability))
            
                # Putting text with label and probability on the original image
                print_text_on_image(image, text_box_sign, x_min, y_min-5, 0.6, text_color, 1)



            """
            """

            # Drawing bounding box on the original current frame
            cv2.rectangle(image, (x_min, y_min), (x_min + int(box_width), y_min + int(box_height)), box_color, 2)

    # Checkpoint
    #print("detected_objects:", count)

    return image


"""
main
"""
probability_minimum = 0.25
threshold = 0.25
frames_count = 1
estimated_time = 0

#path_image = "C:/Users/Aqua/Desktop/yolo_object_detection/yolo-traffic-signs/Traffic_signs_data/00039.jpg"
path_image = "./test_rl.jpg"
path_video = "./input/ts_test_vid.mp4"
path_yolo_weights = "./input/yolo/yolov3_ts.weights"
path_yolo_config = "./input/yolo/yolov3_ts.cfg"
#path_yolo_weights = "./input/yolo_tiny/yolov3-spp.weights"
#path_yolo_config = "./input/yolo_tiny/yolov3_tiny.cfg"

labels, model, yolo_network, mean = load_models(path_yolo_weights, path_yolo_config)
layers_all, layers_names_output = get_layers(yolo_network)
dnn_dim = (416, 416)

"""
image
"""

image = read_image(path_image)
# checkpoint
# show_image("image", image)
image = resize_image(image, 50)
height, width = get_dimensions(image)

# yolo net calculation
start_time = cv2.getTickCount()
image = detect_signs(image, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold)
end_time = cv2.getTickCount()

# time and text processing
estimated_time, fps = calculate_time(frames_count, start_time, end_time)
text_info = "time {0:.3f} s - fps: {1}".format(estimated_time, fps)
image = print_text_on_image(image, text_info, 20, 20, 0.7, [0,255,0], 1)

show_image("bounding_boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# saves image
cv2.imwrite("yolo_image.jpg", image)

"""
video
"""
"""
cap, height, width = read_video(path_video)
while(cap.isOpened()):
    # start timer for fps calculation
    start_time = cv2.getTickCount()

    ret, frame = cap.read()
    if not ret:
        break

    if width is None or height is None:
        height, width = get_dimensions(frame)

    detect_signs(frame, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold)
    end_time = cv2.getTickCount()
    
    estimated_time += (end_time - start_time)/cv2.getTickFrequency()
    calculate_time(frames_count, estimated_time)
    text_info = "time {0:.3f} s - fps: {1}".format(estimated_time, fps)
    image = print_text_on_image(image, text_info, 20, 20, 0.5, [0,0,255], 2)

    show_image("bounding_boxes", image)
    frames_count+=1
    if cv2.waitKey(10) & 0xFF ==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
"""