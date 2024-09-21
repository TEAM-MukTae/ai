from openai import OpenAI
import os, string, json


MULTIPLE_CHOICE = """
Domain Knowledge :
'''
%s
'''
1) Give me %s multiple choice questions about the Domain Knowledge given in Language %s.
2) Return your answer entirely in the form of a JSON object. 
2-1) The JSON object should have a key named "questions" which is an array of the questions. 
2-2) Each quiz question should include the choices, the answer, and a brief explanation of why the answer is correct. 
2-3) Don't include anything other than the JSON. The JSON properties of each question should be "query" (which is the question), "choices", "answer", and "explanation". 
2-4) And the "title", which represents the questions in the given Language.
2-5) The choices shouldn't have any ordinal value like A, B, C, D or a number like 1, 2, 3, 4. 
2-6) The answer should be the 0-indexed number of the correct choice.
"""

SUMMARIZATION = """
Domain Knowledge :
'''
%s
'''
1) Summarize and correct about the Domain Knowledge And suggest me 4 important keywords about the Domain Knowledge.
1-1) Include title text inside the "summarization".
1-2) Consider the big context of whole Domain Knowledge.
1-3) Emphasize the "title" insidee the "summarization" and important "keywords" in "summarization" using Markdown format
1-4) Also be aware that "summarization" should be bullet-pointed summarization and it should be emphasize using **markdown grammer** so that It could listed.
1-5) And you should use language given in the Domain Knowledge.
2) Return your response entirely in the form of a JSON object. 
2-1) The JSON object should have a key named "summarization" which is a result of summarization and correction. 
2-2) Also have a key named "keywords", which is array of each keyword.
2-3) "Summarization" is bullet-pointed, which is array of each emphasized sentence
"""

KEY = os.environ['OPENAI_API_KEY']
class OpenClient:
    
    def __init__(self, prompt: str, role: str, key = KEY):
        self.model = 'gpt-4o-mini'
        self.prompt = prompt
        self.role = role
        self.client = OpenAI(api_key = key)
        
    def request(self, metadata):
        response = self.client.chat.completions.create(
            model = self.model,
            response_format={ 'type': 'json_object' },
            messages = [
                { 'role': 'system', 'content': self.role },
                { 'role': 'user', 'content': self.prompt % tuple(metadata) }
            ],
            n = 1,
            temperature=1,
            max_tokens=2048
        )
        
        result = response.choices[0].message.content        
        return json.loads(result)

class TestClient(OpenClient):
    
    def __init__(self, prompt: str, role: str, key = KEY):
        super().__init__(prompt, role, key)
        
    def request(self, metadata):
        return super().request(metadata)
    
class MultiChoiceClient(OpenClient):
    
    def __init__(self):
        prompt = MULTIPLE_CHOICE
        role = "You're professional Quiz Generator!"
        super().__init__(prompt, role, KEY)
        
    def request(self, metadata):
        return super().request(metadata)
    
class SummaryClient(OpenClient):
    
    def __init__(self):
        prompt = SUMMARIZATION
        role = "You're professional Summarization Generator!"
        super().__init__(prompt, role, KEY)
        
    def request(self, metadata):
        return super().request(metadata)