# Import convention
import streamlit as st


if __name__ == "__main__":
    body = """交互友好，通过语言指引用户文件上传
    3. 纠正
    4. 对于犯的错误做出分类，打标签，一个句子可以被打上多个标签
    5. 用报价那一套方案写数据变化过程
    6. 最后对象怎么持久化
    7. 每人每天两次使用机会
    8. 支持导出anki卡片"""
    st.title("viva")
    st.markdown(body, unsafe_allow_html=False, help=None)

    label="upload your video or audio"
    st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None
                     , kwargs=None, disabled=False, label_visibility="visible")