from pypinyin import pinyin, Style

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

class Zhuyin_Converter:
    def __init__(self):
        pass
    
    def convert(self, key_input, map_dict):
        result = []

        if map_dict == zhuyin_en:
            zhuyin = [i[0] for i in pinyin(key_input, style=Style.BOPOMOFO)]
            key_input = ''.join(zhuyin)
            # print(pinyin(key_input, style=Style.BOPOMOFO))
        
        for char in key_input:
            mapped_char = map_dict.get(char, char)
            result.append(mapped_char)
        
        target = ''.join(result)

        return target

''' [TEST] '''
# converter = Zhuyin_Converter()

# zhuyin_input = '這好爛喔'
# english_output = converter.convert(zhuyin_input, zhuyin_en)
# print(f"注音输入: {zhuyin_input}")
# print(f"英文输出: {english_output}")

# zhuyin_output = converter.convert(english_output, en_zhuyin)
# print(f"英文输入: {english_output}")
# print(f"注音输出: {zhuyin_output}")
''' [TEST] '''