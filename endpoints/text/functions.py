from transformers import pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", framework="tf")

def summary(text_input, aim=50, deviation_input=10, num_summaries=1):
    # text_input = "This is an input text for the summarizer"

    aim_rel = aim/100

    if num_summaries > 1:
        min_length_rel = [0] * num_summaries
        max_length_rel = [0] * num_summaries
        min_length_words = [0] * num_summaries
        max_length_words = [0] * num_summaries
        summary_output = [""] * num_summaries
        text_input_length = len(list(text_input.split()))
        aim_mult = [0] * num_summaries
        compression = [0] * num_summaries

        for i in range(num_summaries):
            min_length_rel[i] = (aim + i*deviation_input)/100
            max_length_rel[i] = (aim + (i+1)*deviation_input)/100
            min_length_words[i] = round(text_input_length * (aim + i*deviation_input)/100)
            max_length_words[i] = round(text_input_length * (aim + (i+1)*deviation_input)/100)
            aim_mult[i] = min_length_rel[i] + (deviation_input/2)/100

        for i in range(num_summaries):
            summary_output[i] = summarizer(
                text_input, 
                min_length=min_length_words[i], 
                max_length=max_length_words[i]
            )
            text = str(summary_output)
            text_length = len(list(text.split()))

            compression = text_length / text_input_length
            deviation_output = abs(compression - aim_rel)

        # print("aim_mult)
        # print(min_length_rel)

    if num_summaries == 1:
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
        compression = text_length / text_input_length
        deviation_output = abs(compression - aim_rel)

    # print("compression:", compression)
    # print("aim", aim_rel)
    # print("deviation:", deviation_output)

    return  text