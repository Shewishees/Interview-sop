# 🤖 Interview SOP Agent 任务工单与大模型交互指南 (Agent LLM Tasks)

本目录将整个 **大厂面试冲刺全流程 SOP 系统** 中所有需要大语言模型（LLM）进行深度推理、诊断、生成与对齐的高阶任务，全部解耦并封装为独立的 Agent 任务工单包。

你可以将本文件夹直接交给任何外部智能体（如 Claude Code, Gemini CLI, Cursor, AutoGPT, LangGraph 或自定义脚本），或直接调用外部大模型 API 进行批量处理。

---

## 📂 目录结构与工单说明

```
agent_llm_tasks/
│
├── README.md                      # [本文档] 顶层 Agent 任务执行总纲与 SOP 交互协议
├── run_pipeline.py                # 流水线工具 (格式校验 --validate, 任务聚合 --aggregate, 快速模拟 --mock)
│
├── inputs/                        # 输入上下文存放区
│   ├── example_context.json       # 基准输入样例 (包含目标公司、JD、候选人简历、本地代码仓库真实事实)
│   └── current_context.json       # Web 界面实时导出的用户实际输入数据
│
├── outputs/                       # 最终产物生成区
│   ├── example_output.json        # 7 大模块全套标准输出示范
│   └── output.json                # Agent 生成或聚合后的全局最终产物 (可直接回填至 Web 系统)
│
├── task_0_resume_optimizer/       # 任务 0: 简历靶向精修与高分子弹点重构 (Resume Optimizer)
│   ├── README.md                  # 任务要求、CoT 推理引导与失分盲区诊断规范
│   ├── system_prompt.txt          # 面向 LLM 的系统角色设定与提示词指令
│   └── output_schema.json         # 严格的 JSON Schema 输出约束
│
├── task_1_matching_radar/         # 任务 1: 5维胜任力雷达与面试冲刺策略 (Matching & Radar)
│   ├── README.md                  # 岗位动态匹配、短板发现与优先级排序说明
│   ├── system_prompt.txt          # 匹配评估专家提示词
│   └── output_schema.json         # 维度、得分与优劣势输出约束
│
├── task_2_star_tradeoff/          # 任务 2: 硬核 STAR 故事与技术权衡决策矩阵 (STAR & Trade-off)
│   ├── README.md                  # 代码事实锚定、方案对比决策矩阵与避坑话术
│   ├── system_prompt.txt          # 顶尖技术架构师提示词
│   └── output_schema.json         # STAR + Trade-off Matrix + Pitfalls 约束
│
├── task_3_questions_bank/         # 任务 3: 大厂定制真题库与加分破局锦囊 (Questions Bank)
│   ├── README.md                  # 底层代码深度追问、三层回答框架与加分锦囊
│   ├── system_prompt.txt          # 大厂首席算法面试官提示词
│   └── output_schema.json         # 4 道高频真题输出约束
│
├── task_4_mock_interviewer/       # 任务 4: 专属定制模拟面试官 Master Prompt (Mock Interviewer)
│   ├── README.md                  # 1v1 真机交互、5段式严厉诊断规则说明
│   ├── system_prompt.txt          # Prompt 架构师提示词
│   └── output_schema.json         # Master Prompt 字符串输出约束
│
├── task_5_reverse_interview/      # 任务 5: 分轮次高阶反向提问策略 (Reverse Interview)
│   ├── README.md                  # 一面/二面架构骨干、三面总监、HR面反向提问要点
│   ├── system_prompt.txt          # 招聘委员会导师提示词
│   └── output_schema.json         # 分轮次反向问题清单输出约束
│
└── task_6_cheatsheet/             # 任务 6: 30分钟临考极速抢分速记卡 (Cheatsheet)
    ├── README.md                  # 5 大必背核心参数与 3 条应答黄金法则
    ├── system_prompt.txt          # 临考提分导师提示词
    └── output_schema.json         # key_numbers 与 golden_rules 输出约束
```

---

## ⚡ 极速开始：外部 Agent 如何处理此任务包？

### 模式 A：由智能体一次性全局生成（推荐）
如果你使用的 Agent（例如 Claude 3.5 Sonnet / GPT-4o）具备超长上下文与强大的多任务规划能力：
1. **读取输入**：读取 `inputs/current_context.json`（若无则参考 `inputs/example_context.json`）。
2. **理解规范**：参考各 `task_*/README.md` 与 `system_prompt.txt` 中对每个模块的深度要求与防幻觉指令（**必须死磕代码库事实，拒绝空洞概念**）。
3. **生成输出**：直接生成完整的 JSON 并保存到 `outputs/output.json`。格式参照 `outputs/example_output.json`。
4. **格式校验**：
   ```bash
   python run_pipeline.py --validate outputs/output.json
   ```

### 模式 B：分步独立处理各子任务（模块化）
如果你希望针对每个子任务单独指派 Agent，或者需要人工分步审核：
1. **针对 Task N**：
   - 提取输入：`inputs/example_context.json`
   - 输入 Prompt：`task_N/system_prompt.txt`
   - 要求模型输出 JSON：保存为 `task_N/output.json`
2. **校验子任务**：
   ```bash
   python run_pipeline.py --validate task_N/output.json
   ```
3. **一键聚合**：
   全部子任务完成后，运行以下命令自动合成最终产物：
   ```bash
   python run_pipeline.py --aggregate
   ```
   该命令会将各子任务的产物自动合并为 `outputs/output.json`。

---

## 🔄 与 Web 系统的无缝双向联动

本 SOP 系统前端 Web 界面已内置与本任务包的双向交互能力：

1. **导出给 Agent**：
   - 在 Web 页面右上角点击 **【🤖 导出给 Agent】**；
   - 系统自动将你当前填写的岗位、简历、JD 以及扫描到的本地代码库特征打包并保存至 `agent_llm_tasks/inputs/current_context.json`，同时支持浏览器下载 `input_context.json`。
2. **装载 Agent 成果**：
   - 当 Agent 执行完毕并生成 `agent_llm_tasks/outputs/output.json` 后；
   - 在 Web 页面右上角点击 **【📥 装载 Agent 成果】**；
   - 系统会自动校验并一键填充所有 7 个 SOP 面板（SOP-0 简历精修、SOP-1 雷达、SOP-2 STAR与矩阵、SOP-3 题库、SOP-4 模拟面试官、SOP-5 反向提问、SOP-6 临考速记卡），即可在线交互并支持一键打印/导出 PDF！

---

## 🛡️ Anti-Hallucination（防大模型幻觉）核心准则
在提示 Agent 时，必须提醒 Agent 遵守以下铁律：
1. **代码事实优先**：严禁无中生有凭空捏造未实现的技术（例如将未用过的 DeepSpeed 描述为核心自研），必须紧密依托 `code_highlights` 和 `model_architecture` 中扫描到的客观事实；
2. **量化指标严谨**：引用具体参数（如 197 个 patch、1.8M 参数、768->1024 映射、4卡 4090 FSDP、收敛 PPL 变化等）时，必须与上下文数据保持前后绝对一致；
3. **技术权衡真实**：Trade-off 决策必须讲清“为什么不选备选方案 B 的真实代价（显存/计算量/延迟/工程复杂度）”，拒绝空洞八股。
