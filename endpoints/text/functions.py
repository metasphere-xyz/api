# from flask import jsonify
from transformers import pipeline
import hashlib
md5 = hashlib.md5()
from fuzzy_match import algorithims as algorithms

def summarize(text, aim, deviation, num_summaries, response_type):
    # TODO: make shell output less verbose/fix libcudart error
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
        # TODO: adjust calculations
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
        (min_length, max_length) = define_min_max(final_aim, deviation)

        summary = str(summarizer(text, max_length=max_length, min_length=min_length))[19:-3]
        # compression = round((len(list(summary.split())) / text_length)*100, 2)
        compression = round(algorithms.trigram(summary, text)*100,2)
        final_deviation = round(abs(compression - final_aim), 2)

        md5.update(summary.encode("utf-8"))
        summary_id = md5.hexdigest()

        response["summary"].append({
            "text": summary,

            "summary_id": summary_id,
            "compression": compression,
            "aim": final_aim,
            "deviation": final_deviation
        })

    return response
