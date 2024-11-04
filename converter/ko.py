class Korean_Converter:
    def __init__(self):

        self.en_ko = {
            '`': '₩',
            'q': 'ㅂ', 'w': 'ㅈ', 'e': 'ㄷ', 'r': 'ㄱ', 't': 'ㅅ', 'y': 'ㅛ',
            'u': 'ㅕ', 'i': 'ㅑ', 'o': 'ㅐ', 'p': 'ㅔ',
            'a': 'ㅁ', 's': 'ㄴ', 'd': 'ㅇ', 'f': 'ㄹ', 'g': 'ㅎ', 'h': 'ㅗ',
            'j': 'ㅓ', 'k': 'ㅏ', 'l': 'ㅣ',
            'z': 'ㅋ', 'x': 'ㅌ', 'c': 'ㅊ', 'v': 'ㅍ', 'b': 'ㅠ', 'n': 'ㅜ',
            'm': 'ㅡ',
            # Shift
            'Q': 'ㅃ', 'W': 'ㅉ', 'E': 'ㄸ', 'R': 'ㄲ', 'T': 'ㅆ',
            'O': 'ㅒ', 'P': 'ㅖ'
        }

        self.ko_en = {value: key for key, value in self.en_ko.items()}

        self.initial_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
                             'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ',
                             'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        self.vowel_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ',
                           'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ',
                           'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        self.final_list = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ',
                           'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ',
                           'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
                           'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

        self.double_jamos = {
            'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ',
            'ㅜㅓ': 'ㅝ', 'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ',
            'ㅡㅣ': 'ㅢ',
            'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ',
            'ㄹㄱ': 'ㄺ', 'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ',
            'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ', 'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ',
            'ㅂㅅ': 'ㅄ'
        }

        self.double_jamos_rev = {v: k for k, v in self.double_jamos.items()}

    def is_initial_consonant(self, char):
        return char in self.initial_list

    def is_vowel(self, char):
        return char in self.vowel_list

    def is_final_consonant(self, char):
        return char in self.final_list and char != ''

    def is_hangul_syllable(self, char):
        return 0xAC00 <= ord(char) <= 0xD7A3

    def compose_syllable(self, initial, vowel, final=''):
        try:
            initial_index = self.initial_list.index(initial)
            vowel_index = self.vowel_list.index(vowel)
            final_index = self.final_list.index(final)
        except ValueError:
            return initial + vowel + final

        syllable_code = 0xAC00 + (initial_index * 21 * 28) + (vowel_index * 28) + final_index
        return chr(syllable_code)

    def decompose_syllable(self, syllable):
        code = ord(syllable) - 0xAC00
        initial_index = code // (21 * 28)
        vowel_index = (code % (21 * 28)) // 28
        final_index = code % 28

        initial = self.initial_list[initial_index]
        vowel = self.vowel_list[vowel_index]
        final = self.final_list[final_index]
        return initial, vowel, final

    def decompose_complex_jamo(self, jamo):
        if jamo in self.double_jamos_rev:
            return list(self.double_jamos_rev[jamo])
        else:
            return [jamo]

    def compose_complex_jamo(self, jamo_list):
        composed = []
        i = 0
        while i < len(jamo_list):
            if i + 1 < len(jamo_list):
                pair = jamo_list[i] + jamo_list[i + 1]
                if pair in self.double_jamos:
                    composed.append(self.double_jamos[pair])
                    i += 2
                    continue
            composed.append(jamo_list[i])
            i += 1
        return composed

    def compose(self, jamo_list):
        jamo_list = self.compose_complex_jamo(jamo_list)
        syllables = []
        i = 0
        while i < len(jamo_list):
            if not self.is_initial_consonant(jamo_list[i]) and not self.is_vowel(jamo_list[i]) and not self.is_final_consonant(jamo_list):
                syllables.append(jamo_list[i])
                i += 1
            initial = ''
            vowel = ''
            final = ''
            if self.is_initial_consonant(jamo_list[i]):
                initial = jamo_list[i]
                i += 1
            if i < len(jamo_list) and self.is_vowel(jamo_list[i]):
                vowel = jamo_list[i]
                i += 1
            
            if i < len(jamo_list) and self.is_final_consonant(jamo_list[i]):
                possible_final = jamo_list[i]
                i += 1
                # Check next jamo whether vowel
                if self.is_vowel(jamo_list[i]):
                    if possible_final in self.double_jamos.values():
                        i -= 1
                        jamo_list.pop(i)
                        jamo_list.insert(i, self.double_jamos_rev[possible_final][1])
                        final = self.double_jamos_rev[possible_final][0]
                    else:
                        i -= 1
                else:
                    final = possible_final

            syllable = self.compose_syllable(initial, vowel, final)
            syllables.append(syllable)

        return ''.join(syllables)

    def decompose(self, syllable_str):
        jamo_list = []
        for char in syllable_str:
            if self.is_hangul_syllable(char):
                initial, vowel, final = self.decompose_syllable(char)
                # 分解复合元音和收音
                vowel_parts = self.decompose_complex_jamo(vowel)
                jamo_list.append(initial)
                jamo_list.extend(vowel_parts)
                if final:
                    final_parts = self.decompose_complex_jamo(final)
                    jamo_list.extend(final_parts)
            else:
                jamo_list.append(char)
        return jamo_list

    def convert(self, key_input):
        ''' [ko_en] '''
        jamo_list = self.decompose(key_input)
        mapped_chars = [self.ko_en[jamo] if jamo in self.ko_en else jamo for jamo in jamo_list]
        result = ''.join(mapped_chars)
        
        return result
    
    def reverse_convert(self, key_input):
        ''' [en_ko] '''
        mapped_chars = [self.en_ko[char] if char in self.en_ko else char for char in key_input]
        result = self.compose(mapped_chars)
        
        return result

''' [TEST] '''
# converter = Korean_Converter()
# korean_input = '웏왹서'
# # korean_input = '내일은 볶음밥 먹고싶다'
# english_output = converter.convert(korean_input)
# print(f"korean_input: {korean_input}")
# print(f"english_output: {english_output}") 

# korean_output = converter.reverse_convert('su3cl3ji32k7au/6y4rul4')
# print(f"korean_output: {korean_output}") 
''' [TEST] '''