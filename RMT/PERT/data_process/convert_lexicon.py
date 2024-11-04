from pypinyin import pinyin, Style
import sys
from tqdm import tqdm
import os

en_zhuyin = {
            '1': 'ㄅ', '2': 'ㄉ', '3': 'ˇ', '4': 'ˋ', '5': 'ㄓ', '6': 'ˊ', '7': '˙', '8': 'ㄚ', '9': 'ㄞ', '0': 'ㄢ', '-': 'ㄦ', '=': '＝',
            'q': 'ㄆ', 'w': 'ㄊ', 'e': 'ㄍ', 'r': 'ㄐ', 't': 'ㄔ', 'y': 'ㄗ', 'u': 'ㄧ', 'i': 'ㄛ', 'o': 'ㄟ', 'p': 'ㄣ', '[': '「', ']': '」',
            'a': 'ㄇ', 's': 'ㄋ', 'd': 'ㄎ', 'f': 'ㄑ', 'g': 'ㄕ', 'h': 'ㄘ', 'j': 'ㄨ', 'k': 'ㄜ', 'l': 'ㄠ', ';': 'ㄤ', '\'': '‘',
            'z': 'ㄈ', 'x': 'ㄌ', 'c': 'ㄏ', 'v': 'ㄒ', 'b': 'ㄖ', 'n': 'ㄙ', 'm': 'ㄩ', ',': 'ㄝ', '.': 'ㄡ', '/': 'ㄥ', '`': '－', '\\': '、', 
            # Shift
            '~': '～', '!': '！', '@': '＠', '#': '＃', '$': '＄', '%': '％', '^': '＾', '&': '＆', '*': '＊', '(': '（', ')': '）', '_': '＿', '+': '＋',
            '{': '『', '}': '』', '|': '｜', ':': '：', '"': '“', '<': '，', '>': '。', '?': '？'
        }
zhuyin_en = {value: key for key, value in en_zhuyin.items()}


input_file = "../Corpus/cn/ModernChineseLexicon4PinyinMapping.txt"
output_file = "../Corpus/tw/ModernChineseLexicon4ZhuyinMapping.txt"

zhuyin_dict = {}

def add_to_zhuyin_dict(characters):

    for char in characters:
        # char = tw_converter.convert(char)
        if len(char) == 1:
          zhuyin_list = pinyin(char, style=Style.BOPOMOFO, heteronym=True)
          for zhuyin_options in zhuyin_list:
              for zhuyin in zhuyin_options:
                  result = []
                  for z in zhuyin:
                    result.append(zhuyin_en.get(z, z))
                  result = ''.join(result)

                  if result not in zhuyin_dict:
                      zhuyin_dict[result] = []
                  
                  if char not in zhuyin_dict[result]:
                      zhuyin_dict[result].append(char)
        else:
          zhuyin_list = pinyin(char, style=Style.BOPOMOFO)
          
          result = []
          for zhuyin_options in zhuyin_list:
              
              for zhuyin in zhuyin_options:
                  for z in zhuyin:
                    result.append(zhuyin_en.get(z, z))
          result = ''.join(result)

          if result not in zhuyin_dict:
              zhuyin_dict[result] = []
          
          if char not in zhuyin_dict[result]:
              zhuyin_dict[result].append(char)

with open(input_file, "r", encoding="utf-8") as f:
    for line in tqdm(f):
        
        line = line.strip()
        if not line:
            continue

        parts = line.split(" ", 1)
        c = parts[1]

        character_list = c.split(" ")
        add_to_zhuyin_dict(character_list)


with open(output_file, "w", encoding="utf-8") as f:
    for zhuyin_key in zhuyin_dict:
        characters = zhuyin_dict[zhuyin_key]
        line = zhuyin_key + ' ' + ' '.join(characters)
        f.write(line + '\n')

print(f"Converted txt saved to {output_file}")