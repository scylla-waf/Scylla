#!/usr/bin/python3


import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
import pickle
from sklearn.cluster import KMeans

from scylla_dependencies.WAF.data import *


class IntelligentDetect:

    def __init__(self):
        pass
        
    def indentify(self, payload):
    
        intelligence = DataEntry()
        new_point = intelligence.all(payload)
    
        kmeans = KMeans(n_clusters=2)

        filename = './scylla_dependencies/WAF/datasets/dataset_test.scy'

        f = open(filename, 'r')
        chunk = f.read()
        f.close()

        dataset = pickle.loads(chunk)

        a = np.array([new_point])
        
        dataset = np.vstack((dataset, a))

        kmeans.fit(dataset)
        predict_vals = kmeans.predict(dataset)
        
        out_chunk = pickle.dumps(dataset)
        
        f2 = open('./scylla_dependencies/WAF/datasets/dataset_test.scy', 'w')
        f2.write(out_chunk)
        f2.close()
        
        if predict_vals[len(predict_vals) - 1] == 0:
            print('[INFO] Attack detected: ' + str(payload))
                
         

