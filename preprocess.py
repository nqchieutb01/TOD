import random
import re
import json
import os
from multiprocessing import Process
import emoji
import unicodedata
consecutive_numbers = re.compile(r"\d{6,}")
email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
substring = "http|www|mua bán|đặt hàng"
sub_pattern = re.compile(r".*" + substring + ".*")
date_pattern= re.compile(r'.*\d{2}[-/]\d{2}[-/]\d{4}.*')

def check_contain_date(text):
    if date_pattern.match(text):
        return True
    else:
        return False

def text_has_emoji(text):
    for character in text:
        if emoji.is_emoji(character):
            return True
    return False

def check_consecutive_numbers(string):
  if consecutive_numbers.search(string):
    return True
  else:
    return False


def check_contain_email(string):
  if email_pattern.search(string):
    return True
  else:
    return False

def check_substring(string, substrings = ["http","www"]):
    if sub_pattern.search(string):
            return True
    if string.count('|') > 1 or string.count('»') > 1:
           return True 
    return False
    
def check_spell_error(string, error_rate=0.3 ,num_char=6):
    string = string.split()
    err = 0.0
    for word in string:
        if len(word)>=num_char:
           err+=1
    err_rate = err / float(len(string)+0.1)
    if err_rate >= error_rate:
       return True,err_rate
    return False, err_rate

def clean(string, debug_mode=False):
    string = unicodedata.normalize("NFC", string)
    string = string.split('\\n')
    err = 0
    final_result = []
    for id , line in enumerate(string):
        oriline = ''+ line
        line = line.lower()
        is_valid = True
        err += 1 
        if check_consecutive_numbers(line):
            is_valid = False 
        if check_contain_email(line) and is_valid:
            is_valid = False 
        if check_substring(line) and is_valid:
            is_valid = False 
        spell,_  = check_spell_error(line, error_rate=0.3 ,num_char=6)
        if spell:
            is_valid = False 
        if text_has_emoji(line) and is_valid:
            is_valid = False
        
        prob = random.random()
        if not is_valid and prob>= 0.75:
            if check_contain_date(line) and (id <=1 or id == len(string)-1):
                is_valid = True
        if is_valid:
            err -=1
            final_result.append(oriline)
        
        if not is_valid and debug_mode:
            print(line) 
    if err >= 2:
        final_result = []
    return '\n'.join(final_result)

from tqdm import tqdm
def process(infile, outfile):
    writer = open(outfile, "w", encoding="utf-8")

    with open(infile, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            data = json.loads(line.strip())
            doc = data["text"]
            new_doc = clean(doc).strip()
            
            if new_doc.count('.') > 3:
                tmp = dict()
                tmp["text"] = new_doc
                jout = json.dumps(tmp, ensure_ascii=False) + "\n"
                writer.write(jout)
    writer.close()
    
if __name__ == "__main__":
    infolder = "./"
    outfolder = "../cleanse_MADLAD_400"

    procs = []
    
    for i, file in enumerate(os.listdir(infolder)):
        if file[-1] =='l':
            proc = Process(target=process, args=(os.path.join(infolder, file), os.path.join(outfolder, file)))
            procs.append(proc)
            proc.start()
    # complete the processes
    for proc in procs:
        proc.join()
