# Import convention

import streamlit as st

from application.main_processor import MainProcessor


class Streamlit:

    def display(self):
        body = """
        相信所有的进步，都来自于尝试、反馈、间隔复习！
        """

        st.title("viva")
        st.markdown(body, unsafe_allow_html=False, help=None)

        st.link_button("B站主页", "https://space.bilibili.com/244791824")
        st.link_button("语法 best practice", "https://space.bilibili.com/483162496/")
        st.link_button("语音 best practice", "https://www.youtube.com/@rachelsenglish")

        label_upload = "在下方上传你和native speaker的对话视频或者录音,得到GPT给出的地道表达建议"
        uploaded_file = st.file_uploader(label_upload, type=["mp4", "mp3"])

        if 'key' not in st.session_state:
            st.session_state.key = 'begin'

        if st.session_state.key == "finished":
            st.info("由于服务成本限制，目前每人每日只提供一次服务哦～")

        if uploaded_file != None and st.session_state.key != "finished":
            try:
                with st.status('Wait for it... 步骤处理比较多，可能需要耐心等几分钟', expanded=True):
                    suggestion_url = MainProcessor(st).execute(uploaded_file)
                    label_download = "点击下载（这是GPT帮你纠正后的地道表达）"
                    if suggestion_url is not None:
                        with open(suggestion_url, "rb") as result:
                            btn = st.download_button(label_download, result, file_name=suggestion_url, mime=None,
                                                     key=None, help=None,
                                                     on_click=None,
                                                     args=None,
                                                     kwargs=None, type="secondary", disabled=False,
                                                     use_container_width=False)
                            st.success('Done!')
                            st.session_state.key = "finished"

            except Exception as e:
                st.error(
                    "服务器崩了，快去提醒up主！！！" + str(e))
