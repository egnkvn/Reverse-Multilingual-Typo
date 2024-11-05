from RMT.model import Model
from RMT.converter.ko import Korean_Converter
from RMT.converter.th import Thai_Converter
from RMT.converter.jp import Japan_Converter
import time
# create model
RMT_model = Model()
# RMT_model.model.to('cuda')
RMT_model.thePy2WordPERT.model.to('cuda')

# Example input (convert the original strings to english encoding)
ko_converter = Korean_Converter()
th_converter = Thai_Converter()
jp_converter = Japan_Converter()

encode_ = jp_converter.convert('靴を買いたいのですが、お金がありません。どうすればいいですか')
# encode_ = ko_converter.convert('오늘날씨가좋다')
# encode_ = 'ji35jp31o4ul4cjo6ru8 xk7'
# encode_ = 'rup wu0 wu0 fu45p cl3'
# encode_ = 'ji3vu;3ul4fm4a93vu,6'
# encode_ = th_converter.convert('ฉันชอบวิ่งเล่นในสนามเด็กเล่น')

# check the execution time
start_time = time.perf_counter()

# convert the input into correct sentence
correct_sentence = RMT_model.generate(encode_)

end_time = time.perf_counter()

execution_time = end_time - start_time

print(f"Original input: {encode_}")
print(f"Correct sentence: {correct_sentence}")
print(f"Execution time: {execution_time}")



