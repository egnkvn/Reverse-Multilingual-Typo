from RMT.converter.jp import Japan_Converter
from RMT.converter.ko import Korean_Converter
from RMT.converter.th import Thai_Converter
from RMT.converter.zy import Zhuyin_Converter
from transformers import MT5ForConditionalGeneration, T5Tokenizer
import torch.nn.functional as F
import torch
from transformers import logging
logging.set_verbosity_error()
class Model():
    def __init__(self, model_name = "google/mt5-base", DEVICE = 'cuda'):
        self.converters = [Japan_Converter(), Korean_Converter(), Thai_Converter(), Zhuyin_Converter()]
        self.jp_converter = Japan_Converter()
        self.ko_converter = Korean_Converter()
        self.th_converter = Thai_Converter()
        self.zy_converter = Zhuyin_Converter()
        # self.llm_filter = LLM_filter()
        print("loading t5 model")
        self.model = MT5ForConditionalGeneration.from_pretrained(model_name)
        self.model.eval()
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.DEVICE = DEVICE

    def generate(self, key_input):

        # sentences = self.convert_sentences(key_input, self.jp_converter, self.ko_converter, self.th_converter, self.zy_converter)
        # print(sentences)
        sentences = []
        for converter in self.converters:
            sentences.append(converter.reverse_convert(key_input))
        # jp_sentence = self.jp_converter.reverse_convert(key_input)
        # ko_sentence = self.ko_converter.reverse_convert(key_input)
        # th_sentence = self.th_converter.reverse_convert(key_input)
        # zy_sentence = self.zy_converter.reverse_convert(key_input)
        # output = self.llm_filter.choose(sentences)

        correct_sentence = self.choose(sentences)
        return correct_sentence

    def choose(self, input_texts):
        # input_texts: should be a list of strings
        # get logits
        inputs = self.tokenizer(input_texts, return_tensors="pt", padding=True, truncation=True, max_length = 1024)

        input_ids = inputs.input_ids.to(self.DEVICE)

        attention_mask = inputs.attention_mask.to(self.DEVICE)

        outputs = self.model(input_ids=input_ids, decoder_input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        # compute perplexity for every candidate
        perplexity_scores = self.compute_perplexity_per_sequence(logits, input_ids, 0)

        correct_sentences = input_texts[torch.argmin(perplexity_scores)]

        return correct_sentences

    def compute_perplexity_per_sequence(self, logits, target, padding_idx):
        # Reshape logits to (batch_size, sequence_length, vocab_size)
        batch_size, seq_len, vocab_size = logits.size()
        
        # Apply log softmax to get log-probabilities
        log_probs = F.log_softmax(logits, dim=-1)
        
        # Gather log-probabilities for the true target tokens
        target_log_probs = log_probs.gather(2, target.unsqueeze(-1)).squeeze(-1)  # Shape: (batch_size, seq_len)
        
        # Create a mask for non-padding tokens
        mask = target != padding_idx  # Shape: (batch_size, seq_len)
        
        # Mask out padding tokens in the log-probabilities
        target_log_probs = target_log_probs * mask
        
        # Calculate negative log-likelihood per sequence, ignoring padding
        sum_nll_per_seq = -target_log_probs.sum(dim=1)  # Shape: (batch_size,)
        valid_tokens_per_seq = mask.sum(dim=1)  # Count non-padding tokens per sequence
        
        # Avoid division by zero for any sequences that are fully padding
        valid_tokens_per_seq = valid_tokens_per_seq.clamp(min=1)
        
        # Calculate the mean negative log-likelihood per sequence
        nll_per_seq = sum_nll_per_seq / valid_tokens_per_seq  # Shape: (batch_size,)
        
        # Compute perplexity for each sequence
        perplexity_per_seq = torch.exp(nll_per_seq)
        return perplexity_per_seq