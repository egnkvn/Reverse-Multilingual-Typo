from converter.jp import Japan_Converter
from converter.ko import Korean_Converter
from converter.th import Thai_Converter
from converter.zy import Zhuyin_Converter

class Model():
    def __init__(self):
        self.jp_converter = Japan_Converter()
        self.ko_converter = Korean_Converter()
        self.th_converter = Thai_Converter()
        self.zy_converter = Zhuyin_Converter()
        