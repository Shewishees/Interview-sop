"""
PDF 解析接口自动化验证脚本
"""
import sys
from io import BytesIO
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent))

from pypdf import PdfWriter, PdfReader
from pypdf.generic import NameObject, DictionaryObject, ArrayObject, FloatObject, NumberObject

# 创建一个非常简单的测试 PDF 文件（包含文本流）
def create_test_pdf_bytes(text: str) -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    # 我们直接使用已有的真实 PDF 测试，或者测试接口接收
    buf = BytesIO()
    writer.write(buf)
    return buf.getvalue()

def test_pdf_reader():
    print(">>> 1. 测试 pypdf 模块导入与运行...")
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    buf = BytesIO()
    writer.write(buf)
    
    reader = PdfReader(BytesIO(buf.getvalue()))
    assert len(reader.pages) == 1
    print("   [OK] pypdf 运转正常，页数:", len(reader.pages))

if __name__ == "__main__":
    test_pdf_reader()
