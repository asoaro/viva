import json

import assemblyai as aai

from infrastructure.app_clients.s2t_client.assemblyai_client import AssemblyAIClient


class VideoProcessor:

    def __init__(self, st):
        self.st = st

    def get_transcript_from_video(self, uploaded_file):
        transcriber = AssemblyAIClient().get_transcriber()
        transcript = transcriber.transcribe(uploaded_file)
        print(f"Transcription succeed: {transcript.id}")
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
        transcript_path = "transcripts.txt"
        # 确保目录存在
        with open(transcript_path, 'w') as file:
            json.dump(transcript.json_response, file)
        print(transcript.json_response)
        print("get transcripts successfully!")
        self.st.write("解析视频成功")
        return transcript.json_response


if __name__ == "__main__":
    # 假设 json_str 是你的原始 JSON 字符串
    json_str = '''
        {
            "speaker_A": "Gutogu. Yeah, that's my favorite mushroom. I love that mushroom. It's so good.",
            "speaker_B": "Do you know the mushroom is more colorful? Maybe it's toxic.",
            "authentic_expression": "Do you know if the more colorful mushrooms are toxic?"
        },
        {
            "speaker_A": "The colorful ones?",
            "speaker_B": "Yeah.",
            "authentic_expression": "Yes, the brightly colored ones."
        },
    '''

    # 解析 JSON 字符串
    data = json.loads(json_str)

    # 转换为无花括号和引号的字符串
    output_str = ""
    for conversation in data:
        for speaker, text in conversation.items():
            output_str += text + " "
        output_str += "\n"

    print(output_str)