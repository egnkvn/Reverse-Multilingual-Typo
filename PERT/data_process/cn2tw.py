import opencc

converter = opencc.OpenCC('s2t.json')

input_file = "../Corpus/cn/train_texts_CharSeg_1k.txt"
output_file = "../Corpus/tw/train_texts_CharSeg_1k.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [converter.convert(line.strip()) for line in f if line.strip()]

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        f.write(f"{line}\n")

print(f"Converted text saved to {output_file}")