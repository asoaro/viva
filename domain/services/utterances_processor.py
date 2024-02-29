import math


class UtterancesProcessor:

    def __init__(self, st):
        self.st = st

    def execute(self, transcript):
        return self.get_utterances_from_transcript(transcript)

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
        if word_count_B > word_count_A:
            revised_lines = []  # Initialize a new list to hold revised lines
            for line in lines:
                speaker, sentence = line.split(': ', 1)
                if speaker == 'speaker A':
                    speaker = 'speaker B'
                elif speaker == 'speaker B':
                    speaker = 'speaker A'
                revised_line = f"{speaker}: {sentence}"
                revised_lines.append(revised_line)  # Append the revised line to the list
        else:
            revised_lines = lines

        print("Conversation revised and saved to revised_conversation.txt")
        return revised_lines  # Return the revised list of lines

    def get_utterances_from_transcript(self, transcript):
        utterances = transcript.get("utterances", [])
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
