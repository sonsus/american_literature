import jsonlines as jsl
from fire import Fire
from pprint import pprint
import subprocess as sb
from pathlib import Path


def return_maxlen(sentlist):
    ls = [len(s.split()) for s in sentlist]
    return max(ls)

def filter_longer(dataroot='./', threshold=[3,75], writing=True):
    # writing True: filters everything (train.jsonl: filtered /  _train.jsonl: before filtered)
    # writing False: write
    root = Path(dataroot)
    spls = ['train', 'val', 'test']
    _spls  = ["_"+s for s in spls]
    for spl, _spl in zip(spls, _spls):
        if (root / f"{_spl}.jsonl").exists():
            assert (root/f"{spl}.jsonl").exists(), f"where is {spl}.jsonl? check {dataroot}"
            continue
        rename_command = f'mv {dataroot}/{spl}.jsonl {dataroot}/{_spl}.jsonl'
        sb.run(rename_command.split())
        print(f"renaming {dataroot}/{spl}.jsonl to {dataroot}/{_spl}.jsonl is done~! \n")

    print(f"renaming spl.jsonl ==> _spl.jsonl all done: do not cancel the execution!")

    for spl, _spl in zip(spls, _spls):
        discarded_len = []
        with jsl.open(root / f'{_spl}.jsonl') as reader, \
            jsl.open(root / f'{spl}.jsonl', mode='w') as writer, \
            jsl.open(root / f'discarded.{spl}.threshold.{threshold}.jsonl', mode='w') as fdiscard:
            reader = list(reader)
            totlen = len(reader)
            for obj in reader:
                l_pre = len(obj['premise'].split()) # str
                l_tru = len(obj['true_h'].split()) # str
                l_fal = return_maxlen(obj['false_hs']) # list

                maxl = max([l_pre, l_tru])
                minl = min([l_pre, l_tru])
                if maxl <= threshold[1] and minl >= threshold[0]:
                    writer.write(obj)
                else:
                    fdiscard.write(obj)
                    discarded_len.append(maxl)

        print(f"with threshold: {threshold}\t{spl}: discarded {len(discarded_len)} which is {100 * ( len(discarded_len) / totlen )}% of total")







if __name__ == "__main__":


    '''
    usage:
    python filter_outliers.py [--dataroot PATH] [--threshold [int1,int2] (w/o whitespace)] [--writing]

    '''

    Fire(filter_longer)
