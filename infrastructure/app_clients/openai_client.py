# 加载 .env 文件中的环境变量
import json
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from domain.entities.revision import Revision


class OpenAIClient():
    def polish_expression(self, utterances):
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        model_name = "gpt-4-1106-preview"
        temperature = 0.1
        model = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=openai_api_key)
        role = """
                我是一位中国人，正在寻求帮助以提高我的英语口语能力。
                我想展示一段我和我的英语老师之间的对话（我是发言者B）。
                能否请你帮忙指出其中的错误或者听起来对于母语为英语的人不自然的短语,并给出地道的表达方式？
                
                请复制我的输入文本，并在B的发言后插入你的纠正或建议，类似这样
                A: 我们称它们为菌株。
                B: 菌株。
                authentic_expression: [你的纠正或建议]
                
                下面是我们的对话：
                
                """

        parser = PydanticOutputParser(pydantic_object=Revision)
        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        _input = prompt.format_prompt(query=role+str(utterances))
        _output = model.invoke(_input.to_string()).content
        start = _output.find('{')
        end = _output.rfind('}') + 1
        jsonl_data = _output[start:end]
        print(jsonl_data)

        # 首先，我们需要将这个字符串转换为一个有效的 JSON 格式
        # 因为这个字符串有多个 JSON 对象，但没有包裹在一个列表中，我们需要先将它们包裹在一个列表中
        json_like_str = "[" + jsonl_data.strip().rstrip(',') + "]"

        # 解析 JSON 字符串
        data = json.loads(json_like_str)

        # 转换为无花括号和引号的字符串
        output_str = ""
        for entry in data:
            for key, value in entry.items():
                output_str += f"{key} says: {value}\n"
            output_str += "\n"

        with(open("utterances_with_suggestion.txt", "w") as f):
            f.write(output_str)
        return "utterances_with_suggestion.txt"

if __name__ == "__main__":
    OpenAIClient().polish_expression(
        '''
        {
          "speaker_A": "Cool.",
          "speaker_B": "The local people really like it.",
          "authentic_expression": "The local people really enjoy them."
        },
        {
          "speaker_A": "That's cool.",
          "speaker_B": "But some are toxic. When you deadly, like deadly, you will have some.",
          "authentic_expression": "But some are toxic. If you're not careful, you could pick a deadly one."
        },
        {
          "speaker_C": "This is a big topic.",
          "speaker_A": "So first of all, people go literally they call it mushroom hunting in the US. Like, they look for mushrooms. People love to go look for mushrooms in the US. We have mushrooms here, too. And it's true. Some of them are like, you can eat them and they're toxic, like deadly. You can actually die from eating them. They're really bad for you. But some of them and we usually call these shrooms, they're hallucinogenic. How do I spell that? I have to figure out how to spell this. Okay. Hallucinogenic, which means that you can kind of see things that aren't there, and.",
          "speaker_C": "It's like a drug, like you said.",
          "speaker_A": "Like a drug.",
          "speaker_C": "Oh, shoot. Keep talking.",
          "speaker_A": "My laptop is going to die. I'm getting my charger, but keep talking. I can hear you. Okay. Yes. So these, like these mushrooms these mushrooms are like people take them for fun. Probably not in China, but in here, people take them for fun, like take jobs, you know what I mean? Yeah, like taking a don't do that. Is it expensive? It's more expensive than just, like, the mushrooms you eat, but I don't think so. They're not like crazy expensive. I have had them for and they're like, they're."
        }
        '''

    )