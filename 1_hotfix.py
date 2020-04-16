import jsonlines as jsl
import subprocess as sb

spls = ['train', 'val', 'test']

for spl in spls:
    with jsl.open(f'{spl}.jsonl') as reader, jsl.open(f'{spl}_.jsonl', mode='w') as writer:
        for obj in reader:
            obj['false_hs'] = [""]
            writer.write(obj)
    
    command0 = f"mv {spl}.jsonl {spl}.jsonl_bak; mv {spl}.jsonl_bak scrape-n-process" 
    command1 = f"mv {spl}_.jsonl {spl}.jsonl"
    sb.run(command0.split())
    sb.run(command1.split())
    print(f"{spl} done!")
