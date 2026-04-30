#!/usr/bin/env python3
"""
scan_knowledge_base.py — 扫描知识库结构

用法:
    python3 scan_knowledge_base.py /path/to/knowledge
    
输出:
    JSON 格式的知识库结构信息
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def scan_knowledge_base(kb_path: str) -> dict:
    """扫描知识库结构，返回动态结构信息"""
    kb = Path(kb_path)
    if not kb.exists():
        return {"error": f"知识库路径不存在: {kb_path}", "categories": []}
    
    result = {
        "scanned_at": datetime.now().isoformat(),
        "root": str(kb),
        "categories": [],
        "total_files": 0,
    }
    
    for item in sorted(kb.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            file_count = 0
            latest_mtime = None
            
            # 使用 os.walk 支持软链接跟踪
            for root, dirs, filenames in os.walk(str(item), followlinks=True):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for fn in filenames:
                    if fn.endswith('.md') or fn.endswith('.html'):
                        file_count += 1
                        f_path = Path(root) / fn
                        try:
                            mtime = datetime.fromtimestamp(f_path.stat().st_mtime)
                            if latest_mtime is None or mtime > latest_mtime:
                                latest_mtime = mtime
                        except OSError:
                            pass
            
            result["categories"].append({
                "name": item.name,
                "path": str(item),
                "file_count": file_count,
                "latest_update": latest_mtime.isoformat() if latest_mtime else None,
            })
            result["total_files"] += file_count
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 scan_knowledge_base.py /path/to/knowledge", file=sys.stderr)
        sys.exit(1)
    
    kb_path = sys.argv[1]
    result = scan_knowledge_base(kb_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
