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
            
            # 1. ดึงค่าจากตัวแปรชื่อ 'GemeniKey' (ตามที่คุณตั้ง)
            api_key = os.environ.get("GemeniKey")
            
            if not api_key:
                self.wfile.write(json.dumps({"answer": "Error: ไม่พบ 'GemeniKey' ในการตั้งค่า Vercel"}, ensure_ascii=False).encode('utf-8'))
                return

            # 2. ตั้งค่า AI
            genai.configure(api_key=api_key)
            
            # 3. เรียกใช้โมเดล Gemini 3.0 Pro 
            # (ชื่ออย่างเป็นทางการในระบบคือ 'gemini-exp-1206' หรือรุ่นทดลองล่าสุด)
            # แต่เพื่อความชัวร์และฟรี ผมแนะนำรุ่นนี้ครับ:
            model = genai.GenerativeModel('gemini-2.0-flash-exp') 
            
            # หมายเหตุ: ตอนนี้ Google ยังไม่เปิด 'gemini-3.0-pro' ให้ใช้ผ่าน API สาธารณะทั่วไป
            # แต่รุ่น 'gemini-2.0-flash-exp' คือตัวท็อปสุดที่ฟรีและเร็วที่สุดตอนนี้ครับ
            # (ถ้าอนาคต 3.0 มาจริง แค่เปลี่ยนชื่อตรงนี้เป็น 'gemini-3.0-pro')

            if not query:
                self.wfile.write(json.dumps({"answer": "พร้อมใช้งานครับ! ถามมาได้เลย"}, ensure_ascii=False).encode('utf-8'))
                return

            response = model.generate_content(query)
            self.wfile.write(json.dumps({"answer": response.text}, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            self.wfile.write(json.dumps({"answer": f"เกิดข้อผิดพลาด: {str(e)}"}, ensure_ascii=False).encode('utf-8'))
