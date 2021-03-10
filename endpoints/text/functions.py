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
def summarize(text, aim, deviation, num_summaries, response_type):
    # md5.update(text.encode("utf-8"))
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
        "summary": [
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

        response["summary"].append({
            "text": summary,
            "summary_id": summary_id,
            "compression": compression,
            "aim": final_aim,
            "deviation": final_deviation
        })

    return response


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
def similarity_tf(similarity_text, num_similar_chunks, similarity_score_treshold):
    # model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    # model = hub.load("/Users/malte/Desktop/universal-sentence-encoder_4")
    model = hub.load("models/universal-sentence-encoder_4")

    # TODO: add filter for type (chunk, summary, entity)
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

    base_embeddings = model([similarity_text])
    embeddings = model(documents)

    scores = cosine_similarity(base_embeddings, embeddings).flatten()

    sorted_scores_indexes = sorted(((value, index) for index, value in enumerate(scores)), reverse=True)
    print(sorted_scores_indexes)

    response_similarity = {
        "chunk_id": "md5",
        "text": similarity_text,
        "similarity": [

        ]
    }

    for i in range(num_similar_chunks):
        index = sorted_scores_indexes[i][1]
        chunk_id = chunk_list[index]
        chunk_text = documents[index]
        score = int(round(sorted_scores_indexes[i][0],2)*100)
        if 100 > score >= int(similarity_score_treshold):
            response_similarity['similarity'].append(
                {
                    "chunk_id": chunk_id,
                    "score": score,
                    "text": chunk_text
                }
            )
    return response_similarity
# %%
