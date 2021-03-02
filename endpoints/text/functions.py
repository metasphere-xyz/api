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
                    framework="tf",
                    # input_ids[torch.LongTensor],
                    do_sample=False,
                    early_stopping=True,
                    num_beams=3,
                    temperature=1.0,
                    top_k=50,
                    top_p=1.0,
                    repetition_penalty=1.0,
                    # pad_token_id[int],
                    # bos_token_id[int],
                    # eos_token_id[int],
                    length_penalty=1.0,
                    no_repeat_ngram_size=0,
                    # bad_words_ids=List[List[int]],
                    num_return_sequences=1,
                    # attention_mask=(batch_size, sequence_length),
                    # decoder_start_token_id[int],
                    use_cache=True,
                    # prefix_allowed_tokens_fn(Callable[[int, torch.Tensor], List[int]]),
                    # model_kwargs
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

        summary = str(summarizer(
            text,
            max_length=max_length,
            min_length=min_length
        ))[19:-3]
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
