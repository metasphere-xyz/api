# Graph endpoints

Find nodes
==========

Returns node(s) as JSON

`/graph/find`
-------------

Looking for any node independent from the Label by matching the id, name and text property.

Request via POST (application/json):
------------------------------------

```java
{
  "id": "1382c2b2873acf23dfcf0e473760a9a2",
  // or "name": "1-Wolfgang",
  // or "text": "That's a very, interesting question, because it's kind of like all, all histories, it's multilayered."
}
```

Response - success (application/json):
--------------------------------------

```java
{
    "status": "success",
    "instance": {
        // all properties of the matched node
        "start_time": 72.34,
        "entities": [],
        "similarity": [],
        "end_time": 78.73,
        "name": "5-Mark",
        "text": "That's a very, interesting question, because it's kind of like all, all histories, it's multilayered.",
        "source_file": "5-Mark.mp3",
        "chunk_id": "cc980bcc6ad2fa883e219a86f0d3cef5",
        "summaries": []
    }
}
```

Response - failed (application/json):
-------------------------------------

```java
{
    "status": "failed",
    "message": "could not find instance (404)",
    "instance": {
        "chunk": "That's a very, interesting question, because it's kind of like all, all histories"
    }
}
```

`/graph/find/chunk (by id)`
---------------------------

Request via POST (application/json):
------------------------------------

With id as search parameter:

```java
{
  "id": "1382c2b2873acf23dfcf0e473760a9a2"
}
```

With name as search parameter:

```java
{
  "name": "For those of you who don't know Forensic Architecture is a research agency that is based in the Goldsmiths University of London, and we are comprised of architects, artists, filmmakers, journalists, software developers, lawyers etc., etc.",    
}
```

Response (application/json):
----------------------------

```java
{
  "status": "success",
  "node": {
    // json of found node (dump from neo4j)
    {
      "chunk_id": "34057c76b74243e12a3ede383a0826ea",
      "text": "This is an example sentence.",
      "source_file": "1-wolfgang.mp3"
      "end_time": 12.33,
      "start_time": 0.21
    }
  }
}
```

`/graph/find/entity (by name or id)`

`/graph/find/collection (by id)`

`/graph/find/summaries (by parent chunk_id)`

### Request via POST (application/json):

With id as search parameter:

```java
{
  "id": "1382c2b2873acf23dfcf0e473760a9a2"
}
```

With name as search parameter:

```java
{
  "name": "For those of you who don't know Forensic Architecture is a research agency that is based in the Goldsmiths University of London, and we are comprised of architects, artists, filmmakers, journalists, software developers, lawyers etc., etc.",    
}
```

### Request via GET (text/plain):

With id as search parameter:

```java
/graph/find/chunk/1382c2b2873acf23dfcf0e473760a9a2
/graph/find/entity/d2a71a312050e043aae21344467dd529
/graph/find/collection/0415a990a0a346a892bd45439e67d196
/graph/find/summaries/1382c2b2873acf23dfcf0e473760a9a2
```

### Response:

Node found (HTTP Response code `200 OK`):

```java
{
  "status": "success",
  "node": {
    // json of found node (dump from neo4j)
    {
      "chunk_id": "34057c76b74243e12a3ede383a0826ea",
      "text": "This is an example sentence.",
      "source_file": "1-wolfgang.mp3"
      "end_time": 12.33,
      "start_time": 0.21
    }
  }
}
```

Node not found (HTTP Response code `404 Not found`):

```java
{
  "status": "error",
  "message": "node not found"
}
```

Add nodes
=========

Adds node to DB, returns HTTP Code 201, returns added node(s) as JSON

`/graph/add/collection`

`/graph/add/chunk (to collection)`

`/graph/add/entity (to chunk)`

`/graph/add/summary (to chunk)`

`/graph/add/urlpreview`
-----------------------

Request via POST (application/json):
------------------------------------

With url as search parameter:

```java
{
  "url": "https://www.magnumfoundation.org"
}
```

Response (application/json) - success:
--------------------------------------

```java
{
    "status": "success",
    "instance": {
        "image": "http://static1.squarespace.com/static/56aa79ef9cadb6c241e3ae46/t/589350efbf629adabaf216d1/1564420859953/MagnumF_Logotype_4C_Pos-WEB.jpg?format=1500w",
        "description": "Magnum Foundation: expanding creativity and diversity in documentary photography.",
        "title": "Magnum Foundation Home",
        "url": "https://www.magnumfoundation.org",
        "timestamp": "25/05/2021, 17:32:57"
    }
}
```

### Request via POST (application/json):

Add chunk:

```java
{
    "text": "So, hello everybody, to the latest edition of our podcast by ECCHR, European Center for Constitutional and Human Rights in Berlin.", // mandatory
    "source_file": "1-wolfgang.mp3", // optional 
    "start_time": 0.21, // optional 
    "end_time": 12.33, // optional 
    "summaries": [], // optional 
    "entities": [], // optional 
    "similarity": [] // optional 
}
```

Add collection:

```java
{
  "name": "Wolfgang & Mark", // mandatory
  "source_type": "audio", // mandatory, possible values: [audio|url|text]
  "source_path": "/episodes/2020-10-3/3644a684f98ea8fe223c713b77189a77/mp3/full-episode.mp3",
  "date": "2021-02-16 15:04:28.539573", // optional creation date python datetime object, calculated from request time if not specified
  "chunk_sequence": [] // optional
}
```

### Response:

Node created (HTTP Response code `201 Created`):

```java
{
  "status": "success",
  "node": {
    // json of newly created node (dump from neo4j) -- chunk in this example (can also be a collection)
    {
      "chunk_id": "c4ca4238a0b923820dcc509a6f75849b", // md5 hash text
      "text": "So, hello everybody, to the latest edition of our podcast by ECCHR, European Center for Constitutional and Human Rights in Berlin.",
      "source_file": "1-wolfgang.mp3", // empty on creation, unless passed in via request
      "start_time": 0.21, // empty on creation, unless passed in via request
      "end_time": 12.33, // empty on creation, unless passed in via request
      "annotations": {}, // empty on creation, unless passed in via request
      "summaries": [], // empty on creation, unless passed in via request
      "entities": [], // empty on creation, unless passed in via request
      "connections": [] // empty on creation, unless passed in via request
    }
  }
}
```

**add summary - Request:**

```java
{
    "chunk_id": "md5sum",
    "summary": {
        "text": "This is a short summary.",
        "summary_id": "md5sum"
        "compression": 32,
        "aim": 35,
        "deviation": 3
    }
}
```

**add summary - Response:**

```java
{
    "status": "success",
    "instance": {
        "text": "This is a short summary.",
        "summary_id": "md5sum"
        "compression": 32,
        "aim": 35,
        "deviation": 3
    }
}
```

Could not create node:

Possible HTTP Response codes:

*   `400 Bad Request (syntax error in JSON)`
    
*   `409 Conflict (conflicts with server state)`
    
*   `413 Payload Too Large (chunk too large)`
    
*   `415 Unsupported Media Type (chunk is not text)`
    

```java
{
  "status": "error",
  "message": "could not create node (" + HTTP Response Code + "): Please supply chunk text."
}
```

Update nodes
============

`/graph/update/urlpreview`

Request via POST (application/json):
------------------------------------

With url as search parameter:

```java
{
  "url": "https://www.magnumfoundation.org"
}
```

Response (application/json) - success:
--------------------------------------

```java
{
    "status": "success",
    "instance": {
        "image": "http://static1.squarespace.com/static/56aa79ef9cadb6c241e3ae46/t/589350efbf629adabaf216d1/1564420859953/MagnumF_Logotype_4C_Pos-WEB.jpg?format=1500w",
        "description": "Magnum Foundation: expanding creativity and diversity in documentary photography.",
        "title": "Magnum Foundation Home",
        "url": "https://www.magnumfoundation.org",
        "timestamp": "25/05/2021, 17:32:57"
    }
}
```

Response (application/json) - failed:
-------------------------------------

```java
{
    "instance": {
        "url": "https://www.magnumfoundatio.org"
    },
    "message": "instance not found",
    "status": "failed"
}
```

Connect nodes
=============

Connects nodes in DB, returns HTTP Code 201

`/graph/connect/chunk (to collection or chunk, with optional weight)`

`/graph/connect/entity (to chunk)`

### Request via POST (application/json):

Connect two nodes with weight:

```java
{
  "connect": "1382c2b2873acf23dfcf0e473760a9a2",
  "with": [
    {
      "id": "c4ca4238a0b923820dcc509a6f75849b",
      "score": "84.5"
    }
  ]
}
```

Connect three nodes without weight:

```java
{
  "connect": "1382c2b2873acf23dfcf0e473760a9a2",
  "with": [
    {
      "id": "c4ca4238a0b923820dcc509a6f75849b",
      "score": "84.5"
    },
    {
      "id": "3644a684f98ea8fe223c713b77189a77"
      // if score is not supplied, the weight is set to 50 %
    }
  ]
}
```

### Response:

Connection created (HTTP Response code `201 Created`):

```java
{
  "status": "success",
  "connected": {
    ... // json of input node (dump from neo4j)
  }
  "with": [ // list of connected nodes 
    {
      "node": {
          ... // json of connected node 1 (dump from neo4j)
      }
      "score": "84.5" // (optional) edge weight in percent, according to the similarity coefficient (fuzzy matching against input chunk)
    }
    ...
  ]
}
```

Connection not created:

One or multiple of the nodes were not found (HTTP Response code `404 Not found`):

```java
{
  "status": "error",
  "message": "node not found: " + id(s) of node
}
```

If one of the nodes can not be found, the whole request is denied and needs to be resubmitted.

Disconnect nodes
================

Disconnects nodes in DB, returns HTTP Code 201

`/graph/disconnect/chunk (from collection)`

### Request via POST (application/json):

```java
{
  "disconnect": "87bd38fd5dc6ea68519703b8b1c18108",
  "from": {
      "id": "4ece0d064575609367f665d617d95d30",
      "relation": "CONTAINED_IN"
    }
}
```

### Response:

```java
{
    "status": "success",
    "disconnected": {
        "start_time": 0.21,
        "entities": [],
        "similarity": [],
        "end_time": 12.33,
        "name": "1-Wolfgang",
        "text": "So, hello everybody, to the latest edition of our podcast by ECCHR, European Center for Constitutional and Human Rights in Berlin.",
        "source_file": "1-Wolfgang.mp3",
        "chunk_id": "87bd38fd5dc6ea68519703b8b1c18108",
        "summaries": []
    },
    "from": {
        "node": {
            "collection_id": "4ece0d064575609367f665d617d95d30",
            "duration": 0,
            "name": "Wolfgang-Mark",
            "type": "",
            "src": ""
        },
        "relation": "CONTAINED_IN"
    }
}
```

`/graph/disconnect/entity (from chunk)`

### Request via POST (application/json):

```java
{
  "disconnect": "87bd38fd5dc6ea68519703b8b1c18108",
  "from": {
      "id": "4ece0d064575609367f665d617d95d30",
      "relation": "SAYS" // if PERSON -> relationship name for other entities must be defined 
    }
}
```

### Response:

Delete nodes
============

Disconnects nodes in DB, returns HTTP Code 200

`/graph/delete/entity` \*

`/graph/delete/collection` \*

`/graph/delete/summary (from chunk)`
