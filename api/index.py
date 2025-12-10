from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import google.generativeai as genai

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            query = parse_qs(urlparse(self.path).query).get('q', [''])[0]
            
            # ใช้ Key ที่คุณตั้งไว้ใน Vercel
            api_key = os.environ.get("GemeniKey")
            
            # หรือถ้ายังไม่ได้แก้ใน Vercel จะแอบใส่ตรงนี้ชั่วคราวก็ได้ (แต่ไม่แนะนำถาวร)
            if not api_key:
                api_key = "AIzaSyD0D6PyhkKk5WUA6qQeC1omUpxy9Ni-A48"

            genai.configure(api_key=api_key)
            
            # ใช้รุ่น Flash (เร็วและฟรี)
            model = genai.GenerativeModel('gemini-1.5-flash')

            if not query:
                self.wfile.write(json.dumps({"answer": "พร้อมรับคำสั่งแล้วครับ!"}, ensure_ascii=False).encode('utf-8'))
                return

            response = model.generate_content(query)
            self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"Error: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
