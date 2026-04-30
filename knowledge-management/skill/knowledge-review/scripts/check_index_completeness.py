#!/usr/bin/env python3
"""
check_index_completeness.py — 检查知识文档索引完整性

用法:
    python3 check_index_completeness.py /path/to/knowledge
    
输出:
    JSON 格式的检查结果（orphan 文档列表）
"""
import os
import sys
import re
import json
from pathlib import Path


def extract_links_from_md(content: str) -> set:
    """从 Markdown 内容中提取链接"""
    links = set()
    # [text](link) 格式
    md_links = re.findall(r'\[.*?\]\(([^)]+)\)', content)
    for link in md_links:
        # 只保留本地文件链接
        if not link.startswith('http') and not link.startswith('#'):
            links.add(link.lstrip('./'))
    return links


def check_index_completeness(kb_path: str) -> dict:
    """检查知识文档是否被索引"""
    kb = Path(kb_path)
    if not kb.exists():
        return {"error": f"知识库路径不存在: {kb_path}"}
    
    # 1. 收集所有知识文档
    all_docs = set()
    for ext in ['*.md', '*.html']:
        for f in kb.rglob(ext):
            if not f.name.startswith('.'):
                rel_path = str(f.relative_to(kb))
                all_docs.add(rel_path)
    
    # 2. 收集所有索引文件中的引用
    indexed_docs = set()
    index_files = ['README.md', 'index.md', 'index.html']
    
    for index_name in index_files:
        index_file = kb / index_name
        if index_file.exists():
            content = index_file.read_text(encoding='utf-8', errors='ignore')
            links = extract_links_from_md(content)
            indexed_docs.update(links)
    
    # 同时检查各子目录的索引
    for subdir in kb.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            for index_name in index_files:
                index_file = subdir / index_name
                if index_file.exists():
                    content = index_file.read_text(encoding='utf-8', errors='ignore')
                    links = extract_links_from_md(content)
                    # 转换为相对于 kb 的路径
                    for link in links:
                        full_link = f"{subdir.name}/{link}"
                        indexed_docs.add(full_link)
    
    # 3. 找出未被索引的文档（排除索引文件本身）
    orphans = []
    for doc in all_docs:
        doc_name = Path(doc).name
        if doc_name in index_files:
            continue
        if doc not in indexed_docs and doc_name not in indexed_docs:
            orphans.append(doc)
    
    return {
        "total_docs": len(all_docs),
        "indexed_docs": len(indexed_docs),
        "orphan_count": len(orphans),
        "orphans": sorted(orphans),
        "status": "P0" if orphans else "OK"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 check_index_completeness.py /path/to/knowledge", file=sys.stderr)
        sys.exit(1)
    
    kb_path = sys.argv[1]
    result = check_index_completeness(kb_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
