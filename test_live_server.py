"""
端到端功能验证脚本 (验证空白初始状态、Demo载入、多仓库扫描、自定义简历与动态 Prompt)
"""
import sys
import json
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:8000"

def get(path: str):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "TestClient"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status, resp.read().decode("utf-8")

def post(path: str, data: dict):
    url = f"{BASE_URL}{path}"
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "TestClient"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def main():
    print(">>> 1. 验证静态首页...")
    st, html = get("/")
    assert st == 200
    assert "样例演示" in html or "多模态 Demo" in html
    assert "导入简历文件" in html
    assert "多代码仓库" in html or "本地代码仓库透视" in html or "代码透视" in html
    print("   [OK] 前端页面新组件已更新！")

    print(">>> 2. 验证初始空白状态与 Demo 解耦...")
    st, defaults_text = get("/api/defaults")
    defaults = json.loads(defaults_text)
    assert defaults["company"] == ""
    assert defaults["resume"] == ""
    assert defaults["repo_paths"] == []
    print("   [OK] /api/defaults 保持干净空白，无强行默认内容！")

    st, demo_text = get("/api/demo_data")
    demo = json.loads(demo_text)
    assert "Mini-LLaVA" in demo["resume"]
    assert len(demo["repo_paths"]) >= 1
    print("   [OK] /api/demo_data 成功提供独立完整的 Demo 演示数据！")

    print(">>> 3. 验证多仓库批量扫描 /api/scan_repos ...")
    repo_path = str(Path(__file__).parent.parent)
    st, scan_res = post("/api/scan_repos", {"repo_paths": [repo_path, repo_path]})
    assert st == 200
    assert scan_res["success"] == True
    assert len(scan_res["results"]) == 2
    print(f"   [OK] 成功同时透视 {len(scan_res['results'])} 个代码仓库！")

    print(">>> 4. 验证多仓库与自定义输入下的 SOP 全流程生成...")
    st, sop_res = post("/api/generate_sop", {
        "company": "测试科技公司",
        "job_title": "多模态大模型与具身算法工程师",
        "jd": "熟练掌握多模态大模型与具身智能，负责模型预训练与微调。",
        "resume": demo["resume"],
        "repo_paths": [repo_path]
    })
    assert st == 200
    sop = sop_res["sop"]
    assert "sop_1_matching" in sop
    assert len(sop["sop_2_star"]) >= 1
    assert "mock_interviewer_prompt" in sop
    print(f"   [OK] SOP 生成正常，STAR 项目数: {len(sop['sop_2_star'])}，匹配分: {sop['sop_1_matching']['overall_score']}")

    print("\n==========================================")
    print("🎉 多仓库支持 + 自主导入简历 + Demo解耦测试全部通过！")
    print("==========================================")

if __name__ == "__main__":
    main()
