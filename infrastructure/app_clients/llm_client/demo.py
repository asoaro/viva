import os
import openai
from openai import OpenAI

with open("../../../instruction.txt", "r") as f:
    instruction = f.read()

client = OpenAI(api_key="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")
with open("utterances.txt", "r") as utterances:
    content = utterances.read()
my_assistant = client.beta.assistants.create(
    instructions="you are an English teacher, master with both English and Chinese",
    name="Viva",
    model="gpt-4-1106-preview",
)
print(my_assistant)

thread = client.beta.threads.create()
print(thread)
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = instruction
)
print(message)
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = my_assistant.id,
)
print(run.status)
# while (run.status != "queued") :
#     print(message.content)

