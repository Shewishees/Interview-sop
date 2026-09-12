# Task 1: 岗位匹配度量化与雷达画像 (Matching & Radar)

## 📌 任务定位
全面对比目标岗位 JD 的任职要求与候选人的全栈能力（涵盖科班基础、模型算法、工程分布式、前沿工具效率等），输出量化的匹配分（0~100）、5 维雷达图评分、3 大核心差异化优势（Key Strengths）、劣势差距弥补建议（Skill Gaps）与考前突击优先级（Sprint Priorities）。

## 🧠 思维链推理指引
1. **多维度能力解构**：
   - 维度 1：核心算法与架构（如多模态对齐 / Agent 推理规划）；
   - 维度 2：底层训练与显存工程（如 FSDP、LoRA、FlashAttention、CUDA）；
   - 维度 3：数据流与评估闭环（如多轮增量编码、高质量数据集清洗、仿真评测）；
   - 维度 4：计算机科班功底与系统素养（如 C++、数据结构、编译原理、云计算）；
   - 维度 5：AI 编程效率与极客解决问题能力（如 Cursor、Claude Code、Vibe Coding）。
2. **差异化壁垒提炼 (Key Strengths)**：
   - 必须突出“源码级复现与改写”而非简单调包；
   - 必须指出候选人跨领域的潜在迁移优势（如具身机械臂控制逻辑向金融多源时序预测的迁移）。
3. **输出格式**：
   - 必须严格遵循 `output_schema.json`，产出 `overall_score`, `radar_dimensions`, `key_strengths`, `skill_gaps`, `sprint_priorities`。
