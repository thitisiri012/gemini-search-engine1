from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import urllib.request
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            query = parse_qs(urlparse(self.path).query).get('q', [''])[0]
            if not query:
                self.wfile.write(json.dumps({"answer": "รอคำสั่ง..."}, ensure_ascii=False).encode('utf-8'))
                return

            # Key ของคุณ (ผมใส่เผื่อไว้ให้เลย ถ้าใน Environment หาไม่เจอ)
            api_key = os.environ.get("GemeniKey")
            if not api_key:
                api_key = "AIzaSyD0D6PyhkKk5WUA6qQeC1omUpxy9Ni-A48"

            # --- วิธีใหม่: ยิงตรงเข้า Google ไม่ผ่าน Library (ตัดปัญหาเรื่องเวอร์ชันทิ้งถาวร) ---
            # ใช้ Gemini 1.5 Flash ผ่าน URL โดยตรง
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{"text": query}]
                }]
            }
            
            # ส่งคำสั่ง
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            
            # รับคำตอบ
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                # แกะคำตอบจาก JSON ที่ Google ส่งกลับมา
                try:
                    answer_text = result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    answer_text = "AI ไม่ตอบกลับ (อาจเพราะเนื้อหาไม่เหมาะสม)"
                
                self.wfile.write(json.dumps({"answer": answer_text}, ensure_ascii=False).encode('utf-8'))
            # ----------------------------------------------------------------------

        except Exception as e:
            # ถ้ายังพังอีก ให้บอกมาเลยว่าพังเพราะอะไร
            self.wfile.write(json.dumps({"answer": f"System Error: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
