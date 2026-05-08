# alignment/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class AlignmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alignment'

    translator = None
    aligner = None

    def ready(self):
        logger.info("Loading NLP models...")
        print(">>> Loading NLP models — please wait 10-20 mins on first run...")

        try:
            from alignment.nlp_engine.translator import Translator
            from alignment.nlp_engine.aligner import Aligner

            AlignmentConfig.translator = Translator()
            AlignmentConfig.aligner = Aligner()

            print(">>> NLP models loaded successfully ✓")

        except Exception as e:
            print(f">>> ERROR loading models: {e}")
            import traceback
            traceback.print_exc()