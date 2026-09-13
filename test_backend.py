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
from app import get_or_create_stage_data, normalize_stage_1, normalize_stage_2, normalize_stage_3

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

    print("\n>>> 2. 测试专家 SOP 生成引擎 (knowledge_base)...")
    sop = generate_expert_sop(
        company=DEFAULT_COMPANY,
        job_title=DEFAULT_JOB_TITLE,
        jd=DEFAULT_JD,
        resume=DEFAULT_RESUME,
        repos_info=[res]
    )
    assert "sop_1_matching" in sop
    assert "sop_2_star" in sop
    assert "sop_3_questions" in sop
    assert "sop_4_mock_prompt" in sop or "sop_4_prompt_builder" in sop or "default_mock_prompt" in sop
    assert "sop_5_reverse" in sop
    assert "sop_6_cheatsheet" in sop
    print("   [OK] SOP-1 匹配得分:", sop["sop_1_matching"]["overall_score"])
    print("   [OK] SOP-2 STAR 项目数:", len(sop["sop_2_star"]))
    print("   [OK] SOP-3 考点题目数:", len(sop["sop_3_questions"]))
    print("   [OK] SOP-5 反问清单轮次:", len(sop["sop_5_reverse"]))

    print("\n>>> 3. 测试 3 阶段 Agent-Native 规范化层与智能兜底预装...")
    # Stage 1
    s1_data, s1_preloaded = get_or_create_stage_data(1, force_mock=True)
    projs = normalize_stage_1(s1_data)
    assert len(projs) > 0, "Stage 1 产物未规范化出项目"
    assert "refined_bullet_points" in projs[0]
    print(f"   [OK] Stage 1 自动预装就绪: 解析出 {len(projs)} 个精修工程项目")

    # Stage 2
    s2_data, s2_preloaded = get_or_create_stage_data(2, force_mock=True)
    matching, star = normalize_stage_2(s2_data)
    assert "overall_score" in matching
    assert len(matching.get("radar_dimensions", [])) >= 5
    assert len(star) > 0
    print(f"   [OK] Stage 2 自动预装就绪: 胜任分 {matching['overall_score']}, STAR 项目 {len(star)} 个")

    # Stage 3
    s3_data, s3_preloaded = get_or_create_stage_data(3, force_mock=True)
    q, mock_p, rev, cheat = normalize_stage_3(s3_data)
    assert len(q) > 0
    assert len(mock_p) > 0
    assert len(rev) > 0
    assert len(cheat) > 0
    print(f"   [OK] Stage 3 自动预装就绪: 题库 {len(q)} 题, Master Prompt 长度 {len(mock_p)} 字符, 反问 {len(rev)} 组, 速记 {len(cheat)} 条")

    print("\n==========================================")
    print("🎉 纯 Agent-Native 架构核心引擎与流水线测试全部通过！")
    print("==========================================")

if __name__ == "__main__":
    test_all()
