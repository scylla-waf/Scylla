#!/usr/bin/python3


import pickle

import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

from scylla_dependencies.WAF.data.data import *


class IntelligentDetect:

    def __init__(self):
        self.BAD = 0
        self.DATASET_PATH = './scylla_dependencies/WAF/datasets/dataset_test.scy'
        sns.set()

    def identify(self, payload):
        intelligence = DataEntry()
        new_point = intelligence.all(payload)

        kmeans = KMeans(n_clusters=2)

        f = open(self.DATASET_PATH, 'rb')
        chunk = f.read()
        f.close()

        dataset = pickle.loads(chunk)

        a = np.array([new_point])

        dataset = np.vstack((dataset, a))

        kmeans.fit(dataset)
        predict_vals = kmeans.predict(dataset)

        out_chunk = pickle.dumps(dataset)

        f2 = open(self.DATASET_PATH, 'wb')
        f2.write(out_chunk)
        f2.close()

        if predict_vals[len(predict_vals) - 1] == self.BAD:
            print('[INFO] Attack detected: ' + str(payload))
