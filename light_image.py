import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from clover import long_callback

rospy.init_node('cv')
bridge = CvBridge()

@long_callback
def image_callback(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')
    light_img = img.copy()
    ksize = (4, 4)
    crop_image = img[20:200, 20:300]
    img_blur = cv2.blur(src = crop_image, ksize = ksize)
    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
    hsv[:,:,2] = 255
    light_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    image_pub.publish(bridge.cv2_to_imgmsg(light_img, 'bgr8'))

image_pub = rospy.Publisher('~debug', Image)
image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)
rospy.spin()