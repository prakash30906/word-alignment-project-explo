# alignment/nlp_engine/aligner.py
import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoTokenizer, AutoModel
from collections import defaultdict
import re

class Aligner:
    MODEL_NAME = "setu4993/LaBSE"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModel.from_pretrained(self.MODEL_NAME)
        self.model.eval()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    # ── tokenizers ──────────────────────────────────────────────
    def _tokenize(self, sentence: str) -> list:
        return [re.sub(r'[।\.\,\?\!]+$', '', w)
                for w in sentence.strip().split() if w]

    # ── embeddings ───────────────────────────────────────────────
    def _word_embeddings(self, words: list, layer: int = 8) -> torch.Tensor:
        enc = self.tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.device)

        word_ids = enc.word_ids()

        with torch.no_grad():
            hidden = self.model(**enc, output_hidden_states=True)\
                         .hidden_states[layer][0]

        word_embs = []
        for idx in range(len(words)):
            positions = [i for i, wid in enumerate(word_ids) if wid == idx]
            word_embs.append(hidden[positions].mean(dim=0) if positions
                             else torch.zeros(hidden.shape[-1], device=self.device))
        return torch.stack(word_embs)

    # ── alignment algorithms ──────────────────────────────────────
    @staticmethod
    def _itermax(sim: np.ndarray, max_iter: int = 60) -> set:
        pairs, m = set(), sim.copy()
        for _ in range(max_iter):
            if m.max() < 1e-6:
                break
            i, j = np.unravel_index(m.argmax(), m.shape)
            pairs.add((int(i), int(j)))
            m[i, :] = 0
            m[:, j] = 0
        return pairs

    @staticmethod
    def _bidir_sym(sim: np.ndarray, threshold: float = 0.25) -> set:
        t = torch.tensor(sim) * 5.0
        fwd = F.softmax(t, dim=1).numpy()
        bwd = F.softmax(t, dim=0).numpy()
        mask = (fwd > threshold) & (bwd > threshold)
        return {(int(i), int(j)) for i, j in zip(*np.where(mask))}

    # ── public API ────────────────────────────────────────────────
    def align(self, src_sentence: str, tgt_sentence: str) -> dict:
        src_words = self._tokenize(src_sentence)
        tgt_words = self._tokenize(tgt_sentence)

        src_emb = F.normalize(self._word_embeddings(src_words), dim=-1)
        tgt_emb = F.normalize(self._word_embeddings(tgt_words), dim=-1)
        sim = torch.matmul(src_emb, tgt_emb.T).cpu().numpy()

        pairs = sorted(self._bidir_sym(sim) | self._itermax(sim))

        # Group for display
        src_to_tgt = defaultdict(list)
        tgt_to_src = defaultdict(list)
        for i, j in pairs:
            src_to_tgt[i].append(j)
            tgt_to_src[j].append(i)

        alignment_rows = []
        for i in sorted(src_to_tgt):
            alignment_rows.append({
                "en_idx":    i,
                "en_word":   src_words[i],
                "hi_indices": src_to_tgt[i],
                "hi_words":  [tgt_words[j] for j in sorted(src_to_tgt[i])],
                "many_to_many": len(src_to_tgt[i]) > 1,
            })

        unaligned_hi = [
            {"idx": j, "word": tgt_words[j]}
            for j in range(len(tgt_words))
            if j not in {j2 for _, j2 in pairs}
        ]

        return {
            "src_words":       src_words,
            "tgt_words":       tgt_words,
            "pairs":           pairs,
            "alignment_rows":  alignment_rows,
            "unaligned_hindi": unaligned_hi,
            "sim_matrix":      sim.tolist(),   # for heatmap
        }