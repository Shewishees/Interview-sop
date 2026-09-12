"""
InterviewSOP Master 一键启动脚本
在浏览器中自动打开面试备战系统
"""

import sys
import time
import webbrowser
import threading
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def open_browser(url: str, delay: float = 1.5):
    time.sleep(delay)
    print(f"[*] 正在自动为你打开浏览器: {url}")
    webbrowser.open(url)

def main():
    try:
        import uvicorn
        import fastapi
    except ImportError:
        print("[!] 正在安装必要依赖 fastapi uvicorn ...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"])
        
    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"
    
    print("=" * 60)
    print("  🚀 欢迎使用 InterviewSOP Master (面试全流程 SOP 备战系统)")
    print(f"  📍 本地访问地址: {url}")
    print("  💡 输入目标公司/岗位要求、个人简历、项目仓库，即可生成全套备战战报！")
    print("=" * 60)
    
    # 后台线程打开浏览器
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    
    # 启动 uvicorn
    from app import app
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
