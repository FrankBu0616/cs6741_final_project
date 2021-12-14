import torch
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
bridge = CvBridge()

def listener():
    rospy.init_node("listener", anonymous='True')
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback)

def callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    results = model(cv_image)
    results.print()
    print(results.pandas().xyxy[0])

if __name__ == '__main__':
    listener()
    rospy.spin()