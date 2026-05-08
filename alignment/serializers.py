# alignment/serializers.py
from rest_framework import serializers
from .models import AlignmentResult

class AlignmentRequestSerializer(serializers.Serializer):
    english  = serializers.CharField(max_length=500)
    hindi    = serializers.CharField(max_length=500, required=False, allow_blank=True)

class AlignmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AlignmentResult
        fields = ['id', 'english_sentence', 'hindi_sentence',
                  'alignment_pairs', 'similarity_matrix', 'created_at']