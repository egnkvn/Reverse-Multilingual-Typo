import json
from transformers import T5Tokenizer
import matplotlib.pyplot as plt
import seaborn as sns

def check_EM(json_file):
		with open(json_file, 'r') as f:
				data = json.load(f)

		correct = 0
		total = 0
		for item in data["results"]:
				target_text = item["target"]
				generated_text = item["generated"]
				
				target_prefix = target_text.split("[SEP]")[0].strip()
				generated_prefix = generated_text.split("[SEP]")[0].strip()
				
				if target_prefix == generated_prefix:
						correct += 1
				total += 1
		return correct / total


tokenizer = T5Tokenizer.from_pretrained("t5-base")

def check_differences_by_token_length(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # 初始化分组字典，每个区间为 10
    length_groups = {f"{i}-{i+9}": [0, 0] for i in range(0, 101, 10)}

    for item in data["results"]:
        target_text = item["target"]
        generated_text = item["generated"]

        target_tokens = tokenizer.encode(target_text, add_special_tokens=False)
        target_length = len(target_tokens)
        
        length_range = f"{(target_length // 10) * 10}-{((target_length // 10) * 10) + 9}"
        if length_range not in length_groups:
            length_groups[length_range] = [0, 0]

        target_prefix = target_text.split("[SEP]")[0].strip()
        generated_prefix = generated_text.split("[SEP]")[0].strip()
        target_last_word = target_prefix.split()[-1]
        generated_last_word = generated_prefix.split()[-1]

        if target_last_word != generated_last_word:
            length_groups[length_range][0] += 1  # difference count
        length_groups[length_range][1] += 1  # total count

    results = {length_range: difference / total 
               for length_range, (difference, total) in length_groups.items() 
               if total > 0}

    return results


json_file = "results.json" 
results = check_differences_by_token_length(json_file)

length_ranges = list(results.keys())
difference_ratios = list(results.values())

plt.figure(figsize=(12, 6))
sns.barplot(x=length_ranges, y=difference_ratios, palette="viridis")

plt.title("Difference/Total Ratio by Token Length Range")
plt.xlabel("Token Length Range")
plt.ylabel("Difference/Total Ratio")

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('differences_by_token_length.png')
print("Chart saved as 'differences_by_token_length.png'")
plt.show()