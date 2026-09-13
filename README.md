# 🎯 InterviewSOP Master (技术面试全流程 SOP 智能备战系统)

<p align="center">
  <b>融合多代码仓库深度透视、AI-Agent 原生协同流水线与工业级全流程 SOP 的技术面试备战平台</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Vue-3.x-4FC08D?logo=vuedotjs" alt="Vue 3" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.x-38B2AC?logo=tailwindcss" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/Architecture-Agent--Native-FF6F00" alt="Agent-Native" />
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License" />
</p>

---

## 📖 项目愿景与设计哲学 (Vision & Philosophy)

技术面试早已告别单纯背诵八股文和刷 LeetCode 的旧时代。现代高阶技术面试（大厂架构师、算法专家、具身智能/大模型工程师）的核心痛点在于：
1. **项目描述空泛**：简历上的项目大多缺少强动词、量化指标与硬核工程壁垒，容易沦为“平庸流水账”；
2. **源码与八股脱节**：准备的八股文与候选人实际写过的代码割裂，面试官一旦结合真实代码底层（如模型结构、显存分布、分布式训练、动态路由）深入追问，极易陷入被动；
3. **技术权衡说不清**：无法清晰回答面试官最致命的追问——“**为什么不选方案 B？你的技术权衡依据是什么？**”；
4. **缺少实战压测与临考速记**：缺乏高度拟真的面试官对抗追问与临场 30 分钟应急锦囊。

**InterviewSOP Master** 旨在打造一套**工业级、端到端闭环的技术面试备战流水线**：
- **纯粹的 Agent-Native 原生协同**：彻底剔除伪装成“内置大模型”的黑盒残留，系统完全专注于**代码底层静态透视 + 阶段标准化工单调度 + 标杆数据离线预装**。真实的高阶深度推理与润色全面开放给外部 Agent（Claude 3.5 Sonnet / DeepSeek-R1 / GPT-4o / Cursor / Antigravity）。
- **Apple 极简毛玻璃 3 阶段工作流**：将繁复的面试准备划分为 **Stage 1 (简历精修)** ➔ **Stage 2 (胜任与权衡)** ➔ **Stage 3 (源码真题与速记)**，逐级流转、渐进解锁，并支持零门槛一键预装。

---

## 🔄 3 阶段工作流详解 (What Happens in Each Stage)

系统采用严谨的**逐级演进依赖机制**，前序阶段未完成时后续阶段严格锁定。每个阶段均支持“**外部 Agent 深度推理**”与“**官方标杆成果一键预装**”双通道：

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           【用户输入与本地静态特征提取】                          │
│     目标公司 / 目标岗位 JD   +   候选人简历 (PDF/MD/TXT)   +   本地代码工程 (RepoScanner)   │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🚀 阶段一：Stage 1 · 候选人简历针对性靶向精修 (Resume Targeting & Refinement)        │
│ ─────────────────────────────────────────────────────────────────────────────── │
│ • 核心输入：目标 JD + 简历原稿 + RepoScanner 提取的代码事实亮点                 │
│ • 智能诊断：对每个项目诊断 3 大失分盲区 (动词弱化 / 缺少量化指标 / 关键算法盲点) │
│ • 高分重塑：基于 STAR 原则输出高分子弹点 (强动词起手 + 量化指标 + 技术壁垒)   │
│ • 交互赋能：Diff 对比展示、子弹点自由勾选微调、一键回写覆盖简历文本框          │
│ • 阶段流转：Stage 1 完成并就绪后，平滑跳转 SOP-0 并解锁 Stage 2 阶段卡片       │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │ (精修简历 + 代码事实输入)
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🎯 阶段二：Stage 2 · 目标人岗胜任匹配度与 STAR 技术权衡 (Matching & Trade-off)    │
│ ─────────────────────────────────────────────────────────────────────────────── │
│ • 核心输入：Stage 1 精修后的高分简历 + 目标岗位 JD + 本地代码工程特征            │
│ • 胜任画像：5 维雷达量化评分 (业务/架构/工程/显存分布式/前沿视野) + 72h 冲刺清单 │
│ • 技术权衡：独创技术决策权衡对比矩阵 (Trade-off Matrix)                         │
│             针对核心设计深度对比备选方案，讲清“为什么不选方案 B”的取舍逻辑      │
│ • 阶段流转：Stage 2 完成并就绪后，平滑跳转 SOP-1 并解锁 Stage 3 冲刺卡片       │
└───────────────────────────────────────┬─────────────────────────────────────────┘
                                        │ (技术权衡 + 架构深度输入)
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ ⚡ 阶段三：Stage 3 · 源码级实战真题、模拟面试与临考速记 (Questions & Cheatsheet)   │
│ ─────────────────────────────────────────────────────────────────────────────── │
│ • 源码真题：结合真实工程代码锚点，定制 4 道大厂级实战真题 + 三层加分锦囊       │
│ • 模拟对练：动态生成工业级 Master Prompt (极客狂/架构师/业务官风格)，5段式诊断   │
│ • 反向提问：分轮次高阶反问清单 (技术一面/二面架构骨干、三面总监、HR 终面)       │
│ • 临考速记：30 分钟抢分速记卡 (5 大必背关键量化参数 + 3 条应答黄金法则)        │
│ • 战报导出：全阶段达成 (3/3)，一键导出排版精良的全局 Markdown 备战手册战报     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 详尽文件架构与职责清单 (Project Layout & File Roles)

每个文件各司其职，无任何冗余或死代码。完整目录结构及定位如下：

```text
Interview-sop/
│
├── 📜 核心服务与引擎
│   ├── app.py                      # FastAPI 后端核心调度服务
│   ├── repo_scanner.py             # 本地代码仓库静态特征透视引擎
│   ├── knowledge_base.py           # 专家知识库、离线规则引擎与标杆演示数据中心
│   ├── run.py                      # 系统主启动脚本（环境检查、拉起服务、自动打开浏览器）
│   ├── requirements.txt            # Python 核心依赖清单
│   ├── push_to_github.bat          # Windows 快捷 Git 提交流水线脚本
│   └── LICENSE                     # MIT 开源许可证
│
├── 🎨 前端界面 (Apple 极简毛玻璃 UI)
│   └── static/
│       ├── index.html              # Vue 3 单页应用（全功能界面：Stepper看板、7大SOP、弹窗与交互）
│       └── vendor/                 # 离线前端第三方资源包（TailwindCSS、Element Plus、Vue、Lucide 图标）
│
├── 🤖 外部 Agent 任务工单与契约体系 (agent_llm_tasks/)
│   ├── SKILL.md                    # 工业级标准化 Agent Skill 契约规范（供外部 Agent 遵循）
│   ├── README.md                   # Agent 任务包专属架构说明与协同指导
│   ├── run_pipeline.py             # 离线流水线任务校验 (--validate) 与合成聚合 (--aggregate) 脚本
│   ├── inputs/                     # 阶段工单导出目录（系统输出给外部 Agent）
│   │   ├── stage_1_input.json      # Stage 1 阶段工单上下文数据
│   │   ├── stage_1_prompt.txt      # Stage 1 阶段执行提示词
│   │   ├── stage_2_input.json      # Stage 2 阶段工单上下文数据
│   │   ├── stage_2_prompt.txt      # Stage 2 阶段执行提示词
│   │   ├── stage_3_input.json      # Stage 3 阶段工单上下文数据
│   │   ├── stage_3_prompt.txt      # Stage 3 阶段执行提示词
│   │   ├── current_context.json    # 用户当前填写的完整上下文快照
│   │   └── example_context.json    # 官方基准输入样例
│   ├── outputs/                    # 阶段成果落盘目录（外部 Agent 输出给系统）
│   │   ├── stage_1_output.json     # Stage 1 简历精修成果（回填 SOP-0）
│   │   ├── stage_2_output.json     # Stage 2 胜任力与权衡成果（回填 SOP-1 & SOP-2）
│   │   ├── stage_3_output.json     # Stage 3 真题/面试官/反问/速记成果（回填 SOP-3~6）
│   │   ├── output.json             # 全局 7 大模块聚合产物
│   │   └── example_output.json     # 官方全量标杆示范输出
│   ├── task_0_resume_optimizer/    # 任务 0 独立工单包：简历靶向精修 (CoT说明 + Prompt + Schema)
│   ├── task_1_matching_radar/      # 任务 1 独立工单包：5 维胜任力雷达画像 (CoT说明 + Prompt + Schema)
│   ├── task_2_star_tradeoff/       # 任务 2 独立工单包：STAR 深度复盘与权衡矩阵 (CoT + Prompt + Schema)
│   ├── task_3_questions_bank/      # 任务 3 独立工单包：源码真题题库与加分锦囊 (CoT + Prompt + Schema)
│   ├── task_4_mock_interviewer/    # 任务 4 独立工单包：沉浸式模拟面试官 Master Prompt (CoT + Prompt + Schema)
│   ├── task_5_reverse_interview/   # 任务 5 独立工单包：分轮次高阶反向提问策略 (CoT + Prompt + Schema)
│   └── task_6_cheatsheet/          # 任务 6 独立工单包：30 分钟临考极速速记卡 (CoT + Prompt + Schema)
│
└── 🧪 自动化测试与质量审计套件
    ├── test_backend.py             # 核心后端引擎与三阶段规范化单元测试
    ├── test_stage_pipeline.py      # 三阶段工单导出/导入/预装等 5 大 REST API 集成测试
    ├── test_final_audit.py         # 10 大核心模块、30 项关键指标全链路深度验收审计
    ├── test_api_server.py          # API 基础接口连通性自动化测试
    ├── test_live_server.py         # 运行中实时服务健康与响应测试
    └── test_pdf_parse.py           # PDF 简历上传解析与去乱码测试
```

---

### 🔍 核心文件功能速查表

| 文件路径 | 职责类型 | 核心功能与技术实现 |
| :--- | :--- | :--- |
| **`app.py`** | 后端主控 | 1. 提供 FastAPI 服务路由与静态资源挂载；<br>2. 调度 `RepoScanner` 进行多仓库并发透视；<br>3. 实现 PDF/文本简历流式清洗解析 (`parse_resume_file`)；<br>4. 智能发现与遍历本机项目目录 (`quick_directories`, `list_subdirectories`)；<br>5. 负责 Stage 1/2/3 工单导出、产物装载与**智能数据规范化校验层 (Normalization Layer)**；<br>6. 支持零门槛**一键预装示范成果兜底**。 |
| **`repo_scanner.py`** | 静态透视 | 1. 递归扫描指定目录下的 `.py`, `.json`, `.yaml` 等源码与配置文件；<br>2. 通过 AST 与正则智能识别模型 Backbone (CLIP, ViT, Qwen, LLaMA)、MLP Projector、Action Head；<br>3. 自动提取训练技术栈 (FSDP, DeepSpeed ZeRO, FlashAttention, LoRA, BF16)；<br>4. 提炼上百条真实代码高光，杜绝面试无话可说的尴尬。 |
| **`knowledge_base.py`** | 专家知识库 | 1. 内置两套工业级标杆数据：Mini-LLaVA 多模态端到端工程 + 金融投研 Agent 架构师；<br>2. 专家级 SOP 生成引擎 (`generate_expert_sop`)；<br>3. 沉浸式模拟面试官 Master Prompt 动态构造器 (`build_custom_mock_prompt`)；<br>4. 包含 Trade-off 决策矩阵、三层破局锦囊与 30 分钟速记口诀库。 |
| **`run.py`** | 启动器 | 1. 检查 Python 环境依赖；<br>2. 启动 Uvicorn 本地服务（默认端口 8000）；<br>3. 自动拉起系统默认浏览器访问 Web 页面。 |
| **`static/index.html`** | 前端核心 | 1. 基于 Vue 3 Composition API 构建极简毛玻璃界面；<br>2. 实现 **【Agent 协同三阶段流水线看板 (Stepper Card)】**；<br>3. 渐进式解锁顶部 Segmented Control 导航；<br>4. 渲染 SOP 0~6 全套视图（Diff 对比、ECharts 雷达图、权衡矩阵表、真题折叠卡）；<br>5. 目录选择器弹窗、全套 Markdown 备战手册一键导出。 |
| **`agent_llm_tasks/SKILL.md`** | Agent 契约 | 严格定义外部智能体（如 Cursor, Claude, Antigravity）在此项目中遵循的角色设定、输入输出规范与防幻觉指令。 |
| **`agent_llm_tasks/run_pipeline.py`**| 离线流水线 | 1. 离线校验各阶段输出是否满足 JSON Schema (`--validate`)；<br>2. 自动将 task_0~task_6 各模块产物合并为全局 `outputs/output.json` (`--aggregate`)。 |

---

## 🚀 极速上手与运行 (Quick Start)

### 1. 环境准备
确保本地安装了 Python 3.10 或更高版本：

```bash
# 克隆仓库
git clone https://github.com/Shewishees/Interview-sop.git
cd Interview-sop

# 安装核心依赖
pip install -r requirements.txt
```

### 2. 一键启动
在项目根目录执行：

```bash
python run.py
```
服务拉起后，系统将**自动在默认浏览器中打开** `http://127.0.0.1:8000`。

---

## 💡 两种经典使用场景指引

### 场景 A：零门槛 1 秒体验官方标杆演示 (Zero-Barrier Preload)
1. 访问首页，点击右上角 **【样例演示】** 载入示例数据（提供多模态具身智能或金融 Agent 两套标杆）；
2. 看到首页中央的 **【Agent 协同三阶段流水线看板】**：
   - 点击 Stage 1 的 **【⚡ 一键预装示范成果】** ➔ 秒级重塑简历并**自动平滑跳转至 SOP-0 靶向精修**；
   - 点击 Stage 2 的 **【⚡ 一键预装示范成果】** ➔ 解锁并**自动跳转至 SOP-1 胜任雷达与 SOP-2 权衡矩阵**；
   - 点击 Stage 3 的 **【⚡ 一键预装示范成果】** ➔ 解锁并**自动跳转至 SOP-3 源码定制真题库**；
3. 此时 3 阶段全部就绪，顶部导航全线解锁，可自由查阅模拟面试人设与临考速记卡，或点击右上角导出全局 Markdown 战报。

### 场景 B：求职者真实项目私有精磨 (Private In-Depth Preparation)
1. **录入与透视**：
   - 录入真实求职公司与岗位 JD；
   - 上传自己的简历（PDF/Markdown/文本）；
   - 在“关联本地代码仓库”区域，直接点选本地开发的项目工程目录（自动透视代码亮点）；
2. **阶段一（简历靶向精修）**：
   - 在 Stage 1 卡片点击 **【📤 导出 Stage 1 工单】**（数据落盘至 `agent_llm_tasks/inputs/`）；
   - 将生成的 Prompt 发送给您的外部大模型 Agent 执行，成果保存至 `outputs/stage_1_output.json`；
   - 点击 **【📥 装载 Stage 1 成果】**，系统自动呈现 Diff 诊断并支持一键将高分精修子弹点回写至简历；
3. **阶段二（胜任匹配与权衡决策）**：
   - 自动解锁后，点击 Stage 2 卡片的 **【📤 导出 Stage 2 工单】**；
   - 外部 Agent 评估生成后，点击 **【📥 装载 Stage 2 成果】**，即刻查阅 5 维雷达与“为什么不选方案 B”权衡矩阵；
4. **阶段三（源码真题与对练速记）**：
   - 自动解锁后，点击 Stage 3 卡片的 **【📤 导出 Stage 3 工单】**；
   - 外部 Agent 结合代码生成真题与速记后，点击 **【📥 装载 Stage 3 成果】**；
   - 获取 4 道源码结合型大厂真题与专属 Master Prompt，直接复制到外部模型开始 1v1 模拟面试！

---

## 🧪 自动化测试与工程质量保证

系统配备了全层级自动化测试与真机端到端走查脚本：

```bash
# 1. 核心后端引擎与阶段数据规范化测试
python test_backend.py

# 2. 三阶段工单导出/导入/预装 REST API 集成测试
python test_stage_pipeline.py

# 3. 10 大核心模块、30 项严苛指标全链路深度验收审计
python test_final_audit.py
```

### 真实浏览器 (CDP) 端到端自动化验收证据
通过 Chrome DevTools Protocol (CDP) 无头浏览器对真实界面进行 6 阶段真机流转走查，DOM 断言与视觉截图验证均 100% 通过：
1. **初始健康状态**：移除旧生成入口，Stage 1 就绪待处理，Stage 2/3 锁定；
2. **Stage 1 预装**：成功装载并自动平滑跳转至 SOP-0 靶向精修；
3. **Stage 2 触发解锁**：返回首页看板，Stage 1 显示已就绪，Stage 2 成功解锁；
4. **Stage 2 预装**：装载胜任匹配与权衡矩阵，自动平滑跳转至 SOP-1；
5. **Stage 3 预装**：装载真题库与速记，自动平滑跳转至 SOP-3 源码真题；
6. **全阶段 3/3 达成**：首页 3 阶段卡片全绿就绪，顶部导航全线点亮。

---

## ❓ 常见问题 (FAQ)

<details>
<summary><b>Q1: 为什么彻底砍掉了“内置大模型”？</b></summary>
所谓的“内置大模型”往往需要用户自行填写公网 API Key，或暗藏死循环漏洞与调用额度限制。我们将大模型深度推理职责完全解耦给外部 Agent（如 Claude、Cursor、DeepSeek、GPT），主系统专注于<b>代码透视、规范约束、成果可视化与离线标杆预装</b>，既保障了私有代码安全性，又提供了确定性极高的使用体验。
</details>

<details>
<summary><b>Q2: 如果外部 Agent 尚未生成 output 文件，点击装载会报错吗？</b></summary>
<b>绝对不会。</b> 系统在后端设计了完善的容错与兜底预装机制。若本地尚未生成文件，系统会自动预装官方标杆成果并返回 200 OK，绝无 404 或界面崩溃风险。
</details>

<details>
<summary><b>Q3: 本地代码仓库透视会上传我的源码吗？</b></summary>
<b>绝对不会。</b> <code>repo_scanner.py</code> 纯在本地运行 AST 与正则静态语法分析，仅提取组件名、超参和代码段亮点，零网络外传，隐私与代码资产 100% 安全。
</details>

<details>
<summary><b>Q4: 上传的 PDF 简历解析会不会出现二进制乱码？</b></summary>
系统集成了 <code>pypdf</code> 文本层提取与专用正则清洗管道，自动剔除 <code>\x00</code>、制表符与非打印符号，确保提取出的简历排版整洁。若简历为纯图片扫描件，建议先使用 OCR 工具识别或直接将文本复制到输入框中。
</details>

---

## 📄 开源许可证 (License)

本项目基于 [MIT License](LICENSE) 协议开源，欢迎自由使用、复用与贡献。