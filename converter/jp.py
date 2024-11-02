import jaconv
import fugashi 



class Japan_Converter:
    def __init__(self):
        self.tagger = fugashi.Tagger()
        self.en_jp = {
            '1': 'ぬ', '2': 'ふ', '3': 'あ', '4': 'う', '5': 'え', '6': 'お', '7': 'や', '8': 'ゆ', '9': 'よ', '0': 'わ', '-': 'ほ', '=': '゜',
            'q': 'た', 'w': 'て', 'e': 'い', 'r': 'す', 't': 'か', 'y': 'ん', 'u': 'な', 'i': 'に', 'o': 'ら', 'p': 'せ', '[': '゛', ']': 'む', '\\': 'へ',
            'a': 'ち', 's': 'と', 'd': 'し', 'f': 'は', 'g': 'き', 'h': 'く', 'j': 'ま', 'k': 'の', 'l': 'り', ';': 'れ', "'": 'け',
            'z': 'つ', 'x': 'さ', 'c': 'そ', 'v': 'ひ', 'b': 'こ', 'n': 'み', 'm': 'も', ',': 'ね', '.': 'る', '/': 'め',
            # Shift
            '#': 'ぁ', 'E': 'ぃ', '$': 'ぅ', '%': 'ぇ', '^': 'ぉ', '&': 'ゃ', '*': 'ゅ', '(': 'ょ', 
            'Z': 'っ', ')': 'を', '<': '、','>': '。','?': '・','{': '」','"': 'ろ','+': '「','}': 'ー',
        }
        self.jp_en = {value: key for key, value in self.en_jp.items()}

    def decompose_diacritics(self, text):
        result = []
        for char in text:
            # Decompose voiced characters
            if char in 'がぎぐげござじずぜぞだぢづでどばびぶべぼ':
                result.append(chr(ord(char) - 1) + '゛')
            elif char in 'ぱぴぷぺぽ':
                result.append(chr(ord(char) - 2) + '゜')
            else:
                result.append(char)
        return ''.join(result)
    
    def combine_diacritics(self, text):
        result = []
        skip_next = False
        
        for i in range(len(text)):
            if skip_next:
                skip_next = False
                continue
            char = text[i]
            if i + 1 < len(text) and text[i + 1] in ['゛', '゜']:
                if text[i + 1] == '゛' and char in 'かきくけこさしすせそたちつてとはひふへほ':
                    result.append(chr(ord(char) + 1))
                elif text[i + 1] == '゜' and char in 'はひふへほ':
                    result.append(chr(ord(char) + 2))
                skip_next = True
            else:
                result.append(char)
        return ''.join(result)
    
    def Hiragana(self, text):
        text = jaconv.kata2hira(text)
        result = []
        for word in self.tagger(text):
            if word.surface in ['。', '、']:
                result.append(word.surface) 
            elif word.feature.kana:
                hiragana_word = jaconv.kata2hira(word.feature.kana)
                result.append(self.decompose_diacritics(hiragana_word))
            else:
                result.append(word.surface)
        return ''.join(result)

    def convert(self, key_input, map_dict):

        if map_dict == "jp_en":
            selected_dict = self.jp_en
        elif map_dict == "en_jp":
            selected_dict = self.en_jp

        if map_dict == "jp_en":  
          key_input = self.Hiragana(key_input)
        target = ''.join(selected_dict[char] if char in selected_dict else char for char in key_input)
        if map_dict == "en_jp":
            target = self.combine_diacritics(target)
        return target

''' [TEST] '''
# converter = Japan_Converter()
# text = '意味のない部分を。'
# en_output = converter.convert(text, "jp_en")
# print(en_output)
# jp_output = converter.convert(en_output, "en_jp")
# print(jp_output)
# print('=================')
# print(text)
''' [TEST] '''