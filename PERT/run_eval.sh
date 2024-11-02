
model='cn_tiny'
CUDA_VISIBLE_DEVICES='0' python py2wordPert.py \
   --charLex "./Corpus/cn/CharListFrmC4P.txt" \
   --pyLex "./Corpus/cn/pinyinList.txt" \
   --pinyin2PhrasePath "./Corpus/cn/ModernChineseLexicon4PinyinMapping.txt" \
   --bigramModelPath "./Models/Bigram/Bigram_cn.json" \
   --modelPath "./Models/$model" \
   --charFile "./Corpus/cn/train_texts_CharSeg_1k.txt" \
   --pinyinFile "./Corpus/cn/train_texts_pinyin_1k.txt" \
   --conversionRsltFile "./result/cn_tiny_rslt.txt" \
   --logFile "./result/cn_tiny_log.txt"

