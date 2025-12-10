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
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                self.wfile.write(json.dumps({"answer": "Error: ไม่พบ API Key"}, ensure_ascii=False).encode('utf-8'))
                return

            genai.configure(api_key=api_key)

            # --- จุดสำคัญ: ลองใช้ชื่อ gemini-pro ดูก่อน ---
            try:
                model = genai.GenerativeModel('gemini-pro') 
                response = model.generate_content(query)
                self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))
            
            except Exception as e:
                # --- ถ้า Error ให้มันบอกชื่อรุ่นที่มีทั้งหมดออกมา ---
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
                
                error_msg = f"เกิดข้อผิดพลาด: {str(e)}\n\n(ระบบมองเห็นรุ่นเหล่านี้: {', '.join(available_models)})"
                self.wfile.write(json.dumps({"answer": error_msg}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"System Error: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
