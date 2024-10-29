
CUDA_VISIBLE_DEVICES='0' python py2wordPert.py \
   --charLex "./Corpus/CharListFrmC4P.txt" \
   --pyLex "./Corpus/pinyinList.txt" \
   --pinyin2PhrasePath "./Corpus/ModernChineseLexicon4PinyinMapping.txt" \
   --bigramModelPath "./Models/Bigram/Bigram_CharListFrmC4P.json" \
   --modelPath "./Models/test/" \
   --charFile "./Corpus/train_texts_CharSeg_1k.txt" \
   --pinyinFile "./Corpus/train_texts_pinyin_1k.txt" \
   --conversionRsltFile "./result/conversionRslt.txt" \
   --logFile "./result/logFile.txt"

