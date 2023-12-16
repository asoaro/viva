import streamlit

from infrastructure.app_clients.llm_client.assistant import Assistant
import streamlit as st

class LLMProcessor:

    def __init__(self, st):
        self.st = st
        self.assistant = Assistant()

    def execute(self, utterances):
        with open("instruction.txt", "r") as f:
            instruction = f.read()
        # 第一次请求
        self.assistant.send_message(instruction + str(utterances))
        # 返回给前端友好提示
        self.st.write("不要着急哦，已经处理完一半的对话了")
        # 第二次请求
        self.assistant.send_message("continue")

        suggestion_json = self.assistant.get_final_result()
        return self.reformat_json_suggestion(suggestion_json)

    def reformat_json_suggestion(self, suggestion_json):

        return suggestion_json
