CUDA_VISIBLE_DEVICES='0' python Trainer.py \
   --vocab "./Corpus/cn/CharListFrmC4P.txt" \
   --pyLex "./Corpus/cn/pinyinList.txt" \
   --chardata "./Corpus/cn/train_texts_CharSeg_1k.txt" \
   --pinyindata "./Corpus/cn/train_texts_pinyin_1k.txt" \
   --num_loading_workers 0 \
   --prefetch_factor 1 \
   --bert_config "./Configs/bert_config_tiny_nezha_py.json" \
   --train_batch_size 2048 \
   --seq_length 16 \
   --num_epochs 20 \
   --continue_train_index 0 \
   --save "./Models/cn_tiny/" \
   --save_per_n_epoches 1 \
   # > "./Logs/Training_pert_tiny_py_lr5e4_2kBs_10e_log.txt" 2>&1 &