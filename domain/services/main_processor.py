from tempfile import NamedTemporaryFile

from domain.services.text_processor import TextProcessor
from domain.services.video_processor import VideoProcessor
from infrastructure.app_clients.openai_client import OpenAIClient


class MainProcessor:
    def __init__(self, st):
        self.st = st

    def execute(self, uploaded_file):
        if uploaded_file is not None:
            videoProcessor = VideoProcessor(self.st)
            textProcessor = TextProcessor(self.st)
            openAIClient = OpenAIClient(self.st)
            if uploaded_file is not None:
                with NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
                    temp.write(uploaded_file.getvalue())
                    temp.seek(0)
                    self.st.write("文件上传成功")
                    transcript = videoProcessor.get_transcript_from_video(temp.name)
                    utterances = textProcessor.get_utterances_from_transcript(transcript)
                    url = openAIClient.polish_expression(utterances)
                    return url
