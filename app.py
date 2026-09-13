"""
面试全流程 SOP 备战系统 (InterviewSOP Master) - FastAPI 后端主服务
支持多代码仓库批量透视、PDF/文本简历智能解析与 Demo 演示样例解耦
"""

import os
import sys
import time
import json
import re
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from pypdf import PdfReader

from repo_scanner import RepoScanner
from knowledge_base import (
    DEMO_RESUME,
    DEMO_COMPANY,
    DEMO_JOB_TITLE,
    DEMO_JD,
    generate_expert_sop
)

app = FastAPI(title="InterviewSOP Master API", version="1.3.0")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# 数据模型
class ScanReposRequest(BaseModel):
    repo_paths: List[str]

class GenerateSOPRequest(BaseModel):
    company: str
    job_title: str
    jd: str
    resume: str
    repo_paths: Optional[List[str]] = []
    repo_path: Optional[str] = ""
    style: Optional[str] = "geek"
    focus: Optional[str] = "code"

class GeneratePromptRequest(BaseModel):
    company: str
    job_title: str
    jd: str
    resume: str
    repo_paths: Optional[List[str]] = []
    style: str = "geek"
    focus: str = "code"

class BrowseFolderRequest(BaseModel):
    initial_dir: Optional[str] = ""

class AgentExportRequest(BaseModel):
    company: str
    job_title: str
    jd: str
    resume: str
    repo_paths: Optional[List[str]] = []

class AgentImportRequest(BaseModel):
    file_path: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None

class Task0ExportRequest(BaseModel):
    company: Optional[str] = ""
    job_title: Optional[str] = ""
    jd: Optional[str] = ""
    resume: Optional[str] = ""
    repo_paths: Optional[List[str]] = []

class Task0ImportRequest(BaseModel):
    file_path: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    current_resume: Optional[str] = ""

class ExportStageRequest(BaseModel):
    stage: int
    company: Optional[str] = ""
    job_title: Optional[str] = ""
    jd: Optional[str] = ""
    resume: Optional[str] = ""
    repo_paths: Optional[List[str]] = []
    style: Optional[str] = "geek"
    focus: Optional[str] = "code"

class ImportStageRequest(BaseModel):
    stage: int
    output_data: Optional[Dict[str, Any]] = None
    current_resume: Optional[str] = ""
    preload_if_missing: Optional[bool] = True
    force_preload: Optional[bool] = False

class PreloadStageRequest(BaseModel):
    stage: int
    current_resume: Optional[str] = ""

class SingleRepoScanRequest(BaseModel):
    repo_path: str

@app.get("/api/defaults")
def get_defaults():
    """获取初始空状态（不预设任何死板内容，保持用户自主填入）"""
    return {
        "company": "",
        "job_title": "",
        "jd": "",
        "resume": "",
        "repo_paths": []
    }

@app.get("/api/demo_data")
def get_demo_data():
    """获取多模态与具身智能 Demo 演示样例（Mini-LLaVA + OpenVLA）"""
    llava_dir = Path(r"C:\Users\24974\Desktop\DL\LLaVA").resolve()
    default_repo_path = str(llava_dir) if llava_dir.exists() else str(Path(BASE_DIR).parent.resolve())
    return {
        "company": DEMO_COMPANY,
        "job_title": DEMO_JOB_TITLE,
        "jd": DEMO_JD,
        "resume": DEMO_RESUME,
        "repo_paths": [default_repo_path]
    }

@app.get("/api/demo_agent_data")
def get_demo_agent_data():
    """获取金融投研预测与大模型 Agent 架构 Demo 演示样例（同花顺实战）"""
    from knowledge_base import DEMO_AGENT_COMPANY, DEMO_AGENT_JOB_TITLE, DEMO_AGENT_JD
    llava_dir = Path(r"C:\Users\24974\Desktop\DL\LLaVA").resolve()
    default_repo_path = str(llava_dir) if llava_dir.exists() else str(Path(BASE_DIR).parent.resolve())
    return {
        "company": DEMO_AGENT_COMPANY,
        "job_title": DEMO_AGENT_JOB_TITLE,
        "jd": DEMO_AGENT_JD,
        "resume": DEMO_RESUME,
        "repo_paths": [default_repo_path]
    }

@app.post("/api/parse_resume_file")
async def parse_resume_file(file: UploadFile = File(...)):
    """智能解析上传的简历文件（完美支持 PDF、Markdown、纯文本，告别二进制乱码）"""
    import re
    filename = (file.filename or "").lower()
    content_bytes = await file.read()
    
    # 1. 如果是 PDF 文件
    if filename.endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(content_bytes))
            pages_text = []
            for i, page in enumerate(reader.pages):
                txt = page.extract_text() or ""
                # 清洗单页文本与多余非打印字符
                txt = txt.replace("\x00", "").replace("\r\n", "\n")
                # 规范化多余空格
                txt = re.sub(r'[ \t]+', ' ', txt)
                txt = txt.strip()
                if txt:
                    pages_text.append(txt)
                    
            full_text = "\n\n".join(pages_text).strip()
            # 规范化多余空行
            full_text = re.sub(r'\n{3,}', '\n\n', full_text)
            
            if not full_text:
                return JSONResponse(
                    status_code=400,
                    content={"error": "该 PDF 解析出的文字为空，可能属于纯图片扫描件，请尝试将文字复制后直接粘贴。"}
                )
            return {
                "success": True,
                "text": full_text,
                "pages": len(reader.pages),
                "filename": file.filename
            }
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"error": f"PDF 解析异常: {str(e)}，建议直接复制文本粘贴。"}
            )
            
    # 2. 如果是 Word .docx 文件（使用标准库 zipfile + xml 提取文本）
    if filename.endswith(".docx"):
        try:
            import zipfile
            import xml.etree.ElementTree as ET
            with zipfile.ZipFile(BytesIO(content_bytes)) as z:
                xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.iterfind('.//w:p', ns):
                texts = [node.text for node in p.iterfind('.//w:t', ns) if node.text]
                if texts:
                    paragraphs.append("".join(texts))
            full_text = "\n\n".join(paragraphs).strip()
            if not full_text:
                return JSONResponse(status_code=400, content={"error": "该 Word 文件提取文字为空，请尝试直接复制粘贴文本。"})
            return {"success": True, "text": full_text, "filename": file.filename}
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Word (.docx) 解析异常: {str(e)}，建议复制文本直接粘贴。"})

    # 3. 如果是纯文本 / Markdown / JSON
    try:
        text = content_bytes.decode("utf-8")
        return {"success": True, "text": text, "filename": file.filename}
    except UnicodeDecodeError:
        try:
            text = content_bytes.decode("gbk")
            return {"success": True, "text": text, "filename": file.filename}
        except Exception:
            return JSONResponse(
                status_code=400,
                content={"error": "文本文件编码无法识别，请使用 UTF-8 格式另存后重试。"}
            )

def _open_native_folder_picker(initial_dir: str = "") -> str:
    """在 Windows 上调起原生系统文件夹选择框（双通道：PowerShell TopMost WinForms + Tkinter 兜底）"""
    import subprocess
    import json

    init_path = initial_dir if (initial_dir and os.path.exists(initial_dir)) else ""

    # 通道 1: Windows PowerShell 强置顶 FolderBrowserDialog
    if sys.platform == "win32":
        try:
            ps_script = f"""
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Add-Type -AssemblyName System.Windows.Forms
$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$form.WindowState = [System.Windows.Forms.FormWindowState]::Minimized
$form.Show()
$form.Activate()
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = '请选择代码仓库根目录'
$dialog.ShowNewFolderButton = $true
if ('{init_path}') {{ $dialog.SelectedPath = '{init_path}' }}
$res = $dialog.ShowDialog($form)
$form.Close()
if ($res -eq [System.Windows.Forms.DialogResult]::OK) {{
    Write-Output $dialog.SelectedPath
}}
"""
            res = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-STA", "-Command", ps_script],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=60
            )
            out_path = res.stdout.strip()
            if out_path and os.path.exists(out_path):
                return out_path
        except Exception:
            pass

    # 通道 2: Tkinter 置顶窗口兜底
    py_code = f"""
import sys, json
try:
    import tkinter as tk
    from tkinter import filedialog
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    root = tk.Tk()
    root.geometry('1x1+-10000+-10000')
    root.attributes('-topmost', True)
    root.lift()
    root.focus_force()
    path = filedialog.askdirectory(parent=root, title="请选择代码仓库根目录", initialdir={json.dumps(init_path)})
    root.destroy()
    if path:
        sys.stdout.write(path.strip())
except Exception as e:
    sys.stderr.write(str(e))
"""
    try:
        res = subprocess.run(
            [sys.executable, "-c", py_code],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60
        )
        return res.stdout.strip()
    except Exception:
        return ""

@app.post("/api/browse_folder")
async def browse_folder(req: Optional[BrowseFolderRequest] = None):
    """调起操作系统原生文件夹选择对话框，免除用户手动输入路径"""
    import asyncio
    init_dir = req.initial_dir if (req and req.initial_dir) else str(Path(BASE_DIR).parent.resolve())
    selected_path = await asyncio.to_thread(_open_native_folder_picker, init_dir)
    if selected_path:
        norm_path = str(Path(selected_path).resolve())
        return {"success": True, "path": norm_path, "name": Path(norm_path).name or norm_path}
    else:
        return {"success": False, "cancelled": True}

@app.get("/api/quick_directories")
def get_quick_directories():
    """快速发现当前工作区及附近的候选代码仓库，供用户一键点选"""
    cwd = Path(BASE_DIR).parent.resolve()  # c:\Users\24974\Desktop\DL\LLaVA
    parent = cwd.parent.resolve()          # c:\Users\24974\Desktop\DL
    candidates = []

    # 1. 当前 LLaVA 项目
    candidates.append({
        "name": cwd.name,
        "path": str(cwd),
        "desc": "当前多模态大模型项目仓库 (Mini-LLaVA / Qwen3 / CLIP)",
        "badge": "当前工作区"
    })

    # 2. 同级目录项目 (例如 RoboTwin 具身智能)
    if parent.exists():
        for item in parent.iterdir():
            if item.is_dir() and item != cwd and not item.name.startswith(('.', '_')):
                desc = "同级项目代码目录"
                badge = "推荐项目"
                if "robotwin" in item.name.lower():
                    desc = "具身智能操控策略项目 (OpenVLA / Aloha / RoboTwin)"
                    badge = "具身智能"
                candidates.append({
                    "name": item.name,
                    "path": str(item.resolve()),
                    "desc": desc,
                    "badge": badge
                })

    # 3. 桌面代码仓库候选
    desktop = Path.home() / "Desktop"
    if desktop.exists() and desktop != parent:
        try:
            for item in desktop.iterdir():
                if item.is_dir() and not item.name.startswith(('.', '_')) and item != parent:
                    if (item / ".git").exists() or any(item.glob("*.py")):
                        candidates.append({
                            "name": item.name,
                            "path": str(item.resolve()),
                            "desc": "桌面本地代码工程",
                            "badge": "桌面仓库"
                        })
        except Exception:
            pass

    return {"success": True, "candidates": candidates}

@app.get("/api/list_subdirectories")
def list_subdirectories(path: Optional[str] = ""):
    """列出指定路径下的子目录，支持网页内可视化浏览与树形点选"""
    import string
    
    shortcuts = [
        {"name": "当前项目 (LLaVA)", "path": str(Path(BASE_DIR).parent.resolve())},
        {"name": "DL 根目录", "path": str(Path(BASE_DIR).parent.parent.resolve())},
        {"name": "桌面 (Desktop)", "path": str(Path.home() / "Desktop")},
        {"name": "用户主目录", "path": str(Path.home())}
    ]
    
    if not path:
        drives = []
        if sys.platform == "win32":
            for d in string.ascii_uppercase:
                dp = f"{d}:\\"
                if os.path.exists(dp):
                    drives.append({"name": f"本地磁盘 ({d}:)", "path": dp, "is_drive": True})
        return {
            "current_path": "",
            "parent_path": "",
            "shortcuts": shortcuts,
            "directories": drives or [{"name": s["name"], "path": s["path"]} for s in shortcuts]
        }

    target = Path(path).resolve()
    if not target.exists() or not target.is_dir():
        return JSONResponse(status_code=400, content={"error": "指定的目录不存在"})

    subdirs = []
    try:
        for item in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.is_dir() and not item.name.startswith(('.', '__pycache__', 'node_modules', '$')):
                is_repo = (item / ".git").exists() or any(item.glob("*.py"))
                subdirs.append({
                    "name": item.name,
                    "path": str(item.resolve()),
                    "is_repo": is_repo
                })
    except PermissionError:
        pass

    parent_path = str(target.parent.resolve()) if target.parent != target else ""
    is_current_repo = (target / ".git").exists() or any(target.glob("*.py"))

    return {
        "current_path": str(target),
        "parent_path": parent_path,
        "shortcuts": shortcuts,
        "directories": subdirs,
        "is_repo": is_current_repo
    }

@app.post("/api/scan_repos")
def scan_repositories(req: ScanReposRequest):
    """批量扫描多个本地项目仓库路径"""
    paths = [p.strip() for p in req.repo_paths if p.strip()]
    if not paths:
        return {"success": True, "results": []}
        
    results = RepoScanner.scan_multiple(paths)
    return {"success": True, "results": results}

@app.post("/api/scan_repo")
def scan_single_repo(req: SingleRepoScanRequest):
    """扫描单个指定代码仓库"""
    scanner = RepoScanner(req.repo_path)
    res = scanner.scan()
    return res

@app.post("/api/generate_sop")
def generate_sop(req: GenerateSOPRequest):
    """生成全流程 6 维一体面试 SOP (支持多仓库与自定义简历)"""
    paths = [p.strip() for p in (req.repo_paths or []) if p.strip()]
    if not paths and req.repo_path and req.repo_path.strip():
        paths = [req.repo_path.strip()]
        
    # 扫描所有输入的仓库
    repos_info = RepoScanner.scan_multiple(paths) if paths else []
    
    # 构建全套 SOP
    sop_data = generate_expert_sop(
        company=req.company,
        job_title=req.job_title,
        jd=req.jd,
        resume=req.resume,
        repos_info=repos_info
    )
    
    # 动态生成专属面试官 Prompt
    builder = sop_data.pop("sop_4_prompt_builder", None)
    if builder:
        custom_prompt = builder(style=req.style or "geek", focus=req.focus or "code")
    else:
        custom_prompt = sop_data.get("default_mock_prompt", "")
        
    sop_data["mock_interviewer_prompt"] = custom_prompt
    sop_data["repos_summary"] = [r.get("summary", {}) for r in repos_info]
    sop_data["input_meta"] = {
        "company": req.company,
        "job_title": req.job_title,
        "repo_paths": paths
    }
    
    return {"success": True, "sop": sop_data}

@app.post("/api/generate_mock_prompt")
def generate_mock_prompt(req: GeneratePromptRequest):
    """根据多仓库与个性化偏好动态刷新面试官 System Prompt"""
    paths = [p.strip() for p in (req.repo_paths or []) if p.strip()]
    repos_info = RepoScanner.scan_multiple(paths) if paths else []
    
    sop_data = generate_expert_sop(
        company=req.company,
        job_title=req.job_title,
        jd=req.jd,
        resume=req.resume,
        repos_info=repos_info
    )
    builder = sop_data.get("sop_4_prompt_builder")
    prompt_str = builder(style=req.style, focus=req.focus) if builder else sop_data.get("default_mock_prompt", "")
    return {"success": True, "prompt": prompt_str}

@app.post("/api/agent/export_inputs")
def export_inputs_for_agent(req: AgentExportRequest):
    """将当前用户输入的上下文与扫描到的代码库特征导出为标准 JSON 格式供外部 Agent 处理"""
    paths = [p.strip() for p in (req.repo_paths or []) if p.strip()]
    repos_info = RepoScanner.scan_multiple(paths) if paths else []
    
    context_data = {
        "company": req.company or "目标公司",
        "job_title": req.job_title or "应聘岗位",
        "jd": req.jd or "",
        "resume": req.resume or "",
        "repo_paths": paths,
        "scanned_repo_facts": [
            {
                "root_name": r.get("root_name", "ProjectRepo"),
                "repo_path": r.get("repo_path", ""),
                "model_architecture": r.get("summary", {}).get("model_architecture", {}),
                "code_highlights": r.get("summary", {}).get("code_highlights", []),
                "key_dependencies": r.get("summary", {}).get("dependencies", []),
                "total_python_files": r.get("summary", {}).get("python_files_count", 0),
                "core_scripts": r.get("summary", {}).get("core_scripts", [])
            }
            for r in repos_info
        ]
    }
    
    # 写入 agent_llm_tasks/inputs/current_context.json
    out_dir = Path(BASE_DIR) / "agent_llm_tasks" / "inputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "current_context.json"
    out_file.write_text(json.dumps(context_data, ensure_ascii=False, indent=2), encoding="utf-8")
    
    return {
        "success": True,
        "context": context_data,
        "saved_path": str(out_file),
        "filename": "input_context.json",
        "message": "已成功导出候选人全景上下文至 current_context.json"
    }

# ==================== Agent 成果全阶段规范化与兜底预装核心层 ====================
def generate_builtin_stage_mock(stage_num: int) -> dict:
    """当所有外部文件均不可用时的内置零依赖安全基准数据"""
    if stage_num == 1:
        return {
            "sop_0_resume_optimizer": [
                {
                    "project_id": "proj_1",
                    "project_name": "Mini-LLaVA: 端到端轻量化多模态大模型系统开发",
                    "target_jd_alignment": "金融投研 Agent 底座模型多模态时序/文档融合与轻量化微调",
                    "original_snippet": "复现了 LLaVA 架构，连接视觉与语言模型，实现基本的图像理解。优化了模型训练过程，减少了显存占用并完成测试。",
                    "diagnosis": [
                        { "type": "动词表现力弱", "flaw": "使用'复现'、'连接'、'减少'等被动词汇，缺乏资深主导感。", "tip": "替换为'自主设计并主导研发'、'构建双层非线性特征映射桥接器'。" },
                        { "type": "量化与工程壁垒缺失", "flaw": "未指明具体参数量、Patch token 数及收敛指标。", "tip": "补充 CLIP 197 个 patch 特征映射、1.8M 参数 MLP、FSDP ZeRO-3、PPL 降至 6.4 等核心事实。" }
                    ],
                    "keyword_matches": [
                        { "keyword": "多模态架构设计", "status": "已深度命中" },
                        { "keyword": "分布式显存优化 (FSDP)", "status": "核心壁垒强化" }
                    ],
                    "refined_bullet_points": [
                        "【架构自研重构】主导设计轻量级多模态底座，自研两层 MLP 投射层（768->1024->1024，1.8M 参数）将 CLIP-ViT 提取的 197 个 Patch 特征与 Qwen 语言模型深度对齐，兼顾非线性表征与极低推理延迟；",
                        "【两阶段训练闭环】实施'对齐预训练 + 指令微调'两阶段策略，Stage 1 冻结主干仅微调投影层（SA1B 100k，PPL 自 16.0 降至 6.4），Stage 2 联合优化使得 CogVLM 验证 PPL 达到 8.5；",
                        "【分布式加速调优】攻坚 4 卡 RTX 4090 分布式环境，重构 FSDP ZeRO-3 显存切分拓扑并结合 FlashAttention-2，显存占用降低 58%，单步迭代耗时缩短 42%，实现 100% 满负载零 OOM 稳定收敛。"
                    ]
                }
            ]
        }
    elif stage_num == 2:
        return {
            "sop_1_matching": {
                "overall_score": 93,
                "radar_dimensions": [
                    { "dimension": "代码工程事实契合度", "score": 96, "comment": "已深度融合本地真实代码亮点", "reason": "已深度融合本地真实代码亮点" },
                    { "dimension": "大模型核心架构理解", "score": 94, "comment": "多模态视觉投影与语言基座机理清晰", "reason": "多模态视觉投影与语言基座机理清晰" },
                    { "dimension": "系统优化与显存工程", "score": 92, "comment": "FSDP ZeRO-3与算子加速实战落地", "reason": "FSDP ZeRO-3与算子加速实战落地" },
                    { "dimension": "业务落地与场景匹配", "score": 95, "comment": "精准命中目标企业岗位要求", "reason": "精准命中目标企业岗位要求" },
                    { "dimension": "高维表达与决策壁垒", "score": 98, "comment": "STAR四段式量化复盘与方案B权衡深入", "reason": "STAR四段式量化复盘与方案B权衡深入" }
                ],
                "key_strengths": [
                    "精通从零搭建多模态大模型架构与底层特征映射流转，对基座模型机理理解深入",
                    "熟练攻坚消费级显卡集群分布式显存瓶颈与 FlashAttention-2 融合算子加速"
                ],
                "skill_gaps": [
                    "需进一步丰富对特定垂域指标体系与风控合规规则的敏感度"
                ],
                "sprint_priorities": [
                    "基于精修简历复盘核心 STAR 故事",
                    "对照技术权衡矩阵梳理技术决策依据"
                ]
            },
            "sop_2_star": [
                {
                    "project_name": "Mini-LLaVA: 端到端轻量化多模态大模型系统开发",
                    "situation": "多模态大模型参数体量庞大、推理开销高，跨模态对齐收敛较慢且易出现图文割裂。",
                    "task": "从零构建端到端轻量多模态系统，设计高表现力投射层并在消费级集群实现全流程低成本分布式收敛。",
                    "action": "自研两层 MLP 投射层，结合两阶段微调策略，集成 FSDP ZeRO-3 显存分片与 FlashAttention-2 加速。",
                    "result": "验证集 PPL 从 16.0 降至 6.4，显存降低 58%，实现 4 卡无 OOM 稳定收敛。",
                    "trade_off_matrix": [
                        {
                            "decision_point": "跨模态投影层架构选择 (MLP vs Q-Former vs Cross-Attention)",
                            "chosen_solution": "2 层非线性 MLP (768 -> 1024 -> 1024，含 GELU)",
                            "alternative_solution": "Q-Former 交叉注意力重压缩结构",
                            "why_not_alternative": "Q-Former 参数庞大且大幅增加推理时延；2层 MLP 仅 1.8M 参数，计算开销接近零且表征能力完备。",
                            "pros_of_chosen": "参数量极小，推理延迟极低，训练稳定且易收敛",
                            "cons_of_chosen": "对基座 LLM 语义表达依赖强，需高纯度对齐数据",
                            "frontier_technology": "业内前沿正在探索动态多尺度投影与混合专家 (MoE) 门控路由桥接"
                        }
                    ],
                    "pitfalls_and_countermeasures": [
                        {
                            "question": "多模态拼接输入计 Loss 时，视觉 token 未做掩码导致语义漂移与梯度爆炸怎么办？",
                            "danger": "视觉特征直接参与自回归交叉熵计算，梯度倒灌污染基座 LLM",
                            "best_answer": "前向构造阶段对前 197 个视觉 Token 统一赋予 -100 标签矩阵，触发 CrossEntropyLoss 自动忽略反传。"
                        }
                    ]
                }
            ]
        }
    else:
        return {
            "sop_3_questions": [
                {
                    "category": "智能体推理机制 (Agent Reasoning)",
                    "title": "请深入阐述 ReAct 与 Plan-and-Solve 的核心区别？在金融研报分析中各自适用的场景是什么？",
                    "framework": "【核心定性】ReAct 属于'单步探索与观察循环'，Plan-and-Solve 属于'两阶段全局规划与逐项求解'；\n【执行差异】1. ReAct 遵循 Thought -> Action -> Observation，遇到动态不确定性能即时自愈，但在长链条中易迷失；2. Plan-and-Solve 预先生成 DAG 执行计划并逐项求解，尤其适合多指标连环对比；\n【工业结合】成熟架构中通常采用 Plan-and-Solve 作为顶层规划器，各子任务内部调用小型 ReAct 执行工具自愈与重试。",
                    "bonus_tip": "结合业务谈：'在宏观研报时序预测中，我们用 Plan-and-Solve 拆分行业指标，在具体抽取数据时用 ReAct 动态查库'。"
                }
            ],
            "mock_interviewer_prompt": "# Role & Identity\n你现在是针对大模型算法专家岗位的主面试官。面试风格严谨冷峻、死磕工程细节与方案B权衡。\n请直接开启第一轮提问，深挖候选人核心项目中的技术决策！",
            "sop_5_reverse": [
                {
                    "stage": "技术一面 / 二面",
                    "purpose": "展现对技术落地细节的严谨与敏感度",
                    "questions": ["团队目前在模型推理延迟优化的主要瓶颈在于算子还是显存带宽？"]
                }
            ],
            "sop_6_cheatsheet": {
                "key_numbers": [
                    { "name": "投射层参数", "val": "1.8M 参数，2层 MLP，延时占比 < 2%" },
                    { "name": "显存优化收益", "val": "FSDP ZeRO-3 降低显存占用 58%" }
                ],
                "golden_rules": [
                    "回答架构选型，必须同时列出备选方案B与否决依据。",
                    "遇到数值计算幻觉，强调代码沙箱与调度器定位。"
                ]
            }
        }

def get_or_create_stage_data(stage_num: int, force_mock: bool = False) -> tuple:
    """
    获取指定阶段的数据。返回 (data: dict, is_preloaded: bool)
    若目标文件不存在或 force_mock 为 True，则自动从 example_output.json 或内置基准提取并写入磁盘。
    """
    agent_tasks_dir = BASE_DIR / "agent_llm_tasks"
    outputs_dir = agent_tasks_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    target_file = outputs_dir / f"stage_{stage_num}_output.json"
    example_file = outputs_dir / "example_output.json"
    output_file = outputs_dir / "output.json"

    stage_keys = {
        1: ["sop_0_resume_optimizer"],
        2: ["sop_1_matching", "sop_2_star"],
        3: ["sop_3_questions", "mock_interviewer_prompt", "sop_5_reverse", "sop_6_cheatsheet"]
    }
    keys = stage_keys.get(stage_num, [])

    if not force_mock and target_file.exists():
        try:
            raw_data = json.loads(target_file.read_text(encoding="utf-8"))
            if any(k in raw_data for k in keys):
                return raw_data, False
        except Exception:
            pass

    # 尝试从全局 output.json 提取
    if not force_mock and output_file.exists():
        try:
            raw_out = json.loads(output_file.read_text(encoding="utf-8"))
            if any(k in raw_out for k in keys):
                stage_data = {k: raw_out[k] for k in keys if k in raw_out}
                target_file.write_text(json.dumps(stage_data, ensure_ascii=False, indent=2), encoding="utf-8")
                return stage_data, True
        except Exception:
            pass

    # 尝试从 example_output.json 预装
    if example_file.exists():
        try:
            ex_data = json.loads(example_file.read_text(encoding="utf-8"))
            stage_data = {k: ex_data[k] for k in keys if k in ex_data}
            if stage_data:
                target_file.write_text(json.dumps(stage_data, ensure_ascii=False, indent=2), encoding="utf-8")
                return stage_data, True
        except Exception:
            pass

    # 终极保底：写入内置示例
    built_in = generate_builtin_stage_mock(stage_num)
    target_file.write_text(json.dumps(built_in, ensure_ascii=False, indent=2), encoding="utf-8")
    return built_in, True

def normalize_stage_1(data: Any) -> list:
    """Stage 1 数据结构自动规范化，彻底兼容各版本字段命名差异"""
    projs = []
    if isinstance(data, list):
        projs = data
    elif isinstance(data, dict):
        projs = data.get("sop_0_resume_optimizer") or data.get("projects") or next((v for v in data.values() if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and ("project_name" in v[0] or "project_id" in v[0])), [])
    
    normalized_projs = []
    for idx, p in enumerate(projs):
        if not isinstance(p, dict):
            continue
        bullets = p.get("refined_bullet_points") or p.get("optimized_bullets") or []
        if isinstance(bullets, str):
            bullets = [bullets]
        
        diag = p.get("diagnosis") or p.get("diagnostic_flaws") or []
        normalized_diag = []
        for d in diag:
            if isinstance(d, dict):
                normalized_diag.append({
                    "type": d.get("type", d.get("label", "失分盲点")),
                    "flaw": d.get("flaw", d.get("issue", "原描述表现力不足")),
                    "tip": d.get("tip", d.get("solution", "结合具体参数与底层实现进行破局话术重塑"))
                })
            elif isinstance(d, str):
                normalized_diag.append({"type": "失分盲点", "flaw": d, "tip": "补充工程量化事实"})

        kw = p.get("keyword_matches") or []
        alignment = p.get("target_jd_alignment") or (", ".join(p.get("target_role_points", [])) if isinstance(p.get("target_role_points"), list) else "") or "核心工程架构落地"
        snippet = p.get("original_snippet") or p.get("original_section") or "原有项目经历回顾"

        normalized_projs.append({
            "project_id": p.get("project_id", f"proj_{idx+1}"),
            "project_name": p.get("project_name", f"核心工程项目 {idx+1}"),
            "target_jd_alignment": alignment,
            "original_snippet": snippet,
            "diagnosis": normalized_diag,
            "keyword_matches": kw,
            "refined_bullet_points": bullets,
            "optimized_bullets": bullets
        })
    return normalized_projs

def normalize_stage_2(data: Any) -> tuple:
    """Stage 2 数据结构自动规范化，彻底兼容五维雷达与 STAR 矩阵"""
    if not isinstance(data, dict):
        data = {}
    matching = data.get("sop_1_matching") or data.get("matching") or (data if ("radar" in data or "dimensions" in data or "score" in data or "killer_points" in data) else None)
    star = data.get("sop_2_star") or data.get("star") or []
    
    if not isinstance(matching, dict):
        matching = generate_builtin_stage_mock(2)["sop_1_matching"]
    else:
        dims = matching.get("radar_dimensions") or matching.get("dimensions") or []
        norm_dims = []
        for d in dims:
            if isinstance(d, dict):
                c = d.get("comment") or d.get("reason") or "能力指标表现优异"
                norm_dims.append({
                    "dimension": d.get("dimension", "核心专业能力"),
                    "score": d.get("score", 90),
                    "comment": c,
                    "reason": c
                })
        matching["radar_dimensions"] = norm_dims
        matching["key_strengths"] = matching.get("key_strengths") or matching.get("strengths") or ["具备坚实的工程与算法底座"]
        matching["skill_gaps"] = matching.get("skill_gaps") or matching.get("gaps") or []
        matching["sprint_priorities"] = matching.get("sprint_priorities") or matching.get("priorities") or ["复盘核心选型权衡依据"]

    norm_star = []
    if isinstance(star, list) and star:
        for proj in star:
            if not isinstance(proj, dict):
                continue
            sit = proj.get("situation", "")
            tsk = proj.get("task", "")
            act = proj.get("action", "")
            rst = proj.get("result", "")
            if "star_framework" in proj and isinstance(proj["star_framework"], dict):
                sf = proj["star_framework"]
                sit = sf.get("situation", sit)
                tsk = sf.get("task", tsk)
                act = sf.get("action", act)
                rst = sf.get("result", rst)
            proj["star_framework"] = {
                "situation": sit,
                "task": tsk,
                "action": act,
                "result": rst
            }
            proj["situation"] = sit
            proj["task"] = tsk
            proj["action"] = act
            proj["result"] = rst

            toms = proj.get("trade_off_matrix") or []
            norm_toms = []
            for tom in toms:
                if isinstance(tom, dict):
                    alt = tom.get("alternative_solution") or tom.get("alternative_solutions") or "方案B备选"
                    why_not = tom.get("why_not_alternative") or tom.get("trade_off_rationale") or "备选方案计算开销过大或侵入基座架构"
                    pros = tom.get("pros_of_chosen") or "架构极简高效，参数量轻量，低延迟推理"
                    cons = tom.get("cons_of_chosen") or "需在对齐预训练阶段严格对齐特征分布"
                    norm_toms.append({
                        "decision_point": tom.get("decision_point", "核心技术选型决策"),
                        "chosen_solution": tom.get("chosen_solution", "主导自研方案"),
                        "alternative_solution": alt,
                        "alternative_solutions": alt,
                        "pros_of_chosen": pros,
                        "cons_of_chosen": cons,
                        "why_not_alternative": why_not,
                        "trade_off_rationale": why_not,
                        "frontier_technology": tom.get("frontier_technology", "业内前沿正在探索动态多尺度投影与混合专家架构")
                    })
            proj["trade_off_matrix"] = norm_toms

            pits = proj.get("pitfalls_and_countermeasures") or proj.get("pitfalls_and_solutions") or []
            norm_pits = []
            for pit in pits:
                if isinstance(pit, dict):
                    q = pit.get("question") or pit.get("pitfall") or pit.get("core_pitfall") or "潜在失分连环追问"
                    danger = pit.get("danger") or pit.get("failure_scenario") or "核心失分盲点"
                    ans = pit.get("best_answer") or pit.get("solution") or pit.get("solution_strategy") or "从张量流转与算子掩码角度进行破局解答"
                    norm_pits.append({
                        "question": q,
                        "danger": danger,
                        "best_answer": ans,
                        "pitfall": q,
                        "solution": ans
                    })
            proj["pitfalls_and_countermeasures"] = norm_pits
            proj["pitfalls_and_solutions"] = norm_pits
            norm_star.append(proj)
    else:
        norm_star = generate_builtin_stage_mock(2)["sop_2_star"]

    return matching, norm_star

def normalize_stage_3(data: Any) -> tuple:
    """Stage 3 数据结构自动规范化，彻底兼容真题、Prompt、反问与速记"""
    if not isinstance(data, dict):
        data = {}
    q = data.get("sop_3_questions") or data.get("questions") or []
    mock_p = data.get("mock_interviewer_prompt") or data.get("prompt") or ""
    rev = data.get("sop_5_reverse") or data.get("reverse_questions") or []
    cheat = data.get("sop_6_cheatsheet") or data.get("cheatsheet") or {}

    norm_q = []
    if isinstance(q, list) and q:
        for item in q:
            if isinstance(item, dict):
                norm_q.append({
                    "category": item.get("category", "核心技术问答"),
                    "title": item.get("title", item.get("question", "大厂经典源码真题")),
                    "framework": item.get("framework", item.get("answer", "三段式高分答题框架")),
                    "bonus_tip": item.get("bonus_tip", item.get("tip", "主动提及工程量化数字与选型权衡"))
                })
    else:
        norm_q = generate_builtin_stage_mock(3)["sop_3_questions"]

    if not mock_p:
        mock_p = generate_builtin_stage_mock(3)["mock_interviewer_prompt"]

    if not isinstance(rev, list) or not rev:
        rev = generate_builtin_stage_mock(3)["sop_5_reverse"]

    if not isinstance(cheat, dict):
        cheat = {}
    if "key_numbers" not in cheat or not isinstance(cheat["key_numbers"], list):
        cheat["key_numbers"] = [
            {"name": "显存优化 ZeRO-3", "val": "参数、梯度与优化器 3 重切分，显存节省 58%"},
            {"name": "特征对齐投射", "val": "197 个 Patch Token 映射至统一维度 1024"},
            {"name": "收敛速度提升", "val": "FlashAttention-2 融合算子，单步迭代耗时缩短 42%"}
        ]
    if "golden_rules" not in cheat or not isinstance(cheat["golden_rules"], list):
        cheat["golden_rules"] = [
            "回答技术方案，先说【核心架构机理】，再说【工程量化指标】，最后提【方案B权衡对比】。",
            "遇到未涉及的盲区，诚实定性后结合底层原理推导可能的技术路线。"
        ]

    return norm_q, str(mock_p), rev, cheat

def synthesize_rewritten_resume(current_resume: str, sop_0_projects: list) -> str:
    """基于外部 Agent 精修的高分 STAR 子弹点，智能重塑并重写回候选人简历，智能保留候选人真实档案与技能"""
    sections = []
    current_resume = (current_resume or "").strip()
    base_info = ""
    trailing_skills = ""
    
    if current_resume:
        parts = re.split(r'【项目经历|项目经历|项目经验|202[0-9]\.', current_resume, maxsplit=1)
        if len(parts) > 0 and len(parts[0].strip()) > 5:
            base_info = parts[0].strip()
            if not base_info.startswith("【基本信息】"):
                base_info = "【基本信息】\n" + base_info

        skills_match = re.search(r'(【(?:专业技能|技能特长|个人优势|教育背景|自我评价)】[\s\S]*)$', current_resume)
        if skills_match:
            trailing_skills = skills_match.group(1).strip()
            
    if not base_info:
        base_info = "【基本信息】\n张三 (示例候选人) | 某重点大学 计算机科学与技术 (本/硕)\n求职意向：大模型算法工程师 / 系统架构师 | 邮箱: candidate@example.com | 电话: 138-0000-0000"
        
    sections.append(base_info)

    for idx, proj in enumerate(sop_0_projects):
        p_name = proj.get("project_name", f"核心工程项目 {idx+1}")
        bullets = proj.get("refined_bullet_points") or proj.get("optimized_bullets") or []
        if bullets:
            bullet_lines = "\n".join([f"- {b}" for b in bullets])
            sections.append(f"【项目经历 {idx+1}：{p_name}】\n{bullet_lines}")

    if trailing_skills:
        sections.append(trailing_skills)
    else:
        sections.append("【专业技能】\n- 深度掌握 Transformer、多模态视觉大模型架构及分布式训练对齐；\n- 熟练掌握 PyTorch、FSDP、DeepSpeed、LoRA 显存优化与高效量化部署；\n- 熟悉 ReAct / Plan-and-Solve 智能体架构、工具调用与多步推理评估；\n- 具备高并发模型 Serving 框架与低延迟推理工程落地实战经验。")

    return "\n\n".join(sections).strip()

@app.post("/api/agent/import_output")
def import_output_from_agent(req: AgentImportRequest):
    """装载由外部 Agent 生成的最终 SOP 成果 (JSON)，支持无文件时智能自动预装与聚合"""
    data = req.output_data
    is_preloaded = False
    outputs_dir = BASE_DIR / "agent_llm_tasks" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    example_path = outputs_dir / "example_output.json"
    
    if not data:
        # 如果明确请求示范样例
        if req.file_path and "example" in str(req.file_path):
            if example_path.exists():
                target_path = example_path
                is_preloaded = True
            else:
                target_path = outputs_dir / "output.json"
        elif req.file_path:
            target_path = Path(req.file_path)
        else:
            target_path = outputs_dir / "output.json"

        if not target_path.exists():
            # 尝试从 example_output.json 预装并写入
            if example_path.exists():
                try:
                    ex_text = example_path.read_text(encoding="utf-8")
                    target_path.write_text(ex_text, encoding="utf-8")
                    is_preloaded = True
                except Exception:
                    pass
            else:
                # 内置全量数据保底
                fallback_full = {
                    **generate_builtin_stage_mock(1),
                    **generate_builtin_stage_mock(2),
                    **generate_builtin_stage_mock(3)
                }
                target_path.write_text(json.dumps(fallback_full, ensure_ascii=False, indent=2), encoding="utf-8")
                is_preloaded = True
            
        try:
            data = json.loads(target_path.read_text(encoding="utf-8"))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"解析成果 JSON 失败: {str(e)}")

    # 规范化各模块
    if "sop_0_resume_optimizer" in data:
        data["sop_0_resume_optimizer"] = normalize_stage_1({"sop_0_resume_optimizer": data["sop_0_resume_optimizer"]})
    if "sop_1_matching" in data or "sop_2_star" in data:
        m, s = normalize_stage_2(data)
        data["sop_1_matching"] = m
        data["sop_2_star"] = s
    if "sop_3_questions" in data or "mock_interviewer_prompt" in data:
        q, mp, rev, cheat = normalize_stage_3(data)
        data["sop_3_questions"] = q
        data["mock_interviewer_prompt"] = mp
        data["sop_5_reverse"] = rev
        data["sop_6_cheatsheet"] = cheat

    expected_keys = ["sop_0_resume_optimizer", "sop_1_matching", "sop_2_star", "sop_3_questions"]
    found_keys = [k for k in expected_keys if k in data]
    if not found_keys:
        raise HTTPException(status_code=422, detail="导入的 JSON 不包含任何有效的 SOP 数据结构")

    if "input_meta" not in data:
        data["input_meta"] = {
            "company": "同花顺" if is_preloaded else "Agent 成果",
            "job_title": "金融投研智能体/算法专家" if is_preloaded else "已装载成果",
            "repo_paths": []
        }

    msg = "未检测到本地生成的 output.json，已自动为您预装并装载官方标准示范成果！" if is_preloaded else f"成功装载 Agent 成果 (包含 {len(found_keys)} 个核心 SOP 模块)！"
    return {
        "success": True,
        "is_preloaded": is_preloaded,
        "sop": data,
        "message": msg
    }

@app.post("/api/agent/export_task0")
def export_task0_for_agent(req: Task0ExportRequest):
    """专属导出 Task 0 (简历针对性靶向精修) 工单、输入上下文与完整可运行 Agent Prompt"""
    paths = [p.strip() for p in (req.repo_paths or []) if p.strip()]
    repos_info = RepoScanner.scan_multiple(paths) if paths else []
    
    task0_context = {
        "target_company": req.company or "目标企业",
        "target_job_title": req.job_title or "应聘岗位",
        "job_description": req.jd or "",
        "candidate_resume": req.resume or "",
        "scanned_repositories": [
            {
                "root_name": r.get("root_name", "ProjectRepo"),
                "repo_path": r.get("repo_path", ""),
                "model_architecture": r.get("summary", {}).get("model_architecture", {}),
                "code_highlights": r.get("summary", {}).get("code_highlights", []),
                "key_dependencies": r.get("summary", {}).get("dependencies", []),
                "core_scripts": r.get("summary", {}).get("core_scripts", [])
            }
            for r in repos_info
        ]
    }
    
    task0_dir = Path(BASE_DIR) / "agent_llm_tasks" / "task_0_resume_optimizer"
    task0_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. 写入专用输入文件 input_context.json
    input_file = task0_dir / "input_context.json"
    input_file.write_text(json.dumps(task0_context, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # 2. 读取 system_prompt.txt 并组装完整可运行的 Agent Master Prompt
    system_prompt_file = task0_dir / "system_prompt.txt"
    sys_prompt = system_prompt_file.read_text(encoding="utf-8") if system_prompt_file.exists() else ""
    
    full_prompt = (
        f"{sys_prompt}\n\n"
        f"==================================================\n"
        f"【以下是候选人真实输入上下文与代码透视事实 (待处理输入)】\n"
        f"==================================================\n"
        f"{json.dumps(task0_context, ensure_ascii=False, indent=2)}\n\n"
        f"请严格按照 output_schema.json 规定的数据结构输出合法 JSON，只输出 JSON 内容即可。"
    )
    
    prompt_file = task0_dir / "agent_prompt.txt"
    prompt_file.write_text(full_prompt, encoding="utf-8")
    
    return {
        "success": True,
        "prompt": full_prompt,
        "input_path": str(input_file),
        "prompt_path": str(prompt_file),
        "context": task0_context,
        "message": "已成功导出 Task 0 专属靶向精修工单至 agent_prompt.txt！"
    }

@app.post("/api/agent/import_task0")
def import_task0_from_agent(req: Task0ImportRequest):
    """装载外部 Agent 针对 Task 0 产出的成果，并自动生成重新写入简历的高分文本"""
    data = req.output_data
    is_preloaded = False
    task0_dir = Path(BASE_DIR) / "agent_llm_tasks" / "task_0_resume_optimizer"
    task0_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(req.file_path) if req.file_path else task0_dir / "output.json"

    if not data:
        if not target_path.exists():
            # 自动预装示范成果
            example_path = Path(BASE_DIR) / "agent_llm_tasks" / "outputs" / "example_output.json"
            if example_path.exists():
                try:
                    raw_ex = json.loads(example_path.read_text(encoding="utf-8"))
                    data = {"sop_0_resume_optimizer": raw_ex.get("sop_0_resume_optimizer", [])}
                    target_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                    is_preloaded = True
                except Exception:
                    pass
            if not data:
                data = {"sop_0_resume_optimizer": normalize_stage_1(get_or_create_stage_data(1, force_mock=True)[0])}
                target_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                is_preloaded = True
        else:
            try:
                data = json.loads(target_path.read_text(encoding="utf-8"))
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"解析成果 JSON 失败: {str(e)}")

    projs = normalize_stage_1(data)
    if not projs:
        raise HTTPException(status_code=422, detail="未能从成果中解析出任何项目的靶向精修数据")

    rewritten_resume = synthesize_rewritten_resume(req.current_resume or "", projs)
    msg = "未检测到 Task 0 自定义产物，已为您自动预装并装载示范精修成果！" if is_preloaded else f"成功装载外部 Agent 精修成果，已解析 {len(projs)} 个工程项目并重构高分简历！"
    return {
        "success": True,
        "is_preloaded": is_preloaded,
        "sop_0_resume_optimizer": projs,
        "rewritten_resume": rewritten_resume,
        "message": msg
    }

# ==================== 3 大阶段 Agent 协同流水线接口 ====================
@app.post("/api/agent/export_stage")
def export_stage_for_agent(req: ExportStageRequest):
    """为外部 Agent 导出指定阶段（Stage 1/2/3）的输入上下文与 Prompt"""
    stage = req.stage
    if stage not in (1, 2, 3):
        raise HTTPException(status_code=400, detail=f"不支持的阶段编号: {stage}")

    agent_tasks_dir = BASE_DIR / "agent_llm_tasks"
    inputs_dir = agent_tasks_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    # 透视代码仓库真实特征
    valid_paths = [p for p in (req.repo_paths or []) if p and Path(p).exists()]
    repo_facts = RepoScanner.scan_multiple(valid_paths) if valid_paths else []

    stage_context = {
        "stage": stage,
        "company": req.company or "目标公司",
        "job_title": req.job_title or "应聘岗位",
        "jd": req.jd or "",
        "resume": req.resume or "",
        "repo_paths": req.repo_paths or [],
        "scanned_repo_facts": repo_facts,
        "style": req.style or "geek",
        "focus": req.focus or "code"
    }

    input_file = inputs_dir / f"stage_{stage}_input.json"
    input_file.write_text(json.dumps(stage_context, ensure_ascii=False, indent=2), encoding="utf-8")

    if stage == 1:
        stage_title = "阶段一 · 简历靶向精修重构 (Stage 1 Resume Optimizer)"
        instructions = (
            "【任务目标】\n"
            "深度诊断候选人简历中各重点项目的 3 大失分盲区（动词弱、缺少量化、关键算法盲点），\n"
            "并结合上述代码仓库真实事实重构 3~4 条高分 STAR 子弹点。\n\n"
            "【输出规范】\n"
            "输出文件应保存至 agent_llm_tasks/outputs/stage_1_output.json，必须包含顶级键 sop_0_resume_optimizer，格式参照 task_0_resume_optimizer/output_schema.json。"
        )
    elif stage == 2:
        stage_title = "阶段二 · 岗位胜任匹配与 STAR 权衡决策矩阵 (Stage 2 Matching & STAR)"
        instructions = (
            "【任务目标】\n"
            "1. 评估候选人针对目标岗位的 5 维胜任力雷达得分（0-100）、求职核心差异化壁垒（杀手锏）、潜在考查盲区 (Gap) 以及面试前 72 小时 Sprint 冲刺清单。\n"
            "2. 针对核心项目提炼 SITUATION / TASK / ACTION / RESULT 四段式硬核复盘，并构建核心技术决策权衡对比矩阵 (Trade-off Matrix，核心攻坚'为什么不选方案 B')。\n\n"
            "【输出规范】\n"
            "输出文件应保存至 agent_llm_tasks/outputs/stage_2_output.json，必须包含顶级键 sop_1_matching 与 sop_2_star。"
        )
    else:
        stage_title = "阶段三 · 源码真题、模拟对练与临考速记 (Stage 3 Questions & Mock)"
        instructions = (
            "【任务目标】\n"
            "1. 结合代码库深度实现定制 4 道大厂高频面试真题与三层加分锦囊。\n"
            "2. 构建高维定制化面试官 Master Prompt，融合候选人真实背景与深挖逻辑。\n"
            "3. 制定分轮次高阶反向提问清单（技术一面/二面、总监三面、HR终面）。\n"
            "4. 输出 30 分钟临考必背核心数字与极速破局口诀。\n\n"
            "【输出规范】\n"
            "输出文件应保存至 agent_llm_tasks/outputs/stage_3_output.json，包含顶级键 sop_3_questions, mock_interviewer_prompt, sop_5_reverse, sop_6_cheatsheet。"
        )

    full_prompt = (
        f"# {stage_title}\n\n"
        f"{instructions}\n\n"
        f"## 输入全景上下文 (Input Context):\n"
        f"```json\n"
        f"{json.dumps(stage_context, ensure_ascii=False, indent=2)}\n"
        f"```\n\n"
        f"请严格输出合法 JSON，并确保通过 python run_pipeline.py --stage {stage} --validate 校验。"
    )

    prompt_file = inputs_dir / f"stage_{stage}_prompt.txt"
    prompt_file.write_text(full_prompt, encoding="utf-8")

    return {
        "success": True,
        "stage": stage,
        "input_file": str(input_file),
        "prompt_file": str(prompt_file),
        "prompt": full_prompt,
        "context": stage_context,
        "message": f"已成功导出阶段 {stage} 工单至 inputs/stage_{stage}_input.json 与 prompt 文件！"
    }

@app.post("/api/agent/preload_stage")
def preload_stage_for_agent(req: PreloadStageRequest):
    """显式为指定阶段预装官方标准示范成果，并写入磁盘文件与返回就绪数据"""
    stage = req.stage
    if stage not in (1, 2, 3):
        raise HTTPException(status_code=400, detail=f"不支持的阶段编号: {stage}")
        
    raw_data, _ = get_or_create_stage_data(stage, force_mock=True)
    
    if stage == 1:
        projs = normalize_stage_1(raw_data)
        rewritten = synthesize_rewritten_resume(req.current_resume or "", projs)
        return {
            "success": True,
            "stage": 1,
            "is_preloaded": True,
            "sop_0_resume_optimizer": projs,
            "rewritten_resume": rewritten,
            "message": "🎉 成功为阶段一预装官方标准示范成果，已重构高分简历并解锁阶段二！"
        }
    elif stage == 2:
        matching, star = normalize_stage_2(raw_data)
        return {
            "success": True,
            "stage": 2,
            "is_preloaded": True,
            "sop_1_matching": matching,
            "sop_2_star": star,
            "message": "🎉 成功为阶段二预装官方标准示范成果，已激活胜任力雷达与技术权衡决策矩阵！"
        }
    else:
        q, mock_p, rev, cheat = normalize_stage_3(raw_data)
        return {
            "success": True,
            "stage": 3,
            "is_preloaded": True,
            "sop_3_questions": q,
            "mock_interviewer_prompt": mock_p,
            "sop_5_reverse": rev,
            "sop_6_cheatsheet": cheat,
            "message": "🎉 成功为阶段三预装官方标准示范成果，已就绪源码真题、对练 Prompt 与临考速记！"
        }

@app.post("/api/agent/import_stage")
def import_stage_from_agent(req: ImportStageRequest):
    """装载外部 Agent 针对指定阶段（Stage 1/2/3）产出的成果，支持无文件时智能自动预装"""
    stage = req.stage
    if stage not in (1, 2, 3):
        raise HTTPException(status_code=400, detail=f"不支持的阶段编号: {stage}")

    outputs_dir = BASE_DIR / "agent_llm_tasks" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    target_file = outputs_dir / f"stage_{stage}_output.json"

    data = req.output_data
    is_preloaded = False

    if not data:
        if req.force_preload or not target_file.exists():
            # 自动预装示范成果，彻底避免 404 错误
            data, is_preloaded = get_or_create_stage_data(stage, force_mock=req.force_preload or False)
        else:
            try:
                data = json.loads(target_file.read_text(encoding="utf-8"))
            except Exception:
                # 解析异常时兜底预装
                data, is_preloaded = get_or_create_stage_data(stage, force_mock=True)

    if stage == 1:
        projs = normalize_stage_1(data)
        if not projs:
            projs = normalize_stage_1(get_or_create_stage_data(1, force_mock=True)[0])
            is_preloaded = True
        rewritten_resume = synthesize_rewritten_resume(req.current_resume or "", projs)
        msg = "未检测到外部生成的成果文件，已自动为您预装阶段一标准示范成果！" if is_preloaded else f"成功装载阶段 1 外部 Agent 成果，已解析 {len(projs)} 个工程项目并重构高分简历！"
        return {
            "success": True,
            "stage": 1,
            "is_preloaded": is_preloaded,
            "sop_0_resume_optimizer": projs,
            "rewritten_resume": rewritten_resume,
            "message": msg
        }
    elif stage == 2:
        matching, star = normalize_stage_2(data)
        if not matching and not star:
            matching, star = normalize_stage_2(get_or_create_stage_data(2, force_mock=True)[0])
            is_preloaded = True
        msg = "未检测到外部生成的成果文件，已自动为您预装阶段二标准示范成果！" if is_preloaded else "成功装载阶段 2 外部 Agent 成果，已激活 5 维胜任力雷达与核心 STAR 权衡矩阵！"
        return {
            "success": True,
            "stage": 2,
            "is_preloaded": is_preloaded,
            "sop_1_matching": matching,
            "sop_2_star": star,
            "message": msg
        }
    else:
        q, mock_p, rev, cheat = normalize_stage_3(data)
        if not q and not mock_p and not rev and not cheat:
            q, mock_p, rev, cheat = normalize_stage_3(get_or_create_stage_data(3, force_mock=True)[0])
            is_preloaded = True
        msg = "未检测到外部生成的成果文件，已自动为您预装阶段三标准示范成果！" if is_preloaded else "成功装载阶段 3 外部 Agent 成果，已就绪源码真题库、模拟对练 Prompt 与临考速记！"
        return {
            "success": True,
            "stage": 3,
            "is_preloaded": is_preloaded,
            "sop_3_questions": q,
            "mock_interviewer_prompt": mock_p,
            "sop_5_reverse": rev,
            "sop_6_cheatsheet": cheat,
            "message": msg
        }

@app.get("/api/agent/stage_status")
def get_stage_status():
    """查询各阶段工单输入与成果输出文件的就绪状态与时间戳"""
    agent_tasks_dir = BASE_DIR / "agent_llm_tasks"
    inputs_dir = agent_tasks_dir / "inputs"
    outputs_dir = agent_tasks_dir / "outputs"

    stages_info = {}
    for s in [1, 2, 3]:
        in_file = inputs_dir / f"stage_{s}_input.json"
        out_file = outputs_dir / f"stage_{s}_output.json"
        
        in_mtime = time.strftime("%m-%d %H:%M", time.localtime(in_file.stat().st_mtime)) if in_file.exists() else None
        out_mtime = time.strftime("%m-%d %H:%M", time.localtime(out_file.stat().st_mtime)) if out_file.exists() else None
        
        stages_info[str(s)] = {
            "input_exists": in_file.exists(),
            "input_time": in_mtime,
            "output_exists": out_file.exists(),
            "output_time": out_mtime
        }

    global_out = outputs_dir / "output.json"
    return {
        "success": True,
        "stages": stages_info,
        "global_output_exists": global_out.exists()
    }

# 静态首页托管
@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "InterviewSOP Master API Running. Static files not yet generated."}

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if __name__ == "__main__":
    import uvicorn
    print(f"启动 InterviewSOP Master 服务...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
