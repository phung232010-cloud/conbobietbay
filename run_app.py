import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("  GEN AI EXAM MASTER — HỆ THỐNG ÔN THI TRÍ TUỆ NHÂN TẠO TẠO SINH")
        print("  Cuộc thi AI or Behind 2026-2027 • Mô phỏng Gmetrix Certiport")
        print("=" * 60)
        print(f"\n[+] Đang mở trang web tại địa chỉ: {url}")
        print("[+] Bạn cũng có thể mở trực tiếp file 'index.html' bằng trình duyệt bất kỳ.")
        print("[+] Bấm Ctrl + C để dừng máy chủ.\n")
        
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng máy chủ.")

if __name__ == '__main__':
    start()
