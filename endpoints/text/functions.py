# from flask import jsonify
import os
import math
import torch
from transformers import pipeline
# from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from transformers import AutoModel, AutoModelForSeq2SeqLM, AutoTokenizer
import hashlib
md5 = hashlib.md5()
from fuzzy_match import algorithims as algorithms
from summarizer import Summarizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}

# summarization_model = "facebook/bart-base"
# summarization_model = "facebook/bart-large-cnn"
summarization_model = "t5-small"
# summarization_model = "t5-base"
# summarization_model = "t5-large"
# summarization_model = "gpt2"
summarization_model_parameters = {
    # input_ids[torch.LongTensor],
    "do_sample": False,
    "early_stopping": True,
    # "early_stopping": False,
    "num_beams": 5,
    "temperature": 1.0,
    "top_k": 50,
    "top_p": 1.0,
    "repetition_penalty": 1.5,
    # pad_token_id[int],
    # bos_token_id[int],
    # eos_token_id[int],
    "length_penalty": 5.0,
    "no_repeat_ngram_size": 3,
    # bad_words_ids=List[List[int]],
    "num_return_sequences": 1,
    # attention_mask=(batch_size, sequence_length),
    # decoder_start_token_id[int],
    "use_cache": True,
    # prefix_allowed_tokens_fn(Callable[[int, torch.Tensor], List[int]]),
    # model_kwargs
}

def preprocess(text):
    return text.replace("\r", "\n ").replace("\n", " ").replace("\s\s+", " ").strip()

summarizer_bert = Summarizer()

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
        # summary = str(summarizer_torch(text, min_length, max_length))
        # summary = summarizer_bert(text, ratio=final_aim/100)
        # summary = summarizer_bert(text, min_length=min_length, max_length=max_length, num_sentences=1)
        summary = text
        print ("text: "+text)
        print("summary: "+summary)

        compression = math.floor(100/(1+round(algorithms.trigram(summary, text)*100,2)))
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
