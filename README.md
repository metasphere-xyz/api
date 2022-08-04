# Text endpoints

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 255.0px;"><col style="width: 505.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Endpoint</strong></p></th><th class="confluenceTh"><p><strong>Description</strong></p></th></tr><tr><td class="confluenceTd"><p><a href="https://metasphere-tech.atlassian.net/wiki/spaces/ECCHRAPP/pages/25493524/4.1+-+Text+Endpoints#%2Ftext%2Fsummarize%2F%7Bshort%2C-medium%2C-long%7D" rel="nofollow">/text/summarize</a></p></td><td class="confluenceTd"><p>Summarizes a given text into at least two summaries of different lengths and returns the summary, it’s hash sum and compression parameters</p></td></tr><tr><td class="confluenceTd"><p><a href="https://metasphere-tech.atlassian.net/wiki/spaces/ECCHRAPP/pages/25493524/4.1+-+Text+Endpoints#%2Ftext%2Fsummarize%2F%7Bshort%2C-medium%2C-long%7D" rel="nofollow">/text/summarize/short</a></p></td><td class="confluenceTd"><p>Summarizes a given text into a short summary and returns the summary, it’s hash sum and compression parameters</p></td></tr><tr><td class="confluenceTd"><p><a href="https://metasphere-tech.atlassian.net/wiki/spaces/ECCHRAPP/pages/25493524/4.1+-+Text+Endpoints#%2Ftext%2Fsummarize%2F%7Bshort%2C-medium%2C-long%7D" rel="nofollow">/text/summarize/medium</a></p></td><td class="confluenceTd"><p>Summarizes a given text into a medium sized summary and returns the summary, it’s hash sum and compression parameters</p></td></tr><tr><td class="confluenceTd"><p><code>/text/extract/chunks</code></p></td><td class="confluenceTd"><p>Segments a given text into chunks and returns a list of chunks and their hash sums</p></td></tr><tr><td class="confluenceTd"><p><code>/text/extract/entities</code></p></td><td class="confluenceTd"><p>Extracts entities from a given text and returns a list of entities with their label, start and end position in the byte stream, and annotations (if available)</p></td></tr></tbody></table>

/text/summarize/{short, medium, long}
=====================================

Summarizes a given text using a transformer based algorithm from tensorflow and returns the summary, the summary’s hash sum and compression parameters.

Input
-----

The endpoints takes a text as an input argument and accepts a number of variables to be set in order to determine the number and quality of the desired summarization:

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 149.0px;"><col style="width: 519.0px;"><col style="width: 92.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Input variables</strong></p></th><th class="confluenceTh"><p><strong>Description</strong></p></th><th class="confluenceTh"><p style="text-align: right;"><strong>optional?</strong></p></th></tr><tr><td class="confluenceTd"><p><code>text</code></p></td><td class="confluenceTd"><p>Original text to be summarized</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>aim</code></p></td><td class="confluenceTd"><p>Compression aim: length of the summarization in % of the original text</p></td><td class="confluenceTd"><p style="text-align: right;"><span class="inline-comment-marker" data-ref="539d32ca-6dd4-4777-82a0-021faa326a66">yes</span></p></td></tr><tr><td class="confluenceTd"><p><code>deviation</code></p></td><td class="confluenceTd"><p>Maximal deviation (±) in % from the compression aim</p></td><td class="confluenceTd"><p style="text-align: right;"><span class="inline-comment-marker" data-ref="94f163d0-2de3-4403-9d5c-7e18a28170ec">yes</span></p></td></tr><tr><td class="confluenceTd"><p><code>num_summaries</code></p></td><td class="confluenceTd"><p>Number of summaries to return, or auto</p></td><td class="confluenceTd"><p style="text-align: right;">yes</p></td></tr></tbody></table>

The API endpoints `short`, `medium` and `long` adjust the summarization corresponding to the following default settings:

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 213.0px;"><col style="width: 241.0px;"><col style="width: 166.0px;"><col style="width: 140.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Endpoint</strong></p></th><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: right;"><code>aim</code></p></td><td data-highlight-colour="#f4f5f7" class="confluenceTd"><p style="text-align: right;"><code>deviation</code></p></td><th class="confluenceTh"><p style="text-align: right;"><code>num_summaries</code></p></th></tr><tr><td class="confluenceTd"><p><code>/text/summarize</code></p></td><td class="confluenceTd"><p style="text-align: right;">50 %</p></td><td class="confluenceTd"><p style="text-align: right;">± 10 %</p></td><td class="confluenceTd"><p style="text-align: right;">3</p></td></tr><tr><td class="confluenceTd"><p><code>/text/summarize/short</code></p></td><td class="confluenceTd"><p style="text-align: right;">20 %</p></td><td class="confluenceTd"><p style="text-align: right;">± 10 %</p></td><td class="confluenceTd"><p style="text-align: right;">1</p></td></tr><tr><td class="confluenceTd"><p><code>/text/summarize/medium</code></p></td><td class="confluenceTd"><p style="text-align: right;">40 %</p></td><td class="confluenceTd"><p style="text-align: right;">± 10 %</p></td><td class="confluenceTd"><p style="text-align: right;">1</p></td></tr><tr><td class="confluenceTd"><p><code>/text/summarize/long</code></p></td><td class="confluenceTd"><p style="text-align: right;">60 %</p></td><td class="confluenceTd"><p style="text-align: right;">± 10 %</p></td><td class="confluenceTd"><p style="text-align: right;">1</p></td></tr></tbody></table>

_Example:_ A compression aim of 40% ± 5% deviation results in a lower compression limit of 35% and an upper limit of 45% compared to the original input text (100%).

If `num_summaries` is set, the `aim` represents the aim for the lowest compression rate and `deviation` as a delimiter between summaries. If the endpoint is to produce 3 summaries with an aim of 15% and a deviation of 10%, the results will be in the range of:

*   15–25%: summary 1
    
*   25–35%: summary 2
    
*   35–45%: summary 3
    

Request
-------

The API can deliver plain text, a JSON object or render an HTML template with the results. The desired output is set by submitting the [Accept request HTTP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept) with the according content-type:

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 362.0px;"><col style="width: 188.0px;"><col style="width: 210.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Accepted input</strong></p></th><th class="confluenceTh"><p><strong>Content-Type</strong><br>(Input)</p></th><th class="confluenceTh"><p><strong>Content-Types</strong><br>(Output)</p></th></tr><tr><td class="confluenceTd"><p>Form field variables<br>(from HTML interface)</p></td><td class="confluenceTd"><p>text/html</p></td><td class="confluenceTd"><p>text/html</p></td></tr><tr><td class="confluenceTd"><p>Plain text</p></td><td class="confluenceTd"><p>text/plain</p></td><td class="confluenceTd"><p>text/plain<br>application/json</p></td></tr><tr><td class="confluenceTd"><p>JSON object</p></td><td class="confluenceTd"><p>application/json</p></td><td class="confluenceTd"><p>text/plain<br>application/json</p></td></tr></tbody></table>

Example request with plain text payload, expecting a JSON object as return:

```bash
curl https://api.metasphere.xyz/text/summarize/ \
  --request POST \
  --header 'Content-Type: text/plain' \
  --header 'Accept: application/json' \
  --data 'This is an input sentence.'
```

Example request with JSON payload, expecting a JSON object as return:

Content-Type: application/json;

```bash
curl https://api.metasphere.xyz/text/summarize/ \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --data ' \
    { \
      "text": "This is an input sentence.",
      "aim": 30, \
      "deviation": 10, \
      "num_summaries": 3
    }'
```

Response
--------

The output is a number of summaries (at least 1), the hash sums of the original input text and summaries, and the compression result, a similarity ratio between the original input and the summarized output, ignoring typos or misspelled words. The `compression` result is calculated using a [fuzzy string matching](https://pypi.org/project/fuzzy-match/) function. The `deviation` in the API response is the actual **calculated deviation**, not the desired deviation from the input request. It can therefore be used to discriminate and discard weak results where the deviation is higher than the desired deviation.

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 149.0px;"><col style="width: 519.0px;"><col style="width: 92.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong><span class="inline-comment-marker" data-ref="c63a20a2-c331-407a-b878-c102b257f280">Output variables</span></strong></p></th><th class="confluenceTh"><p><strong><span class="inline-comment-marker" data-ref="c63a20a2-c331-407a-b878-c102b257f280">Description</span></strong></p></th><th class="confluenceTh"><p style="text-align: right;"><strong><span class="inline-comment-marker" data-ref="c63a20a2-c331-407a-b878-c102b257f280">optional?</span></strong></p></th></tr><tr><td class="confluenceTd"><p><code>chunk_id</code></p></td><td class="confluenceTd"><p>md5sum of the original input text</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>summary</code></p></td><td class="confluenceTd"><p>JSON array of the returned summaries</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>text</code></p></td><td class="confluenceTd"><p>summarized text</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>summary_id</code></p></td><td class="confluenceTd"><p>md5sum of the summarized text</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>compression</code></p></td><td class="confluenceTd"><p>achieved compression rate</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>aim</code></p></td><td class="confluenceTd"><p>compression aim (as per input)</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>deviation</code></p></td><td class="confluenceTd"><p>achieved deviation (<code>compression</code> compared to <code>aim</code>)</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr></tbody></table>

Response:  
Content-Type: application/json;

```java
{
    "chunk_id": "md5sum",
    "summary": [
        {
            "text": "This is a short summary.",
            "summary_id": "md5sum"
            "compression": 32,
            "aim": 35,
            "deviation": 3
        },
        {
            "text": "This is a medium summary.",
            "summary_id": "md5sum"
            "compression": 40,
            "aim": 39,
            "deviation": 3
        },
        {
            "text": "This is a long summary.",
            "summary_id": "md5sum"
            "compression": 45,
            "aim": 43,
            "deviation": 3
        }
    ] 
}
```

text/extract/entities
=====================

**Description:** Extracting entities from text like PERSONS, LOCATIONS and DATES with the help of  
SpaCies NER function.

**Input:** text

**Output:** _entity text_ with according _entity label_

→ Endpoint returns the following JSON object:

```java
{
    "chunk_id": "md5",
    "entities": {
        "Rieke": "PERSON",
        "2019": "DATE",
        "Berlin": "LOC"
    }
}
```

text/similarities
=================

Compares a given text using a transformer based algorithm from tensorflow and returns _n_ similar chunks and their hash sums and the respective similarity score in comparison to the input text.

Input
-----

The endpoint expects a text as an input argument. Optionally, the number of similar chunks to be returned can be submitted. In order to limit the search scope, a collection ID or the type of text to be searched can be specified.

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 186.0px;"><col style="width: 391.0px;"><col style="width: 95.0px;"><col style="width: 88.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Input variables</strong></p></th><th class="confluenceTh"><p><strong>Description</strong></p></th><th class="confluenceTh"><p style="text-align: right;"><strong>optional</strong></p></th><th class="confluenceTh"><p style="text-align: right;"><strong>default</strong></p></th></tr><tr><td class="confluenceTd"><p><code>text</code></p></td><td class="confluenceTd"><p>Original text to be summarized</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td><td class="confluenceTd"><p style="text-align: right;"></p></td></tr><tr><td class="confluenceTd"><p><code>chunks</code></p></td><td class="confluenceTd"><p>Number of similar chunks to be returned</p></td><td class="confluenceTd"><p style="text-align: right;">yes</p></td><td class="confluenceTd"><p style="text-align: right;">3</p></td></tr><tr><td class="confluenceTd"><p><code>type</code></p></td><td class="confluenceTd"><p><code>all</code> <code>chunk</code> <code>summary</code> <code>entity</code></p></td><td class="confluenceTd"><p style="text-align: right;">yes</p></td><td class="confluenceTd"><p style="text-align: right;"><code>all</code></p></td></tr><tr><td class="confluenceTd"><p><code>collection</code></p></td><td class="confluenceTd"><p>ID of a collection to limit the search scope</p></td><td class="confluenceTd"><p style="text-align: right;">yes</p></td><td class="confluenceTd"><p style="text-align: right;"></p></td></tr><tr><td class="confluenceTd"><p><code>minimum_score</code></p></td><td class="confluenceTd"><p>Threshold for similarity score</p></td><td class="confluenceTd"><p style="text-align: right;">yes</p></td><td class="confluenceTd"><p style="text-align: right;">30</p></td></tr></tbody></table>

Response
--------

<table data-layout="default" class="confluenceTable"><colgroup><col style="width: 149.0px;"><col style="width: 519.0px;"><col style="width: 92.0px;"></colgroup><tbody><tr><th class="confluenceTh"><p><strong>Variable</strong></p></th><th class="confluenceTh"><p><strong>Description</strong></p></th><th class="confluenceTh"><p style="text-align: right;"><strong>optional</strong></p></th></tr><tr><td class="confluenceTd"><p><code>status</code></p></td><td class="confluenceTd"><p>Status: <code>success</code> or <code>failed</code></p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>text</code></p></td><td class="confluenceTd"><p>original input text</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>similarities</code></p></td><td class="confluenceTd"><p>Array of similar nodes</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>chunk_id</code></p></td><td class="confluenceTd"><p>md5sum of similar nodes</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>text</code></p></td><td class="confluenceTd"><p>text of similar node</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr><tr><td class="confluenceTd"><p><code>score</code></p></td><td class="confluenceTd"><p>similarity score in percent</p></td><td class="confluenceTd"><p style="text-align: right;">no</p></td></tr></tbody></table>

The endpoint returns the following JSON object:

```java
{
    "text": "This is the request text",
    "similarities": [
        {
            "chunk_id":"md5",
            "score": 95,
            "text": "Chunk text" // summary or original chunk or entity
        },
        {
            "chunk_id":"md5",
            "score": 91,
            "text": "Chunk text"
        },
        {
            "chunk_id":"md5",
            "score": 88,
            "text": "Chunk text"
        }
    ]
}
```


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
