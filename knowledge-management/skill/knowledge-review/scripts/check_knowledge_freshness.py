#!/usr/bin/env python3
"""
check_knowledge_freshness.py — 检查知识文档新鲜度

用法:
    python3 check_knowledge_freshness.py /path/to/knowledge [--stale-days 180] [--warn-days 90]
    
输出:
    JSON 格式的新鲜度检查结果
"""
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


# 默认阈值
DEFAULT_STALE_DAYS = 180  # 超过此天数视为过时
DEFAULT_WARN_DAYS = 90    # 超过此天数发出警告


def check_knowledge_freshness(kb_path: str, stale_days: int = None, warn_days: int = None) -> dict:
    """检查知识库各目录的更新时间"""
    kb = Path(kb_path)
    stale_threshold = stale_days or DEFAULT_STALE_DAYS
    warn_threshold = warn_days or DEFAULT_WARN_DAYS
    
    if not kb.exists():
        return {"error": f"知识库路径不存在: {kb_path}"}
    
    now = datetime.now()
    results = {
        "checked_at": now.isoformat(),
        "thresholds": {
            "stale_days": stale_threshold,
            "warn_days": warn_threshold,
        },
        "categories": [],
        "stale_count": 0,
        "warning_count": 0,
        "fresh_count": 0,
    }
    
    for domain_dir in sorted(kb.iterdir()):
        if not domain_dir.is_dir():
            continue
        if domain_dir.name.startswith(".") or domain_dir.name == "__pycache__":
            continue
        
        # 找到该目录最新的文件修改时间
        latest_mtime = None
        file_count = 0
        
        for f in domain_dir.rglob("*"):
            if f.is_file() and not f.name.startswith("."):
                if f.suffix in ['.md', '.html']:
                    file_count += 1
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if latest_mtime is None or mtime > latest_mtime:
                            latest_mtime = mtime
                    except OSError:
                        pass
        
        if latest_mtime is None:
            continue
        
        days_old = (now - latest_mtime).days
        
        # 确定状态
        if days_old >= stale_threshold:
            status = "stale"
            status_label = "🔴 过时"
            results["stale_count"] += 1
        elif days_old >= warn_threshold:
            status = "warning"
            status_label = "🟡 需关注"
            results["warning_count"] += 1
        else:
            status = "fresh"
            status_label = "🟢 新鲜"
            results["fresh_count"] += 1
        
        results["categories"].append({
            "name": domain_dir.name,
            "file_count": file_count,
            "latest_update": latest_mtime.isoformat(),
            "days_old": days_old,
            "status": status,
            "status_label": status_label,
        })
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查知识库新鲜度")
    parser.add_argument("kb_path", help="知识库路径")
    parser.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS, help=f"过时天数阈值（默认{DEFAULT_STALE_DAYS}）")
    parser.add_argument("--warn-days", type=int, default=DEFAULT_WARN_DAYS, help=f"警告天数阈值（默认{DEFAULT_WARN_DAYS}）")
    
    args = parser.parse_args()
    result = check_knowledge_freshness(args.kb_path, args.stale_days, args.warn_days)
    print(json.dumps(result, ensure_ascii=False, indent=2))
