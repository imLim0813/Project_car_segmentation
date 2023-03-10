import json
import torch
from pathlib import Path
from itertools import repeat
from collections import OrderedDict


def read_json(fname):
    fname = Path(fname)
    with fname.open('rt') as handle:
        return json.load(handle, object_hook=OrderedDict)


if __name__ == '__main__':
    config = read_json('../config.json')
    print(config)