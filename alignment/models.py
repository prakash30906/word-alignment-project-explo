# alignment/models.py
from django.db import models

class AlignmentResult(models.Model):
    english_sentence  = models.TextField()
    hindi_sentence    = models.TextField()
    alignment_pairs   = models.JSONField()   # [(src_idx, tgt_idx), ...]
    similarity_matrix = models.JSONField()   # 2D list for heatmap
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.english_sentence[:50]} ({self.created_at:%Y-%m-%d})"