from endpoints.graph.response import *
import hashlib
md5 = hashlib.md5()

from py2neo import Graph
graph = Graph(
    "bolt://ecchr.metasphere.xyz:7687/",
    auth=('neo4j', 'burr-query-duel-cherry')
)

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
        WHERE s.summary_id=$summary or s.name=$summary
        RETURN s as db_return
    '''
    parameters={'summary': summary}
    response = submit(query, parameters)
    return response

def add_collection_without_connections(name, source_type, source_path, date, chunk_sequence):
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
        'summaries': [],
        'entities': [],
        'similarity': [],
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

def add_entity_to_chunk(chunk_id, name, url, entity_category):
    query = '''
        CREATE (e:Entity {name: $name, url: $url})
        SET e: $entity_category
        WITH e
        MATCH (c:Chunk {chunk_id: $chunk_id})
        CREATE (c)-[:MENTIONS]->(e)
        RETURN e as db_return
    '''
    parameters = {
        'chunk_id': chunk_id,
        'name': name,
        'url': url,
        'entity_category': entity_category
    }
    response = submit(query, parameters)
    return response

def connect_nodes(connect, with_id, with_score):
    query = '''
        MATCH(n1 {chunk_id:$start_id}),(n2 {chunk_id:$end_id})
        CREATE (n1)-[:SIMILARITY {similarity:$similarity}]->(n2)
        RETURN n1, n2
    '''

    result = graph.run(query, parameters={
        'start_id': connect,
        'end_id': with_id,
        'similarity': with_score
    }).data()

    start_chunk = result[0]['n1']
    end_chunk = result[0]['n2']

    response_connect['connected'] = start_chunk
    response_connect['with']['node'] = end_chunk
    response_connect['with']['score'] = with_score

    return response_connect


def disconnect_nodes(disconnect, from_id, from_relation):
    query = '''
        MATCH (c:Chunk {chunk_id: $chunk_id})-[r:CONTAINED_IN]->(co:Collection {collection_id: $collection_id})
        DELETE r
        RETURN c, co, r
    '''

    result = graph.run(query, parameters={
        'chunk_id': disconnect,
        'collection_id': from_id
    }).data()

    chunk = result[0]['c']
    collection = result[0]['co']

    response_disconnect['disconnected'] = chunk
    response_disconnect['from']['node'] = collection
    response_disconnect['from']['relation'] = from_relation

    return response_disconnect