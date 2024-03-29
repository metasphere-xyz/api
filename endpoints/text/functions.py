from config import *

def preprocess(text):
    text_clean = text.replace("\r", "\n ")\
        .replace("\n", " ") \
        .replace("\s\s+", " ") \
        .replace('"', '') \
        .replace("’s", "") \
        .replace("...", "") \
        .replace('" ', "") \
        .replace('"', "") \
        .replace(" - ", "-") \
        .strip()
    return text_clean

def remove_stopwords_from_string(text):
    text_clean = ''
    for word in text.lower().split():
        if word not in stopwords:
            text_clean += word + " "
    return text_clean

def url_preview(url):
    preview = link_preview(url)

    response_urlpreview = {
        "url": url,
        "title": preview.title,
        "description": preview.description,
        "image": preview.image,
    }
    return response_urlpreview

def compute_base_embeddings():
    print(f"[bold]Loading corpus embeddings.[/bold]")
    query = '''
        MATCH (c:Chunk)
        RETURN c.chunk_id, c.text
    '''
    print(eye, f"Retrieving all chunks...")
    result = graph.run(query).data()

    documents = []
    documents_clean = []
    chunk_list = []
    length_corpus = 0
    num_chunks = len(result)
    print(checkmark, f"Successfully loaded {num_chunks} chunks.")

    if len(result) > 1:
        for chunk in result:
            chunk_text = preprocess(chunk['c.text'])
            chunk_text_clean = remove_stopwords_from_string(chunk_text)
            length_corpus += 1
            documents.append(chunk_text)
            documents_clean.append(chunk_text_clean)
            chunk_list.append(chunk['c.chunk_id'])

    print(checkmark, f"Successfully processed {length_corpus}/{num_chunks} chunks.")
    #Load AutoModel from huggingface model repository
    print(eye, f"Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/bert-base-nli-cls-token")
    print(checkmark, f"Successfully loaded tokenizer.")
    print(eye, f"Loading model...")
    model = AutoModel.from_pretrained("sentence-transformers/bert-base-nli-cls-token")
    print(checkmark, f"Successfully loaded model.")

    #Tokenize sentences
    print(eye, f"Tokenizing corpus...")
    if length_corpus > 1:
        encoded_input = tokenizer(documents_clean, padding=True, truncation=True, max_length=128, return_tensors='pt')
    else:
        encoded_input = tokenizer([""], padding=True, truncation=True, max_length=128, return_tensors='pt')

    # encoded_input_sentence = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors='pt')
    print(checkmark, f"Successfully tokenized.")

    #Compute token embeddings
    print(eye, f"Computing base embeddings...")
    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embeddings = model_output[0][:,0]

    print(checkmark, f"Successfully computed {len(sentence_embeddings)} embeddings")
    return documents, tokenizer, model, sentence_embeddings

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
# TODO:
# Update pipeline:
# 1. use bert extractive summarizer to filter out most important sentence in chunk
# 2. pass sentence into summarizer

def summarize(text, aim, deviation, num_summaries, response_type):


    # md5.update(text.encode("utf-8"))
    # TODO: add sentence segmentation and only return full sentences:
    # https://spacy.io/usage/linguistic-features#sbd
    # Alternatively: pass through bert extractive summarizer before processing to filter out most valuable sentence before processing
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
        "summaries": [
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

        response["summaries"].append({
            "text": summary,
            "summary_id": summary_id,
            "compression": compression,
            "aim": final_aim,
            "deviation": final_deviation
        })

    return response


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
    # TODO: port coreference resolution from media/processors/pushCollection.py
    doc = nlp(preprocess(text))
    hash = hashlib.md5(text.encode("utf-8"))
    chunk_id = hash.hexdigest()

    response = {
        "chunk_id": chunk_id,
        "text": text,
        "entities": []
    }

    entities = {}
    entity_names = ''
    nouns = []

    def clean_up(entity_name):
        cleaned_entity = entity_name \
            .replace("the ", "") \
            .replace("The ", "") \
            .replace("this ", "") \
            .replace("’s", "") \
            .replace("...", "") \
            .replace('" ', "") \
            .replace('"', "") \
            .replace(" - ", "-") \
            .strip()
        return cleaned_entity

    # find hardcoded entities
    hardcoded_entities = re.findall('\"((\w+\W)*\w+)', text)
    for entity in hardcoded_entities:
        found_entity = entity[0].replace('\\', '')
        entities.update({clean_up(found_entity): 'HARDCODED'})
        entity_names += clean_up(found_entity)

    for entity in doc.ents:
        if entity.label_ in accepted_entity_labels:
            entities.update({clean_up(entity.lemma_): entity.label_})
            entity_names += clean_up(entity.lemma_)

    # for noun in doc.noun_chunks:
    #     if noun.root.lemma_.lower() not in stopwords and not noun.root.lemma_.isnumeric():
    #         if noun.root.lemma_ not in entity_names:
    #             entities.update({clean_up(noun.root.lemma_): 'NOUN'})
    #             entity_names += clean_up(noun.root.lemma_)

    for (entity_name, entity_label) in entities.items():
        if entity_name != '':
            response["entities"].append({
                "entity_name": entity_name,
                "entity_label": entity_label
            })

    print(response)
    return response

# %% NER Huggingface
def ner_huggingface(text):
    ner_huggingface_processed = ner_huggingface_pipeline(text)
    return ner_huggingface_processed

#%% Text Similarity
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

    print(f"[bold]Finding similar chunks.[/bold]")
    print(f"{text}")

    print(eye, f"Tokenizing...")
    text_without_stopwords = remove_stopwords_from_string(text)
    print(text_without_stopwords)
    encoded_input_sentence = tokenizer(text_without_stopwords, padding=True, truncation=True, max_length=128, return_tensors='pt')
    print(checkmark, f"Successfully tokenized.")

    print(eye, f"Computing embeddings...")
    with torch.no_grad():
        sentence_output = model(**encoded_input_sentence)
        base_embeddings = sentence_output[0][:,0]
    print(checkmark, f"Successfully computed embeddings.")

    print(eye, f"Computing similarity...")
    scores = cosine_similarity(base_embeddings, sentence_embeddings).flatten()
    print(checkmark, f"Successfully computed similarity.")

    sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
    print(sorted_scores_indexes)

    hash = hashlib.md5(text.encode("utf-8"))
    chunk_id = hash.hexdigest()

    response_similarity = {
        "chunk_id": chunk_id,
        "text": text,
        "similar_chunks": [

        ]
    }

    for i in range(num_similar_chunks):
        index = sorted_scores_indexes[i][1]
        chunk_id = chunk_list[index]
        chunk_text = documents[index]
        score = int(round(sorted_scores_indexes[i][0],2)*100)
        if 98 > score >= int(similarity_score_treshold):
            response_similarity['similar_chunks'].append(
                {
                    "chunk_id": chunk_id,
                    "score": score,
                    "text": chunk_text
                }
            )
    print(response_similarity)
    return response_similarity
