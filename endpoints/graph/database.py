from config import *
from endpoints.graph.response import submit

def find_node(search):
    query = '''
        MATCH (n)
        WHERE n.chunk_id=$search or n.text=$search or n.name=$search or n.summary_id=$search or n.collection_id=$search or n.entity_id=$search or n.name=$search
        RETURN n as db_return
    '''
    parameters={'search': search}
    response = submit(query, parameters)
    return response

def find_chunk(chunk):
    query = '''
        MATCH (c:Chunk)
        WHERE c.chunk_id=$chunk or c.text=$chunk or c.name=$chunk
        RETURN c as db_return
    '''
    parameters={'chunk': chunk}
    response = submit(query, parameters)
    return response

def find_entity(entity):
    query = '''
        MATCH (e:Entity)
        WHERE e.entity_id=$entity or e.name=$entity
        RETURN e as db_return
    '''
    parameters={'entity': entity}
    response = submit(query, parameters)
    return response

def find_collection(collection):
    query = '''
        MATCH (co:Collection)
        WHERE co.collection_id=$collection or co.name=$collection
        RETURN co as db_return
    '''
    parameters={'collection': collection}
    response = submit(query, parameters)
    return response

def find_summary(summary):
    query = '''
        MATCH (s:Summary)
        WHERE s.summary_id=$summary or s.name=$summary or s.text=$summary
        RETURN s as db_return
    '''
    parameters={'summary': summary}
    response = submit(query, parameters)
    return response

def add_collection_with_chunks(collection_id, name, source_type, source_path, date, intro_audio, outro_audio, intro_text, trigger_warning, num_chunks, chunk_sequence):
    # hash = hashlib.md5(name[0].encode("utf-8"))
    # collection_id = hash.hexdigest()
    print(f"[bold]Adding collection.[/bold]")
    print(f"Number of chunks: {len(chunk_sequence)}")

    chunk_ids = json.dumps(chunk_sequence)

    for chunk in chunk_sequence:
        chunk["entities"] = json.dumps(chunk["entities"])
        chunk["summaries"] = json.dumps(chunk["summaries"])


    query_1 = '''
        WITH $chunk_sequence AS seq
        UNWIND seq AS data
        CREATE(c:Chunk)
        SET c = data
        SET c.name = data.source_file
        WITH c
        ORDER BY c.name ASC
        WITH collect(c) as chunks
        CALL apoc.nodes.link(chunks, 'NEXT_CHUNK')
        RETURN chunks as db_return
    '''

    parameters_1 = {
        'chunk_sequence': chunk_sequence
    }

    response = submit(query_1, parameters_1)
    print(response)

    query_2 = '''
        CREATE(co:Collection {collection_id: $collection_id, name: $name, source_type: $source_type, source_path: $source_path, date: $date, intro_audio: $intro_audio, outro_audio: $outro_audio, intro_text: $intro_text, num_chunks: $num_chunks, chunk_sequence: $chunk_ids})
        RETURN co as db_return
    '''

    parameters_2 = {
        'collection_id': collection_id,
        'name': name,
        'source_type': source_type,
        'source_path': source_path,
        'date': date,
        'intro_audio': intro_audio,
        'outro_audio': outro_audio,
        'intro_text': intro_text,
        'intro_text': intro_text,
        'num_chunks': num_chunks,
        'chunk_ids': chunk_ids
    }

    response = submit(query_2, parameters_2)
    print(response)

    query_3 = '''
        MATCH (c:Chunk {collection_id: $collection_id}),(co:Collection {collection_id: $collection_id})
        WITH COLLECT(c) AS chunks, co
        FOREACH (ch IN chunks |
            CREATE (ch)-[:CONTAINED_IN]->(co))
        RETURN co as db_return
    '''

    parameters_3 = {
        'collection_id': collection_id
    }

    response = submit(query_3, parameters_3)
    print (response)
    return response

def add_collection_without_chunks(name, source_type, source_path, date, chunk_sequence):
    query = '''
        CREATE(co:Collection {name: $name, source_type: $source_type, source_path: $source_path, date: $date, chunk_sequence: $chunk_sequence})
        RETURN co as db_return
    '''
    parameters={
        'name': name,
        'source_type': source_type,
        'source_path': source_path,
        'date': date,
        'chunk_sequence': chunk_sequence
    }
    response = submit(query, parameters)
    return response

def add_chunk_to_collection(text, source_file, start_time, end_time, summaries, entities, similarity, collection_id):
    hash = hashlib.md5(text[0].encode("utf-8"))
    chunk_id = hash.hexdigest()
    query_1 = '''
        CREATE(c:Chunk {name: $source_file, chunk_id: $chunk_id, source_file: $source_file, start_time: $start_time, end_time: $end_time, text: $text, summaries: $summaries, entities: $entities, similarity: $similarity})
        RETURN c as db_return
    '''

    query_2 = '''
        MATCH(co:Collection {collection_id: $collection_id}),(c:Chunk {chunk_id: $chunk_id})
        CREATE (c)-[:CONTAINED_IN]->(co)
    '''

    parameters_1 = {
        'chunk_id': chunk_id,
        'text': text,
        'source_file': source_file,
        'start_time': start_time,
        'end_time': end_time,
        'summaries': "",
        'entities': "",
        'similarity': "",
        'collection_id': collection_id
    }

    parameters_2 = {
        'chunk_id': chunk_id,
        'collection_id': collection_id
    }

    response = submit(query_1, parameters_1)
    submit(query_2, parameters_2)
    return response

def add_unwrap_chunk_to_collection(text, source_file, start_time, end_time, summaries, entities, similarity, collection_id):
    hash = hashlib.md5(text[0].encode("utf-8"))
    chunk_id = hash.hexdigest()
    query_1 = '''
        WITH split($text, " ") as words
        CREATE(c:Chunk {name: $source_file, chunk_id: $chunk_id, source_file: $source_file, start_time: $start_time, end_time: $end_time, text: $text, summaries: $summaries, entities: $entities, similarity: $similarity})
        FOREACH (w IN words |
            MERGE (wo:Word {name: w})
            MERGE (wo)-[:CONTAINED_IN]->(c))
        RETURN c as db_return
    '''
    query_2 = '''
        WITH split($text, " ") as words
        WITH words as text
        UNWIND range(0, size(text)-2) AS i
        MATCH (w1:Word {name: text[i]})
        MATCH (w2:Word {name: text[i+1]})
        MERGE (w1)-[:NEXT_WORD]->(w2)
    '''
    query_3 = '''
        MATCH(co:Collection {collection_id: $collection_id}),(c:Chunk {chunk_id: $chunk_id})
        CREATE (c)-[:CONTAINED_IN]->(co)
    '''
    parameters_1 = {
        'chunk_id': chunk_id,
        'text': text,
        'source_file': source_file,
        'start_time': start_time,
        'end_time': end_time,
        'summaries': [],
        'entities': [],
        'similarity': []
    }
    parameters_2 = {
        'text': text
    }
    parameters_3 = {
        'chunk_id': chunk_id,
        'collection_id': collection_id
    }

    response = submit(query_1, parameters_1)
    submit(query_2, parameters_2)
    submit(query_3, parameters_3)
    return response

def add_entity_to_chunk(chunk_id, name, url, entity_label):
    query = '''
        CREATE (e:Entity:ORG {name: $name, url: $url})
        SET e:$entity_label
        WITH e
        MATCH (c:Chunk {chunk_id: $chunk_id})
        CREATE (c)-[:MENTIONS]->(e)
        RETURN e as db_return
    '''
    parameters = {
        'chunk_id': chunk_id,
        'name': name,
        'url': url,
        'entity_label': entity_label
    }
    response = submit(query, parameters)
    return response

def add_summary_to_chunk(chunk_id, summary_id, text, compression, aim, deviation):
    query = '''
        CREATE (s:Summary {summary_id: $summary_id, text: $text, compression: $compression, aim: $aim, deviation: $deviation})
        WITH s
        MATCH (c:Chunk {chunk_id: $chunk_id})
        CREATE (s)-[:BELONGS_TO]->(c)
        RETURN s as db_return
    '''
    parameters = {
        'chunk_id': chunk_id,
        'summary_id': summary_id,
        'text': text,
        'compression': compression,
        'aim': aim,
        'deviation': deviation
    }
    response = submit(query, parameters)
    return response

def update_chunk_data(chunk_id, text, source_file, start_time, end_time, summaries, entities, similarity, collection_id):
    query = '''
        MATCH (c:Chunk {chunk_id: $chunk_id})

        SET c.text = $text,
        c.source_file = $source_file,
        c.start_time = $start_time,
        c.end_time = $end_time,
        c.summaries = $summaries,
        c.entities = $entities,
        c.similarity = $similarity,
        c.collection_id = $collection_id
        RETURN c as db_return
    '''
    parameters={
        'chunk_id': chunk_id,
        'text': text,
        'source_file': source_file,
        'start_time': start_time,
        'end_time': end_time,
        'summaries': summaries,
        'entities': entities,
        'similarity': similarity,
        'collection_id': collection_id
    }

    response = submit(query, parameters)
    return response

def connect_chunk_to_chunk(connect, with_id, with_score):
    query = '''
        MATCH(n1 {chunk_id: $start_id}),(n2 {chunk_id: $end_id})
        CREATE (n1)-[w:SIMILARITY {similarity: $similarity}]->(n2)
        RETURN n1, n2, w.similarity as similarity
    '''
    parameters={
        'start_id': connect,
        'end_id': with_id,
        'similarity': with_score
    }

    response = connect_chunk_to_chunk_submit(query, parameters)
    return response

def connect_entity_to_chunk(connect, with_id):
    query = '''
        MATCH(e {entity_id: $entity_id}),(c {chunk_id: $chunk_id})
        CREATE (e)<-[w:MENTIONS]-(c)
        RETURN c, e
    '''
    parameters={
        'entity_id': connect,
        'chunk_id': with_id
    }
    response = connect_entity_to_chunk_submit(query, parameters)
    return response

def disconnect_chunk_from_chunk(disconnect, from_id):
    query = '''
        MATCH (c:Chunk {chunk_id: $chunk_id})-[r:CONTAINED_IN]->(co:Collection {collection_id: $collection_id})
        DELETE r
        RETURN c, co, r
    '''
    parameters = {
        'chunk_id': disconnect,
        'collection_id': from_id
    }
    response = disconnect_chunk_from_chunk_submit(query, parameters)
    return response

def disconnect_entity_from_chunk(disconnect, from_id):
    query = '''
        MATCH (c:Chunk {chunk_id: $chunk_id})-[r:MENTIONS]->(e:Entity {entity_id: $entity_id})
        DELETE r
        RETURN e, c, r
    '''
    parameters = {
        'entity_id': disconnect,
        'chunk_id': from_id
    }
    response = disconnect_entity_from_chunk_submit(query, parameters)
    return response
