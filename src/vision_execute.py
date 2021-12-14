import os
import torch
import rospy
import numpy as np
import similarity_model
import torchvision
import PIL.Image as IM
import torchvision.transforms as T
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torchvision import transforms
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from os import listdir 
from os.path import isfile, join
import rospy
from vision_utils import get_iou
from detection_msg.msg import objMessage

ENCODER_MODEL_PATH = "./data/FRANK_encoder.pt"
# EMBEDDING_PATH = "./data/models/Frank_embedding_f.npy"

bridge = CvBridge()
model = torch.hub.load('ultralytics/yolov5', 'yolov5l') 
transform_resize = transforms.Resize([512, 512])

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
encoder = similarity_model.ConvEncoder()

# Load the state dict of encoder
encoder.load_state_dict(torch.load(ENCODER_MODEL_PATH, map_location=device))
encoder.eval()
encoder.to(device)
onlyfiles = [f for f in listdir("../examples/") if isfile(join("../examples/", f))]

embeddings = np.zeros((29, 65536))
count = 0

pub = rospy.Publisher("object_detected", objMessage, queue_size=10)

def load_image_tensor(image_path, device):
    image_tensor = T.ToTensor()(IM.open(image_path))
    image_tensor = transform_resize(image_tensor)
    image_tensor = image_tensor.unsqueeze(0)
    input_images = image_tensor.to(device)
    return input_images

def convert_IM_to_tensor(im, device):
    image_tensor = T.ToTensor()(im)
    image_tensor = transform_resize(image_tensor)
    image_tensor = image_tensor.unsqueeze(0)
    input_images = image_tensor.to(device)
    return input_images


for f in onlyfiles:
    obj_tensor = load_image_tensor("../examples/"+f, device)
    with torch.no_grad():
        embedding = encoder(obj_tensor[:,:3,:,:]).cpu().detach()
    obj_flattened_embedding = embedding.reshape((embedding.shape[0], -1))
    embeddings[count] = obj_flattened_embedding
    count += 1


def callback(data):
    image = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    results = model(image)
    df = results.pandas().xyxy[0]
    query = df.loc[df.confidence >= 0.3]

    for i in range(len(query)):
        try:
            image = IM.fromarray(image.astype('uint8'))
            im = image.crop((query.iloc[i]['xmin'],query.iloc[i]['ymin'],query.iloc[i]['xmax'],query.iloc[i]['ymax']))

            hd, dd = {}, {}
            hd['x1'], hd['x2'], hd['y1'], hd['y2'] = query.iloc[i]['xmin'], query.iloc[i]['xmax'], query.iloc[i]['ymin'], query.iloc[i]['ymax']
            dd['x1'], dd['x2'], dd['y1'], dd['y2'] = 760, 1160, 100, 820
            score = get_iou(hd, dd)
            image_tensor = convert_IM_to_tensor(im, device)
            with torch.no_grad():
                image_embedding = encoder(image_tensor[:,:3,:,:]).cpu().detach()
            flattened_embedding = image_embedding.reshape((image_embedding.shape[0], -1))

            knn = NearestNeighbors(n_neighbors=10, metric="cosine")
            knn.fit(embeddings)

            _, indices = knn.kneighbors(flattened_embedding)
            msg = objMessage()
            msg.obj = onlyfiles[indices[0][0]][:-5]
            msg.score = score
            pub.publish(msg)
        except:
            pass
    return

def listener():
    rospy.init_node("listener")
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()