import hashlib
md5 = hashlib.md5()

from py2neo import Graph
graph = Graph(
    # "bolt://127.0.0.1:7687",
    "bolt://ecchr.metasphere.xyz:7687/",
    auth=('neo4j', 'burr-query-duel-cherry')
)

response = {
        "status": "success",
        "node": {

        }
    }

# graph functions / cypher commands

# This function find all nodes independent from the Label
def find_node(search):
    query = '''
        MATCH (n)
        WHERE n.chunk_id=$search or n.text=$search or n.name=$search or n.summary_id=$search or n.collection_id=$search
        RETURN n
    '''
    result = graph.run(query, parameters={'search': search}).data()
    result = result[0]['n']
    response['node']=result
    return response

# This function find just the nodes with the Label "Chunk"
def find_chunk(chunk):
    query = '''
        MATCH (c:Chunk)
        WHERE c.chunk_id=$chunk_search or c.text=$chunk_search or c.name=$chunk_search
        RETURN c
    '''
    result = graph.run(query, parameters={'chunk_search': chunk}).data()
    result = result[0]['c']
    response['node']=result
    return response

# TODO: add missing functions for other endpoints

def add_node(text, source_file, start_time, end_time, summaries, entities, similarity):
    hash = hashlib.md5(text[0].encode("utf-8"))
    chunk_id = hash.hexdigest()

    query = '''
        CREATE(c:Chunk {name: $source_file, chunk_id: $chunk_id, source_file: $source_file, start_time: $start_time, end_time: $end_time, text: $text, summaries: $summaries, entities: $entities, similarity: $similarity})
        RETURN c as chunk
    '''

    result = graph.run(query, parameters={
        'chunk_id': chunk_id,
        'text': text, 
        'source_file': source_file, 
        'start_time': start_time, 
        'end_time': end_time,
        'summaries': [],
        'entities': [],
        'similarity': []
        }).data()

    result = result[0]['chunk']
    response['node']=result
    return response

def connect_nodes(connect, with_id, with_score):
    query = '''
        MATCH(n1 {chunk_id:$start_id}),(n2 {chunk_id:$end_id})
        CREATE (n1)-[:SIMILARITY {similarity:$similarity}]->(n2)
        RETURN n1, n2
    '''

    result = graph.run(query, parameters={
        'start_id':connect,
        'end_id': with_id,
        'similarity': with_score
        }).data()
    
    return result
    