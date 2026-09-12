#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interview SOP Agent Pipeline Tool (Agent 任务流水线验证与聚合工具)

功能：
1. 校验 (Validate): 验证 Agent 生成的 JSON 输出是否符合各自模块与阶段的 JSON Schema
2. 阶段支持 (Stage): 支持 --stage 1 | 2 | 3 分阶段独立校验与模拟生成
3. 聚合 (Aggregate): 将各 stage 或各 task_* 独立结果合并为最终系统全量 output.json
4. 模拟 (Mock): 使用基准样例一键生成阶段或全局标准成果，供本地联调

用法：
  python run_pipeline.py --stage 1 --validate
  python run_pipeline.py --stage 1 --mock
  python run_pipeline.py --aggregate
  python run_pipeline.py --validate outputs/output.json
"""

import sys
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).parent

TASK_SCHEMAS = {
    "sop_0_resume_optimizer": BASE_DIR / "task_0_resume_optimizer" / "output_schema.json",
    "sop_1_matching": BASE_DIR / "task_1_matching_radar" / "output_schema.json",
    "sop_2_star": BASE_DIR / "task_2_star_tradeoff" / "output_schema.json",
    "sop_3_questions": BASE_DIR / "task_3_questions_bank" / "output_schema.json",
    "mock_interviewer_prompt": BASE_DIR / "task_4_mock_interviewer" / "output_schema.json",
    "sop_5_reverse": BASE_DIR / "task_5_reverse_interview" / "output_schema.json",
    "sop_6_cheatsheet": BASE_DIR / "task_6_cheatsheet" / "output_schema.json"
}

STAGE_KEYS = {
    1: ["sop_0_resume_optimizer"],
    2: ["sop_1_matching", "sop_2_star"],
    3: ["sop_3_questions", "mock_interviewer_prompt", "sop_5_reverse", "sop_6_cheatsheet"]
}

STAGE_FILES = {
    1: BASE_DIR / "outputs" / "stage_1_output.json",
    2: BASE_DIR / "outputs" / "stage_2_output.json",
    3: BASE_DIR / "outputs" / "stage_3_output.json"
}

def validate_data_against_schema(data: dict, schema_path: Path) -> tuple[bool, str]:
    """简易轻量级 Schema 结构校验器"""
    if not schema_path.exists():
        return False, f"Schema 文件未找到: {schema_path}"
    
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"解析 Schema 失败: {e}"
    
    required_keys = schema.get("required", [])
    for rk in required_keys:
        if rk not in data:
            return False, f"缺失顶级必填键: '{rk}'"
        
        expected_type = schema.get("properties", {}).get(rk, {}).get("type")
        val = data[rk]
        if expected_type == "array" and not isinstance(val, list):
            return False, f"字段 '{rk}' 应为 List 数组，实际为 {type(val).__name__}"
        elif expected_type == "object" and not isinstance(val, dict):
            return False, f"字段 '{rk}' 应为 Object 字典，实际为 {type(val).__name__}"
        elif expected_type == "string" and not isinstance(val, str):
            return False, f"字段 '{rk}' 应为 String 字符串，实际为 {type(val).__name__}"
            
    return True, "校验通过"

def validate_file(filepath: Path, expected_keys: list = None) -> bool:
    print(f"🔍 正在校验文件: {filepath} ...")
    if not filepath.exists():
        print(f"❌ 错误: 文件不存在 -> {filepath}")
        return False
    
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ JSON 语法解析失败: {e}")
        return False

    all_passed = True
    matched_any = False
    keys_to_check = expected_keys if expected_keys else TASK_SCHEMAS.keys()

    for key in keys_to_check:
        schema_p = TASK_SCHEMAS.get(key)
        if not schema_p:
            continue
        if key in data:
            matched_any = True
            ok, msg = validate_data_against_schema({key: data[key]}, schema_p)
            if ok:
                print(f"  ✓ 模块 [{key}] 校验通过")
            else:
                print(f"  ✗ 模块 [{key}] 校验失败: {msg}")
                all_passed = False
        elif expected_keys:
            print(f"  ✗ 缺失该阶段必需的模块: [{key}]")
            all_passed = False

    if not matched_any and not expected_keys:
        print("  ⚠️ 未在文件中检测到任何 SOP 顶级字段")
        return False

    if all_passed:
        print(f"🎉 文件 [{filepath.name}] 校验通过，完全符合规范！")
    return all_passed

def validate_stage(stage_num: int) -> bool:
    if stage_num not in STAGE_FILES:
        print(f"❌ 未知阶段: {stage_num}")
        return False
    target_file = STAGE_FILES[stage_num]
    expected_keys = STAGE_KEYS[stage_num]
    print(f"--- 校验 阶段 {stage_num} 成果 ---")
    return validate_file(target_file, expected_keys)

def mock_stage(stage_num: int):
    example_file = BASE_DIR / "outputs" / "example_output.json"
    if not example_file.exists():
        print(f"❌ 找不到参考基准文件: {example_file}")
        return
    full_data = json.loads(example_file.read_text(encoding="utf-8"))
    
    keys = STAGE_KEYS.get(stage_num, [])
    stage_data = {k: full_data[k] for k in keys if k in full_data}
    
    dst = STAGE_FILES[stage_num]
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(stage_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✨ 成功模拟生成 阶段 {stage_num} 产物 -> {dst}")

def aggregate_tasks(output_file: Path = None):
    if output_file is None:
        output_file = BASE_DIR / "outputs" / "output.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print("📦 正在扫描并聚合阶段产物与子任务成果...")
    aggregated = {}

    # 1. 优先从 stage_1_output.json, stage_2_output.json, stage_3_output.json 读取
    for st_num in [1, 2, 3]:
        st_file = STAGE_FILES[st_num]
        if st_file.exists():
            try:
                st_data = json.loads(st_file.read_text(encoding="utf-8"))
                for k in STAGE_KEYS[st_num]:
                    if k in st_data:
                        aggregated[k] = st_data[k]
                        print(f"  ✓ 从 stage_{st_num}_output.json 装载模块: {k}")
            except Exception as e:
                print(f"  ⚠️ 读取 {st_file} 出错: {e}")

    # 2. 从各个 task_* 目录补充缺失模块
    task_dirs = [
        ("task_0_resume_optimizer", "sop_0_resume_optimizer"),
        ("task_1_matching_radar", "sop_1_matching"),
        ("task_2_star_tradeoff", "sop_2_star"),
        ("task_3_questions_bank", "sop_3_questions"),
        ("task_4_mock_interviewer", "mock_interviewer_prompt"),
        ("task_5_reverse_interview", "sop_5_reverse"),
        ("task_6_cheatsheet", "sop_6_cheatsheet")
    ]

    for dir_name, key in task_dirs:
        if key not in aggregated:
            task_out = BASE_DIR / dir_name / "output.json"
            if task_out.exists():
                try:
                    task_data = json.loads(task_out.read_text(encoding="utf-8"))
                    if key in task_data:
                        aggregated[key] = task_data[key]
                        print(f"  ✓ 从 {dir_name}/output.json 补充装载 -> {key}")
                    else:
                        aggregated[key] = task_data
                        print(f"  ✓ 从 {dir_name}/output.json 补充装载 (直接作为 {key})")
                except Exception as e:
                    print(f"  ⚠️ 读取 {task_out} 出错: {e}")

    output_file.write_text(json.dumps(aggregated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 聚合完成！已生成全量 SOP 成果: {output_file} (包含 {len(aggregated)} 个模块)")

def mock_demo():
    src = BASE_DIR / "outputs" / "example_output.json"
    dst = BASE_DIR / "outputs" / "output.json"
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"✨ 成功模拟生成 output.json -> {dst}")
        # 同步生成各 stage 产物方便测试
        for s in [1, 2, 3]:
            mock_stage(s)
    else:
        print("❌ example_output.json 不存在！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interview SOP Agent 流水线工具")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3], help="指定阶段 (1, 2 或 3)")
    parser.add_argument("--validate", nargs="?", const="DEFAULT", help="验证指定文件或当前阶段")
    parser.add_argument("--aggregate", action="store_true", help="聚合各个阶段产物为 outputs/output.json")
    parser.add_argument("--mock", action="store_true", help="一键模拟生成阶段或全量标准成果")
    
    args = parser.parse_args()

    if args.stage:
        if args.mock:
            mock_stage(args.stage)
        elif args.validate or args.validate == "DEFAULT":
            validate_stage(args.stage)
        else:
            print(f"提示: 请配合 --validate 或 --mock 使用 --stage {args.stage}")
    elif args.validate and args.validate != "DEFAULT":
        validate_file(Path(args.validate))
    elif args.aggregate:
        aggregate_tasks()
    elif args.mock:
        mock_demo()
    else:
        print("未指定参数，默认执行全量 example_output.json 校验与 stage 模拟测试:")
        validate_file(BASE_DIR / "outputs" / "example_output.json")
