import jsonlines as jsl
from fire import Fire
import numpy as np
from pprint import pprint
from pathlib import Path
import sys

def make_res_stats(len_list):
    maximum = max(len_list)
    minimum = min(len_list)
    mean = np.mean(len_list)
    std = np.std(len_list)
    n = len(len_list)
    return {
        'max/min': [maximum, minimum],
        'mean': mean,
        'std': std,
        'n': n,
        'histogram5':(np.histogram(len_list, bins = [i*4 for i in range(n//4 + 2)])[0]*100 / n)[1:].sum(),
    }

def len_false_hs_avg(listofsentences):
    print("\n>>> false_hs_avg length is not implemented yet <<<")
    print("TO USE THIS function, implement it on length_measure.py")
    return 0

def sent_len_measure(dataroot='./'):
    root = Path(dataroot)
    spls = ['train', 'val', 'test']
    res_spls = []
    for spl in spls:
        with jsl.open( root / f'{spl}.jsonl') as reader:
            pre, tru, fal  = [], [], []
            for obj in reader:
                lenpre = len(obj['premise'].split())
                lentru = len(obj['true_h'].split())
                lenfal = 0 #len_false_hs_avg(obj['false_hs'])
                pre.append(lenpre)
                tru.append(lentru)
                fal.append(lenfal)
        res_dict = {
            'premise': make_res_stats(pre),
            'true_h': make_res_stats(tru),
            'false_hs_avg': "not implemented: see length_measure.py @ data/amerlit/length_measure.py",
            }
        res_spls.append(res_dict)

    pprint( dict( zip(spls, res_spls) ) )



if __name__ == "__main__":
    '''
    usage: python length_measure.py [--dataroot PATH=./]

    output: max/min, mean, std, n
    '''
    np.set_printoptions(precision=2, threshold=3000)
    Fire(sent_len_measure)
