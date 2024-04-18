from openai import OpenAI
import datetime
MESSAGE_FILE = 'message.txt'
class Modal():
    
    def __init__(self,model='/data2/huangwenhao/hf_model/Mistral-7B-Instruct-v0.2',port=8091):
        openai_api_key = "EMPTY"
        openai_api_base = f"http://10.176.40.140:{port}/v1"
        self.model = model
        
        self.client = OpenAI(
            api_key=openai_api_key,
            base_url=openai_api_base,
            )
    def call_with_messages(self,query):
        # mess = [{"role": "user", "content": " "}]
        # mess[0]['content'] = query[0]['content']+query[1]['content']
        chat_response = self.client.chat.completions.create(
            model=self.model,
            messages=query,

            temperature = 0.5,
            )
        current_time = datetime.datetime.now()
        with open(MESSAGE_FILE, 'a+') as f:
            f.write(str(current_time)+'\t' + str(chat_response.usage)+'\n')
        return chat_response.choices[0].message