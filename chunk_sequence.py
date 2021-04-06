import json

summary_percentage_document = 10
chunk_sequence_json = '''
[
    {
        "chunk_id": "d0a11af617ef4b6a0c9ccdd64eaa3279",
        "speaker": "Wolfgang",
        "text": "So, hello everybody, to the latest edition of our podcast by ECCHR, European Center for Constitutional and Human Rights in Berlin. We’re having a series of talks on arts and human rights with some of the most well-known curators, artists, people from the arts world. And today my guest is Mark Sealy, curator, writer and director of The Association of Black Photographers in London, photography expert and scholar.",
        "source_file": "1-Wolfgang.mp3",
        "start_time": 0.21,
        "end_time": 36.32,
        "duration": 36.11
    },
    {
        "chunk_id": "c54f0f5320582a68619b813c003d6bde",
        "speaker": "Wolfgang",
        "text": "So hello, Mark it’s a pleasure to have you here. Yeah, unfortunately, we cannot record this podcast at your gallery, at Autograph Gallery, Rivington Place in Shoreditch, East London. I love the space very much. Mark, would you like to tell us a little bit about the history of the place and and also about the intentions to set up a place, a physical space, like Autograph in East London?",
        "source_file": "2-Wolfgang.mp3",
        "start_time": 36.51,
        "end_time": 71.43,
        "duration": 34.92
    },
    {
        "chunk_id": "1848b94249db073c0d389fe485a5615d",
        "speaker": "Mark",
        "text": "That’s a very interesting question, because it’s kind of like all, all histories, it’s multilayered. I guess one of the first things that we were very concerned with as kind of activists, really, was the idea of a sense of place. Where does one belong? How do we fit in within the kind of cultural offer within the state?",
        "source_file": "3-Mark.mp3",
        "start_time": 72.34,
        "end_time": 94.41,
        "duration": 22.07
    },
    {
        "chunk_id": "de3693a0943a3b9a2b5a7462a9976d25",
        "speaker": "Mark",
        "text": "From the very outset I guess one of the key things about Autograph, and it built this building in partnership with the Institute of International Visual Arts at the time, was to try and get what I would call a kind of cultural stake in the heart of the city. ",
        "source_file": "4-Mark.mp3",
        "start_time": 136.72,
        "end_time": 153.76,
        "duration": 17.04
    },
    {
        "chunk_id": "7493aad2a04aefd07a316722841ed3e0",
        "speaker": "Mark",
        "text": "To have a bit like a property, like if you’re an individual rather than renting places, it’s important to kind of own something. And we know that in modernist societies, it’s all about what you’ve got: your building, your museum, your assets.",
        "source_file": "5-Mark.mp3",
        "start_time": 153.76,
        "end_time": 172.21,
        "duration": 18.45
    },
    {
        "chunk_id": "142684a218bc7d9a38a9f40d9b07ea87",
        "speaker": "Wolfgang",
        "text": "Yeah, I understand this kind of building up of counter-infrastructure. You also say in one of your statements that Autograph intends to articulate a politics in which unspoken and invisible subjects have challenged spaces of representation – but then establish another kind of representation. ",
        "source_file": "11-Wolfgang.mp3",
        "start_time": 270.6,
        "end_time": 303.12,
        "duration": 32.52
    },
    {
        "chunk_id": "a4660ede807e5cbf4675d9016d11c45f",
        "speaker": "Wolfgang",
        "text": "Is that the right thing or do we have to question the whole  concept of representation?",
        "source_file": "12-Wolfgang.mp3",
        "start_time": 303.12,
        "end_time": 303.12,
        "duration": 0.0
    }
]
'''

chunk_sequence = json.loads(chunk_sequence_json)

def sequence_by_speaker(chunk_sequence):
    try:
        json_loads(chunk_sequence)
    except:
        print ("error")

    if len(chunk_sequence) > 1:
        chunks_by_speaker = []

        sequence = 0
        speaker = ""

        for chunk in chunk_sequence:
            if speaker != chunk["speaker"]:
                speaker = chunk["speaker"]
                sequence = len(chunks_by_speaker)
                chunks_by_speaker.append([{}])
                chunks_by_speaker[sequence] = []
            chunks_by_speaker[sequence].append(dict(chunk))

        return json.dumps(chunks_by_speaker)

chunks_by_speaker = json.loads(sequence_by_speaker(chunk_sequence))

print (json.dumps(chunks_by_speaker, indent=4))

for sequence in chunks_by_speaker:
    speaker = sequence[0]["speaker"]
    contribution = ""
    print(speaker)

    for chunk in sequence:
        contribution += chunk["text"] + " "

    num_chunks = len(sequence)
    print ("num_chunks: " + str(num_chunks))
    ratio = int(num_chunks)/int(summary_percentage_document)
    print ("ratio: " + str(ratio))
    print (contribution)


    # summary = sentence_summarizer(contribution, ratio=ratio)

    # response["chunk_sequence"].append({
    #     "text": summary,
    #     "speaker": contributions[sequence]["speaker"]
    # })
