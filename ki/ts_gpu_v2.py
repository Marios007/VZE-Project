"""
done:
changed box_size for cnn input by factor 1.35
print boxes and labels after feeding all captured signs to the cnn
if the cnn probability is low (maybe <=65%) dont show box and label

to do:
play with probability mininimum and threshold
"""

import numpy as np
import pandas as pd
import cv2
import pickle
from keras.models import load_model
import tensorflow as tf

# allow tensorflow to use gpu
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


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
    labels = pd.read_csv("./input/labels/signnames.csv", sep=";", encoding="mac_latin2")
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

def calculate_time(estimated_time, frames_count, start_time, end_time, frames_hist, number_traffic_signs):
    frameTime = (end_time - start_time)/cv2.getTickFrequency()
    estimated_time += (end_time - start_time)/cv2.getTickFrequency()
    avgFps = round((frames_count / estimated_time), 1)
    frameFps = round((1/ frameTime), 1)

    frames_hist = np.vstack((frames_hist, np.array([frames_count, frameTime, estimated_time, frameFps, avgFps, number_traffic_signs])))

    #print("calculating time {0:.3f} seconds - FPS: {1}".format(estimated_time, fps))
    #print('FPS:', round((frames_count / estimated_time), 1))
    return estimated_time, avgFps, frameFps, frames_hist

def print_text_on_image(image, text, x_min, y_min, font_size, color, thickness):
    cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, [0,0,0], thickness+1)
    cv2.putText(image, text, (x_min, y_min), cv2.FONT_HERSHEY_DUPLEX, font_size, color, thickness)
    return image

def convert_grayscale(image):
    #GPU
    #image = cv2.cuda.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #CPU
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def equalize_histogram(image):
    #GPU
    #image = cv2.cuda.equalizeHist(image)
    #CPU
    image = cv2.equalizeHist(image)
    return image

def preprocessing_images(image):
    """
    maybe we should use variables instead of constants
    """
    #GPU
    # source = cv2.cuda_GpuMat()
    # source.upload(image)
    # image_cuda = cv2.cuda.resize(source, (32,32), interpolation = cv2.INTER_AREA) 
    # image_cuda = convert_grayscale(image_cuda)
    # image_cuda = equalize_histogram(image_cuda)
    # image = image_cuda.download()
    
    #CPU
    image = cv2.resize(image, (32,32), interpolation = cv2.INTER_AREA) 
    image = convert_grayscale(image)
    image = equalize_histogram(image)

    image = image/255
    image = image.reshape(1,32,32,1)
    
    # checkpoint
    #print("shape for cnn: ", image.shape)
    return image

def detect_signs(image, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold, dnn_dim):
    #only for debugging
    number_traffic_signs = 0
    
    #for one anchor box: [tx, ty, tw, th, obj score, class probs.]
    output_from_yolo_network = yolo_detection(image, dnn_dim, layers_names_output)
    
    #create arrays out of list
    arr_output_layer1 = np.array(output_from_yolo_network[0], dtype=np.float32)
    arr_output_layer2 = np.array(output_from_yolo_network[1], dtype=np.float32)
    arr_output_layer3 = np.array(output_from_yolo_network[2], dtype=np.float32)
    # concetanate arrays
    arr_output_layers = np.vstack((arr_output_layer1,arr_output_layer2,arr_output_layer3))
    # create index array with indexes if probability is higher than the min value
    max_output_layers = np.argwhere(arr_output_layers[:,5:]>probability_minimum)
    # create array with the relevant detected boxes and confidences
    if max_output_layers.size == 0:
        results = []
    else:
        arr_output_layers_relevant = arr_output_layers[max_output_layers[:,0]]
        confidences = np.amax(arr_output_layers_relevant[:,5:], axis=1)
        #confidences.reshape(confidences.shape[0],1)

        box_current = arr_output_layers_relevant[:,:4] * np.array([width, height, width, height])

        #xmin, ymin, box_width, box_height
        bounding_boxes = np.array([box_current[:,0]-(box_current[:,2]/2),
                                    box_current[:,1]-(box_current[:,3]/2),
                                    box_current[:,2],
                                    box_current[:,3]], dtype=int).T

        #NMSBoxes dont accept an array, adress this issue later
        bounding_boxes_list = np.ndarray.tolist(bounding_boxes)

        # non-maximum suppression of given bounding boxes, deletes duplicates, contains number of kept indicies
        results = cv2.dnn.NMSBoxes(bounding_boxes_list, confidences, probability_minimum, threshold)

        #only for fps analysis
        number_traffic_signs = len(results)

    """
    bounding_boxes = []
    confidences = []
    
    for result in output_from_yolo_network:
        #print(len(result))
        #print(result)
        for detected_objects in result:
            #list of obj scores from boxes
            max_confidence = max(detected_objects[5:])

            # Eliminating weak predictions by minimum probability
            if max_confidence > probability_minimum:
                #print(len(detected_objects))
                #print(detected_objects)
                # Scaling bounding box coordinates to the initial frame size and get top left coordinates
                
                box_current = detected_objects[0:4] * np.array([width, height, width, height])
                x_center, y_center, box_width, box_height = box_current
                # offsets for bounding boxes
                if box_width > 15.0 and box_height > 15.0:
                    box_width*=1.35
                    box_height*=1.35
                    x_min = int(x_center - (box_width / 2))
                    y_min = int(y_center - (box_height / 2))

                    # Adding results to lists
                    bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                    confidences.append(float(max_confidence))

                    # checkpoint
                    #print(max_confidence, x_min, y_min, box_current)

    
    # non-maximum suppression of given bounding boxes, deletes duplicates, contains number of kept indicies
    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)
    #print(len(results))
    #print(results)
    
    sign_data = np.array([])
    #box_color = [0, 0, 255]
    #text_color = [0, 255, 0]
    
    number_traffic_signs = len(results)


    """

    sign_data = np.array([])

    if len(results) > 0:
        for i in results.flatten():
            x_min, y_min = bounding_boxes[i,0], bounding_boxes[i,1]
            box_width, box_height = bounding_boxes[i,2], bounding_boxes[i,3]
            
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
                """
                # feeding the cnn and get prediction and probability
                probabilities = model.predict_proba(captured_sign_pcd)
                prediction = np.argmax(probabilities, axis = 1)
                name = labels.iat[int(prediction), 2]
                probability = probabilities[0,prediction]*100
                # checkpoint
                #print("class: {0} - predict: {1} - probability: {2:.2f}%".format(prediction, name , float(probability)))
            
                # to prevent boxes and texts from beeing drawn if probability is low
                if probability > 65:
                    # Preparing text with label and confidence for current bounding box
                    text_box_sign = '{}: {:.2f}'.format(name, float(probability))
                    # store data of each captured sign to draw boxes and text after all detected signs are feeded in the cnn
                    sign_data = np.append(sign_data, [x_min, y_min, box_width, box_height, text_box_sign])
                    # feeding the cnn and get prediction and probability
                    probabilities = model.predict_proba(captured_sign_pcd)
                    prediction = np.argmax(probabilities, axis = 1)
                    name = labels.iat[int(prediction), 2]
                    probability = probabilities[0,prediction]*100
                    # checkpoint
                    #print("class: {0} - predict: {1} - probability: {2:.2f}%".format(prediction, name , float(probability)))

    
                    # to prevent boxes and texts from beeing drawn if probability is low
                    if probability > 65:
                        # Preparing text with label and confidence for current bounding box
                        text_box_sign = '{}: {:.2f}'.format(name, float(probability))
                        # store data of each captured sign to draw boxes and text after all detected signs are feeded in the cnn
                        sign_data = np.append(sign_data, [x_min, y_min, box_width, box_height, text_box_sign])


    image = print_boxes_on_image(sign_data, image)
    #print()
    """
    return image, number_traffic_signs


def print_boxes_on_image(sign_data, image):
    box_color = [0, 0, 255]
    text_color = [0, 255, 0]

    for i in range(0,len(sign_data), 5):
        x_min = int(sign_data[i])
        y_min = int(sign_data[i+1])
        box_width = int(sign_data[i+2])
        box_height = int(sign_data[i+3])
        text_box_sign = str(sign_data[i+4])

        font_size = box_width/100*0.9
    
        cv2.rectangle(image, (x_min, y_min), (x_min + int(box_width), y_min + int(box_height)), box_color, 2)
        print_text_on_image(image, text_box_sign, x_min, y_min-5, font_size, text_color, 1)
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
path_video = "./input/Ausschnitt_5.mp4"
path_yolo_weights = "./input/yolo/yolov3_ts.weights"
path_yolo_config = "./input/yolo/yolov3_ts.cfg"
#path_yolo_weights = "./input/yolo_tiny/yolov3-spp.weights"
#path_yolo_config = "./input/yolo_tiny/yolov3_tiny.cfg"

labels, model, yolo_network, mean = load_models(path_yolo_weights, path_yolo_config)
layers_all, layers_names_output = get_layers(yolo_network)
dnn_dim = (416, 416)

# set CUDA as the preferable backend and target
print("[INFO] setting preferable backend and target to CUDA...")
yolo_network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
yolo_network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)



# checkpoint
print("models loaded")

"""
image
"""
"""
image = read_image(path_image)
# checkpoint
#show_image("image", image)


image = resize_image(image, 50)
height, width = get_dimensions(image)
# checkpoint
#show_image("resized", image)

# yolo net calculation
start_time = cv2.getTickCount()
image = detect_signs(image, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold, dnn_dim)
end_time = cv2.getTickCount()

# time and text processing
estimated_time, fps = calculate_time(estimated_time, frames_count, start_time, end_time)
text_info = "time {0:.3f} s - fps: {1}".format(estimated_time, fps)
image = print_text_on_image(image, text_info, 20, 20, 0.7, [0,255,0], 1)

show_image("bounding_boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# saves image
cv2.imwrite("yolo_image.jpg", image)
"""
"""
video
"""
cap, height, width = read_video(path_video)

# to save the video
frame_width = int(cap.get(3)/2)
frame_height = int(cap.get(4)/2)
print(frame_width, frame_height)
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc(*"MJPG"), 10, (frame_width,frame_height))

frames_hist = np.array(["frame", "frame_time", "sum_time", "frame_fps", "avg_fps", "num_detect_ts"])

while(cap.isOpened()):
    # start timer for fps calculation
    start_time = cv2.getTickCount()

    ret, frame = cap.read()
    if not ret:
        break

    frame = resize_image(frame, 50)

    if width is None or height is None:
        height, width = get_dimensions(frame)

    frame, number_traffic_signs = detect_signs(frame, height, width, labels, model, yolo_network, mean, layers_names_output, probability_minimum, threshold, dnn_dim)
    end_time = cv2.getTickCount()
    
    estimated_time, avgFps, frameFps, frames_hist = calculate_time(estimated_time, frames_count, start_time, end_time, frames_hist, number_traffic_signs)
    text_info = "time {0:.3f} s - frame-fps: {1} - avg-fps: {2}".format(estimated_time, frameFps, avgFps)
    frame = print_text_on_image(frame, text_info, 20, 20, 0.5, [0,0,255], 2)
    out.write(frame)
    show_image("bounding_boxes", frame)
    frames_count+=1
    if cv2.waitKey(10) & 0xFF ==ord("q"):
        break

pd.DataFrame(frames_hist).to_csv("./fps_analysis.csv", index=False)

print("done")
cap.release()
out.release()
cv2.destroyAllWindows()