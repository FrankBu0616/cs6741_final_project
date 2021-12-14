import re
import spacy
nlp = spacy.load("en_core_web_sm")

command = "move to the couch and turn left, then move to the front of the lamp"
x = re.split(",| and | then", command)

for d in x:
    if len(d) == 0:
        continue
    doc = nlp(d)
    print(d)
    for chunk in doc.noun_chunks:
        print("--", chunk.text)
    print("")
