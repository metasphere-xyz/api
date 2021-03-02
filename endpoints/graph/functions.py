from py2neo import Graph
graph = Graph(
    "bolt://127.0.0.1:7687",
    auth=('neo4j', 'burr-query-duel-cherry')
)

# graph functions / cypher commands
def find_node(node_id):
    query = '''
        MATCH (c:Chunks {chunk_id: {node_id}})
        RETURN c as Chunk
    '''

    result = graph.run(query, parameters={'node_id': node_id}).data()
    return result

# TODO: add missing functions for other endpoints
    