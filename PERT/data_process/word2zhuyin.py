from pypinyin import pinyin, Style
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from converter.zy import Zhuyin_Converter


input_file = "../Corpus/tw/train_texts_CharSeg_1k.txt"
output_file = "../Corpus/tw/train_texts_zhuyin_1k.txt"

converter = Zhuyin_Converter()

with open(input_file, "r", encoding="utf-8") as f:
    lines = [converter.convert(line.strip(), "zhuyin_en") for line in f if line.strip()]

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(f"{line}\n")

print(f"Converted text saved to {output_file}")