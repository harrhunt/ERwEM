import json
import numpy as np


class TheoryStructs:
    with open("data/music/theory_structs.json", "r") as file:
        data = json.load(file)
    modes = data["modes"]
    transforms = data["transforms"]
    majors = data["majors"]
    notes = data["notes"]

    @classmethod
    def construct_transform(cls, start_mode, end_mode):
        if type(start_mode) is str:
            start_index = cls.modes[start_mode]
        else:
            start_index = start_mode
        if type(end_mode) is str:
            end_index = cls.modes[end_mode]
        else:
            end_index = end_mode

        if start_index > end_index:
            end_index += 7

        transform_matrix = [cls.transforms[i % 7] for i in range(start_index, end_index)]

        if len(transform_matrix) is 1:
            return np.sum(transform_matrix, axis=0)
        elif len(transform_matrix) > 1:
            return np.sum(transform_matrix, axis=0)
        else:
            return np.zeros((7,), dtype=int)
