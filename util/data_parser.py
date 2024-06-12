import os
from enum import StrEnum
from typing import TypeAlias

import numpy as np

DATA_OBJ_FOLDERPATH = "data/obj"

obj_map: dict[str, str] = {
    "mursik": "20430_Cat_v1_NEW.obj"  # https://free3d.com/3d-model/cat-v1--220685.html1
}


class OBJSymbols(StrEnum):
    VERTEX = "v"
    NORMAL = "vn"
    TEXTURE = "vt"
    FACE = "f"


ARRAY_MAP: TypeAlias = dict[str, np.ndarray[np.float32]]


def determine_vertex_buffer_format(array_map: ARRAY_MAP) -> tuple[int, int, int]:
    # TODO: Implement this for array map, current implementation is deprecated
    return (3, 3, 2)
    if obj_map[OBJSymbols.VERTEX][0].split(" ") == 3:
        vertex_dim = 3
    else:
        raise NotImplementedError("Vertex Buffer dim != 3 not supported yet.")

    if obj_map[OBJSymbols.NORMAL][0].split(" ") == 3:
        normal_dim = 3
    else:
        raise NotImplementedError("Vertex Buffer dim != 3 not supported yet.")

    if obj_map[OBJSymbols.NORMAL][0].split(" ")[:2] == 2:
        texture_dim = 2
    else:
        raise NotImplementedError("Vertex Buffer dim != 3 not supported yet.")

    (vertex_dim, normal_dim, texture_dim)


def parse_obj_to_numpy(obj_lines: list[str]) -> np.ndarray:
    array_map: ARRAY_MAP = {}
    for symbol in OBJSymbols:
        list_: list[str] = [
            line.removeprefix(symbol.value).lstrip().removesuffix("\n").rstrip()
            for line in obj_lines
            if line.startswith(symbol.value + " ")
        ]
        list_ = list(filter(lambda x: x != "", list_))
        list_split: list[list[str]] = [s.split(" ") for s in list_]
        if symbol != OBJSymbols.FACE:
            array_map[symbol] = np.array(list_split, dtype=np.float32)
        else:
            face_list: list[list[str]] = list_split


if __name__ == "__main__":
    with open(os.path.join(DATA_OBJ_FOLDERPATH, obj_map["mursik"])) as file:
        parse_obj_to_numpy(file.readlines())
