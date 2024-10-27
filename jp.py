import jaconv
import fugashi 

en_jp = {
    '1': 'ぬ', '2': 'ふ', '3': 'あ', '4': 'う', '5': 'え', '6': 'お', '7': 'や', '8': 'ゆ', '9': 'よ', '0': 'わ', '-': 'ほ', '=': '゜',
    'q': 'た', 'w': 'て', 'e': 'い', 'r': 'す', 't': 'か', 'y': 'ん', 'u': 'な', 'i': 'に', 'o': 'ら', 'p': 'せ', '[': '゛', ']': 'む', '\\': 'へ',
    'a': 'ち', 's': 'と', 'd': 'し', 'f': 'は', 'g': 'き', 'h': 'く', 'j': 'ま', 'k': 'の', 'l': 'り', ';': 'れ', "'": 'け',
    'z': 'つ', 'x': 'さ', 'c': 'そ', 'v': 'ひ', 'b': 'こ', 'n': 'み', 'm': 'も', ',': 'ね', '.': 'る', '/': 'め',
    # Shift
    '#': 'ぁ', 'E': 'ぃ', '$': 'ぅ', '%': 'ぇ', '^': 'ぉ', '&': 'ゃ', '*': 'ゅ', '(': 'ょ', 
    'Z': 'っ', ')': 'を', '<': '、','>': '。','?': '・','{': '」','"': 'ろ','+': '「','}': 'ー',
}
jp_en = {'ぬ': '1', 'ふ': '2', 'あ': '3', 'う': '4', 'え': '5', 'お': '6', 'や': '7', 'ゆ': '8', 'よ': '9', 'わ': '0', 'ほ': '-', '゜': '=', 
         'た': 'q', 'て': 'w', 'い': 'e', 'す': 'r', 'か': 't', 'ん': 'y', 'な': 'u', 'に': 'i', 'ら': 'o', 'せ': 'p', '゛': '[', 'む': ']', 
         'へ': '\\', 'ち': 'a', 'と': 's', 'し': 'd', 'は': 'f', 'き': 'g', 'く': 'h', 'ま': 'j', 'の': 'k', 'り': 'l', 'れ': ';', 'け': "'", 
         'つ': 'z', 'さ': 'x', 'そ': 'c', 'ひ': 'v', 'こ': 'b', 'み': 'n', 'も': 'm', 'ね': ',', 'る': '.', 'め': '/', 'ぁ': '#', 'ぃ': 'E', 
         'ぅ': '$', 'ぇ': '%', 'ぉ': '^', 'ゃ': '&', 'ゅ': '*', 'ょ': '(', 'っ': 'Z', 'を': ')', '、': '<', '。': '>', '・': '?', '」': '{', 
         'ろ': '"', '「': '+', 'ー': '}'
}

class Japan_Convert:
    def __init__(self):
        self.tagger = fugashi.Tagger()

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
        if map_dict == jp_en:  
          key_input = self.Hiragana(key_input)
        target = ''.join(map_dict[char] if char in map_dict else char for char in key_input)
        if map_dict == en_jp:
            target = self.combine_diacritics(target)
        return target

''' [DEBUG] '''
# converter = Japan_Convert()
# text = '意味のない部分を、他のパッケージや方法を使って意味のある現象として表現してください。'
# en_output = converter.convert(text, jp_en)
# print(en_output)
# jp_output = converter.convert(en_output, en_jp)
# print(jp_output)
# print('=================')
# print(text)
''' [DEBUG] '''