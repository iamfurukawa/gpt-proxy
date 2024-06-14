from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI
import os
import json

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Set up OpenAI client
        client = OpenAI(api_key=os.environ.get('GPT_KEY'))
        MODEL = "gpt-4o"

        # Read the content length to know how much data to read
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Parse the JSON data
            data = json.loads(post_data)
            messages = data.get('messages', [])

            # Ensure messages are provided
            if not messages:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No messages provided"}).encode('utf-8'))
                return

            # Create the completion
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "completion": completion
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))