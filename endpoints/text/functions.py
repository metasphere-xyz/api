from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")

def summary(text_input, aim=50, deviation_input=10, num_summaries=1):
    # text_input = "This is an input text for the summarizer"

    text_input_length = len(list(text_input.split()))
    aim_rel = aim/100

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
    compression = text_length / text_input_length
    deviation_output = abs(compression - aim_rel)
    print("compression:", compression)
    print("aim", aim_rel)
    print("deviation:", deviation_output)

    return  text