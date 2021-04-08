from config import *

def preprocess(text):
    return text.replace("\r", "\n ").replace("\n", " ").replace("\s\s+", " ").strip()

def summarizer_pipeline(text, min_length, max_length):
    summarizer = pipeline(
        "summarization",
        model=summarization_model,
        tokenizer=summarization_model,
        framework="tf"
    )
    summary = str(summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        **summarization_model_parameters
        )[0]["summary_text"])
    return summary

def summarizer_torch(text, min_length, max_length):
    # model = AutoModelForSeq2SeqLM.from_pretrained(summarization_model)
    # tokenizer = AutoTokenizer.from_pretrained(summarization_model)
    # model = T5ForConditionalGeneration.from_pretrained('t5-base')
    # model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    # tokenizer = T5Tokenizer.from_pretrained('t5-base')

    model = AutoModelForSeq2SeqLM.from_pretrained(summarization_model)
    # model = AutoModel.from_pretrained(summarization_model)
    tokenizer = AutoTokenizer.from_pretrained(summarization_model)

    device = torch.device('cpu')

    preprocessed_text = preprocess(text)
    # preprocessed_text = text
    if summarization_model.startswith("t5"):
        preprocessed_text = "summarize: " + preprocessed_text

    tokenized_text = tokenizer.encode(preprocessed_text, truncation=True, return_tensors="pt").to(device)

    summaries = model.generate(
        tokenized_text,
        max_length=max_length,
        min_length=min_length,
        **summarization_model_parameters
    )

    summary = tokenizer.decode(summaries[0], clean_up_tokenization_spaces=True, skip_special_tokens=True)
    return summary

# %% Summarization
<<<<<<< HEAD
def summarize(text, aim, deviation, num_summaries, response_type):
    # TODO: add sentence segmentation and only return full sentences:
    # https://spacy.io/usage/linguistic-features#sbd
    # Alternatively: pass through bert extractive summarizer before processing to filter out most valuable sentence before processing
=======
# TODO:
# Update pipeline:
# 1. use bert extractive summarizer to filter out most important sentence in chunk
# 2. pass sentence into summarizer

def summarize(text, aim, deviation, num_summaries, response_type):


    # md5.update(text.encode("utf-8"))
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
    hash = hashlib.md5(text.encode("utf-8"))
    chunk_id = hash.hexdigest()
    text_length = len(list(text.split()))

    def define_min_max(text_length, aim, deviation):
        # TODO: bei zu kleinem aim kommen negative Zahlen raus
        aim_rel = aim/100
        min_length_rel = aim - deviation
        max_length_rel = aim + deviation
        min_length = round(text_length * (min_length_rel/100))
        max_length = round(text_length * (max_length_rel/100))
        return (min_length, max_length)

    response = {
        "chunk_id": chunk_id,
<<<<<<< HEAD
        "summaries": [
=======
        "summary": [
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
        ]
    }

    for i in range(num_summaries):
        final_aim = aim + deviation * i
        (min_length, max_length) = define_min_max(text_length, final_aim, deviation)

        # summary = str(summarizer_pipeline(text, min_length, max_length))
        summary = str(summarizer_torch(text, min_length, max_length))
        # summary = summarizer_bert(text, num_sentences=0) // returns 1 sentence
        # summary = summarizer_bert(text, min_length=5, max_length=15, num_sentences=0)
        # summary = summarizer_bert(text, min_length=min_length, max_length=max_length, num_sentences=0)
        # summary = text
        print ("text: "+text)
        print("summary: "+summary)

        compression = 100 - round(algorithms.trigram(summary, text)*100,2)
        final_deviation = round(abs(compression - final_aim), 2)

        hash = hashlib.md5(summary.encode("utf-8"))
        summary_id = hash.hexdigest()

<<<<<<< HEAD
        response["summaries"].append({
=======
        response["summary"].append({
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
            "text": summary,
            "summary_id": summary_id,
            "compression": compression,
            "aim": final_aim,
            "deviation": final_deviation
        })

    return response


<<<<<<< HEAD
def sequence_by_speaker(chunk_sequence):
    try:
        json_loads(chunk_sequence)
    except:
        print ("error")

    if len(chunk_sequence) > 1:
        chunks_by_speaker = []

        sequence = 0
        speaker = ""

        for chunk in chunk_sequence:
            if speaker != chunk["speaker"]:
                speaker = chunk["speaker"]
                sequence = len(chunks_by_speaker)
                chunks_by_speaker.append([{}])
                chunks_by_speaker[sequence] = []
            chunks_by_speaker[sequence].append(dict(chunk))

        return json.dumps(chunks_by_speaker)

# %% summarize chunk sequence
# Takes a chunk sequence as argument, joins contributions per speaker, summarizes chunk sequence per speaker


def summarize_chunk_sequence(chunk_sequence):
    response = {
        "chunk_sequence": []
    }

    chunks_by_speaker = json.loads(sequence_by_speaker(chunk_sequence))

    for sequence in chunks_by_speaker:
        speaker = sequence[0]["speaker"]
        contribution = ""
        print(speaker)

        for chunk in sequence:
            contribution += chunk["text"] + " "

        num_chunks = len(sequence)
        print ("num_chunks: " + str(num_chunks))
        ratio = int(num_chunks)/int(summary_percentage_document)
        print ("ratio: " + str(ratio))
        print (preprocess(contribution))

        # summaries = sentence_summarizer(preprocess(contribution), ratio=ratio)
        summaries = nlp(sentence_summarizer(preprocess(contribution), num_sentences=0, min_length=2))

        for sentence in summaries.sents:
            for chunk in sequence:
                if sentence.text in chunk["text"]:
                    response["chunk_sequence"].append(chunk)

    return response

# %% NER SpaCy
def ner(text):
    # TODO: add coreference resolution before extracting entities:
    # 1. look up chunk in database
    # 2. if chunk is found, look up previous chunk in chain
    # 3. run coreference resolution on previous chunk and current chunk
    # Example:
    # Chunk 1: Mark Sealy, Director of the Autograph Gallery and the Association of Black Photographers in London, was my guest today in our podcast series.
    # Chunk 2: Everybody who liked this, or at least parts of this talk, is invited to look at our website and follow us on social media and also have Mark, it was a pleasure to talk to you.
    # Correct entity: 'Mark Sealy': 'PERSON'
    # Incorrect entity: 'Mark': 'PERSON'
    # References:
    # https://spacy.io/universe/project/neuralcoref
    # https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e
=======
# %% NER SpaCy
def ner(text):
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
    doc = nlp(text)
    hash = hashlib.md5(text.encode("utf-8"))
    chunk_id = hash.hexdigest()

    ner_proccessed = {
        "chunk_id": chunk_id,
        "text": text,
        "entities": {

        }
    }
    for ent in doc.ents:
<<<<<<< HEAD
        entity_name = ent.text
        entity_label = ent.label_
        entity_name = entity_name.replace("the ", "")

        if entity_label in accepted_entity_labels:
            ner_proccessed['entities'][entity_name]=entity_label
=======
        ner_proccessed['entities'][ent.text]=ent.label_
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403

    return ner_proccessed

# %% NER Huggingface
def ner_huggingface(text):
    ner_huggingface_processed = ner_huggingface_pipeline(text)
    return ner_huggingface_processed

#%% Text Similarity
<<<<<<< HEAD
# def similarity_tf(text, num_similar_chunks, similarity_score_treshold):
#     # model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
#     # model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")
#     model = hub.load("models/universal-sentence-encoder_4")
#
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
#     base_embeddings = model([text])
#     embeddings = model(documents)
#
#     scores = cosine_similarity(base_embeddings, embeddings).flatten()
#
#     sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
#     print(sorted_scores_indexes)
#
#     hash = hashlib.md5(text.encode("utf-8"))
#     chunk_id = hash.hexdigest()
#
#     response_similarity = {
#         "chunk_id": chunk_id,
#         "text": text,
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
#         if 100 > score >= int(similarity_score_treshold):
#             response_similarity['similarity'].append(
#                 {
#                     "chunk_id": chunk_id,
#                     "score": score,
#                     "text": chunk_text
#                 }
#             )
#     return response_similarity

# %% Text Similarity with HUGGINGFACE
def similarity_huggingface(text, num_similar_chunks, similarity_score_treshold):
=======
def similarity_tf(text, num_similar_chunks, similarity_score_treshold):
    # TODO: port to huggingface:
    # https://huggingface.co/sentence-transformers/bert-base-nli-cls-token
    #
    # model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    # model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")
    model = hub.load("models/universal-sentence-encoder_4")

    # TODO: add filter for type (chunk, summary, entity)
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
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

<<<<<<< HEAD
    #Load AutoModel from huggingface model repository
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/bert-base-nli-cls-token")
    model = AutoModel.from_pretrained("sentence-transformers/bert-base-nli-cls-token")

    #Tokenize sentences
    encoded_input = tokenizer(documents, padding=True, truncation=True, max_length=128, return_tensors='pt')
    encoded_input_sentence = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')

    #Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_output = model(**encoded_input_sentence)
        sentence_embeddings = model_output[0][:,0]
        base_embeddings = sentence_output[0][:,0]

    scores = cosine_similarity(base_embeddings, sentence_embeddings).flatten()
=======
    base_embeddings = model([text])
    embeddings = model(documents)

    scores = cosine_similarity(base_embeddings, embeddings).flatten()
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403

    sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
    print(sorted_scores_indexes)

    hash = hashlib.md5(text.encode("utf-8"))
    chunk_id = hash.hexdigest()

    response_similarity = {
        "chunk_id": chunk_id,
        "text": text,
<<<<<<< HEAD
        "similar_chunks": [
=======
        "similarity": [
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403

        ]
    }

    for i in range(num_similar_chunks):
        index = sorted_scores_indexes[i][1]
        chunk_id = chunk_list[index]
        chunk_text = documents[index]
        score = int(round(sorted_scores_indexes[i][0],2)*100)
        if 100 > score >= int(similarity_score_treshold):
<<<<<<< HEAD
            response_similarity['similar_chunks'].append(
=======
            response_similarity['similarity'].append(
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
                {
                    "chunk_id": chunk_id,
                    "score": score,
                    "text": chunk_text
                }
            )
    return response_similarity
<<<<<<< HEAD
=======
# %%
>>>>>>> 135d02a0982f27b8e4e0337b123d031d3fc39403
