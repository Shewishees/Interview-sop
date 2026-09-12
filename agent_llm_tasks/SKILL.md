---
name: interview-sop-pipeline
description: 负责分阶段（阶段一·简历靶向精修 ➔ 阶段二·胜任匹配与STAR权衡 ➔ 阶段三·源码真题与对练速记）或全流程处理 InterviewSOP Master 的大模型深度推理工单，基于工程代码事实输出严格符合 JSON 规范的高分面试战略成果。
---

# 🤖 InterviewSOP Pipeline 外部 Agent 核心执行技能 (Skill)

本技能常驻于 `agent_llm_tasks` 目录，专为外部智能体（Claude Code, Cursor Agent, Antigravity, AutoGPT 或自定义 LLM 脚本）设计。

你的目标是：根据当前阶段导出的输入文件，结合代码仓库真实实现细节与目标岗位 JD，分阶段生成高质量、无幻觉、结构化的高分面试 SOP 产物。

---

## 🧭 阶段式执行工作流 (Stage-by-Stage Execution)

系统采用 **3 大里程碑阶段** 渐进式流转。用户在 Web 页面每完成一步资料准备后会导出工单，你只需按对应阶段执行：

| 阶段 | 任务目标 | 输入文件 | 对应子任务包 | 产出文件 | 校验指令 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Stage 1** | **简历靶向精修重构**<br>诊断失分盲区，重构高分子弹点 | `inputs/stage_1_input.json` | `task_0_resume_optimizer/` | `outputs/stage_1_output.json` | `python run_pipeline.py --stage 1 --validate` |
| **Stage 2** | **岗位胜任匹配与 STAR 矩阵**<br>五维雷达评估、求职杀手锏与技术选型权衡 | `inputs/stage_2_input.json` | `task_1_matching_radar/`<br>`task_2_star_tradeoff/` | `outputs/stage_2_output.json` | `python run_pipeline.py --stage 2 --validate` |
| **Stage 3** | **源码真题、模拟对练与速记**<br>定制题库与加分锦囊、Master Prompt、30min口诀 | `inputs/stage_3_input.json` | `task_3_questions_bank/`<br>`task_4_mock_interviewer/`<br>`task_5_reverse_interview/`<br>`task_6_cheatsheet/` | `outputs/stage_3_output.json` | `python run_pipeline.py --stage 3 --validate` |

---

## 📋 各阶段执行细则与防幻觉指令

### 🌟 阶段一：简历靶向精修重构 (Stage 1)
1. **读取输入**：读取 `inputs/stage_1_input.json`（包含公司、岗位、JD、初始简历、本地代码仓库事实）。
2. **诊断原则**：
   - 拒绝泛泛而谈，必须对原简历每个重点项目诊断 **3 大核心失分盲区**（动词表现力弱、缺乏量化硬核指标、缺少底层算法实现盲点）。
   - 重构的 **高分 STAR 子弹点（3~4条）** 必须严格锚定真实代码仓库事实（如张量维度、激活函数、显存优化技术）。
3. **写入产物**：输出保存至 `outputs/stage_1_output.json`，结构如下：
   ```json
   {
     "sop_0_resume_optimizer": [
       {
         "project_name": "项目名称",
         "original_section": "原描述文字",
         "target_role_points": ["核心考点1", "核心考点2"],
         "diagnostic_flaws": [
           { "type": "verb_weakness", "label": "动词表现力", "issue": "原描述问题", "solution": "破局话术" },
           { "type": "metric_absence", "label": "量化与工程壁垒", "issue": "缺少硬核指标", "solution": "补充收益指标" },
           { "type": "algo_blindspot", "label": "关键算法盲点", "issue": "未提及核心算法", "solution": "深入底层原理" }
         ],
         "optimized_bullets": [
           "【架构自研重构】...",
           "【两阶段流水线训练】...",
           "【数据工程与分词防漂移】..."
         ]
       }
     ]
   }
   ```
4. **校验命令**：执行 `python run_pipeline.py --stage 1 --validate`。

---

### 🌟 阶段二：胜任匹配与 STAR 权衡决策矩阵 (Stage 2)
1. **读取输入**：读取 `inputs/stage_2_input.json`（包含由用户在页面确认重写的优质简历文本 + JD + 代码仓库透视）。
2. **执行重点**：
   - **Task 1 胜任力雷达**：评估 5 个关键维度的得分（0~100）及详尽理由，提炼 3 条杀手锏（求职核心差异化壁垒），诊断 2 项 Gap 及备战建议，输出综合匹配分（80~98）与 72 小时冲刺清单。
   - **Task 2 STAR 复盘**：按 SITUATION / TASK / ACTION / RESULT 四段式深度复盘，并构建**核心技术决策权衡对比矩阵 (Trade-off Matrix)**，重点输出“秒杀‘为什么不选方案B’”。
3. **写入产物**：输出保存至 `outputs/stage_2_output.json`，结构包含 `sop_1_matching` 与 `sop_2_star`。
4. **校验命令**：执行 `python run_pipeline.py --stage 2 --validate`。

---

### 🌟 阶段三：源码真题、模拟对练与临考速记 (Stage 3)
1. **读取输入**：读取 `inputs/stage_3_input.json`。
2. **执行重点**：
   - **Task 3 源码真题**：定制 4 道大厂高频考题，每题包含【一句活定性】、【结构对比/核心原理】、【源码实现细节】与【高分加分锦囊】；
   - **Task 4 模拟面试官 Master Prompt**：根据候选人真实经历与代码事实，生成可直接投喂给大模型的严格冷峻主考官 Prompt；
   - **Task 5 反向提问策略**：分轮次（技术一面/二面、总监三面、HR面）设计高阶反问清单；
   - **Task 6 30分钟临考速记**：提炼 5 组核心数字指标（如隐层维度、学习率、显存、PPL）与 3 条应答避坑心法口诀。
3. **写入产物**：输出保存至 `outputs/stage_3_output.json`。
4. **校验命令**：执行 `python run_pipeline.py --stage 3 --validate`。

---

## 🛠️ 辅助命令一览 (CLI Helper Commands)

在当前目录可以直接运行以下命令协助调试与自动化：

- 校验指定阶段产物格式：
  ```bash
  python run_pipeline.py --stage 1 --validate
  python run_pipeline.py --stage 2 --validate
  python run_pipeline.py --stage 3 --validate
  ```
- 快速生成某阶段的基准示范产物（用于快速测试）：
  ```bash
  python run_pipeline.py --stage 1 --mock
  python run_pipeline.py --stage 2 --mock
  python run_pipeline.py --stage 3 --mock
  ```
- 将 3 个阶段的产物一键合并为全套全局产物 `output.json`：
  ```bash
  python run_pipeline.py --aggregate
  ```
- 校验全局 `outputs/output.json` 完整性：
  ```bash
  python run_pipeline.py --validate outputs/output.json
  ```
