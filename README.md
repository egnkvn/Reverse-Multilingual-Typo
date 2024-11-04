# Reverse-Multilingual-Typo

### Converter
* jp: 意味のない部分を。 -> **いみのないぶぶんを。** <==> **enkue2[2[y)>**
* th: **วันนี้อากาศดีมาก** <==> **yoouhvkdkLfu,kd**
* zy: **我好棒喔** -> **ㄨㄛˇㄏㄠˇㄅㄤˋㄛ** <==> **ji3cl31;4i**
* ko: **내일은 볶음밥 먹고싶다** <==> **sodlfdms qhRdmaqkq ajrrhtlvek**

## Usage
### First install the model
```
pip install -e .
```
### Loading the model and call generate function
```
from RMT.model import Model
RMT_model = Model()
RMT_model.model.to('cuda')
correct_sentence = RMT_model.generate(key_input)
```
You can see example.py.
