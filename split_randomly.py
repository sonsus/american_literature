import jsonlines as jsl
import numpy
from numpy import random
from tqdm import tqdm
random.seed(777) #make it reproducible


with jsl.open("amerlit.jsonl") as reader:
    with jsl.open('train.jsonl', mode='w') as train, \
        jsl.open('val.jsonl', mode='w') as val, \
        jsl.open('test.jsonl', mode='w') as test:
            testidx=[]
            validx=[]
            for i, obj in tqdm(enumerate(reader)):
                #index a: goes to val, b: goes to test split 
                if i%10==0: # every 10 iteration, a, b idx are randomly picked, a!=b
                    a= random.randint(10)
                    while 1:
                        b= random.randint(10)
                        if b!=a: break
                    testidx.append(b)
                    validx.append(a)

                if i%10==a:
                    val.write(obj)
                elif i%10==b:
                    test.write(obj)
                else:
                    train.write(obj)
            print(f"test and val categorical distribution of indices: 0~9 (albeit it does not necessarily have to be random)")
            print(f"testidx: {[testidx.count(i) for i in range(10)]}")
            print(f"validx: {[validx.count(i) for i in range(10)]}")

#check the number of lines 
with open("amerlit.jsonl", errors='replace') as f:
    rawlen = len(f.readlines())
    with open('train.jsonl', encoding='utf-8') as t,\
        open('val.jsonl', encoding='utf-8') as v,\
        open('test.jsonl', encoding='utf-8') as test:
            trainlen = len(t.readlines())
            vallen = len(v.readlines())
            testlen = len(test.readlines())
            print(f"rawfile lines= {rawlen}")
            print(f"train, val, test = {trainlen}, {vallen}, {testlen}")
            assert rawlen == trainlen + vallen + testlen, "why differnt?"
