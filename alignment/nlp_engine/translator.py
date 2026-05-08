# alignment/nlp_engine/translator.py
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    MODEL_NAME = "facebook/nllb-200-distilled-600M"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_NAME)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def translate(self, sentence: str) -> str:
        if not sentence.strip():
            return ""

        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        ).to(self.device)

        with torch.no_grad():
            output_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.convert_tokens_to_ids("hin_Deva"),
                max_length=512,
                num_beams=5,
                early_stopping=True,
            )

        return self.tokenizer.batch_decode(
            output_tokens,
            skip_special_tokens=True
        )[0]