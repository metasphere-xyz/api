def optionalParameter():
    if response["status"]=="success":
        print("chunk was found")
        if source_file != "":
            source_file = source_file
        else:
            source_file = response["instance"]["source_file"]

        if start_time != 0.0:
            start_time = start_time
        else:
            start_time = response["instance"]["start_time"]

        if end_time != 0.0:
            end_time = end_time
        else:
            end_time = response["instance"]["end_time"]

        if summaries != []:
            summaries = summaries
        else:
            summaries = response["instance"]["summaries"]

        if entities != []:
            entities = entities
        else:
            entities = response["instance"]["entities"]
        
        if similarity != []:
            similarity = similarity
        else:
            similarity = response["instance"]["similarity"]