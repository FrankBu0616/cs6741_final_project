import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import rospy
from geometry_msgs.msg import Twist
from detection_msg.msg import objMessage
import tf
from nltk.parse import ShiftReduceParser
from nltk import CFG
import fasttext.util
import spacy
with open('all.txt') as f:
    lines = f.readlines()
nlp = spacy.load("en_core_web_sm")
ft = fasttext.load_model('../src/cc.en.300.bin')
# count = 0
# num = []
# for line in lines:
#     count += len(line.split())
#     num.append(len(line.split()))
# print(count/60.)

# import seaborn as sns
# sns.set_theme(); 
# ax = sns.displot(data=np.array(num), kde=True)
# ax.set(xlabel='sentence length')

# plt.show()


couch_em = ft.get_word_vector('couch')
plant_em = ft.get_word_vector('plant')
chair_em = ft.get_word_vector('chair')
bookshelf_em = ft.get_word_vector('bookshelf')
desk_em = ft.get_word_vector('desk')
trashcan_em = ft.get_word_vector('trashcan')
items = ["couch", "plant", "chair", "bookshelf", "desk", "trashcan"]
em = np.vstack((couch_em, plant_em, chair_em, bookshelf_em, desk_em, trashcan_em))
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
c = 0
for sentence in lines:
    sentence = sentence.replace(",", "")
    sentence = sentence.replace(".", "")
    doc = nlp(sentence)
    count = 0
    sentence = sentence.split()
    for token in doc:
        if token.pos_ == "NOUN":
            c_em = ft.get_word_vector(sentence[count])
            similarity_scores = em.dot(c_em)/ (np.linalg.norm(em, axis=1) * np.linalg.norm(c_em))
            if sentence[count] == "front" or sentence[count] == "the" or sentence[count] == "turn" or sentence[count] == "back":
                continue
            sentence[count] = items[np.argmax(similarity_scores)]
        count += 1

    try:
        for t in rd.parse(sentence):
            lines = str(t).split('\n')
            # print(t)
        c += 1
    except:
        print(sentence)
        pass
print("good ", c)