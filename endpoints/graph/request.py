from config import *

def get_single_json_value():
    if request_type(request) == 'application/json':
        data_json = request.json
        json_key=[*data_json][0]
        search=request.get_json()[json_key]
        return search
    else:
        return 'json expected'

def get_chunk_json_value():
    if request_type(request) == 'application/json':
        text = request.get_json()['text']
        source_file = request.get_json()['source_file']
        start_time = request.get_json()['start_time']
        end_time = request.get_json()['end_time']
        summaries = request.get_json()['summaries']
        entities = request.get_json()['entities']
        similarity = request.get_json()['similarity']
        collection_id = request.get_json()['collection_id']
        return text, source_file, start_time, end_time, summaries, entities, similarity, collection_id
    else:
        return 'json expected'

def get_collection_json_value():
    if request_type(request) == 'application/json':
        collection_id = request.get_json()['collection_id']
        name = request.get_json()['name']
        source_type = request.get_json()['source_type']
        source_path = request.get_json()['source_path']
        date = request.get_json()['date']
        intro_audio = request.get_json()['intro_audio']
        outro_audio = request.get_json()['outro_audio']
        intro_text = request.get_json()['intro_text']
        trigger_warning = request.get_json()['trigger_warning']
        num_chunks = request.get_json()['num_chunks']
        chunk_sequence = request.get_json()['chunk_sequence']
        return collection_id, name, source_type, source_path, date, intro_audio, outro_audio, intro_text, trigger_warning, num_chunks, chunk_sequence
    else:
        return 'json expected'

def get_entity_json_value():
    if request_type(request) == 'application/json':
        # chunk_id = request.get_json()['chunk_id']
        # entity_id = request.get_json()['entity_id']
        # name = request.get_json()['name']
        # text = request.get_json()['text']
        # url = request.get_json()['url']
        # entity_label = request.get_json()['entity_label']
        # return chunk_id, entity_id, name, text, url, entity_label
        try:
            values_from_json = json.loads(str(json.dumps(request.get_json())))
        except:
            return 'could not unpack json'
        finally:
            return values_from_json
    else:
        return 'json expected'

def parse_json_from_request():
    if request_type(request) == 'application/json':
        try:
            # make sure we get json in the first place
            request_json = request.get_json()
        except:
            return 'could not unpack json'
        finally:
            values_from_json = json.loads(str(json.dumps(request_json)))
            return values_from_json
    else:
        return 'json expected'

def get_summary_json_value():
    if request_type(request) == 'application/json':
        chunk_id = request.get_json()['chunk_id']
        summary_id = request.get_json()['summary']['summary_id']
        text = request.get_json()['summary']['text']
        compression = request.get_json()['summary']['compression']
        aim = request.get_json()['summary']['aim']
        deviation = request.get_json()['summary']['deviation']
        return chunk_id, summary_id, text, compression, aim, deviation
    else:
        return 'json expected'

def update_chunk_json_value():
    if request_type(request) == 'application/json':
        chunk_id = request.get_json()['chunk_id']
        text = request.get_json()['text']
        source_file = request.get_json()['source_file']
        start_time = request.get_json()['start_time']
        end_time = request.get_json()['end_time']
        summaries = request.get_json()['summaries']
        entities = request.get_json()['entities']
        similarity = request.get_json()['similarity']
        collection_id = request.get_json()['collection_id']
        return chunk_id, text, source_file, start_time, end_time, summaries, entities, similarity, collection_id
    else:
        return 'json expected'

def connect_chunk_json_value():
    if request_type(request) == 'application/json':
        connect = request.get_json()['connect']
        with_id = request.get_json()['with']['id']
        with_score = request.get_json()['with']['score']
        return connect, with_id, with_score
    else:
        return 'json expected'

def connect_entity_json_value():
    if request_type(request) == 'application/json':
        connect = request.get_json()['connect']
        with_id = request.get_json()['with']['id']
        return connect, with_id
    else:
        return 'json expected'

def disconnect_entity_json_value():
    if request_type(request) == 'application/json':
        disconnect = request.get_json()['disconnect']
        from_id = request.get_json()['from']['id']
        return disconnect, from_id
    else:
        return 'json expected'