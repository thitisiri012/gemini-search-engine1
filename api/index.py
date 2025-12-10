from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import google.generativeai as genai

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            # --- วิธีไม้ตาย: ฝัง Key ตรงๆ ---
            # (ถ้าโค้ดนี้ทำงานได้ แสดงว่าปัญหาอยู่ที่ Vercel Environment จริงๆ)
            my_secret_key = "AIzaSyD0D6PyhkKk5WUA6qQeC1omUpxy9Ni-A48"
            
            genai.configure(api_key=my_secret_key)
           model = genai.GenerativeModel('gemini-pro') 
            # ---------------------------

            query = parse_qs(urlparse(self.path).query).get('q', [''])[0]

            if not query:
                self.wfile.write(json.dumps({"answer": "เชื่อมต่อสำเร็จแล้ว! (โหมดฝัง Key)"}, ensure_ascii=False).encode('utf-8'))
                return

            response = model.generate_content(query)
            self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"Error: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
