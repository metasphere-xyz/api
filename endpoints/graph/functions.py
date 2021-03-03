from flask import jsonify
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
def find_node(node_id):
    query = '''
        MATCH (c:Chunk {chunk_id: $chunk_id})
        RETURN c as chunk
    '''
    result = graph.run(query, parameters={'chunk_id': node_id}).data()
    result = result[0]['chunk']
    response['node']=result
    return response

# TODO: add missing functions for other endpoints
    