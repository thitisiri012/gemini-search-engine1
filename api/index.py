from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
import google.generativeai as genai

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ตั้งค่า Header ให้คุยกับหน้าเว็บรู้เรื่อง
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        try:
            # 1. รับคำถาม
            query = parse_qs(urlparse(self.path).query).get('q', [''])[0]
            
            # 2. เช็ค Key
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self.wfile.write(json.dumps({"answer": "Error: ไม่พบ API Key"}, ensure_ascii=False).encode('utf-8'))
                return

            # 3. ตั้งค่า AI และเรียกใช้รุ่นที่ถูกต้อง (จากลิสต์ที่คุณส่งมา)
            genai.configure(api_key=api_key)
            
            # --- แก้ตรงนี้เป็นรุ่นที่มีในลิสต์ของคุณ ---
            model = genai.GenerativeModel('gemini-1.5-flash') 
            # ------------------------------------

            if not query:
                self.wfile.write(json.dumps({"answer": "พร้อมทำงานครับ! พิมพ์คำถามมาได้เลย"}, ensure_ascii=False).encode('utf-8'))
                return

            # 4. ส่งคำถามและรอคำตอบ
            response = model.generate_content(query)
            
            # 5. ส่งคำตอบกลับไปที่หน้าเว็บ
            self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"เกิดข้อผิดพลาด: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
