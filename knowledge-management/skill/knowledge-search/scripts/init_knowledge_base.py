#!/usr/bin/env python3
"""
init_knowledge_base.py — 初始化知识库目录结构

用法:
    python3 init_knowledge_base.py /path/to/knowledge [--categories cat1,cat2,cat3]
    
输出:
    JSON 格式的初始化结果

初始化完成后，会在本脚本所在的 skill 目录下写入位置标记文件：
- .knowledge-base-in-project  → 知识库在项目目录下（非 ~/.knowledge）
- .knowledge-base-in-personal → 知识库在个人主目录（~/.knowledge）下
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


def write_location_marker(kb_path: str):
    """在 skill 目录下写入位置标记文件，文件名体现知识库类型：
    - .knowledge-base-in-project  → 知识库在项目目录下（非 ~/.knowledge）
    - .knowledge-base-in-personal → 知识库在个人主目录（~/.knowledge）下
    """
    skill_dir = Path(__file__).resolve().parent.parent
    kb_resolved = Path(kb_path).resolve()
    personal_kb = Path.home().resolve() / ".knowledge"

    if kb_resolved == personal_kb or str(kb_resolved).startswith(str(personal_kb) + "/"):
        location_type = "personal"
    else:
        location_type = "project"

    marker_name = f".knowledge-base-in-{location_type}"
    marker_file = skill_dir / marker_name
    marker_file.write_text(str(kb_resolved), encoding="utf-8")
    return str(marker_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="初始化知识库目录结构")
    parser.add_argument("kb_path", help="知识库路径")
    parser.add_argument("--categories", "-c", help="自定义分类，逗号分隔", default=None)
    
    args = parser.parse_args()
    
    categories = args.categories.split(",") if args.categories else None
    result = init_knowledge_base(args.kb_path, categories)
    
    # 写入位置标记文件
    marker_path = write_location_marker(args.kb_path)
    result["location_marker"] = marker_path
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
