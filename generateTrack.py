
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


# Initialize the model.
print("Initializing Melody RNN...")
bundle = sequence_generator_bundle.read_bundle_file('basic_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()

print('🎉 Done!')


#---------------------------------

midi_data = pretty_midi.PrettyMIDI('friendsAgain.mid')
print("midi data: ")
print(midi_data)




friendsAgainSequence = note_seq.midi_to_note_sequence(midi_data)

#  friendsAgainSequence.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
#  friendsAgainSequence.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
#  friendsAgainSequence.notes.add(pitch=60, start_time=0.0, end_time=0.5, velocity=80)
#  friendsAgainSequence.total_time = 8
#  friendsAgainSequence.tempos.add(qpm=60);



#  note_seq.plot_sequence(friendsAgainSequence)
#  note_seq.play_sequence(friendsAgainSequence,synth=note_seq.synthesize)

#-----------------------------
input_sequence = friendsAgainSequence # change this to teapot if you want
num_steps = 5000 # change this for shorter or longer sequences
temperature = 1.0 # the higher the temperature the more random the sequence.

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



note_seq.sequence_proto_to_midi_file(finalSequence, 'output.mid')


