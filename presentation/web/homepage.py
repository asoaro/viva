# Import convention
import os
from tempfile import NamedTemporaryFile

import streamlit as st

from domain.services.main_processor import MainProcessor
from domain.services.video_processor import VideoProcessor


class Streamlit:
    def display(self):
        body = """
        相信所有的进步，都来自于尝试、反馈、间隔复习！
        """
        st.title("viva")
        st.markdown(body, unsafe_allow_html=False, help=None)

        st.link_button("B站主页", "https://space.bilibili.com/244791824")

        label_upload = "在下方上传你和native speaker的对话视频或者录音,耐心等待一段时间后，会出现下载按钮，你将得到GPT给出的地道表达"
        uploaded_file = st.file_uploader(label_upload, type=["mp4", "mp3"])
        url = None
        if uploaded_file is not None:
            url = MainProcessor().execute(uploaded_file)

        label_download = "这是GPT帮你纠正后的地道表达"
        if url is not None:
            with open(url , "rb") as result:
                btn = st.download_button(label_download, result, file_name=url, mime=None, key=None, help=None, on_click=None, args=None,
                                   kwargs=None, type="secondary", disabled=False, use_container_width=False)




