# 🎯 InterviewSOP Master (技术面试全流程 SOP 智能备战系统)

<p align="center">
  <b>融合多代码仓库深度透视、大模型 Agent 协同流水线与工业级全流程 SOP 的技术面试备战平台</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Vue-3.x-4FC08D?logo=vuedotjs" alt="Vue 3" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwindcss" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg" alt="PRs Welcome" />
</p>

---

## 📖 项目愿景与设计哲学 (Vision & Philosophy)

技术面试早已告别单纯背诵八股文和刷 LeetCode 的旧时代。现代高阶技术面试（大厂架构师、算法专家、具身智能/大模型工程师）的核心痛点在于：
1. **项目描述空泛**：简历上的项目大多缺少强动词、量化指标与硬核工程壁垒，容易沦为“平庸流水账”；
2. **源码与八股脱节**：准备的八股文与候选人实际写过的代码割裂，面试官一旦结合真实仓库底层（如模型结构、显存分布、分布式训练、动态路由）追问，极易陷入被动；
3. **技术权衡说不清**：无法清晰回答面试官最致命的追问——“**为什么不选方案 B？你的技术权衡依据是什么？**”；
4. **缺少实战压测与临考速记**：缺乏高度拟真的面试官对抗追问与临场 30 分钟应急锦囊。

**InterviewSOP Master** 旨在打造一套**工业级、端到端闭环的技术面试备战流水线**。系统通过**本地代码仓库静态透视引擎**自动抓取真实工程亮点，串联 **7 大核心 SOP 模块**，并原生支持**外部大模型 Agent（Antigravity / Cursor / Claude / GPT 等）阶段协同工作流**，帮助候选人从“简历靶向精修”到“源码真题深挖”再到“反向提问策略”全维度提升竞争力。

---

## 🌟 核心特色与功能矩阵 (Features)

### 1. 🔍 多维信息智能接入与本地代码仓库静态透视
- **多工程并行透视 (`RepoScanner`)**：
  - 本地直接挂载候选人的真实代码仓库（如自研多模态框架、金融投研 Agent、分布式训练项目等）；
  - 自动 AST 与规则语法分析，深度识别：模型 Backbone（Vision Encoder / LLM / Projector 维度）、分布式并行方案（FSDP / DeepSpeed ZeRO-1/2/3）、训练超参、显存优化（FlashAttention、Activation Checkpointing）与核心关键脚本；
  - 提供全盘可视化目录选择器，支持实时扫描与亮点一键重算。
- **简历全格式智能解析与数据清洗**：
  - 原生集成 `pypdf` 引擎，支持 PDF、Markdown、纯文本简历文件极速上传解析；
  - 自动剔除二进制零字符、多余制表符与非打印乱码，保留高保真排版。
- **目标岗位 JD 针对性对齐**：
  - 自由录入目标公司（如阿里、字节、同花顺、商汤等）与目标职位职责要求；
  - 内置两套工业级开箱即用标杆演示数据（Mini-LLaVA 多模态端到端工程 + 金融投研 Agent 架构师）。

### 2. ⚡ 七大一体化 SOP 备战模块 (SOP 0 ~ 6)

| 模块 | 核心能力 | 产出价值 |
| :--- | :--- | :--- |
| **SOP-0 · 简历靶向精修重构** | 自动诊断项目 3 大失分盲区（动词弱、缺少量化、关键算法盲点），重构高分 STAR 子弹点 | 支持子弹点实时交互勾选微调，**一键永久回写并升级简历文本框** |
| **SOP-1 · 胜任力雷达与 Gap 画像** | 0-100 分量化画像、核心求职壁垒（杀手锏）、考查盲区深度预警 | 输出 **面试前 72 小时冲刺优先级清单 (Sprint Roadmap)**，指引黄金突击路径 |
| **SOP-2 · STAR 复盘与权衡决策矩阵** | 四段式硬核技术拆解、致命陷阱连环追问与满分破局话术 | **独创技术决策权衡对比矩阵 (Trade-off Matrix)**，击破大厂面试官“为什么不选方案 B”连环追问 |
| **SOP-3 · 源码结合型定制真题库** | 结合候选人真实代码与业务场景定制 4 道大厂级高频实战深挖题 | 配备 **三层逐级加分锦囊** 与 **30 秒黄金回答破局框架**，彻底告别八股死记 |
| **SOP-4 · AI 沉浸式模拟面试官** | 动态合成涵盖背景与深挖逻辑的 Master Prompt，支持 3 种面试官风格（极客狂/架构师/业务官） | 在线多轮对练打分，逐轮提供扣分点诊断与润色示范 |
| **SOP-5 · 分轮次高阶反向提问策略库** | 技术一面/二面、技术总监三面、HR 终面深度反问清单 | 展现高阶业务敏锐度、团队领导力潜质与组织协同视野 |
| **SOP-6 · 30 分钟临考速记卡** | 关键工程量化指标速查、核心避坑心法与破局口诀 | 支持一键导出排版精美的 **完整 Markdown 备战手册战报** |

### 3. 🤖 外部 Agent 协同流水线 (3-Stage Milestone Workflow)
除了系统内置的极速生成能力外，系统针对复杂工程场景构建了**人机协同的标准阶段式工单流**：
- **标准技能常驻契约 (`agent_llm_tasks/SKILL.md`)**：严格定义每个阶段工单的 JSON Schema 与任务边界，外部 Agent 可直接理解并精准输出；
- **阶段一 (Stage 1 · Resume Optimizer)**：基础资料 ➔ 导出工单 ➔ Agent 深度精修 ➔ 读取产物并重塑简历；
- **阶段二 (Stage 2 · Matching & STAR)**：已重塑简历 ➔ 导出工单 ➔ Agent 深度评估 ➔ 装载匹配画像与权衡矩阵；
- **阶段三 (Stage 3 · Questions & Mock)**：权衡已定 ➔ 导出工单 ➔ Agent 生成源码真题 ➔ 解锁模拟对练与速记；
- **智能降级与自动预装**：具备 **4 级容错机制**，在外部 Agent 未运行时，点击任意阶段均可**一键预装官方标准示范成果**，杜绝 404 阻断，即开即用。

---

## 🏗️ 架构设计 (Architecture)

```text
[用户输入: 岗位JD / 简历文件 / 本地代码库]
           │
           ▼
[FastAPI 后端核心 (app.py)]
   ├─► RepoScanner 本地代码静态透视 (AST / 超参 / 分布式架构)
   ├─► PDF/Text 智能解析与清洗引擎
   │
   ▼
[双模驱动引擎]
   ├─► 模式 1: 内置专家规则 & LLMClient 实时极速生成
   └─► 模式 2: 3 大阶段外部 Agent 协同流水线 (agent_llm_tasks/)
           ├─ Stage 1: 简历针对性精修工单 (SOP-0)
           ├─ Stage 2: 胜任力雷达与 STAR 权衡矩阵 (SOP-1, SOP-2)
           └─ Stage 3: 源码真题、Master 对练与速记 (SOP-3, 4, 5, 6)
   │
   ▼
[前端 Apple 极简毛玻璃交互界面 (Vue 3 + Tailwind + Element Plus)]
   ├─ 阶段工单导出 / 产物自动装载与智能兜底
   ├─ 简历子弹点自由编辑与一键回填
   ├─ 五维雷达交互画像与技术决策权衡矩阵
   ├─ 多风格模拟对练与 30 分钟速记口诀
   └─ 一键下载完整 SOP 备战手册 Markdown
```

---

## 🚀 极速上手 (Quick Start)

### 1. 环境准备
确保本地已安装 Python 3.10 或更高版本。

```bash
# 克隆仓库
git clone https://github.com/Shewishees/Interview-sop.git
cd Interview-sop

# 安装核心依赖
pip install -r requirements.txt
```

### 2. 一键启动服务
在项目根目录下直接运行：

```bash
python run.py
```

终端将启动 FastAPI 服务并**自动在系统默认浏览器中打开**：
```
http://127.0.0.1:8000
```

> **提示**：Windows 用户也可以直接双击根目录下的 `push_to_github.bat` 脚本快捷完成 GitHub 提交与推送。

---

## 💡 两种备战工作模式指引 (Usage Modes)

### 模式 A：单机极速体验模式（内置样例 / 一键直出）
1. 打开网页右上角 **【样例演示】** 菜单：
   - 可选择 `多模态具身智能 (Mini-LLaVA + OpenVLA)` 或 `金融投研大模型 Agent (同花顺)`；
2. 页面自动填入岗位 JD、精选高分简历与本地仓库路径；
3. 点击顶部 **【⚡ 一键直接分析生成全套 SOP】**；
4. 系统将根据内置专家规则库秒级合成 7 大板块完整战报。

### 模式 B：外部 Agent 深度协同流水线模式（推荐工业级精细打磨）
当需要针对您自己的私有大型项目进行深度复盘时，推荐使用顶部 **【Agent 协同三阶段工作流】**：
1. **阶段一（靶向精修）**：
   - 录入您的个人简历与代码库；
   - 点击 **【导出阶段一工单】**，工单自动保存在 `agent_llm_tasks/inputs/`；
   - 让您的外部 Agent（如 Cursor / Antigravity / Claude）读取 `agent_llm_tasks/SKILL.md` 与输入文件完成深度精修；
   - 返回页面点击 **【读取阶段一产物】**（或点击 **【⚡ 一键预装示范成果】**），页面自动应用优化后的 STAR 描述并回写简历输入框；
2. **阶段二（胜任匹配与权衡决策）**：
   - 点击进入阶段二，导出工单并交由 Agent 评估；
   - 读取产物后，解锁 5 维雷达匹配分、Gap 诊断以及“为什么不选方案 B”的权衡矩阵；
3. **阶段三（源码真题与模拟对练）**：
   - 导出工单，Agent 结合代码细节生成定制真题；
   - 读取后即可解锁 4 道硬核真题、加分锦囊与 30 分钟临考速记口诀；
4. 点击右上角 **【下载完整 SOP 备战手册】**，保存为离线 Markdown。

---

## 📁 详细目录结构 (Project Layout)

```text
Interview-sop/
├── app.py                          # FastAPI 后端服务主入口（API 路由、规范化清洗、多阶段工单调度）
├── knowledge_base.py               # 内置专家知识库、标杆示范工程数据与离线生成引擎
├── llm_client.py                   # 大模型客户端适配器（支持 DeepSeek / OpenAI / 自定义代理）
├── repo_scanner.py                 # 本地代码仓库静态特征透视引擎（AST、超参、分布式策略解析）
├── run.py                          # 一键启动脚本（环境检查、服务拉起、自动打开浏览器）
├── requirements.txt                # 运行环境核心依赖清单
├── LICENSE                         # MIT 开源许可证
├── README.md                       # 项目全景使用与架构文档
├── push_to_github.bat              # Windows 一键安全推送 GitHub 辅助脚本
├── static/                         # 前端单页 Web 应用
│   ├── index.html                  # 交互主页面（Vue 3 + TailwindCSS + Element Plus + Lucide Icons）
│   └── vendor/                     # 离线前端静态依赖库
└── agent_llm_tasks/                # 外部 Agent 协同核心工作区
    ├── SKILL.md                    # 工业级标准化 Agent Skill 契约规范
    ├── run_pipeline.py             # 离线验证与流水线任务自动聚合执行脚本
    ├── inputs/                     # 阶段工单导出目录（stage_1/2/3_input.json, prompt.txt）
    ├── outputs/                    # 阶段成果落盘目录（stage_1/2/3_output.json, example_output.json）
    ├── task_0_resume_optimizer/    # 任务 0 专属定义与 JSON Schema
    ├── task_1_matching_radar/      # 任务 1 专属定义与 JSON Schema
    ├── task_2_star_tradeoff/       # 任务 2 专属定义与 JSON Schema
    ├── task_3_questions_bank/      # 任务 3 专属定义与 JSON Schema
    ├── task_4_mock_interviewer/    # 任务 4 专属定义与 JSON Schema
    ├── task_5_reverse_interview/   # 任务 5 专属定义与 JSON Schema
    └── task_6_cheatsheet/          # 任务 6 专属定义与 JSON Schema
```

---

## ⚙️ 大模型 API 配置（可选）

系统默认处于**高精度离线专家规则库模式**，无需配置任何 API Key 即可体验全部完整功能。

若需要针对生僻自定义岗位调用公网大模型实时扩写，可在系统环境变量中配置：

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-your-deepseek-api-key"
$env:DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"

# Linux / macOS
export DEEPSEEK_API_KEY="sk-your-deepseek-api-key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
```

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q1: 点击读取产物时，如果外部 Agent 还没生成文件会报错吗？</b></summary>
<b>绝对不会。</b> 系统内置了完善的 4 级智能容错机制。若未检测到本地 <code>stage_X_output.json</code>，系统会自动兜底并预装官方标准示范成果，以 200 OK 顺畅渲染页面，绝无 404 错误阻断。
</details>

<details>
<summary><b>Q2: 扫描本地代码仓库会上传我的私有代码到公网吗？</b></summary>
<b>绝对不会。</b> <code>repo_scanner.py</code> 是纯本地静态解析脚本，仅在本地提取文件结构、模型组件名与超参关键特征，全程零网络外传，隐私与代码绝对安全。
</details>

<details>
<summary><b>Q3: 上传的 PDF 简历解析出来会不会乱码？</b></summary>
系统使用 <code>pypdf</code> 进行精准文字层提取，并由后端正则清洗非打印字符、制表符与多余空行。若遇到纯图片扫描件 PDF，建议使用 OCR 工具或直接将文字复制粘贴进简历文本框。
</details>

---

## 🤝 贡献与反馈 (Contributing)

欢迎提交 Issue 与 Pull Request！
- 代码规范：建议遵循 PEP 8 规范；
- 前端规范：保持 Apple 极简毛玻璃审美风格，兼顾深色与浅色自适应体验。

---

## 📄 开源许可证 (License)

本项目基于 [MIT License](LICENSE) 协议开源。
