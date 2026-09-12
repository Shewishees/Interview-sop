"""
FastAPI HTTP 接口端到端自动化测试
使用 starlette.testclient 进行全接口测试
"""
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

import json as _json
import urllib.request
import urllib.error

# 自适应客户端：优先使用 TestClient，若未安装 httpx 则通过标准库 urllib 请求在线服务
class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self._test_client = None
        try:
            from starlette.testclient import TestClient
            from app import app
            self._test_client = TestClient(app)
        except Exception:
            pass

    class ResponseWrapper:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text
        def json(self):
            return _json.loads(self.text)

    def get(self, path):
        if self._test_client:
            try:
                return self._test_client.get(path)
            except Exception:
                pass
        req = urllib.request.Request(f"{self.base_url}{path}", headers={"User-Agent": "TestClient"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return self.ResponseWrapper(resp.status, resp.read().decode("utf-8"))

    def post(self, path, json_data=None, json=None):
        payload_dict = json if json is not None else json_data
        if self._test_client:
            try:
                return self._test_client.post(path, json=payload_dict)
            except Exception:
                pass
        payload = _json.dumps(payload_dict or {}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "TestClient"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return self.ResponseWrapper(resp.status, resp.read().decode("utf-8"))

client = ApiClient()

def test_api_routes():
    print(">>> 测试 1: GET /api/defaults ...")
    res = client.get("/api/defaults")
    assert res.status_code == 200
    data = res.json()
    assert "company" in data
    assert "resume" in data
    print("   [OK] 默认配置读取成功:", data["job_title"])

    print(">>> 测试 2: POST /api/scan_repo ...")
    repo_path = str(Path(__file__).parent.parent)
    res = client.post("/api/scan_repo", json={"repo_path": repo_path})
    assert res.status_code == 200
    scan_data = res.json()
    assert scan_data["success"] == True
    print("   [OK] 仓库扫描成功，识别出核心亮点:", len(scan_data["summary"]["code_highlights"]))

    print(">>> 测试 3: POST /api/generate_sop ...")
    res = client.post("/api/generate_sop", json={
        "company": data["company"],
        "job_title": data["job_title"],
        "jd": data["jd"],
        "resume": data["resume"],
        "repo_path": repo_path
    })
    assert res.status_code == 200
    sop_res = res.json()
    assert sop_res["success"] == True
    sop = sop_res["sop"]
    assert "sop_1_matching" in sop
    assert "sop_2_star" in sop
    print("   [OK] 全套 SOP 生成成功，匹配度综合得分:", sop["sop_1_matching"]["overall_score"])

    print(">>> 测试 4: POST /api/mock_interview/chat ...")
    res = client.post("/api/mock_interview/chat", json={
        "question": "请介绍一下你的 Mini-LLaVA 项目",
        "user_answer": "这是一个基于 Qwen3 和 CLIP 的轻量多模态模型，我重写了 CLIP forward 提取 197 个 patch 特征，并通过两层 MLP 对齐到 1024 维语言空间。",
        "round_num": 1,
        "interview_style": "geek"
    })
    assert res.status_code == 200
    chat_res = res.json()
    assert chat_res["success"] == True
    print("   [OK] 模拟面试打分与追问成功:", chat_res["review"]["score"], "分")

    print(">>> 测试 5: GET / 静态首页渲染 ...")
    res = client.get("/")
    assert res.status_code == 200
    assert "InterviewSOP Master" in res.text
    print("   [OK] 前端单页 Web 首页托管成功！")

    print("\n==========================================")
    print("🎉 FastAPI 全部 5 项端到端 API 路由自检 100% 通过！")
    print("==========================================")

if __name__ == "__main__":
    test_api_routes()
