# NLP Functions
from transformers import pipeline
import spacy
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

from py2neo import Graph
graph = Graph(
    "bolt://ecchr.metasphere.xyz:7687/",
    auth=('neo4j', 'burr-query-duel-cherry')
)

# load nlp modules
nlp = spacy.load("en_core_web_sm")
ner_huggingface_pipeline = pipeline("ner")
# model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")


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

#%% Text Similarity
def similarity_tf(similarity_text, similarities):
    query = '''
        MATCH (c:Chunk)
        RETURN c.chunk_id, c.text 
    '''
    result = graph.run(query).data()

    documents = []
    chunk_list = []

    for chunks in result:
        documents.append(chunks['c.text'])
        chunk_list.append(chunks['c.chunk_id'])

    
    # documents = [
    #     "I am Malte Schneider",
    #     "I am Malte. I also have dog named Pluto",
    #     "I am living in Dortmund and looking forward to become a doctor",
    #     "I am Julian and I enjoy cruising with my boat. I'm loving dogs.",
    #     "Pluto is a dog"
    # ]

    base_embeddings = model([similarity_text])
    embeddings = model(documents)

    scores = cosine_similarity(base_embeddings, embeddings).flatten()

    sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
    print(sorted_scores_indexes)

    response_similarity = {
        "collection_id": "md5",
        "chunk_id": "md5",
        "text": similarity_text,
        "similarity": [

        ]
    }

    for i in range(similarities):
        index = sorted_scores_indexes[i][1]
        chunk_id = chunk_list[index]
        chunk_text = documents[index]
        score = int(round(sorted_scores_indexes[i][0],2)*100)
        response_similarity['similarity'].append(
            {
                "chunk_id": chunk_id,
                "score": score,
                "text": chunk_text
            }
        )
    return response_similarity
# %%
