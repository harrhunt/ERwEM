import subprocess
import os


def midi2audio(midi, sf2, audio_type='wav'):
    out = os.path.splitext(os.path.basename(midi))[0] + "." + audio_type
    print(out)
    print(['fluidsynth', '-T', audio_type, '-F', out, '-ni', sf2, midi])

    subprocess.call(['fluidsynth', '-g 1.1', '-T', audio_type, '-F', out, '-ni', sf2, midi])


if __name__ == '__main__':
    midi2audio("sample6000/sample6000.ionian.mid", "soundfonts/SalamanderGood.sf2")
