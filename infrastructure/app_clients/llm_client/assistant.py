import json
import os
import time
import dotenv
from datetime import datetime
from openai import OpenAI
dotenv.load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

LOGFILE = 'AssistantLog.md'  # We'll store all interactions in this file
AI_RESPONSE = '-AIresponse-'  # GUI event key for Assistant responses


def show_json(data):
    """
    Converts a Python object to a JSON formatted string and prints it.

    Args:
    data: A Python object (e.g., dict, list) to be converted into JSON.
    """
    # Convert the Python object to a JSON formatted string
    json_data = json.dumps(data, indent=4)

    # Print the JSON formatted string
    print(json_data)

class Assistant:

    def __init__(self):
        # 环境变量
        while OpenAI.api_key is None:
            input("Hey! Couldn't find OPENAI_API_KEY. Put it in .env then press any key to try again...")
            dotenv.load_dotenv()
            OpenAI.api_key = os.getenv('OPENAI_API_KEY')

        # 初始化要素
        self.client = OpenAI()
        self.assistant = None
        self.run = None
        self.message = None

        # 初始化assistant
        self.assistant = self.client.beta.assistants.create(
            name="Random Assistant",
            instructions="Format your responses in markdown.",
            model="gpt-4-1106-preview",
        )

        # 初始化thread
        self.create_AI_thread()

        #
        self.suggestion = ""

    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating llm_client thread...')
        self.thread = self.client.beta.threads.create()
        print(self.thread)
        with open(LOGFILE, 'a+') as f:
            f.write(f'# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread.id}\n\n')

    def wait_on_run(self):
        """Waits for an OpenAI llm_client run to finish and handles the response."""

        # polling
        while self.run.status == "queued" or self.run.status == "in_progress":
            # refresh run
            self.run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=self.run.id)

            now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print(now + '  Waiting for llm_client response...')
            time.sleep(1)

        # Get messages added after our last user message
        new_messages = self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc",
                                                              after=self.message.id)
        with open(LOGFILE, 'a+') as f:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print(now + '  write response...')
            f.write('\n**Assistant**:\n')
            for m in new_messages:
                self.suggestion += str(m.content[0].text.value)
                f.write(m.content[0].text.value)
            f.write('\n\n---\n')

    def send_message(self, message_text: str):
        """
        Send a message to the llm_client.

        Parameters
        ----------
        window : PySimpleGUI.window
            GUI element with .write_event_value() callback method, which will receive the Assistant's response.
        message_text : str
        """
        self.message = self.client.beta.threads.messages.create(self.thread.id,
                                                                role="user",
                                                                content=message_text)
        print('\nSending:\n' + str(self.message))
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')

        self.run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)
        self.wait_on_run()

    def get_final_result(self):
        return self.suggestion

if __name__ == "__main__":
    assistant = Assistant()  # 懒汉式初始化 assistant和thread
    assistant.send_message("who you are ")
    assistant.send_message("what's your name ")
