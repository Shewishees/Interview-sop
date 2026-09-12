"""
面试知识库与专家 SOP 模板数据中心
支持多代码仓库批量透视、通用简历/岗位动态萃取，以及多模态与金融/Agent架构双重深度支持。
内置两套工业级 Demo 演示数据：
1. 多模态与具身智能全套 Demo（Mini-LLaVA + OpenVLA）
2. 金融投研与智能体架构 Demo（同花顺实战：LLM + Agent + ReAct + Multi-Agent）
"""

from typing import List, Dict, Any

# 🌟 示例引导数据 1：多模态大模型与分布式系统 (通用示例引导模板)
DEMO_RESUME = """【基本信息】
张三 (示例候选人) | 2002.06 | 某重点大学 计算机科学与技术 (本/硕)
邮箱: candidate@example.com | 电话: 138-0000-0000
求职意向: 大模型算法工程师 / 系统架构师

【重点项目 1：基于 Transformer 的轻量化多模态对话模型研发 (示例项目)】
- 架构实现：基于开源轻量语言模型底座与预训练视觉编码器，自主设计双层非线性特征映射桥接层 (Projector)，将高维视觉 Token 精准对齐至文本 Embedding 空间；
- 模态对齐预训练：在千万级高质量图文数据集上实施 Stage 1 投影层特征对齐预训练，有效冻结主干权重，降低模态坍塌风险，验证集困惑度 (PPL) 显著收敛；
- 指令微调与部署：构建多轮图文对话微调集实施 Stage 2 全链路增量微调，结合 FlashAttention 与 FP16 混合精度优化，推理端单图端到端响应延迟低于 150ms。

【重点项目 2：企业级多智能体协同分析与决策系统 (示例项目)】
- 架构设计：基于 ReAct 范式与 Plan-and-Solve 机制主导设计分布式 Multi-Agent 协作架构，定义有向无环图 (DAG) 状态迁移流转规范；
- 工具沙箱与检索增强：集成工具调用安全沙箱与 Hybrid RAG 稠密检索模块，结合动态反思自纠机制，工具调用准确率提升至 94.2%；
- 性能优化与压测：采用异步并发读写与局部状态隔离机制，单节点吞吐处理能力突破 300 QPS，稳定保障高并发业务场景。

【专业技能】
- 熟练掌握 Python、C++、Linux、Docker、Git；
- 熟练掌握 PyTorch 深度学习框架与主流大模型微调推理工具；
- 深入理解 Transformer、VLM、LLM 底层注意力与分布式并行机制 (FSDP / DeepSpeed / LoRA)；
- 熟悉大模型 Agent 开发范式 (ReAct, Function Calling, LangGraph, RAG)。
"""

DEMO_COMPANY = "头部互联网大厂 / 前沿人工智能实验室"
DEMO_JOB_TITLE = "多模态大模型算法工程师 (示例校招/社招)"
DEMO_JD = """【岗位职责】
1. 负责多模态大模型（Vision-Language Models）的架构设计、数据流水线构建与模型预训练/微调；
2. 探索视觉编码器与 LLM 的模态对齐与融合机制，优化模型图文理解、复杂推理及多轮对话能力；
3. 负责大规模分布式训练（FSDP / DeepSpeed）、显存优化（FlashAttention、Gradient Checkpointing、混合精度训练）；
4. 推动模型在业务落地场景及智能体决策方向的性能评测与工程优化。

【任职要求】
1. 计算机、人工智能或相关专业本科及以上学历，具有扎实的深度学习基础；
2. 熟练掌握 PyTorch，熟悉主流 Transformer、VLM 架构原理及实现；
3. 具备多模态数据处理、两阶段对齐训练或智能体架构实战经验者优先；
4. 具备良好的分析解决问题能力与团队协作精神。
"""

# 🌟 示例引导数据 2：金融投研预测与大模型 Agent 架构实战（通用示例）
DEMO_AGENT_COMPANY = "示例金融科技股份有限公司 / 智能投研创新中心"
DEMO_AGENT_JOB_TITLE = "大模型与金融智能体架构算法专家 (示例岗位)"
DEMO_AGENT_JD = """【岗位职责】
1. 负责基于 LLM 与 Agent 架构的金融投研预测系统研发与业务落地，包括高质量数据构建、复杂推理链路设计与效果评估；
2. 深入探索 Multi-Agent 协作、复杂任务规划（Plan-and-Solve）、自我反思纠错机制在投研决策中的应用；
3. 探索将代码解释器、外部知识库检索（Hybrid RAG）与 Tool Use 高效集成。

【岗位要求】
1. 深入理解 Agent 工作原理（如 ReAct、Plan-and-Solve 等），有 Multi-Agent 应用或复杂推理系统实践经历；
2. 具备优秀的算法与代码基础，熟练掌握 Python 及主流大模型框架；
3. 具备出色的逻辑分析能力与团队协作精神。
"""

# 🌟 Demo 兼容历史默认命名别名
DEFAULT_RESUME = DEMO_RESUME
DEFAULT_COMPANY = DEMO_COMPANY
DEFAULT_JOB_TITLE = DEMO_JOB_TITLE
DEFAULT_JD = DEMO_JD

def generate_resume_optimizations(
    resume: str,
    jd: str,
    repos_info: Any = None,
    is_agent_focus: bool = False,
    is_multimodal_demo: bool = False
) -> List[Dict[str, Any]]:
    """
    根据目标岗位 JD、候选人现有简历及本地仓库代码事实，生成项目级针对性润色建议 (SOP-0: Resume Optimizer)
    """
    if repos_info is None:
        repos_info = []
    elif isinstance(repos_info, dict):
        repos_info = [repos_info]

    optimizations = []
    repos_str = str(repos_info).lower()
    
    # 1. 匹配 Mini-LLaVA / 多模态项目
    if "llava" in resume.lower() or "多模态" in resume or "llava" in repos_str:
        orig_snippet = (
            "基于 Transformer 架构的轻量化多模态对话大模型研发\n"
            "项目概述：LLaVA 架构通过视觉编码器和 Projection，提取图像特征输入到 LLM 中... 我基于 Qwen3-0.6B 语言模型和预训练 CLIP，手动复现了 LLaVA 架构的多模态大模型，涵盖模型搭建、两阶段训练流程及数据处理全链路。\n"
            "主要工作：1）LLaVA 架构实现；2）Stage1 模态对齐预训练；3）Stage2 多模态指令微调。"
        )
        if "Mini-LLaVA" in resume or "LLaVA" in resume:
            lines = resume.split("\n")
            found = []
            capturing = False
            for line in lines:
                if "llava" in line.lower() or "多模态" in line:
                    capturing = True
                elif capturing and line.strip().startswith(("【项目经历", "2025.", "2024.", "【专业技能")) and "llava" not in line.lower():
                    break
                if capturing and line.strip():
                    found.append(line.strip())
            if found:
                orig_snippet = "\n".join(found[:6])

        optimizations.append({
            "project_id": "proj_llava",
            "project_name": "基于 LLaVA 架构的轻量化多模态对话大模型 (Mini-LLaVA)",
            "target_jd_alignment": "多模态大模型架构 / 两阶段对齐训练 / 数据前处理与 Tokenizer 边界攻坚",
            "original_snippet": orig_snippet,
            "diagnosis": [
                {
                    "type": "动词表现力",
                    "flaw": "使用“手动复现了”、“选择Qwen”，动词偏向跟做与被动执行，缺乏工业级主导感与架构权衡。",
                    "tip": "替换为“深度重构多模态端到端架构”、“主导构建两阶段流水线”。"
                },
                {
                    "type": "量化与工程壁垒",
                    "flaw": "缺少投射层参数量 (1.8M)、半精度显存压缩 (2.4GB)、推理首字延迟 (120ms) 等硬核系统指标。",
                    "tip": "补充硬件显存收益、推理延迟以及 2 层 MLP 含 GELU 激活的精确参数。"
                },
                {
                    "type": "关键算法亮点",
                    "flaw": "未将自主攻坚的“增量前缀差值编码（解决 BPE 分词错位与 Label 漂移）”作为一级要点突出。",
                    "tip": "独立提炼出专门的数据工程子弹点，展现区分于普通调包侠的源码级排障能力。"
                }
            ],
            "keyword_matches": [
                {"keyword": "多模态架构设计 (Vision-Language)", "status": "已深度命中"},
                {"keyword": "两阶段对齐预训练 (Alignment & SFT)", "status": "已量化命中"},
                {"keyword": "增量分词与 Label Masking 错位排障", "status": "核心壁垒强化"},
                {"keyword": "半精度 (FP16) 流式推理显存优化", "status": "新增指标对齐"}
            ],
            "refined_bullet_points": [
                "【架构自研重构】深度重构 LLaVA 多模态对话架构，选用 Qwen3-0.6B 为 LLM 底座并融合预训练 CLIP ViT-B/16；自主设计 2 层带 GELU 激活的线性投射层 (768→1024→1024，参数量约 1.8M)，将图像经过预处理的 197 个 Patch 特征投射至 LLM 嵌入空间，实现视觉与语言语义空间的端到端对齐。",
                "【两阶段流水线训练】主导构建全链路多模态训练流程：Stage 1 采用 SA1B 100k 高质量图文对冻结视觉与语言底座仅微调 Projection，验证集困惑度 (PPL) 由 16.0 骤降至 6.4；Stage 2 采用 CogVLM 120k 多轮对话联合微调 Projection 与 LLM，PPL 进一步降至 8.5，实现高保真图像描述与多轮图文交互问答。",
                "【数据工程与分词防漂移】针对多轮图文对话中 BPE 分词边界不具备可加性的业界共性难题，自主设计增量前缀差值编码算法，精准切分每一轮回答的 Token 起止区间，彻底规避序列拼接导致的 Token 错位与 Label Masking 漂移隐患，提升 DataLoader 构建吞吐效率。",
                "【流式推理与决策预留】基于 PyTorch 实现半精度 (FP16) 交互式多模态推理脚本，峰值推理显存开销仅 2.4GB，首字生成延迟控制在 120ms 以内；同时预留标准化多模态特征前缀接口，为后续向具身控制与 Agent 决策系统的调用迁移奠定高扩展性底座。"
            ]
        })

    # 2. 匹配 OpenVLA / 具身智能项目
    if "openvla" in resume.lower() or "具身" in resume or "robotwin" in resume.lower() or "机器人" in resume or "robotwin" in repos_str:
        orig_snippet = (
            "基于 VLA 架构的具身机器人策略学习与多卡分布式微调\n"
            "主要工作：1）架构重构：深入研究 OpenVLA-oft 结构，在预训练模型基础上进行 oft 改造；设计基于 MLP 的 ActionHead；"
            "2）数据构建：利用 RoboTwin 仿真平台调用 Aloha 专家策略采集 600 条轨迹；"
            "3）分布式训练与评测：针对 7B 规模在 4 卡 4090 上利用 FSDP 训练，收敛后仿真取得 81% 成功率。"
        )
        if "OpenVLA" in resume or "RoboTwin" in resume:
            lines = resume.split("\n")
            found = []
            capturing = False
            for line in lines:
                if "openvla" in line.lower() or "robotwin" in line.lower() or "具身" in line:
                    capturing = True
                elif capturing and line.strip().startswith(("【项目经历", "2025.", "2024.", "【专业技能")) and "openvla" not in line.lower():
                    break
                if capturing and line.strip():
                    found.append(line.strip())
            if found:
                orig_snippet = "\n".join(found[:6])

        optimizations.append({
            "project_id": "proj_openvla",
            "project_name": "基于 OpenVLA 的具身机器人策略迁移与多卡分布式微调",
            "target_jd_alignment": "具身大模型 (VLA) / FSDP 多卡分布式训练加速 / 复杂决策与强化学习迁移",
            "original_snippet": orig_snippet,
            "diagnosis": [
                {
                    "type": "分布式深度不足",
                    "flaw": "原句仅提及“利用 FSDP 在 4 卡 4090 上实现分布式加速”，缺乏具体的 ZeRO-3 参数分片机制与显存节省量化收益。",
                    "tip": "增加 FSDP 参数/梯度/优化器状态分片描述，明确显存占用降低 55% 的硬核数据。"
                },
                {
                    "type": "动作空间与损失函数模糊",
                    "flaw": "ActionHead 未说明具体的输出维度（如 7 自由度连续动作空间），未解释为何采用 Smooth L1 回归而非离散化。",
                    "tip": "说明连续动作空间建模与多视角特征融合的投射机制，体现算法选型深度。"
                },
                {
                    "type": "数据泛化价值弱化",
                    "flaw": "对“域随机化 (Domain Randomization)”一笔带过，未突出其在缓解 Sim-to-Real 鸿沟上的核心价值。",
                    "tip": "强调对光照、纹理、相机外参施加随机扰动构建的 600 条高鲁棒性专家动作序列。"
                }
            ],
            "keyword_matches": [
                {"keyword": "VLA 具身大模型策略学习", "status": "前沿风口强化"},
                {"keyword": "PyTorch FSDP (ZeRO-3) 多卡显存优化", "status": "核心工程亮点"},
                {"keyword": "RoboTwin / Aloha 轨迹与域随机化", "status": "高质量数据闭环"},
                {"keyword": "Smooth L1 连续动作回归预测", "status": "算法选型对齐"}
            ],
            "refined_bullet_points": [
                "【具身架构重塑】深入剖析 7B 级预训练 VLA 大模型，在 OpenVLA-oft 基础上进行模块化重构；自研基于多层 MLP 的 ActionHead 动作头，提取 Transformer 末层隐藏状态并通过 Smooth L1 损失实现机械臂 7 自由度连续动作轨迹的高精度回归，融合多视角观测与本体感觉输入。",
                "【专家轨迹与域随机化】依托 RoboTwin 仿真平台接入 Aloha 专家策略采集操控轨迹，引入光照条件、材质纹理与相机位姿的多维域随机化 (Domain Randomization) 技术，从源头缓解 Sim-to-Real 泛化鸿沟，累计沉淀 600 条高质量高抗噪专家示范数据。",
                "【4卡 FSDP 分布式显存优化】针对 7B 规模大模型在有限算力环境下的微调瓶颈，采用 LoRA 轻量化与 PyTorch 原生 FSDP (Fully Sharded Data Parallel) 混合策略；在 4 卡 RTX 4090 上实现参数、梯度与优化器状态的完全分片，显存占用降低 55%，在 50k step 内平稳收敛。",
                "【闭环评测与决策迁移】构建端到端仿真测试评估闭环，在特定操控任务中取得 81% 的执行成功率；成功验证了通用大模型语义理解与复杂物理动作执行的对齐逻辑，具备向金融投研时序预测与复杂多步决策系统无缝迁移的通用技术底座。"
            ]
        })

    # 3. 如果针对同花顺 / 金融 Agent 岗位，追加针对该业务的高分定制项目点
    if is_agent_focus:
        optimizations.append({
            "project_id": "proj_agent",
            "project_name": "基于大模型与 Agent 架构的金融投研预测系统研发实践",
            "target_jd_alignment": "同花顺金融投研预测 / ReAct & Plan-and-Solve 推理范式 / 混合 RAG 与 Code Interpreter 防幻觉",
            "original_snippet": "（针对同花顺核心业务定向拓展的高分项目经历，可直接并入简历作为第 3 项或在面试中作为核心业务理解主动阐述）",
            "diagnosis": [
                {
                    "type": "岗位靶向契合度",
                    "flaw": "现有简历以底层视觉和多模态模型见长，缺乏明确的金融专有名词（如研报分析、时序量化指标、合规风控）支撑同花顺业务。",
                    "tip": "提炼出 ReAct 推理循环、沙箱代码解释器防幻觉、金融混合 RAG 三大杀手锏。"
                },
                {
                    "type": "推理决策稳定性",
                    "flaw": "普通简历常将 Agent 描述为简单的 LangChain 拼装，缺乏对多智能体通信死循环与长链路累计误差的思考。",
                    "tip": "引入 Plan-and-Solve 预规划与 Max Loops=8 熔断机制的系统级设计。"
                }
            ],
            "keyword_matches": [
                {"keyword": "ReAct 循环 vs Plan-and-Solve 规划", "status": "同花顺 JD 绝对核心"},
                {"keyword": "Code Interpreter 沙箱 (防计算幻觉)", "status": "金融投研刚需"},
                {"keyword": "混合检索 (Dense 向量 + BM25 + 重排)", "status": "大厂 RAG 标配"},
                {"keyword": "Multi-Agent 协同与死循环熔断保护", "status": "系统级架构亮点"}
            ],
            "refined_bullet_points": [
                "【智能体推理规划范式】针对金融长研报多步分析场景，设计并落地融合 ReAct (单步反思) 与 Plan-and-Solve (两阶段预分解) 的混合决策 Agent 架构；将复杂的宏观投研预测拆解为多步子任务并引入动态回溯纠错机制，显著降低长程推理中的累计幻觉。",
                "【Code Interpreter 沙箱防幻觉】针对金融指标定量计算的严苛准确性要求，集成 Python Code Interpreter 沙箱代码解释器；大模型作为逻辑规划调度器输出可执行代码，交由沙箱计算并回填结果，实现市盈率、波动率等复杂金融数值计算准确率 100%。",
                "【金融研报混合 RAG 增强】针对金融专有术语多、时效性强的特点，构建“Dense 语义向量 + BM25 专有代码 + Cross-Encoder 交叉重排”的三级混合检索流水线；配合滑动窗口切片，研报核心数据召回率与答案准度相比纯向量检索提升 32%。",
                "【Multi-Agent 协作与熔断治理】构建“研报分析师 - 宏观策略员 - 风控审核员”多智能体博弈协作拓扑，基于共享 Blackboard 维持上下文一致性；设置单次任务 Max Loops=8 与超时熔断保护，彻底规避智能体相互指责与死循环导致的 Token 成本暴增。"
            ]
        })

    # 4. 如果是其他通用输入且未匹配到上述特定项目，提供智能提炼版本
    if not optimizations:
        optimizations.append({
            "project_id": "proj_custom",
            "project_name": "核心技术项目经历（基于当前简历与 JD 靶向精修版）",
            "target_jd_alignment": f"高度对齐目标岗位：{jd[:40]}...",
            "original_snippet": (resume[:300] + "...") if len(resume) > 300 else resume,
            "diagnosis": [
                {
                    "type": "动词与结构弱化",
                    "flaw": "项目描述倾向于陈述事实，缺少 STAR 法则中 Action 的决策深度与 Result 的量化数据。",
                    "tip": "以强动作动词开头，突出面对的痛点与攻坚手段。"
                },
                {
                    "type": "指标说服力不足",
                    "flaw": "缺少性能指标对比（如吞吐量提升%、显存占用降低%、准确率增长%）。",
                    "tip": "在结果中强化前后量化对照。"
                }
            ],
            "keyword_matches": [
                {"keyword": "核心技术栈精准对齐", "status": "已匹配"},
                {"keyword": "量化业务收益与性能优化", "status": "已补全"}
            ],
            "refined_bullet_points": [
                "【核心技术架构落地】深入结合业务需求进行底层算法架构选型与重构，攻坚核心工程瓶颈，建立高可用、高并发的数据处理与推理闭环流水线。",
                "【关键算法优化与排障】针对系统运行中的关键痛点（如分词边界、显存瓶颈、长程累积误差）设计针对性解决方案，大幅提升流水线吞吐与模型推理稳定性。",
                "【量化成果与业务交付】制定严苛的基准测试流水线，在标准测试集上达成关键性能指标显著提升，验证了算法方案在生产环境落地的高可靠性。"
            ]
        })
        
    return optimizations

def generate_expert_sop(
    company: str = "",
    job_title: str = "",
    jd: str = "",
    resume: str = "",
    repos_info: Any = None,
    repo_info: Any = None,
    **kwargs
) -> dict:
    if repos_info is None and repo_info is not None:
        repos_info = repo_info
    if repos_info is None:
        repos_info = []
    elif isinstance(repos_info, dict):
        repos_info = [repos_info]

    company = (company or "").strip() or "目标科技公司"
    job_title = (job_title or "").strip() or "大模型算法与研发工程师"
    jd = (jd or "").strip() or "大模型算法训练、调优与工程落地。"
    resume = (resume or "").strip() or "未提供完整简历文本。"

    # 提取输入的意图倾向
    is_agent_focus = any(kw in (jd + job_title + company).lower() for kw in ["agent", "react", "plan-and-solve", "智能体", "金融", "投研", "同花顺", "rag", "tool"])
    is_multimodal_demo = ("LLaVA" in resume or "Mini-LLaVA" in resume) and ("OpenVLA" in resume or "Aloha" in resume)

    # 汇总所有扫描仓库的关键数据
    repo_names = []
    valid_repos = []
    for r in repos_info:
        if not isinstance(r, dict):
            continue
        s = r.get("summary", {})
        if s.get("root_name"):
            repo_names.append(s["root_name"])
            valid_repos.append(s)

    # ── 0. 动态生成 SOP-0: 简历靶向精修 (Resume Optimizer) ─────────
    sop_0_resume_optimizer = generate_resume_optimizations(
        resume=resume,
        jd=jd,
        repos_info=repos_info,
        is_agent_focus=is_agent_focus,
        is_multimodal_demo=is_multimodal_demo
    )

    # ── 1. 动态生成 SOP-1: 岗位匹配度分析 ─────────────────────────
    if is_agent_focus:
        sop_1_matching = {
            "overall_score": 94,
            "radar_dimensions": [
                {"dimension": "Agent架构与推理链路 (ReAct/Plan)", "score": 95, "comment": "深入理解 ReAct 循环、Plan-and-Solve 预规划与 Multi-Agent 通信机制"},
                {"dimension": "大模型微调与底层工程化", "score": 93, "comment": "具备完整的开源 LLM 微调、数据对齐清洗与长上下文管理经验"},
                {"dimension": "数据流水线与金融时序评估", "score": 90, "comment": "熟悉高质量数据构建、Domain Randomization 与仿真评估闭环"},
                {"dimension": "计算机科班底层与算法竞赛", "score": 96, "comment": "计科高分(云计算100/编译98)，具备扎实 C++/Python 算法与系统级素养"},
                {"dimension": "AI前沿工具与快速研发效率", "score": 95, "comment": "熟练使用 Cursor、Claude Code 等前沿工具，工程交付与原型落地极快"}
            ],
            "key_strengths": [
                "【架构深度胜过调包】绝大多数应聘 Agent 岗位的候选人只懂 LangChain 简易包装，而你拥有自研修改底层网络前向、多阶段对齐与增量分词编码的硬核工程底座，能够排查复杂 Agent 运行时的底层幻觉与 Token 错位！",
                "【复杂决策控制经验迁移】你在具身智能 OpenVLA 中积累的多视角感知融合、连续动作预测与仿真评估经验，可直接无缝迁移至金融投研中多源数据融合与时序趋势预测！",
                "【科班底座与学习爆发力】计科专业核心课满分，对编译原理、分布式架构理解极深，能够极速吃透并落地前沿的 Plan-and-Solve 和 Multi-Agent 架构。"
            ],
            "skill_gaps": [
                {"skill": "金融多源时序数据对齐与归一化", "level": "Medium", "suggestion": "补充针对金融 K 线、宏观指标与突发研报新闻的跨模态时间戳对齐处理方案。"},
                {"skill": "Agent 循环熔断与成本控制", "level": "Low", "suggestion": "熟记在复杂 Multi-Agent 协作中防止无限死循环、最大递归深度限制与 Token 成本配额机制。"}
            ],
            "sprint_priorities": [
                "优先级 1：吃透 ReAct (Thought-Action-Observation) 与 Plan-and-Solve (规划-求解) 在金融研报多步分析中的本质差异与适用场景。",
                "优先级 2：准备好一个'如何利用 Code Interpreter 沙箱解决金融大模型数值计算幻觉'的实战案例话术。",
                "优先级 3：掌握 Multi-Agent（分析师、风控官、交易员角色扮演）协作博弈的通信设计与一致性维护。"
            ]
        }
    elif is_multimodal_demo:
        sop_1_matching = {
            "overall_score": 93,
            "radar_dimensions": [
                {"dimension": "多模态架构理解", "score": 96, "comment": "深入自研复现 LLaVA 架构，熟悉 ViT patch 提取与 MLP 投射"},
                {"dimension": "工程与数据流实战", "score": 95, "comment": "掌握多轮增量差值编码、SA1B 及 CogVLM 真实洗数与 DataLoader 构建"},
                {"dimension": "分布式与训练优化", "score": 89, "comment": "实操过 4 卡 4090 FSDP、LoRA 微调、FlashAttn-2 与梯度检查点"},
                {"dimension": "前沿具身拓展(VLA)", "score": 92, "comment": "具备 OpenVLA-oft 改造、Aloha 轨迹数据生成及仿真经验"},
                {"dimension": "计算机与代码基础", "score": 91, "comment": "计科科班高分(云计算100/编译98)，具备良好底层工程与前后端素养"}
            ],
            "key_strengths": [
                "【源码级复现】绝大部分应届生只会调用 API，你手动重写了 CLIP 的 forward，保留 197 个 token，并自主实现 2 阶段训练与增量 DataLoader，这是核心差异化壁垒！",
                "【全流程闭环】从预训练 SA1B 模态对齐 (PPL 16->6.4) 到指令微调 (PPL 20->8.5)，拥有完整的两阶段指标变化支撑，数据可信度极高。",
                "【多项目协同跨域】同时覆盖经典 LLaVA 多模态对话大模型与具身智能 OpenVLA 策略迁移，完美契合当前 VLA 具身大模型最前沿风口。"
            ],
            "skill_gaps": [
                {"skill": "大并发推理部署优化", "level": "Medium", "suggestion": "补充 vLLM、PagedAttention、TensorRT-LLM 的原理及如何针对多模态 vision tokens 做 KV Cache 优化的思考。"},
                {"skill": "大规模数据清洗策略", "level": "Low", "suggestion": "补充关于多模态脏数据过滤、图文语义匹配度评分（如 CLIP-Score 过滤）的具体经验。"}
            ],
            "sprint_priorities": [
                "优先级 1：背熟并清晰画出 LLaVA 端到端张量变化图（[B,3,224,224] -> [B,197,768] -> [B,197,1024] 与 [B,T,1024] 拼接 -> [B,197+T,1024]）。",
                "优先级 2：吃透多轮对话增量差值编码算法的本质——为什么 BPE 分词不可加？为什么不能分别 tokenize 再拼？",
                "优先级 3：复习 FSDP（ZeRO-3 分片通信 AllGather / ReduceScatter）与 LoRA 的参数计算公式。"
            ]
        }
    else:
        score = min(96, max(75, 80 + len(valid_repos) * 4 + min(10, len(resume) // 180)))
        sop_1_matching = {
            "overall_score": score,
            "radar_dimensions": [
                {"dimension": "核心专业技能匹配", "score": min(95, score + 2), "comment": "简历技能项与目标 JD 核心要求重合度良好"},
                {"dimension": "项目实战与落地深度", "score": min(94, score + 1), "comment": f"提供了 {len(valid_repos)} 个本地代码仓库支撑，具备工程落地依据"},
                {"dimension": "底层工程与代码质量", "score": min(92, score - 2), "comment": "从代码库识别出结构化模块与关键亮点"},
                {"dimension": "架构设计与技术视野", "score": min(90, score - 3), "comment": "具备完整的模块设计与技术选型权衡经验"},
                {"dimension": "综合发展潜力", "score": min(95, score + 3), "comment": "具备扎实的软硬件基础与主动探索技术前沿的能力"}
            ],
            "key_strengths": [
                f"【多仓库代码实证】绑定了 {', '.join(repo_names) if repo_names else '真实项目工程'}，在面试官面前具备绝对的真实性说服力！",
                "【技术全栈打通】简历中具备清晰的架构链路与落地闭环，能够清晰阐明业务与算法选型背后的逻辑。",
                "【具备前沿探索力】不仅停留在使用基础工具，而且在核心流程中进行了针对性自研或微调优化。"
            ],
            "skill_gaps": [
                {"skill": "大规模生产环境高并发调优", "level": "Medium", "suggestion": "结合 JD 深入准备关于高并发场景下的资源排队、分布式容灾与吞吐压测指标。"},
                {"skill": "前沿竞品与演进方案对比", "level": "Low", "suggestion": "熟记技术权衡矩阵中‘为什么不选备选方案 B’的核心论据。"}
            ],
            "sprint_priorities": [
                "优先级 1：根据 SOP-2 的 STAR 结构，熟练背诵每个项目的核心成果与指标。",
                "优先级 2：吃透技术权衡矩阵中我方选型 vs 备选方案 B 的优劣势对比。",
                "优先级 3：将生成的专属面试官 Prompt 喂给私有大模型，进行至少 3 轮压力模拟对答。"
            ]
        }

    # ── 2. 动态生成 SOP-2: 多项目 STAR 复盘与技术权衡对比矩阵 ────────
    sop_2_star = []

    # 若岗位匹配 Agent 架构（如同花顺）
    if is_agent_focus:
        sop_2_star.append({
            "project_name": "金融投研复杂推理智能体系统 (Financial Agent Architecture)",
            "one_sentence_pitch": "基于大模型与多智能体协同架构，集成 ReAct 动态反思循环与 Plan-and-Solve 任务分解，打造多源金融研报解析与高精度预测系统。",
            "star_framework": {
                "situation": "传统金融投研依赖人工阅读海量研报和手工计算时序财务指标，效率低且无法实时感知突发舆情；而简单的大模型问答存在严重的数值计算幻觉（Hallucination）和长链路推理逻辑断裂问题。",
                "task": "设计并落地一套基于 LLM 的金融投研 Agent 系统，实现复杂投研任务的自动拆解、外部工具（行情API/计算沙箱/知识库）可靠调度，以及多智能体（宏观分析师、财务审计员、风控评判员）的协同推理。",
                "action": "1. 决策架构：设计混合型规划引擎，针对多步骤复杂任务采用 Plan-and-Solve 预生成全局拓扑计划，针对执行中的单步异常采用 ReAct (Thought-Action-Observation) 进行动态自适应微调；\n2. 解决计算幻觉：接入独立 Python 代码解释器沙箱与严格的 JSON Schema 函数调用（Function Calling），计算指标由代码执行而非 LLM 自回归预测；\n3. 多智能体协作：构建基于分层黑板模式的 Multi-Agent 通信机制，设定严格的最大跳步阈值（Max Steps）与死循环熔断机制，防止 Token 爆炸；\n4. 评估闭环：构建包含真实金融时序历史数据集与研报预测回测基准，实现量化评分。",
                "result": "在多任务金融投研复杂问答场景下，任务执行完成率达到 91%，关键财务数据计算准确率提升至 99.2%，单次投研分析耗时从人工的数小时缩短至分钟级。"
            },
            "trade_off_matrix": [
                {
                    "decision_point": "智能体推理规划范式选型",
                    "chosen_solution": "Plan-and-Solve 预规划 + ReAct 单步动态调整混合机制",
                    "alternative_solution": "纯 ReAct 步步循环 / 纯单提示词 Zero-shot CoT",
                    "pros_of_chosen": "全局目标感强，不会出现纯 ReAct '走一步看一步导致后半段偏离主题'的盲目性，同时又保留了单步失败时利用 Observation 自我反思与自愈的能力。",
                    "cons_of_chosen": "首字响应时间略长，需要先等待 LLM 输出完整的 JSON 计划树。",
                    "why_not_alternative": "纯 ReAct 在面对多达 10 步以上的复杂金融投研链路时，容易在中间步骤陷入无限死循环（如反复查询同一类无效数据），导致上下文剧烈膨胀并爆 Token；CoT 缺乏与环境工具的真实交互能力，遇到实时股价时直接生成虚假预测。",
                    "frontier_technology": "【当前前沿演进】LangGraph / Reflexion (自反思记忆库) 结合 MCTS (蒙特卡洛树搜索 / AlphaGo 式思维树搜索)，通过多分支路径推演寻找最优投研决策链。"
                },
                {
                    "decision_point": "智能体协作组织拓扑架构选型",
                    "chosen_solution": "Multi-Agent 分层主从协作模式 (Leader-Worker + 专家辩论)",
                    "alternative_solution": "单 Agent 大统一 Prompt / 完全去中心化自由广播",
                    "pros_of_chosen": "角色职责清晰（如'宏观分析师'只负责行业背景，'风控官'专门负责质疑风险），大幅降低了单 Agent 提示词过长导致的注意力分散，互为对抗监督能显著抑制幻觉。",
                    "cons_of_chosen": "多智能体之间存在多轮上下文流转，整体 API 调用 Token 消耗量较大。",
                    "why_not_alternative": "单个 Agent 如果强行把分析、计算、风控全部写在 System Prompt 中，模型极易顾此失彼；完全去中心化广播通信开销呈 O(N^2) 爆炸，极易引发群体幻觉共振。",
                    "frontier_technology": "【当前前沿演进】基于状态机的有向无环图 (DAG 工作流) 与动态环境自适应组织 (Swarm 模式)，按需唤醒特定专家智能体，执行完即释放上下文。"
                },
                {
                    "decision_point": "外部研报知识检索与增强机制 (RAG)",
                    "chosen_solution": "混合检索 (Dense 稠密向量 + BM25 稀疏词法 + Cross-Encoder 重排 Rerank)",
                    "alternative_solution": "纯向量相似度检索 (Pure Vector Search)",
                    "pros_of_chosen": "既具备语义抽象泛化能力，又对金融专有代码（如股票代码 '000001'、专业财报术语 'EBITDA'）具备 100% 精确召回率，Rerank 模块保证最关键条款置顶于 Prompt 头部。",
                    "cons_of_chosen": "系统需要额外维护 BM25 倒排索引和 Reranker 模型，检索延迟增加约 50ms。",
                    "why_not_alternative": "纯向量模型在长数字、专业缩写和股票代码匹配上存在固有弱点，容易将相近代码的异质公司混淆召回，给投研带来灾难性误导。",
                    "frontier_technology": "【当前前沿演进】GraphRAG (知识图谱与实体关系拓扑检索)，能够回答跨产业链上下游联动（如'若锂矿减产，新能源整车供应链将受何影响'）的高维推理难题。"
                }
            ],
            "pitfalls_and_countermeasures": [
                {
                    "question": "在金融 Agent 执行过程中，如果大模型调用的 API 返回了报错或格式错误，系统怎么容错？",
                    "danger": "回答太简单（如只说'写个 try-catch 重试'），暴露缺乏 Agent 工程设计经验。",
                    "best_answer": "在 Agent 系统中，简单的 try-catch 无法解决语义错误。我们设计了三级自愈机制：\n1. 结构化反思反馈：将工具报错信息（如 '参数缺少 start_date'）作为 Observation 回传给大模型，利用 Few-Shot 引导大模型重新理解缺失参数并自动更正入参；\n2. 确定性降级兜底：若连续 2 次重试仍未成功，Agent 会自动切换到备用工具源（如从主数据源切换至快照缓存源）或向用户输出澄清提示；\n3. 全局熔断保护：设置全局最大思考步数（如 Max Loops=8）和 Token 消费配额，防止模型陷入无休止的重试死循环。"
                }
            ]
        })

    # 多模态项目（Mini-LLaVA）
    if is_multimodal_demo or any("CLIP" in str(r) or "llava" in str(r).lower() for r in valid_repos):
        sop_2_star.append({
            "project_name": "Mini-LLaVA: 基于 Qwen3-0.6B 与 CLIP 的轻量化多模态对话大模型",
            "one_sentence_pitch": "基于 Qwen3 与 CLIP ViT-B/16 从零手动复现 LLaVA 架构，设计两阶段模态对齐与指令微调方案，验证集 PPL 显著优化并实现交互式多轮对话系统。",
            "star_framework": {
                "situation": "多模态大模型通常参数庞大、计算昂贵且官方实现封装过深，难以清晰观测模态对齐的本质与细粒度数据流转。为此我决定基于轻量级 Qwen3-0.6B 与中文 CLIP，从零手写核心网络组件与训练流程，探索低资源下的多模态对齐与问答能力。",
                "task": "1. 架构搭建：实现视觉编码器与 LLM 嵌入空间的维度投影映射与 Token 拼接；\n2. 阶段一对齐：基于 100k SA1B 数据仅训练投影层，实现视觉到语言语义空间的对齐；\n3. 阶段二微调：基于 120k CogVLM-SFT 对话数据微调 LLM 与投影层，赋予模型多轮图文交互能力。",
                "action": "1. 视觉端改造：重写 CLIP VisualTransformer 前向，摒弃原版丢弃空间特征的 CLS 池化，保留全部 197 个 patch 特征，跳过原图文共享空间投影；\n2. 投影层设计：采用 2 层 MLP (Linear-GELU-Linear)，将 768 维映射至 1024 维；\n3. 训练数据流：设计增量前缀差值编码算法解决 BPE 分词边界不可加导致的错位问题；视觉 token 及 user 轮全部打上 -100 掩码，仅对 assistant 轮次计算交叉熵损失；\n4. 工程加速：引入 FlashAttention-2 与梯度检查点技术，显著降低显存开销。",
                "result": "阶段一使验证集 PPL 从 16 稳定下降至 6.4，模型建立图像全局描述能力；阶段二在验证集上 PPL 降至约 8.5，成功实现了支持图像 URL 动态载入的多轮交互问答 Demo。"
            },
            "trade_off_matrix": [
                {
                    "decision_point": "模态融合连接器架构选型",
                    "chosen_solution": "2-Layer MLP (Linear-GELU-Linear 前缀拼接)",
                    "alternative_solution": "BLIP-2 Q-Former / Flamingo Gated Cross-Attention",
                    "pros_of_chosen": "计算开销极小(仅~1.8M参数)，无需额外学习复杂 Query，视觉特征无损作为 Token 序列前缀传入，最大限度保全 LLM 原生自注意力与因果推理能力，训练稳定性高。",
                    "cons_of_chosen": "Token 数量较多 (单图固定 197 tokens)，占用了语言模型的上下文窗口长度。",
                    "why_not_alternative": "Q-Former 虽然能通过可学习 Query 压缩 Token 数量（如 32 个），但引入了复杂的两阶段交叉注意力，结构臃肿且极易丢失空间细粒度局部几何信息；Flamingo 的 Cross-Attention 需要在 LLM 每层插入门控层，破坏了 LLM 预训练权重的完整性，微调显存开销大。",
                    "frontier_technology": "【当前前沿演进】LLaVA-NeXT (AnyRes) 结合 2x2 Pixel Shuffle 进行局部降采样，或采用 SigLIP-SO400M 替换 CLIP，以及当前最新的统一自回归架构（Chameleon / GPT-4o 离散 VQ-VAE 混合 Token 流）。"
                },
                {
                    "decision_point": "训练方案与模态对齐策略",
                    "chosen_solution": "两阶段解耦训练 (Stage 1 对齐 Projection + Stage 2 微调 LLM)",
                    "alternative_solution": "端到端联合训练 (直接同时训练 Projection 与 LLM)",
                    "pros_of_chosen": "Stage 1 冻结两端先让随机初始化的 Projection 暖机，将视觉流形拉近到语言流形附近；Stage 2 再放开 LLM 进行语义推理与对话微调，避免灾难性遗忘，收敛极快且平稳。",
                    "cons_of_chosen": "流水线分为两阶段，需要保存和加载中间 checkpoint，工程管理上多了一步。",
                    "why_not_alternative": "直接端到端微调时，由于 Projection 初始为纯噪声，反向传播的巨大梯度会瞬间冲击 LLM 的词嵌入和自注意力权重，破坏模型预训练的语言能力，导致文本困惑度激增、生成退化。",
                    "frontier_technology": "【当前前沿演进】Stage 1.5 高质量密集重述（Dense Captioning 预对齐） + Stage 2.5 视觉直接偏好对齐（Direct Preference Optimization, DPO / RLHF），防止模型视觉幻觉（Hallucination）。"
                },
                {
                    "decision_point": "多轮对话 Tokenization 与掩码机制",
                    "chosen_solution": "增量前缀差值编码算法 (逐轮格式化完整上下文做差值)",
                    "alternative_solution": "逐轮独立调用 tokenizer 编码并用 torch.cat 拼接",
                    "pros_of_chosen": "严格遵循 BPE 分词的边界一致性与 Chat Template 上下文完整性，从数学原理上杜绝 token 错位与 label 掩码打偏。",
                    "cons_of_chosen": "每轮需要多次调用 apply_chat_template，代码实现逻辑相对复杂。",
                    "why_not_alternative": "BPE 分词具有不可加性（tokenize(A+B) ≠ tokenize(A) + tokenize(B)），单独分词再拼接会导致跨句词元被合并或切分不一致，造成 Labels 与 Input IDs 偏移，导致模型把 prompt 误当 target 计算 loss，或者关键 target 被 mask 掉。",
                    "frontier_technology": "【当前前沿演进】基于 FlashAttention-2 的变长序列打包（Packed Sequence / Sample Packing），消除 Batch 内部 Padding 的无效计算浪费，吞吐量可提升 2~3 倍。"
                }
            ],
            "pitfalls_and_countermeasures": [
                {
                    "question": "为什么分成两阶段？直接端到端同时训 CLIP + LLM 不行吗？",
                    "danger": "回答太肤浅（如只说'大家都是这么做的'），会显得缺乏对多模态本质的思考。",
                    "best_answer": "不行。两阶段有非常本质的动力学考量：\n1. 语义空间鸿沟巨大：初始化时 Projection 权重是随机的，如果一开始就端到端微调 LLM，随机的视觉 embedding 梯度会直接冲垮 LLM 预训练阶段学到的成熟语言语法与语义结构，导致灾难性遗忘；\n2. 计算成本与解耦：Stage 1 冻结两端、只训 1.8M 参数的 Projection，计算极快，旨在先将视觉特征预热到语言模型的流形附近；Stage 2 再解冻 LLM 进行深度的图文推理与对话微调，训练平稳且收敛效率高。"
                }
            ]
        })

    # 具身智能项目（OpenVLA）
    if is_multimodal_demo or any("vla" in str(r).lower() or "oft" in str(r).lower() or "action" in str(r).lower() for r in valid_repos):
        sop_2_star.append({
            "project_name": "OpenVLA: 机器人具身策略迁移与分布式训练",
            "one_sentence_pitch": "基于 OpenVLA-oft 改造多视角感知与本体感觉投射，结合 RoboTwin+Aloha 采集专家轨迹并通过 4 卡 FSDP 完成微调，仿真任务成功率达 81%。",
            "star_framework": {
                "situation": "传统端到端机器人策略泛化性差，亟需利用预训练 VLM 的通用语义推理与空间感知能力迁移到物理控制领域。",
                "task": "在预训练 OpenVLA 基础上引入 OFT 结构进行低成本高效调优，融合多视角与本体感觉，并在 4 卡 4090 算力受限下完成 7B 模型训练与仿真评估。",
                "action": "1. 架构上在输入序列嵌入占位符实现并行编码，设计 MLP ActionHead 提取最后一层隐藏状态做 L1 回归动作预测；\n2. 利用 RoboTwin 采集 600 条 Aloha 轨迹并施加域随机化（Domain Randomization）；\n3. 采用 PyTorch FSDP 策略对模型参数、梯度与优化器状态进行全切片，配合 LoRA 实现 4 卡并行训练。",
                "result": "50k step 顺利收敛，仿真单任务操控任务成功率达 81%，验证了将 VLM 泛化先验迁移至具身控制的可行性。"
            },
            "trade_off_matrix": [
                {
                    "decision_point": "动作生成建模 (Action Head) 选型",
                    "chosen_solution": "连续空间 MLP + L1 回归预测",
                    "alternative_solution": "离散 Token 分箱预测 (RT-2 方案) / 扩散动作策略 (Diffusion Policy)",
                    "pros_of_chosen": "计算效率最高，连续动作直接输出高精度 7-DOF 轨迹 (位置/姿态/夹爪)，免去多次迭代降噪步骤，能够满足实时高频控制 (20Hz+) 的低延迟需求。",
                    "cons_of_chosen": "在多模态动作分布（即一个视觉场景下有多种合法动作路径）时，容易预测出多种动作的平均值导致控制抖动。",
                    "why_not_alternative": "RT-2 的离散分箱法将动作离散化为 256 个 bin 占用词表空间，动作精度受限于 bin 划分颗粒度，且自回归生成每个维度的动作耗时长；Diffusion Policy 虽然表达多模态分布强，但在部署时需要 10~50 步采样迭代，难以兼顾 LLM 的高延迟与机器人的实时响应。",
                    "frontier_technology": "【当前前沿演进】Flow-Matching 连续流匹配技术（如 3D-VLA / Octo-Flow），在单步或极少步内完成连续高保真动作生成，兼具扩散模型的分布表达力与回归模型的超高推理速度。"
                },
                {
                    "decision_point": "分布式微调与显存优化策略",
                    "chosen_solution": "PyTorch FSDP (ZeRO-3) + LoRA 轻量化微调",
                    "alternative_solution": "标准 DDP (Distributed Data Parallel) 全参数微调 / DeepSpeed-ZeRO2",
                    "pros_of_chosen": "在 4 卡 4090 (单卡 24G 显存) 严格受限环境下，FSDP 将 7B 模型的模型权重、梯度与优化器状态均匀打散，结合 LoRA 将可训练参数降至千万级，成功消除 OOM 并最大化显存利用率。",
                    "cons_of_chosen": "FSDP 前向与反向需要额外的 AllGather 和 ReduceScatter 通信，对 PCI-e 带宽有一定压力。",
                    "why_not_alternative": "7B 模型在标准 DDP 全微调下，每张卡都需要完整维护 14GB 权重 + 28GB AdamW 状态 + 激活值，单卡需求超过 50GB，在 24GB 的 4090 上根本无法启动；ZeRO-2 只分片优化器状态，模型参数依然不分片，显存依然超限。",
                    "frontier_technology": "【当前前沿演进】QLoRA (NF4 4-bit 量化) + Liger Kernel 算子融合，或者使用 Megatron-LM 的 TP(张量并行) + PP(流水线并行) 混合切片。"
                }
            ],
            "pitfalls_and_countermeasures": [
                {
                    "question": "4 张 4090 (每卡 24G) 跑 7B 模型，显存怎么安排的？为什么用 FSDP 而不是 DDP？",
                    "danger": "算错显存模型（7B 参数在 FP16 下 14G，加上 AdamW 状态 28G，单卡绝对爆显存）。",
                    "best_answer": "7B 模型如果用全量 DDP，单张显卡仅模型权重和 AdamW 优化器状态就需要 14GB + 28GB = 42GB，24G 显存直接 OOM。因此我们采用了 LoRA 微调将可训练参数压缩至千万级，同时配合 FSDP（Full Sharded Data Parallel）的 ZeRO-3 思想，将模型权重、梯度与优化器状态均匀分片到 4 张显卡上，每张卡仅承担约 1/4 的分片显存，再配合梯度检查点，成功在 4 卡 4090 上平稳跑通。"
                }
            ]
        })

    # 其他用户自定义上传的代码仓库
    for repo in valid_repos:
        repo_title = repo.get("root_name", "自定义代码工程")
        if any(repo_title.lower() in p["project_name"].lower() for p in sop_2_star):
            continue
        models_str = ", ".join(f"{k}: {v}" for k, v in repo.get("model_architecture", {}).items()) or "模块化系统设计"
        highlights_str = "\n".join(f"- {h}" for h in repo.get("code_highlights", [])) or "- 实现了核心业务与算法逻辑，具备完整的工程接口"
        sop_2_star.append({
            "project_name": f"{repo_title}: 代码仓库工程实战",
            "one_sentence_pitch": f"基于本地工程 {repo_title} 打造的关键技术模块，涵盖 {models_str}，具备完整的接口与测试闭环。",
            "star_framework": {
                "situation": f"在 {repo_title} 项目中，为解决特定业务场景下的算法精度与工程吞吐瓶颈开展技术攻关。",
                "task": f"负责 {repo_title} 核心模块的算法设计、代码编写与测试调优，确保指标达到工业化标准。",
                "action": f"1. 核心架构：{models_str}；\n2. 关键工程动作：\n{highlights_str}",
                "result": "系统代码模块解耦良好，通过了端到端的功能与性能压测。"
            },
            "trade_off_matrix": [
                {
                    "decision_point": "项目核心框架与工程选型",
                    "chosen_solution": f"轻量自研与成熟开源生态结合 ({repo_title})",
                    "alternative_solution": "纯黑盒闭源方案",
                    "pros_of_chosen": "完全掌控核心代码细节与数据流转，可控性高，便于进行二次算子级或逻辑级调优。",
                    "cons_of_chosen": "需要自行维护边界异常与测试覆盖。",
                    "why_not_alternative": "黑盒方案难以排查底层内存/显存泄露问题，且难以进行高精度的业务定制化改造。",
                    "frontier_technology": "【当前前沿演进】自动化编译优化、轻量级 Kernel 算子融合 (Triton) 与端到端流水线部署。"
                }
            ],
            "pitfalls_and_countermeasures": [
                {
                    "question": f"你在 {repo_title} 中最自豪的代码设计是哪一部分？遇到了什么性能瓶颈？",
                    "danger": "只讲业务流程不讲底层数据结构或算法细节。",
                    "best_answer": "在本项目中，我最核心的工作是对数据流转与关键模块的处理机制进行解耦优化，重点解决了边界数据对齐与异常处理，使得吞吐与稳定性得到大幅增强。"
                }
            ]
        })

    # 若未匹配到任何预设项目且无代码仓库，提供工业级通用 STAR 兜底
    if not sop_2_star:
        sop_2_star.append({
            "project_name": "核心业务系统研发与关键算法工程落地",
            "one_sentence_pitch": f"面向【{job_title}】的核心职责，主导端到端模块架构设计、关键瓶颈攻坚与工程交付闭环。",
            "star_framework": {
                "situation": f"在【{company}】相关业务场景下，系统面临高可靠、低延迟以及算法与复杂工程深度融合的多维挑战。",
                "task": "梳理端到端系统核心瓶颈，独立负责关键技术方案选型、数据处理闭环构建与高并发服务交付。",
                "action": "1. 架构重塑：针对关键吞吐瓶颈完成轻量化模块解耦，消除冗余依赖与单点脆弱性；\n2. 性能攻坚：重写数据流水线交互逻辑，引入缓存机制与异常保护机制；\n3. 落地推进：制定严苛的基准测试流水线，针对边界异常与资源开销进行全方位压测与调优。",
                "result": "核心模块平稳上线，系统端到端吞吐提升 35% 以上，接口平均响应延迟与异常率显著降低。"
            },
            "trade_off_matrix": [
                {
                    "decision_point": "底层技术路线选型",
                    "chosen_solution": "轻量自研与精准工程优化方案",
                    "alternative_solution": "开箱即用的大型重度全家桶框架",
                    "pros_of_chosen": "依赖极简、执行链路完全透明可控、可观测性强，深度调试与二次定制成本极低。",
                    "cons_of_chosen": "前期需要自行构建脚手架与自动化测试套件。",
                    "why_not_alternative": "重度框架封装过深，面对极限边界用例或偶发排障时排查困难，且引入大量冗余开销。",
                    "frontier_technology": "【当前前沿演进】结合端到端编译优化、算子融合加速 (Triton) 与自适应熔断自愈机制。"
                }
            ],
            "pitfalls_and_countermeasures": [
                {
                    "question": f"在该项目推进中，你踩过的最深的技术坑是什么？如何定位并根治的？",
                    "danger": "回答流于表面或归咎于外部环境，缺乏真实排障与底层追溯深度。",
                    "best_answer": "在早期联调时，由于长链路异步调度导致偶发边界状态竞争与内存缓慢泄露。我通过搭建单步追踪打点与内存 Profile 工具，准确定位到资源释放的边界缺陷，重构了生命周期管理并增加了超时熔断，彻底根治了该问题。"
                }
            ]
        })

    # ── 3. 动态考点题库 ─────────────────────────────────────────
    if is_agent_focus:
        sop_3_questions = [
            {
                "category": "智能体推理机制 (Agent Reasoning)",
                "title": "请深入阐述 ReAct 与 Plan-and-Solve 的核心区别？在金融研报分析中各自适用的场景是什么？",
                "framework": "【核心定性】ReAct 属于'单步探索与观察循环'，Plan-and-Solve 属于'两阶段全局规划与逐项求解'；\n【执行差异】1. ReAct 遵循 Thought -> Action -> Observation，遇到动态不确定性（如行情突变）能够即时调整，但面对超过 10 步的长链条容易迷失目标；2. Plan-and-Solve 先生成完整的 DAG 执行计划子任务列表，再由求解器逐步计算，结构严密，尤其适合多指标财务报表连环对比；\n【工业结合】在成熟架构中通常采用 Plan-and-Solve 作为顶层规划器，各子任务内部调用小型 ReAct 执行工具自愈与重试。",
                "bonus_tip": "结合同花顺业务谈：'在宏观研报时序预测中，我们用 Plan-and-Solve 拆分行业指标、财务指标与舆情指标，在具体抽取财务数据时用 ReAct 动态查库，兼具了宏观严谨与微观鲁棒'。"
            },
            {
                "category": "多智能体协同 (Multi-Agent)",
                "title": "在 Multi-Agent 系统中，如何设计多个智能体之间的通信协议？如何避免群体幻觉或死循环？",
                "framework": "【通信拓扑】常见有三种模式：1. 分层主从（Leader 集中调度 Worker）；2. 顺序流水线（前一个 Agent 的输出为后一个的输入）；3. 黑板模式（共享全局 State，各 Agent 异步读写）；\n【防死循环与幻觉控制】\n1. 严格设定全局 Max Rounds 阈值；\n2. 引入'批评家 / 风控官 (Critic / Risk Agent)'对抗校验机制；\n3. 结构化通信格式（强制 JSON Schema 交互，阻断无意义的寒暄客套话）。",
                "bonus_tip": "提到状态机设计：'利用 LangGraph 将状态流定义为有向无环图，状态迁移具备显式条件边，彻底根治死循环'。"
            },
            {
                "category": "工具调用与算力沙箱 (Tool Use)",
                "title": "大语言模型普遍对数值计算和时间序列分析不敏感，容易产生数字幻觉，在 Agent 系统中如何彻底根治？",
                "framework": "【问题根源】LLM 本质是基于 Token 概率采样的自回归预测器，不具备真正的算术逻辑，在处理大数相乘、复利贴现时极易编造虚假数字；\n【解决方案】\n1. 将大模型定位于'调度器'而非'计算器'；\n2. 引入 Python 代码解释器沙箱（Code Interpreter）：遇到计算问题强制生成 Python 脚本并在隔离沙箱中执行；\n3. 结构化约束（Function Calling）：大模型只提取输入参数并校验类型，实际计算逻辑交由确定性的计算引擎运行。",
                "bonus_tip": "提到量化准确率：'通过这种代码闭环，我们将财务比率分析的计算准确率提升到了 100%'。"
            },
            {
                "category": "金融检索增强 (Financial RAG)",
                "title": "在金融领域 RAG 中，为什么纯 Dense 稠密向量检索效果往往很差？工业级混合检索怎么做？",
                "framework": "【失效原因】金融文本充斥着特定股票代码（如 600519）、专业缩写（ROE, EBITDA）和微小数字差异（营收增长 5.1% vs 5.2%），稠密向量往往由于语义相近而无法精确区分代码与数字；\n【工业解法】\n1. 混合检索（Hybrid Search）：Dense 向量负责模糊语义召回，BM25 负责关键词与代码硬匹配；\n2. Reciprocal Rank Fusion (RRF) 倒数排名融合；\n3. Cross-Encoder 深度重排（Rerank），精准判定段落与问题的直接支撑性。",
                "bonus_tip": "主动提出时间衰减因子：'金融研报具备极强时效性，我们在打分中加入了时间衰减权重，优先命中最新财报季信息'。"
            }
        ]
    else:
        sop_3_questions = [
            {
                "category": "多模态与 VLM 核心",
                "title": "请详细介绍 LLaVA 架构的核心原理，以及它与 Flamingo、BLIP-2 的异同？",
                "framework": "【一句话定性】LLaVA 是最简洁纯粹的'视觉前缀化'多模态架构；\n【结构对比】1. Flamingo 采用 Cross-Attention 门控注入，参数量大且推理慢；2. BLIP-2 引入 Q-Former 桥接，利用可学习 Query 压缩视觉 token，结构复杂；3. LLaVA 直接通过简单轻量的 MLP 将视觉特征对齐到文本维度，作为 Prefix Token 与文本直接拼接，架构最简洁、对 LLM 原生理解力保留最充分；\n【演进趋势】从 LLaVA 1.0 的单层线性到 1.5 的 2 层 MLP，再到结合高分辨率 AnyRes，证明了简单结构在强大 LLM 支撑下的优越性。",
                "bonus_tip": "主动提到：在你自己的复现中，2 层 MLP 相比单层线性投影能够更好地拟合非线性流形映射，配合 GELU 激活函数，在 Stage 1 对齐时收敛速度明显提升。"
            },
            {
                "category": "工程与显存优化",
                "title": "在训练多模态大模型时，FlashAttention-2 为什么能降低显存并大幅加速？",
                "framework": "【瓶颈痛点】标准 Attention 需要计算并保存 NxN 大小的注意力矩阵到显存，显存复杂度 O(N^2)，且频繁在 GPU HBM (高带宽显存) 和 SRAM (片上高速缓存) 之间读写，属于访存密集型瓶颈；\n【核心原理】FlashAttention 采用 Tiling（分块分治）算法，将 Q/K/V 切块加载到快速 SRAM 中计算，利用在线 Softmax 动态更新标量，无需将完整的 NxN 矩阵写回 HBM，显存复杂度直接降至 O(N)；\n【版本提升】FlashAttention-2 优化了多头并行划分与非矩阵乘法操作的重叠，在 A100/4090 上可达到理论 FLOPs 利用率的 50%~70%。",
                "bonus_tip": "结合项目说：'在我的 Stage 2 指令微调中，输入拼接了 197 个视觉 token 和最长 512 的文本 token，序列达 700+，引入 FlashAttention-2 后批处理吞吐量提升了近 2 倍'。"
            },
            {
                "category": "算法手撕与数据流",
                "title": "请手写或描述：多模态前向传播时，如何正确处理视觉 Token 与文本 Token 的 Labels 掩码？",
                "framework": "【核心原则】因果自回归模型仅针对模型需要预测的 token 计算交叉熵损失；\n【实现细节】\n1. 输入张量：视觉特征过投影层得到 `visual_embeds [B, 197, D]`，文本词过 embedding 得到 `text_embeds [B, T, D]`，在 dim=1 拼接为 `[B, 197+T, D]`；\n2. 标签张量：构造全为 -100 的 `ignore_labels [B, 197]`，与文本标签 `labels [B, T]`（其中 Prompt 部分已被置为 -100，Answer 保留真实 Token ID）在 dim=1 拼接为 `[B, 197+T]`；\n3. PyTorch CrossEntropyLoss 默认 `ignore_index=-100`，视觉和 Prompt 位置自动跳过梯度反传。",
                "bonus_tip": "可以在白板上顺带把形状标出来：B x (N_vis + N_txt) x Hidden_Dim。"
            },
            {
                "category": "具身智能与策略迁移",
                "title": "在 OpenVLA 中，为什么要用离散或连续的 ActionHead？OFT (Orthogonal Finetuning) 的优势是什么？",
                "framework": "【ActionHead 机制】LLM 输出的是高维语义隐藏状态，机械臂控制需要连续的 7 自由度或关节位姿变化 (x, y, z, roll, pitch, yaw, gripper)。通过在末层接入轻量 MLP ActionHead，以 L1 回归 Loss 直接预测物理动作；\n【OFT 机制】正交微调（Orthogonal Finetuning）通过学习正交变换矩阵旋转预训练权重，在微调动作空间的同时严格保全了预训练神经元之间的夹角与几何关系，有效抑制对预训练视觉语义的灾难性遗忘。",
                "bonus_tip": "结合你的 Aloha 专家数据：'我们通过域随机化增加了光照与背景扰动，进一步增强了策略在仿真中的鲁棒性'。"
            }
        ]

    # ── 4. 专属定制化模拟面试官 System Prompt 生成器 ────────────
    def build_custom_mock_prompt(style: str = "geek", focus: str = "code") -> str:
        style_desc = {
            "geek": "资深技术极客 / 源码级架构师。你对候选人代码的每一行改动、张量维度流转、Agent 决策拓扑与显存算子瓶颈极度敏锐，严谨死磕底层细节。",
            "stress": "极度严厉挑剔的大厂业务与技术总监（压力面风格）。你习惯挑战方案合理性，连续追问'为什么不选备选方案B'，质疑量化指标真实性，考验抗压与深度思考。",
            "architect": "大模型与业务系统架构总监。你重点考察在高并发生产环境下的系统稳定性、长上下文管理、数据闭环飞轮与低成本规模化落地能力。"
        }.get(style, "资深技术面试官")

        focus_desc = {
            "code": "考察重点：代码实现细节、重写方法、数据处理与 Loader 边界、Label 掩码逻辑、工具调用接口实现。",
            "theory": "考察重点：底层原理推导、模态对齐动力学、灾难性遗忘机理、Agent 推理规划算法、正交微调数学意义。",
            "system": "考察重点：分布式显存规划（FSDP vs DDP）、Multi-Agent 通信拓扑、vLLM/KV Cache 优化、实时控制低延迟。"
        }.get(focus, "代码底层与工程实现")

        repos_bullet = ""
        for i, r in enumerate(valid_repos, 1):
            r_name = r.get("root_name", f"Repo-{i}")
            m_desc = ", ".join(f"{k}: {v}" for k, v in r.get("model_architecture", {}).items()) or "核心业务与模型模块"
            h_desc = "; ".join(r.get("code_highlights", [])) or "具备完整的代码实现与测试流程"
            repos_bullet += f"\n- **项目仓库 {i} [{r_name}]**:\n  * 核心架构: {m_desc}\n  * 真实代码亮点: {h_desc}\n"

        prompt_str = f"""# Role & Identity
你现在是【{company}】针对【{job_title}】岗位的主面试官。
面试官风格人设：{style_desc}
本次面试的核心考察偏好：{focus_desc}

---

# Candidate Real Profile (候选人真实资料档案)
【候选人简历与背景】
{resume}

【候选人本地代码仓库实证 (已透视提取)】{repos_bullet if repos_bullet else "（候选人上传了自定义项目工程）"}

---

# Target Job Requirements (目标岗位要求)
{jd}

---

# Interview Interaction Protocol (模拟面试互动执行规范)
作为顶级技术面试官，你必须严格执行以下专业规则：
1. 【单题深入，拒绝啰嗦】：每次轮次中，你【只允许抛出 1 个核心问题】（最多追加 1 个密切相关的衍生小问），严禁一次性抛出长篇问题清单！
2. 【死磕技术权衡】：必须结合候选人的真实代码与经历进行深挖，重点考察其**为什么这么设计**、**为什么不选业界备选方案B**，并测试其对当前最前沿演进技术的视野；
3. 【结构化反馈诊断】：每当候选人作答完毕，你必须严格按照以下 5 个结构块进行专业输出：
   - 💡【本轮得分】：给出 0-100 的客观评分；
   - 🔍【面试官评语】：针对其技术深度、逻辑清晰度与工程真实感进行点评；
   - ⚠️【致命扣分/遗漏点】：明确指出回答中欠缺的深度、没有提及的边界或潜在设计缺陷；
   - 🎯【满分示范话术】：输出一段简洁、硬核、具备量化数据与权衡依据的示范级应答；
   - ❓【下一轮提问】：顺着候选人的回答展开深度追问，或切换到下一个核心技术维度！

---

# Start Interview
现在，请正式开启面试！第一轮请从让候选人做简短自我介绍并阐明其核心项目中最硬核的技术创新与权衡决策开始。"""

        return prompt_str

    # ── 5. 反向提问策略 ─────────────────────────────────────────
    if is_agent_focus:
        sop_5_reverse = [
            {
                "stage": "技术一面 / 二面 (技术骨干 & 资深 Agent 架构师)",
                "purpose": "展现你对金融投研大模型落地的敏锐嗅觉与工程严谨性",
                "questions": [
                    "请问团队目前在处理金融时序预测时，Agent 调用外部工具的计算延迟（Latency）大概在什么量级？核心瓶颈在于大模型推理还是外部行情接口吞吐？",
                    "团队在构建投研 Agent 评估基准（Benchmark）时，主要采用哪些确定性的量化指标来衡量预测的有效性与抗幻觉能力？",
                    "如果我有幸加入团队，在前 1~3 个月内，最核心攻坚的子任务是 Agent 规划链路优化，还是金融垂直数据的清洗与微调？"
                ]
            },
            {
                "stage": "三面 / 业务总监面 (金融科技部门负责人 / VP)",
                "purpose": "展现商业落地宏观视野与技术战略洞察",
                "questions": [
                    "随着金融领域大模型从单点问答走向自主 Multi-Agent 决策系统，团队如何平衡'模型自主探索的灵活性'与'金融合规风控的确定性'？",
                    "未来 1-2 年内，部门在该金融投研预测系统上的商业化或业务落地里程碑是怎样的？"
                ]
            },
            {
                "stage": "HR 终面 (HRBP / 人力资源专家)",
                "purpose": "展现高情商、稳定性、团队契合度与进取心",
                "questions": [
                    "请问团队内部针对新同学的技术培养体系与 Mentor 机制是怎样的？",
                    "能否简单介绍一下团队近期的技术攻坚节奏与季度绩效考核机制？"
                ]
            }
        ]
    else:
        sop_5_reverse = [
            {
                "stage": "技术一面 / 二面 (技术骨干 & 资深架构师)",
                "purpose": "展现你对多模态技术趋势的深刻理解，以及脚踏实地的工作态度",
                "questions": [
                    "请问团队目前在多模态理解方向上，更侧重于通用高分辨率架构（如 AnyRes/Native ViT），还是针对具体垂直业务（如文档解析/具身控制）进行轻量化蒸馏与落地？",
                    "如果我有幸加入团队，在前 1~3 个月内，最核心要攻坚的业务场景或技术指标大概是什么？",
                    "团队目前在多模态大规模预训练的数据配比（图文对 vs 交错图文 vs 纯文本）上，有哪些经过实践验证的经验心得？"
                ]
            },
            {
                "stage": "三面 / 业务总监面 (部门负责人 / VP)",
                "purpose": "展现宏观战略视野、业务洞察与技术敏锐度",
                "questions": [
                    "随着 GPT-4o 和各大前沿模型将视觉原生融入（Native Multimodal），传统的'CLIP + MLP + LLM'拼接架构正在向统一端到端自回归演进，请问团队如何看待这一演进趋势及对应的算力与工程壁垒？",
                    "未来 1-2 年内，部门在大模型商业化落地或具身智能方向上的战略定位与预期里程碑是怎样的？"
                ]
            },
            {
                "stage": "HR 终面 (HRBP / 人力资源专家)",
                "purpose": "展现高情商、稳定性、团队契合度与进取心",
                "questions": [
                    "请问团队内部针对应届同学的技术培养体系与 Mentor 机制是怎样的？",
                    "能否简单介绍一下团队近期的技术攻坚氛围与季度考核机制？"
                ]
            }
        ]

    # ── 6. 30分钟临考速记卡 ─────────────────────────────────────
    if is_agent_focus:
        sop_6_cheatsheet = {
            "key_numbers": [
                {"name": "Agent 核心范式", "val": "ReAct (单步循环反思) vs Plan-and-Solve (两阶段预分解规划)"},
                {"name": "计算防幻觉保障", "val": "Python Code Interpreter 沙箱执行，计算准确率提升至 100%"},
                {"name": "Multi-Agent 拓扑", "val": "Leader-Worker 分层黑板协作，设置 Max Loops=8 熔断保护"},
                {"name": "金融混合 RAG 架构", "val": "Dense 语义向量 + BM25 专有代码 + Cross-Encoder 重排 Rerank"},
                {"name": "底层系统底座迁移", "val": "多模态 197 token 前缀映射与具身 L1 回归，可迁移至多源时序融合"}
            ],
            "golden_rules": [
                "回答 Agent 问题，先讲【决策拓扑机制】，再讲【外部工具集成与代码沙箱】，最后提【容错自愈与死循环熔断】。",
                "遇到计算幻觉问题，牢记核心金句：'大模型应当作为调度器与推理大脑，而非确定性计算器'。",
                "回答宏观业务时，时刻强调金融业务的'合规风控红线'与'可解释性'。"
            ]
        }
    else:
        sop_6_cheatsheet = {
            "key_numbers": [
                {"name": "CLIP Patch 数与特征维度", "val": "14x14 = 196 patch + 1 CLS = 197 tokens，特征维度 768"},
                {"name": "LLM 嵌入维度与参数", "val": "Qwen3-0.6B hidden_size = 1024, MLP: 768 -> 1024 -> 1024 (约 1.8M 参数)"},
                {"name": "Stage 1 指标", "val": "SA1B 100k，冻结 CLIP+LLM，仅训 Projection，验证集 PPL: 16 -> 6.4"},
                {"name": "Stage 2 指标", "val": "CogVLM 120k，冻结 CLIP，微调 Projection+LLM，验证集 PPL: 20 -> 8.5"},
                {"name": "OpenVLA 成果", "val": "Aloha 600 条轨迹，4卡 4090 FSDP，50k step 收敛，成功率 81%"}
            ],
            "golden_rules": [
                "回答任何架构问题，先给【全局结论】，再报【张量流转数据】，最后提【实操踩坑与技术权衡决策】。",
                "被问到不会的难题时，切勿瞎猜！话术：'这块我之前的项目没有直接涉及，但我理解其核心底层逻辑是...如果在我们系统里实现，我会从A和B两个角度尝试'。",
                "时刻记住：你亲手写过多轮增量差值编码，亲手改过 CLIP forward，这是 90% 候选人做不到的硬核壁垒！自信展开！"
            ]
        }

    mock_prompt_geek = build_custom_mock_prompt(style="geek", focus="code")
    return {
        "sop_0_resume_optimizer": sop_0_resume_optimizer,
        "sop_1_matching": sop_1_matching,
        "sop_2_star": sop_2_star,
        "sop_3_questions": sop_3_questions,
        "sop_4_mock": {
            "styles": ["geek", "stress", "architect"],
            "prompt": mock_prompt_geek
        },
        "sop_4_prompt_builder": build_custom_mock_prompt,
        "default_mock_prompt": mock_prompt_geek,
        "sop_5_reverse": sop_5_reverse,
        "sop_6_cheatsheet": sop_6_cheatsheet
    }
