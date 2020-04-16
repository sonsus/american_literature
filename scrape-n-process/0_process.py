#from __future__ import unicode_literals, print_function
import jsonlines
import json
from pathlib import Path
from fire import Fire
from typing import List
from ftfy import fix_text

from spacy.lang.en import English # updated


def process_amerlit(filename='none', len_premises=1, len_hypotheses=1):
    '''
    python process.py --filename [amerlit_shortstories.json] --len_premises 1 --len_hypotheses 1
    '''
    with open(filename, 'r', errors='replace', encoding='utf-8') as r_f, jsonlines.open("amerlit.jsonl", 'w') as r_w:
        amerlit = json.load(r_f)
        for title, paragraphs in amerlit.items():
            storysents = flatten_paragraphs(paragraphs)

            for i, s in enumerate(storysents):
                if i+1+len_premises+len_hypotheses > len(storysents):
                    print(f"wrote {i} lines for story:<{title}> in amerlit.jsonl")
                    break

                obj = dict()
                obj['title'] = title
                obj['premise'] = storysents[i]
                obj['true_h'] = storysents[i+1]
                obj['false_hs'] = [""]
                r_w.write(obj)

    with jsonlines.open('amerlit.jsonl', 'r') as reader:
        print(f"amerlit.jsonl has total: {len(reader)} lines of sentences now")
        print(f"each has {len_premises} premise(s) and {len_hypotheses} hyp(s)")

    return

def flatten_paragraphs(paragraphs:List)->List:
    """
    in: list of paragraph strings
    out: list of sentences
    """
    sents = []
    for p in paragraphs:
        psents = sentencize(p)
        psents = [fix_text(s.strip()) for s in psents]
        if psents: #psents is not empty
            sents.extend(psents)
    return sents

def sentencize(paragraph):
    """
    spacy sentencizer
    """
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(paragraph)
    sents = [sent.string.strip() for sent in doc.sents]

    return sents


if __name__ == "__main__":
    Fire(process_amerlit)
