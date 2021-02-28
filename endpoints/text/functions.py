# from flask import jsonify
from transformers import pipeline
import hashlib
md5 = hashlib.md5()

def summarize(text, aim, deviation, num_summaries, response_type):
    summarizer = pipeline(
                    "summarization",
                    model="t5-small",
                    tokenizer="t5-small",
                    framework="tf"
                )

    md5.update(text.encode("utf-8"))
    chunk_id = md5.hexdigest()
    text_length = len(list(text.split()))

    def define_min_max(aim, deviation):
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
        aim = aim + deviation * i
        (min_length, max_length) = define_min_max(aim, deviation)

        summary = str(summarizer(text, min_length, max_length))
        compression = round(len(list(summary.split())) / text_length, 2)
        deviation = round(abs(compression - aim),2)

        md5.update(summary.encode("utf-8"))
        summary_id = md5.hexdigest()

        response["summary"].append({
            "text": summary,
            "summary_id": summary_id,
            "compression": compression,
            "aim": aim,
            "deviation": deviation
        })

    if response_type == "text/plain":
        return str(response["summary"][0])
    elif response_type == "application/json":
        return response
