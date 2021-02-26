from flask import jsonify
import json
from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")

def summary(text_input, aim=50, deviation_input=10, num_summaries=1, chunk_number=1):

    if num_summaries > 1:
        min_length_rel = [0] * num_summaries
        max_length_rel = [0] * num_summaries
        min_length_words = [0] * num_summaries
        max_length_words = [0] * num_summaries
        text = [""] * num_summaries
        aim_rel = [0] * num_summaries
        compression = [0] * num_summaries
        deviation_output = [0] * num_summaries
        text_input_length = len(list(text_input.split()))

        for i in range(num_summaries):
            min_length_rel[i] = (aim + i*deviation_input)/100
            max_length_rel[i] = (aim + (i+1)*deviation_input)/100
            min_length_words[i] = round(text_input_length * (aim + i*deviation_input)/100)
            max_length_words[i] = round(text_input_length * (aim + (i+1)*deviation_input)/100)
            aim_rel[i] = min_length_rel[i] + (deviation_input/2)/100

            summary_output = summarizer(
                text_input, 
                min_length=min_length_words[i], 
                max_length=max_length_words[i]
            )
            text[i] = str(summary_output)
            text_length = len(list(text[i].split()))
            compression[i] = round(text_length / text_input_length,3)
            deviation_output[i] = round(abs(compression[i] - aim_rel[i]),3)

    if num_summaries == 1:
        aim_rel = aim/100
        text_input_length = len(list(text_input.split()))

        min_length_rel = aim - deviation_input
        max_length_rel = aim + deviation_input

        min_length_abs = round(text_input_length * (min_length_rel/100))
        max_length_abs = round(text_input_length * (max_length_rel/100))
        
        summary_output = summarizer(
            text_input, 
            min_length=min_length_abs, 
            max_length=max_length_abs
        )
        text = str(summary_output)
        text_length = len(list(text.split()))
        compression = round(text_length / text_input_length, 2)
        deviation_output = round(abs(compression - aim_rel),2)

    return  text, compression, aim_rel, deviation_output