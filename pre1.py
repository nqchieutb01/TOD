import glob
import fitz
import string
from tqdm import tqdm

directory = 'lsvn/'
file_lst = glob.glob(directory+ '*')

print (file_lst[0])
blocks = []
text = ''
for file in file_lst:
    doc = fitz.open(file)
    block_content = ''
    for page in doc: # iterate the document pages
        block = page.get_text('blocks') # get plain text encoded as UTF-8
        # print (block)
        for i in range(1, len(block)-2):
            block_content += block[i][4].replace('\n',' ') + '\n'
    with open (('/media/lamnt53/sda1_mnt/projects/llm_data/lsvn_text/'+file[5:]+'.txt').replace('pdf',''),'w') as f:
        f.write(block_content)

        


import json
def process(file_id):
    f = open(f"txt/lich-su-viet-nam-tron-bo-15-tap-txt-tap-{file_id}.txt", "r")
    data = []
    for x in f:
        data.append(x.strip())
    res = [True] * (len(data)+5)

    for id in range(len(data)):
        line = data[id]
        if line.isnumeric() and int(line) < 1000:
            stopline = False
            for i in range(max(id-7,0),id):
                if data[i][0].isnumeric() and int(data[i][0]) ==1:
                    stopline = i
                    break
    #         print(stopline)
            if stopline:
                for i in range(stopline,id+1):
                    res[i] = False
#                 print(data[stopline])
            res[id+1] = False
    final = []
    for i in range(len(data)):
        if res[i]:
            final.append(data[i])
    
    f = open(f"./clean/book{file_id}.txt", "w")
    f.write(' '.join(final))
    
for i in range(1,16):
    process(i)
    

    
    
    
    
import os
import unicodedata
from string import punctuation

syllable_set = set()

with open("vietnamese.cm.dict", "r") as f:
    for line in f:
        syllable_set.add(unicodedata.normalize("NFC", line.strip()))

def norm_word(word):
    if len(word) == 0:
        return word
    start = 0
    end = len(word)-1
    while word[start] in punctuation and start < len(word)-1:
        start += 1
    while word[end] in punctuation and end > start:
        end -= 1
    
    return word[start:end+1]

def norm_text(infile, outfile):
    with open(infile, "r") as f:
        text = f.read()

    text = unicodedata.normalize("NFC", text)
    words = text.split(" ")

    new_words = []
    i = 0
    while i+2 < len(words):
        if norm_word(words[i] + words[i+1] + words[i+2]).lower() in syllable_set:
            new_words.append(words[i] + words[i+1] + words[i+2])
            print(words[i] + words[i+1] + words[i+2])
            i = i + 3
#         elif (words[i] + words[i+1] + words[i+2])[:-1].lower() in syllable_set and (words[i] + words[i+1] + words[i+2])[-1] in punctuation:
#             new_words.append(words[i] + words[i+1] + words[i+2])
#             print(words[i] + words[i+1] + words[i+2])
#             i = i + 3   
#         elif (words[i] + words[i+1] + words[i+2])[1:].lower() in syllable_set and (words[i] + words[i+1] + words[i+2])[0] in punctuation:
#             new_words.append(words[i] + words[i+1] + words[i+2])
#             print(words[i] + words[i+1] + words[i+2])
#             i = i + 3
        elif norm_word(words[i] + words[i+1]).lower() in syllable_set:
            new_words.append(words[i] + words[i+1])
            print(words[i] + words[i+1])
            i = i + 2
#         elif (words[i] + words[i+1])[:-1].lower() in syllable_set and (words[i] + words[i+1])[-1] in punctuation:
#             new_words.append(words[i] + words[i+1])
#             print(words[i] + words[i+1])
#             i = i + 2
#         elif (words[i][1:] + words[i+1]).lower() in syllable_set and words[i][0] in punctuation:
#             new_words.append(words[i] + words[i+1])
#             print(words[i] + words[i+1])
#             i = i + 2
        else:
            new_words.append(words[i])
            i = i+1

    new_text = " ".join(new_words)

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(new_text)

infolder = "clean"
outfolder = "cleanse"
files = os.listdir(infolder)

for file in files:
    norm_text(os.path.join(infolder, file), os.path.join(outfolder, file))
