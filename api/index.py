from http.server import BaseHTTPRequestHandler
import json
import sys

# โค้ดนี้ถูกเขียนมาเพื่อ "ดักจับ Error" โดยเฉพาะ
# จะไม่ทำให้เกิดหน้าจอ 500 แต่จะบอกสาเหตุที่แท้จริงแทน

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        report = {
            "status": "Checking system...",
            "python_version": sys.version,
            "error_details": ""
        }

        # 1. เช็คว่าลง Library Google หรือยัง?
        try:
            import google.generativeai as genai
            report["library_check"] = "✅ ติดตั้ง google-generativeai สำเร็จ"
        except ImportError as e:
            report["library_check"] = f"❌ พังตรงนี้: หา Library ไม่เจอ ({str(e)})"
            report["hint"] = "เช็คไฟล์ requirements.txt ว่าสะกดถูกไหม"
            self.wfile.write(json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
            return

        # 2. เช็คว่าเรียกใช้ Gemini ได้ไหม?
        try:
            # ใส่ Key ตรงๆ เพื่อทดสอบระบบ (Hardcode)
            genai.configure(api_key="AIzaSyD0D6PyhkKk5WUA6qQeC1omUpxy9Ni-A48")
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("ตอบสั้นๆว่า 'พร้อมใช้งาน'")
            
            report["gemini_response"] = response.text
            report["final_result"] = "🎉 ยินดีด้วย! ระบบทำงานได้แล้ว"
            
        except Exception as e:
            report["gemini_check"] = f"❌ พังตอนเรียก AI: {str(e)}"
        
        self.wfile.write(json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
