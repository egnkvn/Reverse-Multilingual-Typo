from pypinyin import pinyin, Style


class Zhuyin_Converter:
    def __init__(self):
        self.en_zhuyin = {
            '1': 'ㄅ', '2': 'ㄉ', '3': 'ˇ', '4': 'ˋ', '5': 'ㄓ', '6': 'ˊ', '7': '˙', '8': 'ㄚ', '9': 'ㄞ', '0': 'ㄢ', '-': 'ㄦ', '=': '＝',
            'q': 'ㄆ', 'w': 'ㄊ', 'e': 'ㄍ', 'r': 'ㄐ', 't': 'ㄔ', 'y': 'ㄗ', 'u': 'ㄧ', 'i': 'ㄛ', 'o': 'ㄟ', 'p': 'ㄣ', '[': '「', ']': '」',
            'a': 'ㄇ', 's': 'ㄋ', 'd': 'ㄎ', 'f': 'ㄑ', 'g': 'ㄕ', 'h': 'ㄘ', 'j': 'ㄨ', 'k': 'ㄜ', 'l': 'ㄠ', ';': 'ㄤ', '\'': '‘',
            'z': 'ㄈ', 'x': 'ㄌ', 'c': 'ㄏ', 'v': 'ㄒ', 'b': 'ㄖ', 'n': 'ㄙ', 'm': 'ㄩ', ',': 'ㄝ', '.': 'ㄡ', '/': 'ㄥ', '`': '－', '\\': '、', ' ':' ',
            # Shift
            '~': '～', '!': '！', '@': '＠', '#': '＃', '$': '＄', '%': '％', '^': '＾', '&': '＆', '*': '＊', '(': '（', ')': '）', '_': '＿', '+': '＋',
            '{': '『', '}': '』', '|': '｜', ':': '：', '"': '“', '<': '，', '>': '。', '?': '？'
        }
        self.zhuyin_en = {value: key for key, value in self.en_zhuyin.items()}
    
    def convert(self, key_input):
        ''' [zy_en] '''
        result = []
        zhuyin = []
        tones = [' ', 'ˊ', 'ˇ', 'ˋ', '˙']
        for i in pinyin(key_input, style=Style.BOPOMOFO):
            if i[0][-1] not in tones:
                i[0] = i[0] + ' '
            zhuyin.append(i[0])
        # zhuyin = [i[0] for i in pinyin(key_input, style=Style.BOPOMOFO)]
        key_input = ''.join(zhuyin)

        for char in key_input:
            mapped_char = self.zhuyin_en.get(char, char)
            result.append(mapped_char)
        target = ''.join(result)

        return target
    
    def reverse_convert(self, key_input):
        ''' [en_zy] '''
        result = []
        for char in key_input:
            mapped_char = self.en_zhuyin.get(char, char)
            result.append(mapped_char)
        target = ''.join(result)

        return target

''' [TEST] '''
# converter = Zhuyin_Converter()

# zhuyin_input = '我好棒喔'
# english_output = converter.convert(zhuyin_input)
# print(f"中文输入: {zhuyin_input}")
# print(f"英文输出: {english_output}")

# zhuyin_output = converter.reverse_convert(english_output)
# print(f"英文输入: {english_output}")
# print(f"注音输出: {zhuyin_output}")
''' [TEST] '''
