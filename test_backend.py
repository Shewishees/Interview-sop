"""
后端接口与模块自动化验证脚本
"""
import sys
from pathlib import Path

# 保证 Windows 下 UTF-8 打印
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 确保能引用本目录
sys.path.insert(0, str(Path(__file__).parent))

from repo_scanner import RepoScanner
from knowledge_base import generate_expert_sop, DEFAULT_COMPANY, DEFAULT_JOB_TITLE, DEFAULT_JD, DEFAULT_RESUME
from llm_client import LLMClient

def test_all():
    print(">>> 1. 测试仓库扫描器 RepoScanner...")
    target_repo = str(Path(__file__).parent.parent)
    scanner = RepoScanner(target_repo)
    res = scanner.scan()
    assert res["success"] == True, f"扫描失败: {res.get('error')}"
    summary = res["summary"]
    print("   [OK] 成功识别仓库:", summary["root_name"])
    print("   [OK] 识别核心架构:", summary["model_architecture"])
    print("   [OK] 识别训练特征:", list(summary["training_specs"].keys()))
    print("   [OK] 识别关键亮点数:", len(summary["code_highlights"]))

    print("\n>>> 2. 测试专家 SOP 生成引擎...")
    sop = generate_expert_sop(
        company=DEFAULT_COMPANY,
        job_title=DEFAULT_JOB_TITLE,
        jd=DEFAULT_JD,
        resume=DEFAULT_RESUME,
        repo_info=res
    )
    assert "sop_1_matching" in sop
    assert "sop_2_star" in sop
    assert "sop_3_questions" in sop
    assert "sop_4_mock" in sop
    assert "sop_5_reverse" in sop
    assert "sop_6_cheatsheet" in sop
    print("   [OK] SOP-1 匹配得分:", sop["sop_1_matching"]["overall_score"])
    print("   [OK] SOP-2 STAR 项目数:", len(sop["sop_2_star"]))
    print("   [OK] SOP-3 考点题目数:", len(sop["sop_3_questions"]))
    print("   [OK] SOP-4 模拟面试轮次与风格:", len(sop["sop_4_mock"]["styles"]))
    print("   [OK] SOP-5 反问清单轮次:", len(sop["sop_5_reverse"]))

    print("\n>>> 3. 测试模拟面试评估引擎 (LLMClient)...")
    client = LLMClient()
    review = client.mock_review_answer(
        question="请介绍一下 Mini-LLaVA 项目中重写 CLIP forward 的技术细节",
        user_answer="我重写了 CLIP 的 VisualTransformer，保留了全部 197 个 patch 特征，跳过了原版的 CLS pooling 和投射矩阵，再用两层 MLP 投射到 1024 维。",
        round_num=1
    )
    assert "score" in review
    assert "evaluation" in review
    assert "improvements" in review
    assert "polished_answer" in review
    assert "next_question" in review
    print(f"   [OK] 智能打分: {review['score']} / 100")
    print(f"   [OK] 评价: {review['evaluation']}")
    print(f"   [OK] 下一轮追问: {review['next_question']}")

    print("\n==========================================")
    print("🎉 所有底层核心引擎与逻辑自动化测试全部通过！")
    print("==========================================")

if __name__ == "__main__":
    test_all()
