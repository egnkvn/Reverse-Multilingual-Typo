from RMT.converter.jp import Japan_Converter
from RMT.converter.ko import Korean_Converter
from RMT.converter.th import Thai_Converter
from RMT.converter.zy import Zhuyin_Converter
from transformers import MT5ForConditionalGeneration, T5Tokenizer
import torch.nn.functional as F
import torch
from transformers import logging
import RMT.PERT as PERT
import os
from RMT.PERT.py2wordPert import Py2WordPERT
from opencc import OpenCC
import re
from transformers import AutoTokenizer, AutoModelForMaskedLM
from transformers import pipeline
logging.set_verbosity_error()
class Model():
    def __init__(self, t5_model_name = "csebuetnlp/mT5_multilingual_XLSum", DEVICE = 'cuda', PERT_path = "/data2/enginekevin/Reverse-Multilingual-Typo/RMT/PERT/Models/tw_tiny"):
        self.converters = [Japan_Converter(), Korean_Converter(), Thai_Converter()]
        self.jp_converter = Japan_Converter()
        self.ko_converter = Korean_Converter()
        self.th_converter = Thai_Converter()
        self.zy_converter = Zhuyin_Converter()
        
        # loading llama model
        print("loading llama")

        model_name = "meta-llama/Llama-3.2-3B-Instruct"
        self.pipe = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        print("loading PERT model")
        # loading PERT model
        corpus_path = PERT.__file__.replace('/__init__.py', '')
        charLex_path = os.path.join(corpus_path, 'Corpus/cn/CharListFrmC4P.txt')
        pyLex_path = os.path.join(corpus_path, 'Corpus/tw/zhuyinList.txt')

        pinyin2PhrasePath = os.path.join(corpus_path, 'Corpus/tw/ModernChineseLexicon4ZhuyinMapping.txt')
        bigramModelPath = os.path.join(corpus_path, "Models/Bigram/Bigram_cn.json")

        charFile = os.path.join(corpus_path, 'Corpus/cn/train_texts_CharSeg_1k.txt')
        pinyinFile = os.path.join(corpus_path, 'Corpus/tw/train_texts_zhuyin_1k.txt')

        self.thePy2WordPERT = Py2WordPERT(
            charLexPath = charLex_path, 
            pyLexPath = pyLex_path, 
            pinyin2PhrasePath = pinyin2PhrasePath,
            phrase2CharPath = '', 
            bigramModelPath = bigramModelPath, 
            modelPath = PERT_path)
        
        self.cn2tw = OpenCC('s2tw')
        with open(pyLex_path, 'r') as file:
            self.available_zyin = {line.strip() for line in file}

    def generate(self, key_input):
        
        sentences = [converter.reverse_convert(key_input) for converter in self.converters ]

        tw_sentence = self.convert_tw(key_input)
        if tw_sentence != '':
            sentences.append(tw_sentence)

        labels = ['(A)', '(B)', '(C)', '(D)']
        formatted_output = "\n".join([f"{label}'{string}'" for label, string in zip(labels, sentences)])

        messages = [
            {"role": "system", "content": "You are a Language expert."},
            {"role": "user", "content": f"Which of following sentences is the most meaningful sentence ? Only give me the correct option. Don't explain it.\n{formatted_output}"},
        ]

        outputs = self.pipe(
            messages,
            max_new_tokens=256,    
            num_beams=1,     # Single beam for greedy decoding
            do_sample=False,
            temperature=None,
            top_p=None
        )

        answer = outputs[0]["generated_text"][-1]['content'][:3]

        for i in range(len(labels)):
            if answer == labels[i]:
                return sentences[i]
    
    def convert_tw(self, key_input):
        # Split by any of the characters ' ', '6', '3', '4', '7'
        result = re.split(r'(?<=[ 6347])', key_input)

        # Filter out any empty strings that may result from splitting
        zhuyins = []
        for s in result:
            clean_s = s.strip()
            if clean_s != '' and clean_s not in self.available_zyin:
                zhuyins = []
                return ''
            elif clean_s != '':
                zhuyins.append(clean_s)

        charList = self.thePy2WordPERT.ConvertPinyinListToCharList(zhuyins)
        inputs = self.cn2tw.convert(''.join(charList))
        return inputs
        # return ''.join(charList)