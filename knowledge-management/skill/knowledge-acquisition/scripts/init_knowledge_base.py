#!/usr/bin/env python3
"""
init_knowledge_base.py — 初始化知识库目录结构

用法:
    python3 init_knowledge_base.py /path/to/knowledge [--categories cat1,cat2,cat3]
    
输出:
    JSON 格式的初始化结果
"""
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


# 默认推荐分类
DEFAULT_CATEGORIES = [
    "research",      # 调研报告
    "guides",        # 使用指南  
    "notes",         # 笔记记录
    "deep-research", # 深度调研
    "archives",      # 归档内容
]


def init_knowledge_base(kb_path: str, categories: list = None) -> dict:
    """初始化知识库目录结构"""
    kb = Path(kb_path)
    cats = categories or DEFAULT_CATEGORIES
    
    created = []
    
    # 创建知识库根目录
    if not kb.exists():
        kb.mkdir(parents=True, exist_ok=True)
        created.append(str(kb))
    
    # 创建分类目录
    for cat in cats:
        cat_path = kb / cat
        if not cat_path.exists():
            cat_path.mkdir(parents=True, exist_ok=True)
            created.append(cat)
    
    # 创建 README.md 索引文件
    readme = kb / "README.md"
    if not readme.exists():
        today = datetime.now().strftime('%Y-%m-%d')
        content = f"""# 知识库索引

> 创建时间: {today}

## 目录结构

"""
        for cat in cats:
            content += f"- `{cat}/` — 待填充\n"
        
        content += """
## 使用说明

- 使用 `evo-knowledge-base` 技能检索内容
- 使用 `evo-knowledge-curator` 技能维护健康度
- 使用 `evo-knowledge-acquisition` 技能学习新领域
"""
        readme.write_text(content, encoding='utf-8')
        created.append("README.md")
    
    return {
        "kb_path": str(kb),
        "created": created,
        "categories": cats,
        "message": f"初始化完成，创建了 {len(created)} 个目录/文件" if created else "知识库已存在，无需初始化"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化知识库目录结构")
    parser.add_argument("kb_path", help="知识库路径")
    parser.add_argument("--categories", "-c", help="自定义分类，逗号分隔", default=None)
    
    args = parser.parse_args()
    
    categories = args.categories.split(",") if args.categories else None
    result = init_knowledge_base(args.kb_path, categories)
    print(json.dumps(result, ensure_ascii=False, indent=2))
