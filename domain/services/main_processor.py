from tempfile import NamedTemporaryFile

from domain.services.text_processor import TextProcessor
from domain.services.video_processor import VideoProcessor
from infrastructure.app_clients.openai_client import OpenAIClient


class MainProcessor:
    def execute(self, uploaded_file):
        if uploaded_file is not None:
            videoProcessor = VideoProcessor()
            if uploaded_file is not None:
                with NamedTemporaryFile(suffix="mp4") as temp:
                    temp.write(uploaded_file.getvalue())
                    temp.seek(0)

                    transcript = videoProcessor.get_transcript_from_video(temp.name)
                    utterances = TextProcessor.get_utterances_from_Transcript(transcript)
                    url = OpenAIClient().polish_expression(utterances)
                    return url





