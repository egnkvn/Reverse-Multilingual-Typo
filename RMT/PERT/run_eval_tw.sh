
model='tw_tiny'
CUDA_VISIBLE_DEVICES='0' python py2wordPert.py \
   --charLex "./Corpus/cn/CharListFrmC4P.txt" \
   --pyLex "./Corpus/tw/zhuyinList.txt" \
   --pinyin2PhrasePath "./Corpus/tw/ModernChineseLexicon4ZhuyinMapping.txt" \
   --bigramModelPath "./Models/Bigram/Bigram_cn.json" \
   --modelPath "./Models/$model" \
   --charFile "./Corpus/cn/train_texts_CharSeg_1k.txt" \
   --pinyinFile "./Corpus/tw/train_texts_zhuyin_1k.txt" \
   --conversionRsltFile "./result/tw_tiny_rslt.txt" \
   --logFile "./result/tw_tiny_log.txt"

