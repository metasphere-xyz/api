from endpoints.graph.response import *
from endpoints.graph.routes import *

def optionalParameter(chunk_id, source_file, start_time, end_time, summaries, entities, similarity):
    response = find_chunk(chunk_id)

    if response["status"]=="success":
        print("chunk was found")
        if source_file != None:
            source_file = source_file
        else:
            source_file = response["instance"]["source_file"]

        if start_time != None:
            start_time = start_time
        else:
            start_time = response["instance"]["start_time"]

        if end_time != None:
            end_time = end_time
        else:
            end_time = response["instance"]["end_time"]

        if summaries != None:
            summaries = summaries
        else:
            summaries = response["instance"]["summaries"]

        if entities != None:
            entities = entities
        else:
            entities = response["instance"]["entities"]
        
        if similarity != None:
            similarity = similarity
        else:
            similarity = response["instance"]["similarity"]

    else:
        print("chunk does not exist")  