#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import shutil
#from pprint import pprint


personPatLIST = ["^{}\s?（[^名又a-zA-Z]+）",
                 "^{}\s?\([^名又a-zA-Z]+\)",
                 "^{}\s?（[^名又a-zA-Z]*）",
                 "^{}，[^a-zA-Z]+人\b",
                 "^{}，[^a-zA-Z]+人(?=[，。])"
                ]


dataDIR = "../data/zhwiki_abstract_2306"
destination_dir = "../data/People/{}"

def main(entryDIR):

    personLIST = []
    for json_f in os.listdir(entryDIR):
        try:
            with open("{}/{}".format(entryDIR, json_f), encoding="utf-8") as f:
                topicSTR = json_f.replace(".json", "")
                entrySTR = json.load(f)["abstract"]
            for p in personPatLIST:
                pat = re.compile(p.format(topicSTR))
                if len(list(re.finditer(pat, entrySTR))) > 0:
                    personLIST.append(topicSTR)
                    if topicSTR == "麥人杰":
                        print(pat)
                else:
                    pass
        except IsADirectoryError:
            pass
    return personLIST

if __name__ == "__main__":
    personLIST = []
    data_files = os.listdir(dataDIR)
    num_files = len(data_files)
    batch_size = 10

    for i in range(0, num_files, batch_size):
        batch_files = data_files[i:i+batch_size]

        for init_s in batch_files:
            if init_s.startswith("._"):
                continue
            else:
                personLIST.extend(main("{}/{}".format(dataDIR, init_s)))

    for root, dirs, files in os.walk(dataDIR):
        for file in files:
            if file.endswith(".json"):
                for member in personLIST:
                    if file.replace(".json", "") == member:
                        source_path = os.path.join(root, file)

                        if os.path.exists(destination_dir.format(file[0])):
                            pass
                        else:
                            os.makedirs(destination_dir.format(file[0]))

                        destination_path = os.path.join(destination_dir.format(file[0]), file)
                        shutil.copy(source_path, destination_path)
                        print(f"檔案 {file} 已成功複製到 {destination_path} 資料夾。")



    print("Finished processing part of the data files.")
