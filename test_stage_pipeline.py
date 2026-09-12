import unittest
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).parent

class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    class ResponseWrapper:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text
        def json(self):
            return json.loads(self.text)

    def post(self, path, json_data):
        req = urllib.request.Request(
            f"{self.base_url}{path}",
            data=json.dumps(json_data).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "TestClient"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return self.ResponseWrapper(resp.status, resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return self.ResponseWrapper(e.code, e.read().decode("utf-8"))

    def get(self, path):
        req = urllib.request.Request(f"{self.base_url}{path}", headers={"User-Agent": "TestClient"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return self.ResponseWrapper(resp.status, resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return self.ResponseWrapper(e.code, e.read().decode("utf-8"))

client = ApiClient()

class TestStagePipeline(unittest.TestCase):
    def setUp(self):
        self.demo_company = "测试大厂"
        self.demo_job = "多模态大模型算法工程师"
        self.demo_jd = "负责多模态大模型架构研发，熟悉 ViT、LLaVA、Projection 层与分布式训练。"
        self.demo_resume = """【基本信息】
测试候选人 | 13800138000 | test@test.com
【项目经历 1: 基于 LLaVA 架构的轻量化多模态对话大模型】
- 架构实现：基于 Qwen 与 CLIP 手动实现多模态投影层；
- 训练加速：引入 FlashAttention-2 提升吞吐。"""

    def test_01_export_stage_1(self):
        resp = client.post("/api/agent/export_stage", {
            "stage": 1,
            "company": self.demo_company,
            "job_title": self.demo_job,
            "jd": self.demo_jd,
            "resume": self.demo_resume,
            "repo_paths": []
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["stage"], 1)
        self.assertIn("inputs/stage_1_input.json", data["input_file"].replace("\\", "/"))
        self.assertIn("inputs/stage_1_prompt.txt", data["prompt_file"].replace("\\", "/"))
        self.assertTrue((BASE_DIR / "agent_llm_tasks" / "inputs" / "stage_1_input.json").exists())

    def test_02_export_stage_2_and_3(self):
        # Stage 2
        r2 = client.post("/api/agent/export_stage", {
            "stage": 2,
            "company": self.demo_company,
            "job_title": self.demo_job,
            "jd": self.demo_jd,
            "resume": self.demo_resume,
            "repo_paths": []
        })
        self.assertEqual(r2.status_code, 200)
        self.assertTrue((BASE_DIR / "agent_llm_tasks" / "inputs" / "stage_2_input.json").exists())

        # Stage 3
        r3 = client.post("/api/agent/export_stage", {
            "stage": 3,
            "company": self.demo_company,
            "job_title": self.demo_job,
            "jd": self.demo_jd,
            "resume": self.demo_resume,
            "repo_paths": []
        })
        self.assertEqual(r3.status_code, 200)
        self.assertTrue((BASE_DIR / "agent_llm_tasks" / "inputs" / "stage_3_input.json").exists())

    def test_03_stage_status(self):
        resp = client.get("/api/agent/stage_status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertIn("1", data["stages"])
        self.assertTrue(data["stages"]["1"]["input_exists"])

    def test_04_import_stage_1(self):
        # First ensure stage 1 output exists (created by mock)
        stage_1_file = BASE_DIR / "agent_llm_tasks" / "outputs" / "stage_1_output.json"
        if not stage_1_file.exists():
            import subprocess
            subprocess.run(["python", "agent_llm_tasks/run_pipeline.py", "--stage", "1", "--mock"], check=True)

        resp = client.post("/api/agent/import_stage", {
            "stage": 1,
            "current_resume": self.demo_resume
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["stage"], 1)
        self.assertIn("sop_0_resume_optimizer", data)
        self.assertIn("rewritten_resume", data)
        self.assertIn("测试候选人", data["rewritten_resume"])

    def test_05_import_stage_2_and_3(self):
        # Ensure outputs exist
        import subprocess
        subprocess.run(["python", "agent_llm_tasks/run_pipeline.py", "--stage", "2", "--mock"], check=True)
        subprocess.run(["python", "agent_llm_tasks/run_pipeline.py", "--stage", "3", "--mock"], check=True)

        # Stage 2 import
        r2 = client.post("/api/agent/import_stage", {"stage": 2})
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertTrue(d2["success"])
        self.assertIn("sop_1_matching", d2)
        self.assertIn("sop_2_star", d2)

        # Stage 3 import
        r3 = client.post("/api/agent/import_stage", {"stage": 3})
        self.assertEqual(r3.status_code, 200)
        d3 = r3.json()
        self.assertTrue(d3["success"])
        self.assertIn("sop_3_questions", d3)
        self.assertIn("mock_interviewer_prompt", d3)
        self.assertIn("sop_5_reverse", d3)
        self.assertIn("sop_6_cheatsheet", d3)

if __name__ == "__main__":
    unittest.main()
