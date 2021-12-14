import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("move to the couch and turn left, then move to the front of the lamp")
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)