from http.server import BaseHTTPRequestHandler
from openai import OpenAI
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        client = OpenAI(api_key=os.environ.get('GPT_KEY'))
        MODEL="gpt-4o"

        completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps me with my math homework!"},
            {"role": "user", "content": "Hello! Could you solve 20 x 5?"}]
        )
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(completion.choices[0].message.content.encode('utf-8'))
        return