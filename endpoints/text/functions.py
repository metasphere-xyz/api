# from flask import jsonify
from transformers import pipeline

def summarize(text, aim, compression, num_summaries, response_type):
    summarizer = pipeline(
                    "summarization",
                    model="t5-small",
                    tokenizer="t5-small",
                    framework="tf"
                )

    hash.update(text)
    chunk_id = hash.hexdigest()
    text_length = len(list(text.split()))

    def define_min_max(aim, deviation):
        aim_rel = aim/100
        min_length_rel = aim - deviation_input
        max_length_rel = aim + deviation_input
        min_length_abs = round(text_length * (min_length_rel/100))
        max_length_abs = round(text_length * (max_length_rel/100))
        return (min_length, max_length)

    response = {
        "chunk_id": chunk_id,
        "summary": [
        ]
    }

    for i in range(num_summaries):
        aim = aim + deviation * i
        (min_length, max_length) = define_min_max(aim, deviation)

        summary = str(summarizer(text, min_length, max_length))
        compression = round(summary / text_length, 2)
        deviation = round(abs(compression - aim),2)

        hash.update(summary)
        summary_id = hash.hexdigest()

        response["summary"][i] = {
            "text": summary,
            "summary_id": summary_id
            "compression": compression,
            "aim": aim,
            "deviation": deviation
        }

    if response_type == "text/plain":
        return str(response["summary"][0])
    elif response_type == "application/json":
        return response
