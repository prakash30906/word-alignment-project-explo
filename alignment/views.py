# alignment/views.py
import time
import logging
from django.shortcuts import render
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AlignmentRequestSerializer, AlignmentResultSerializer
from .models import AlignmentResult

logger = logging.getLogger(__name__)


def index(request):
    """Renders the main NLP Lab UI page."""
    recent = AlignmentResult.objects.all()[:5]
    return render(request, 'alignment/index.html', {'recent': recent})


class AlignView(APIView):
    """
    POST /api/align/
    Body: { "english": "...", "hindi": "..." (optional) }
    Returns full alignment result + saves to DB.
    """

    def post(self, request):
        serializer = AlignmentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        english = serializer.validated_data['english'].strip()
        hindi   = serializer.validated_data.get('hindi', '').strip()

        # Get models from app config (loaded once at startup)
        app_config  = apps.get_app_config('alignment')
        translator  = app_config.translator
        aligner     = app_config.aligner

        if not translator or not aligner:
            return Response(
                {"error": "NLP models not loaded. Check server logs."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            t0 = time.time()

            # Step 1: translate if Hindi not provided
            if not hindi:
                hindi = translator.translate(english)

            # Step 2: align
            result = aligner.align(english, hindi)

            elapsed = round(time.time() - t0, 2)

            # Step 3: save to DB
            db_obj = AlignmentResult.objects.create(
                english_sentence  = english,
                hindi_sentence    = hindi,
                alignment_pairs   = result['pairs'],
                similarity_matrix = result['sim_matrix'],
            )

            return Response({
                "id":              db_obj.id,
                "english":         english,
                "hindi":           hindi,
                "src_words":       result['src_words'],
                "tgt_words":       result['tgt_words'],
                "alignment_rows":  result['alignment_rows'],
                "unaligned_hindi": result['unaligned_hindi'],
                "sim_matrix":      result['sim_matrix'],
                "elapsed_sec":     elapsed,
            })

        except Exception as e:
            logger.exception("Alignment failed")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoryView(APIView):
    """GET /api/history/ — last 20 alignment results."""
    def get(self, request):
        results = AlignmentResult.objects.all()[:20]
        return Response(AlignmentResultSerializer(results, many=True).data)