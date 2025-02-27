import unicodedata



class Thai_Converter:
    def __init__(self):
        self.en_th = {'`': '-', '~': '%', '1': 'ๅ', '!': '+', '2': '/', '@': '๑', '3': '_', '#': '๒', '4': 'ภ', '$': '๓',
          '5': 'ถ', '%': '๔', '6': 'ุ', '^': 'ู', '7': 'ึ', '&': '฿', '8': 'ค', '*': '๕', '9': 'ต', '(': '๖', 
          '0': 'จ', ')': '๗', '-': 'ข', '_': '๘', '=': 'ช', '+': '๙', 'q': 'ๆ', 'Q': '๐', 'w': 'ไ', 'W': '"',
          'e': 'ำ', 'E': 'ฎ', 'r': 'พ', 'R': 'ฑ', 't': 'ะ', 'T': 'ธ', 'y': 'ั', 'Y': 'ํ', 'u': 'ี', 'U': '๊',
          'i': 'ร', 'I': 'ณ', 'o': 'น', 'O': 'ฯ', 'p': 'ย', 'P': 'ญ', '[': 'บ', '{': 'ฐ', ']': 'ล', '}': ',',
          '\\': 'ฃ', '|': 'ฅ', 'a': 'ฟ', 'A': 'ฤ', 's': 'ห', 'S': 'ฆ', 'd': 'ก', 'D': 'ฏ', 'f': 'ด','F': 'โ',
          'g': 'เ', 'G': 'ฌ', 'h': '้', 'H': '็', 'j': '่', 'J': '๋', 'k': 'า', 'K': 'ษ', 'l': 'ส', 'L': 'ศ',';': 'ว',
          ':': 'ซ', "'": 'ง', '"': '.', 'z': 'ผ', 'Z': '(', 'x': 'ป', 'X': ')', 'c': 'แ','C': 'ฉ', 'v': 'อ', 'V': 'ฮ', 
          'b': 'ิ', 'B': 'ฺ', 'n': 'ื', 'N': '์', 'm': 'ท', 'M': '?', ',': 'ม', '<': 'ฒ', '.': 'ใ', '>': 'ฬ', '/': 'ฝ', '?': 'ฦ'}

        self.th_en = {value: key for key, value in self.en_th.items()}

    def decompose_diacritics(self, text):
        decomposed_text = unicodedata.normalize('NFD', text)
        return decomposed_text

    def combine_diacritics(self, text):
        combined_text = unicodedata.normalize('NFC', text)
        return combined_text

    def convert(self, key_input):
        ''' [th_en] '''
        key_input = self.decompose_diacritics(key_input)
        result = []
        for char in key_input:
            mapped_char = self.th_en.get(char, char)
            result.append(mapped_char)
        target = ''.join(result)
        target = unicodedata.normalize('NFC', target)

        return target

    def reverse_convert(self, key_input):
        ''' [en_th] '''
        key_input = unicodedata.normalize('NFC', key_input)
        result = []
        for char in key_input:
            mapped_char = self.en_th.get(char, char)
            result.append(mapped_char)
        target = ''.join(result)
        target = self.combine_diacritics(target)

        return target

''' [TEST] '''
# converter = Thai_Converter()
# english_input = ';yoouhvkdkLfu,kd'
# thai_output = converter.reverse_convert(english_input)
# print(f"English Input: {english_input}")
# print(f"Thai Output: {thai_output}")

# # Convert Thai text to English key inputs
# english_output = converter.convert(thai_output)
# print(f"Thai Input: {thai_output}")
# print(f"English Output: {english_output}")
''' [TEST] '''