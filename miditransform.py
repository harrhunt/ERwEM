import operator

from theory_structs import TheoryStructs as Theory
import mido


class MidiTransform:

    @staticmethod
    def transpose_mode(file, mode):
        midi = MidiTransform.__parse_midi(file)

        midi.ticks_per_beat = 240

        key = MidiTransform.find_key(midi)

        scale = Theory.majors[key].copy()

        transform = Theory.construct_transform("ionian", mode)
        print(transform)

        for track in midi.tracks:
            for msg in track:
                if msg.type in "program_change":
                    msg.program = 0
                if "note" in msg.type:
                    note = msg.note % 12
                    if note in scale:
                        i = scale.index(note)
                        msg.note += transform[i]
                if msg.type is "note_on":
                    msg.velocity = 115
        sliced = str(midi.filename).split('.')
        sliced.insert(1, mode)
        filename = '.'.join(sliced)
        midi.save(filename)

    @staticmethod
    def find_key(file):
        midi = MidiTransform.__parse_midi(file)

        notes = {}

        for i in range(0, 12):
            notes[str(i)] = 0

        for track in midi.tracks:
            for msg in track:
                if msg.type is "note_on":
                    note = str(msg.note % 12)
                    notes[note] += 1

        top_notes = []
        for i in range(7):
            if len(notes.keys()) > 0:
                top = max(notes.items(), key=operator.itemgetter(1))[0]
                if notes[top] is not 0:
                    top_notes.append(int(top))
                del notes[top]
        print(top_notes)
        record = 7
        found_key = None
        for key in Theory.majors:
            difference = set(top_notes) - set(Theory.majors[key])
            print(difference)
            if len(difference) < record:
                record = len(difference)
                found_key = key
        print(found_key)
        return found_key

    @staticmethod
    def __parse_midi(file):
        if type(file) is mido.MidiFile:
            return file
        elif type(file) is str:
            return mido.MidiFile(file)
        else:
            raise ValueError


if __name__ == '__main__':
    # MidiTransform.find_key("sample2000.lydian.mid")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "lydian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "ionian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "mixolydian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "dorian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "aeolian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "phrygian")
    MidiTransform.transpose_mode("sample6000/sample6000.mid", "locrian")
