# # NLP Functions
# from transformers import pipeline
# import spacy
# import tensorflow_hub as hub
# from sklearn.metrics.pairwise import cosine_similarity
#
# from py2neo import Graph
# graph = Graph(
#     "bolt://ecchr.metasphere.xyz:7687/",
#     auth=('neo4j', 'burr-query-duel-cherry')
# )
#
# # load nlp modules
# nlp = spacy.load("en_core_web_sm")
# ner_huggingface_pipeline = pipeline("ner")
# model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
# # model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")
# # model = hub.load("models/universal-sentence-encoder_4")
#
#
# # %% NER SpaCy
# def ner(text):
#     doc = nlp(text)
#     ner_proccessed = {
#         "chunk_id": "md5",
#         "entities": {
#
#         }
#     }
#     for ent in doc.ents:
#         ner_proccessed['entities'][ent.text]=ent.label_
#
#     return ner_proccessed
#
# # %% NER Huggingface
# def ner_huggingface(text):
#     ner_huggingface_processed = ner_huggingface_pipeline(text)
#     return ner_huggingface_processed
#
# #%% Text Similarity
# def similarity_tf(similarity_text, num_similar_chunks):
#     # TODO: add filter for type (chunk, summary, entity)
#     query = '''
#         MATCH (c:Chunk)
#         RETURN c.chunk_id, c.text
#     '''
#     result = graph.run(query).data()
#
#     documents = []
#     chunk_list = []
#
#     for chunks in result:
#         documents.append(chunks['c.text'])
#         chunk_list.append(chunks['c.chunk_id'])
#
#
#     base_embeddings = model([similarity_text])
#     embeddings = model(documents)
#
#     scores = cosine_similarity(base_embeddings, embeddings).flatten()
#
#     sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
#     print(sorted_scores_indexes)
#
#     response_similarity = {
#         "chunk_id": "md5",
#         "text": similarity_text,
#         "similarity": [
# 
#         ]
#     }
#
#     for i in range(num_similar_chunks):
#         index = sorted_scores_indexes[i][1]
#         chunk_id = chunk_list[index]
#         chunk_text = documents[index]
#         score = int(round(sorted_scores_indexes[i][0],2)*100)
#         response_similarity['similarity'].append(
#             {
#                 "chunk_id": chunk_id,
#                 "score": score,
#                 "text": chunk_text
#             }
#         )
#     return response_similarity
# # %%
