from tempfile import NamedTemporaryFile

from domain.services.llm_processor import LLMProcessor
from domain.services.utterances_processor import UtterancesProcessor
from domain.services.video_processor import VideoProcessor
import streamlit as st


class MainProcessor:
    def __init__(self, st):
        self.st = st
        self.video_processor = VideoProcessor(self.st)
        self.utterances_processor = UtterancesProcessor(self.st)
        self.llm_processor = LLMProcessor(self.st)

    def execute(self, uploaded_file):
        if uploaded_file is not None:
            with NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
                temp.write(uploaded_file.getvalue())
                temp.seek(0)
                self.st.write("文件上传成功")

            # speech to text
            transcript = self.video_processor.execute(temp.name)
            # get utterances with correct speaker label
            utterances = self.utterances_processor.execute(transcript)
            # get suggestion from GPT
            suggestion = self.llm_processor.execute(utterances)

            result_file_name = "suggestion_for_you.txt"
            with open(result_file_name, "w") as f:
                f.write(suggestion)
            return result_file_name
