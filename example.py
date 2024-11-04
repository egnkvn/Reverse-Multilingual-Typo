from RMT.model import Model
from RMT.converter.ko import Korean_Converter
import time
# create model
RMT_model = Model()
RMT_model.model.to('cuda')

# Example inputs 오늘날씨가좋다 (今天天氣真好), convert them into keyboard typing
ko_converter = Korean_Converter()
encode_ = ko_converter.convert('오늘날씨가좋다')

# check the execution time
start_time = time.perf_counter()

# convert the input into correct sentence
correct_sentence = RMT_model.generate(encode_)

end_time = time.perf_counter()

execution_time = end_time - start_time

print(f"Original input: {encode_}")
print(f"Correct sentence: {correct_sentence}")
print(f"Execution time: {execution_time}")



