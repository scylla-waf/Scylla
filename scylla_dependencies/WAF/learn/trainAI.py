#!/usr/bin/python3

import seaborn as sns
import numpy as np
import pickle
from scylla_dependencies.WAF.data.data import *


class trainAI:

    def __init__(self):
        self.DATASET_PATH = './scylla_dependencies/WAF/datasets/dataset_test.scy'  # dataset path
        sns.set()

    def add(self, payload):

        learn = DataEntry()
        new_point = learn.all(payload)

        f = open(self.DATASET_PATH, 'r')
        chunk = f.read()
        f.close()

        dataset = pickle.loads(chunk)

        a = np.array([new_point])

        dataset = np.vstack((dataset, a))

        out_chunk = pickle.dumps(dataset)

        f2 = open(self.DATASET_PATH, 'w')
        f2.write(out_chunk)
        f2.close()
