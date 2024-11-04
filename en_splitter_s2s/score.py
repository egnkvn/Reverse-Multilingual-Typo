import json

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

def check_differences(json_file):
  with open(json_file, 'r') as f:
    data = json.load(f)
  
  difference = 0
  total = 0
  for item in data["results"]:
    target_text = item["target"]
    generated_text = item["generated"]
    
    target_prefix = target_text.split("[SEP]")[0].strip()
    generated_prefix = generated_text.split("[SEP]")[0].strip()
    target_last_word = target_prefix.split()[-1]
    generated_last_word = generated_prefix.split()[-1]

    difference_count = sum(1 for a, b in zip(target_last_word, generated_last_word) if a != b)
    difference_count += abs(len(target_last_word) - len(generated_last_word))
    difference += difference_count
    total += 1
  return difference / total
    

json_file = "results.json"
print(f"EM score: {check_EM(json_file):4f}")
print(f"Avg_alphabet_diff: {check_differences(json_file):4f}")
