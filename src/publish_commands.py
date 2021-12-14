import numpy as np
import rospy
from geometry_msgs.msg import Twist
from detection_msg.msg import objMessage
import tf
from nltk.parse import ShiftReduceParser
from nltk import CFG
import fasttext.util
import spacy

nlp = spacy.load("en_core_web_sm")
ft = fasttext.load_model('cc.en.300.bin')
couch_em = ft.get_word_vector('couch')
plant_em = ft.get_word_vector('plant')
chair_em = ft.get_word_vector('chair')
bookshelf_em = ft.get_word_vector('bookshelf')
desk_em = ft.get_word_vector('desk')
trashcan_em = ft.get_word_vector('trashcan')
items = ["couch", "plant", "chair", "bookshelf", "desk", "trashcan"]
em = np.vstack((couch_em, plant_em, chair_em, bookshelf_em, desk_em, trashcan_em))

sentence = 'move to the sofa then turn right and move to the table'
# sentence = 'move to the couch and turn left then move to the chair and then move to the plant'
# sentence = 'move to the couch'
# sentence = "turn left"
doc = nlp(sentence)
count = 0
sentence = sentence.split()
for token in doc:
    if token.pos_ == "NOUN":
        c_em = ft.get_word_vector(sentence[count])
        similarity_scores = em.dot(c_em)/ (np.linalg.norm(em, axis=1) * np.linalg.norm(c_em))
        sentence[count] = items[np.argmax(similarity_scores)]
    count += 1

grammar = CFG.fromstring("""
do_sequentially -> CMD CONJ CMD | do_sequentially CONJ CMD
CMD -> V DIR | V PP
PP -> P TARGET | P POS TARGET
TARGET -> 'the' N | N
CONJ -> CONJ CONJ
POS -> 'the' DIR PREP

N -> 'couch' | 'plant' | 'chair' | 'bookshelf' | 'desk' | 'trashcan' | 'window' | 'wall' | 'door' | 'table'
P -> 'to' | 'towards' 
V -> 'go' |'move' | 'turn' | 'drive'
DIR -> 'left' | 'right' | 'around' | 'front'
CONJ -> 'and' | 'then'
PREP -> 'of'
""")
rd = ShiftReduceParser(grammar)
print(sentence)
for t in rd.parse(sentence):
    lines = str(t).split('\n')
    print(t)

cmds = []
for c in lines:
    if "CONJ" not in c:
        if " (P to) " in c:
            c = c.replace(" (P to)", "")
        if "PP " in c:
            c = c.replace("PP ", "")

        if "the (N " in c:
            c = c.replace("the (N ", "")
        c = c.replace("(", "")
        c = c.replace(")", "")
        cmds.append(c)

machine_cmd = []
for s in cmds:
    if "TARGET" in s:
        machine_cmd.append(s.split(" TARGET ")[-1])
    if "turn" in s:
        machine_cmd.append(s.split("turn DIR ")[-1])

print(machine_cmd)

obj_loc = {
    "couch": np.array([-3.5458, 0.3452]),
    "plant": np.array([-3.844, -4.318]),
    "chair": np.array([2.11, -2.91]),
    "table": np.array([0.9028, 0.4533]),
    "bookshelf": np.array([4.226, 4.715]),
    "trashcan": np.array([-3.926, 4.748]),
    "door": np.array([0.71, 4.82])
}

class commander:
    def __init__(self):
        self.sub = rospy.Subscriber("/object_detected", objMessage, self.callback)
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        self.goal = ""
        self.score = 0
        self.found = False
        self.tf_listener = tf.TransformListener()
        self.done = False
        self.left = True

    def callback(self, msg):
        self.obj = msg.obj
        self.score = msg.score
        if self.obj == self.goal and self.score >= 0.08 and self.found == False:
            print(self.obj)
            self.stop()
            rospy.sleep(0.1)
            self.found == True
            self.move_to_target()
        elif self.found == False:   
            print(self.goal) 
            if self.left:
                self.turn_left()
            else:
                self.turn_right()
        else:
            pass
        # self.stop()
    
    def move_to_target(self):
        while True:
            (trans,rot) = self.tf_listener.lookupTransform('/odom', '/base_footprint', rospy.Time(0))
            dist = np.sqrt((np.array(trans)[0] - obj_loc[self.goal][0])**2 + (np.array(trans)[1] - obj_loc[self.goal][1]))**2
            self.move_forward()
            if dist <= 2.5:
                self.stop()
                self.done = True
                rospy.sleep(2)
                return

    def observer(self):
        return

    def move_forward(self):
        cmd = Twist()
        cmd.linear.x = 0.6
        self.pub.publish(cmd)

    def stop(self):
        cmd = Twist()
        cmd.linear.x = 0
        cmd.angular.z = 0
        self.pub.publish(cmd)

    def turn_left(self):
        cmd = Twist()
        cmd.angular.z = 0.4
        self.pub.publish(cmd)

    def turn_right(self):
        cmd = Twist()
        cmd.angular.z = -0.4
        self.pub.publish(cmd)

    def set_goal(self, goal):
        self.found = False
        if "left" in goal:
            # current_time = rospy.get_time()
            # while rospy.get_time - current_time() <= 2:
            #     self.turn_left()
            # self.stop()
            self.left = True
        elif "right" in goal:
            # current_time = rospy.get_time()
            # while rospy.get_time - current_time() <= 2:
            #     self.turn_right()
            # self.stop()
            self.left = False
        else:
            self.goal = goal



if __name__ == '__main__':
    rospy.init_node("commander")
    rospy.sleep(0.1)
    com = commander()
    for c in machine_cmd:
        com.set_goal(c)
        while not com.done:
            pass
        com.done = False
    rospy.spin()


