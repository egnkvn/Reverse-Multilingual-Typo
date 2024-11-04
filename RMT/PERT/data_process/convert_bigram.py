import json
import opencc
from tqdm import tqdm

converter = opencc.OpenCC('s2t.json')

# 读取 JSON 文件
input_file = "../Models/Bigram/Bigram_cn.json"
output_file = "../Models/Bigram/Bigram_tw.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)
converted_data = []

converted_data.append({converter.convert(key): data[0][key] for key in data[0]})

converted_data2 = {}
for w in tqdm(data[1]):
    converted_data2[converter.convert(w)] = {converter.convert(key): data[1][w][key] for key in data[1][w]}

converted_data.append(converted_data2)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(converted_data, f, ensure_ascii=False)

print(f"Converted JSON saved to {output_file}")