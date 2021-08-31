import sys
import re
import pandas as pd
# import requests
from json import dumps

file_path = "test.csv"
if(len(sys.argv) > 2):
    exit(1)
elif(len(sys.argv) == 2):
    file_path = sys.argv[1]

df = pd.read_csv(file_path)
class buffer(list):

    def __init__(self, maxSize : int, *args, **kwargs):
        if(maxSize < 0):
            raise ValueError("Incorrect Buffer Size")
        self.maxSize = maxSize
        
        super().__init__(*args, **kwargs)

    def append(self, object):
        super().append(object)
        while(self.maxSize > 0 and len(self) > self.maxSize):
            self.pop(0)
        return None


list_context_answer_dict = []
b = buffer(1)
intended_author = "jozef#1337"
filters = ["tenor.com", "Joined the server."]
for _, row in df.iterrows():
    if(any(fil in row["Content"] for fil in filters)):
        continue

    if(row["Author"] == intended_author):
        list_context_answer_dict.append(dict(prompt="\n".join(b), completion=row["Content"]))
        b.clear()
        continue

    b.append("{0}".format(row["Content"]))

with open(re.sub("\\.[A-Za-z0-9]+$", "", file_path) + ".jsonl", "w") as f:
    f.writelines(dumps(context_answer_dict) + "\n" for context_answer_dict in list_context_answer_dict)