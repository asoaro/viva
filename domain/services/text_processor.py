import json
import math


class TextProcessor:

    def __init__(self, st):
        self.st = st

    def swap_label_if_necessary(self, content):
        # Step 1: Read the conversation from a .txt file
        lines = content
        # Step 2: Parse the conversation to count words
        word_count_A = 0
        word_count_B = 0
        for line in lines:
            speaker, sentence = line.split(': ', 1)
            words = sentence.split()

            if speaker == 'speaker A':
                word_count_A += len(words)
            elif speaker == 'speaker B':
                word_count_B += len(words)
        # Step 3: Rewrite the conversation to a new .txt file
        print(f"Speaker A spoke {word_count_A} words")
        print(f"Speaker B spoke {word_count_B} words")

        # Swap speakers if B spoke more than A
        swap = False
        if word_count_B > word_count_A:
            word_count_A, word_count_B = word_count_B, word_count_A
            swap = True
        for line in lines:
            speaker, sentence = line.split(': ', 1)

            if swap:
                if speaker == 'speaker A':
                    speaker = 'speaker B'
                elif speaker == 'speaker B':
                    speaker = 'speaker A'
            line = f"{speaker}: {sentence}"
        print("Conversation revised and saved to revised_conversation.txt")
        self.st.write("语音解析完成 您本次对话进行了 {} 轮, 共输出单词 {} 个, 外教输出 {} 个".format(math.ceil(len(lines) / 2), word_count_B, word_count_A))
        return lines

    def get_utterances_from_transcript(self, json_data):
        utterances = json_data.get("utterances", [])
        content = []
        if utterances is not None:
            for entry in utterances:
                speaker = entry["speaker"]
                text = entry["text"]
                content.append(f"speaker {speaker}: {text}")

        content_labeled = self.swap_label_if_necessary(content)
        print("TXT file created successfully!" + " - ")
        # Save the content to the txt file
        with open("utterances.txt", 'w') as file:
            file.write('\n'.join(content_labeled))
        return content_labeled
