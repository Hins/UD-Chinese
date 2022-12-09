import udchinese
import os
import time
import json
from pathlib import Path
import logging

def main(input_path, result_path):
    json_obj = []
    for file in Path(input_path).glob('**/*.txt'):
        logging.info("file{}".format(file))
        mid = os.path.relpath(str(file), input_path)
        logging.info("mid{}".format(mid))
        dst_json = os.path.join(result_path, os.path.dirname(mid), str(file.stem) + '.json')
        logging.info("dst_json{}".format(dst_json))
        os.makedirs(os.path.dirname(dst_json), exist_ok=True)

        zh = udchinese.load()
        test_start_time = time.time()

        with open(str(file), 'r') as f:
            idx = 0
            for line in f:
                s = zh(line.replace("\n", ""))
                sentence_json_obj = {}
                sentence_json_obj["ID"] = idx
                sentence_json_obj["text"] = line.replace("\n", "")
                sentence_json_obj["words"] = []
                for id, token in enumerate(s):
                    elements = str(token).split("\t")
                    token_obj = {}
                    token_obj["id"] = id + 1
                    token_obj["form"] = elements[1]
                    token_obj["head"] = elements[6]
                    token_obj["pos"] = elements[3]
                    token_obj["deprel"] = ""
                    token_obj["stanfordnlpdependencies"] = ""
                    sentence_json_obj["words"].append(token_obj)
                json_obj.append(sentence_json_obj)
        test_time = time.time() - test_start_time
        with open(dst_json, 'w', encoding='utf-8') as f:
            json.dump(json_obj, f, indent=4, ensure_ascii=False)
        return len(json_obj), test_time, json_obj