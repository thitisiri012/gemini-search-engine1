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
            # 1. รับคำถาม
            query = parse_qs(urlparse(self.path).query).get('q', [''])[0]
            
            if not query:
                self.wfile.write(json.dumps({"answer": "พร้อมรับใช้ครับ! พิมพ์คำถามมาได้เลย"}, ensure_ascii=False).encode('utf-8'))
                return

            # 2. ดึงกุญแจ (สำคัญมาก)
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                self.wfile.write(json.dumps({"answer": "Error: ลืมใส่ GEMINI_API_KEY ใน Vercel ครับ"}, ensure_ascii=False).encode('utf-8'))
                return

            # 3. ถาม AI
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.0-pro')
            response = model.generate_content(query)
            
            self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"เกิดข้อผิดพลาด: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
