# NLP Functions
from transformers import pipeline
import spacy

# load nlp modules
nlp = spacy.load("en_core_web_sm")
ner_huggingface_pipeline = pipeline("ner")

# %% NER SpaCy
def ner(text):
    doc = nlp(text)
    ner_proccessed = {
        "chunk_id": "md5",
        "entities": {

        }
    }
    for ent in doc.ents:
        ner_proccessed['entities'][ent.text]=ent.label_

    return ner_proccessed

# %% NER Huggingface
def ner_huggingface(text):
    ner_huggingface_processed = ner_huggingface_pipeline(text)
    return ner_huggingface_processed