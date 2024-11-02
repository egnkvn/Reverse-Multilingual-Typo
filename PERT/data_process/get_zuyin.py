from pypinyin import pinyin, Style
import sys
from tqdm import tqdm
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from converter.zy import Zhuyin_Converter

converter = Zhuyin_Converter()

start = int('4E00', 16)
end = int('9FA5', 16)  

zhuyin_set = []

for code_point in tqdm(range(start, end + 1)):
    char = chr(code_point)
    zhuyin = converter.convert(char, "zhuyin_en")
    if zhuyin not in zhuyin_set:
        zhuyin_set.append(zhuyin)
    
output_file = "../Corpus/tw/zhuyinList.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for item in zhuyin_set:
        f.write(f"{item}\n")

print(f"Zhuyin list saved to {output_file}")