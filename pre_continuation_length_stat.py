import jsonlines as jsl
from fire import Fire
from pprint import pprint
import subprocess as sb
from pathlib import Path

#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

def length_stat(dataroot='./', conti='true_h'): #dataroot contains jsonl files
    root = Path(dataroot)
    spls = ['test', 'val']#['train', 'val', 'test']
    print(f"premise -- {conti} length stats ")
    print( "           ^^^^^^^^           ")

    lengthdict = dict()
    for spl in spls:
        lengths = list()
        print(f"collecting {spl}.jsonl stats")
        with jsl.open(root / f"{spl}.jsonl") as reader:
            reader = list(reader)
            for obj in tqdm(reader):
                continuation = obj[conti]
                concat = f"{obj['premise']} {continuation}".split()
                len_cat = len(concat)
                lengths.append(len_cat)
            lengthdict[spl] = pd.Series(lengths, name = spl).hist()


    for spl, hist in lengthdict.items():
        fig = hist.get_figure()
        fig.savefig(root / f"{spl}_bin20.png")
        print(f"saving {spl}_bin20.png done @ dataroot")







if __name__ == "__main__":


    '''
    usage:
    python pre_continuation_length_stat.py --dataroot PATH --conti [true_h, false_hs]

    '''

    Fire(length_stat)
