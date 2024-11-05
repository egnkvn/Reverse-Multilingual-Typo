import json
from hanziconv import HanziConv

with open('result/tw_predict.json', 'r') as file:
    data = json.load(file)

total_chars = 0
correct_chars = 0

for item in data:
    gt_simplified = HanziConv.toSimplified(item["gt"])
    predict_text = item["predict"]
    
    for gt_char, predict_char in zip(gt_simplified, predict_text):
        if gt_char == predict_char:
            correct_chars += 1
        total_chars += 1

# 计算准确率
accuracy = correct_chars / total_chars if total_chars > 0 else 0
print(f"Accuracy: {accuracy:.2%}")