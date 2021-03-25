from flask import Flask, request, jsonify, redirect, session, url_for, send_file
import json

import pretty_midi
print("pretty midi imported")

import magenta
import tensorflow
print("magenta and tensorflow imported")

import note_seq
from note_seq.protobuf import music_pb2
print("note seq imported")


from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2



PORT = "5000"
app = Flask(__name__)

origin = "*"

def extendSequence(input_sequence, temperature): 
    # Initialize the model.
    print("Initializing Melody RNN...")
    bundle = sequence_generator_bundle.read_bundle_file('assets/basic_rnn.mag')
    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    print('melody rnn initialized')

    num_steps = 5000 # change this for shorter or longer sequences

    # Set the start time to begin on the next step after the last note ends.
    last_end_time = (max(n.end_time for n in input_sequence.notes)
            if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm 
    seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
            start_time=last_end_time + seconds_per_step,
            end_time=total_seconds)

    # Ask the model to continue the sequence.
    finalSequence = melody_rnn.generate(input_sequence, generator_options)
    return finalSequence

@app.route("/generateTrack/", methods=["POST"])
def generateTrack(): 

    isFile = request.json["isFile"]
    temperature = request.json["temperature"]

    if (isFile): 
        initialSequence = note_seq.midi_to_note_sequence(request.json["midiFile"])
    else: 
        initialSequence = music_pb2.NoteSequence()
        notes = request.json["notes"]
        for aNote in notes: 
            print(aNote)
            initialSequence.notes.add(pitch=aNote["pitch"], start_time=aNote["start_time"], end_time=aNote["end_time"], 
                    is_drum=True, instrument=10, velocity=80)
        initialSequence.total_time = 1.25
        initialSequence.tempos.add(qpm=60)
        print("notes successfully added")
        print("initialSequence: ")
        print(initialSequence)
        note_seq.plot_sequence(initialSequence)

    extendedSequence = extendSequence(initialSequence, temperature)
    print("extendedSequence: ")
    print(extendedSequence)

    return_json = {"status": "success", 'extendedSequence': extendedSequence}
    return json.dumps(return_json, default=str), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)

