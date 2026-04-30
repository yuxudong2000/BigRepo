# knowledge-curator - 详细内容

> 本文件包含从SKILL.md移出的详细内容

## 分类修正详细规则

| 原位置   | 内容特征               | 建议位置       |
| :------- | :--------------------- | :------------- |
| 根目录   | 含"调研"/"分析"        | `research/`    |
| 根目录   | 含"思想"/"体系"        | `methodology/` |
| 根目录   | 含"指南"/"实践"/"使用" | `guides/`      |
| 错误分类 | 技术调研内容           | `research/`    |
| 错误分类 | 方法论总结             | `methodology/` |

## 过时标记模板

在文档顶部添加过时警告：

```markdown
> ⚠️ **本文档已过时** — 最后更新于 {DATE}，内容可能已失效。
> 如需引用，请先核实信息准确性。
```

## 完整报告格式

```markdown
## 知识优化报告

**日期**: {TODAY}
**执行者**: evo-knowledge-curator skill

### 扫描概况

| 指标         | 数值    |
| ------------ | ------- |
| 知识文件总数 | {N} 个  |
| 分类目录数   | {M} 个  |
| 索引完整性   | {✅/❌} |

### 健康度诊断

| 级别 | 数量 | 详情   |
| ---- | ---- | ------ |
| P0   | {N}  | {列表} |
| P1   | {N}  | {列表} |
| P2   | {N}  | {列表} |

### 操作记录

| 序号 | 操作类型   | 目标   | 结果 |
| ---- | ---------- | ------ | ---- |
| 1    | reindex    | {path} | ✅   |
| 2    | reclassify | {file} | ✅   |
| ...  | ...        | ...    | ...  |

### 健康度变化

- **优化前**: {X}% ({评级})
- **优化后**: {Y}% ({评级})
- **提升**: +{Y-X}%

### 下次建议

- 建议 {N} 天后执行下次检查
- 重点关注: {重点分类}
```

## 节点深度审计详解

### K1 信息时效性检查

检查文档中的数据是否过时：

```python
def check_info_freshness(doc):
    """
    检查知识文档中的数据是否过时
    """
    # 1. 提取时间性表述
    temporal_phrases = extract_patterns(doc, [
        r"截至.*\d{4}",       # "截至2025年"
        r"目前",               # "目前GPT-4是最强的"
        r"最新",               # "最新版本"
        r"\d{4}年.*数据",      # "2025年数据"
        r"Top\s*\d+",          # "排名Top 10"
    ])

    for phrase in temporal_phrases:
        age_days = calc_age(phrase, doc.mtime)
        if age_days > 180:
            report("info_outdated", phrase, age_days)

    # 2. 检查具体数值是否可能已变
    numbers = extract_stats(doc)  # 如 "参数量1750亿"
    if numbers and doc.age > 90:
        report("info_outdated", "含具体数值且文档超过90天，建议核实")
```

### K3 结构完整性检查

```python
def check_structure_completeness(doc):
    """
    检查文档结构是否完整
    """
    headings = extract_headings(doc)

    # 1. 检查空章节（heading后无实质内容）
    for h in headings:
        content = get_section_content(doc, h)
        if len(content.strip()) < 20:
            report("incomplete_structure",
                   f"章节 '{h.text}' 无实质内容（仅{len(content)}字符）")

    # 2. 检查目录引用（如果有目录）
    toc_items = extract_toc(doc)
    for item in toc_items:
        if not section_exists(doc, item):
            report("incomplete_structure",
                   f"目录引用了 '{item}' 但此章节不存在")

    # 3. 检查占位符
    placeholders = find_patterns(doc, ["TODO", "TBD", "待补充", "待完善"])
    for p in placeholders:
        report("incomplete_structure", f"占位符: {p}")
```

### K4 链接有效性检查

```python
def check_links(doc):
    """
    检查文档中的链接是否有效
    """
    # 1. 内部链接（文件引用）
    internal_links = extract_internal_links(doc)
    for link in internal_links:
        resolved = resolve_path(doc.path, link)
        if not file_exists(resolved):
            report("broken_link", f"内部链接无效: {link}")

    # 2. 外部链接（可选，仅检查格式是否合法）
    external_links = extract_external_links(doc)
    for link in external_links:
        if not is_valid_url(link):
            report("broken_link", f"URL格式无效: {link}")
        # 注意：不主动访问外部URL（避免网络请求），
        # 仅标记超过90天的链接为"建议核实"
```

## 与记忆/技能的转化关系

### 知识→记忆

当知识核心结论需要快速检索时：

```python
# 提取知识核心结论
conclusion = extract_conclusion(knowledge_doc)

# 转化为记忆
update_memory({
    "category": "domain_knowledge",
    "content": conclusion,
    "source": f"knowledge:{knowledge_doc.path}",
})
```

### 知识→技能

当知识包含可复用流程/规范时：

```markdown
# 从知识中提取可复用方法论

# 创建新技能或更新现有技能的 references
```

## 元认知反问（标记完成前必须自问）

1. 是否有遗漏的问题未处理？
2. 优化操作是否都有记录？
3. 健康度是否有实质提升？
4. 下次检查时间是否已设定？

---

## 版本历史

| 版本   | 日期       | 变更                               |
| ------ | ---------- | ---------------------------------- |
| v1.0.0 | 2026-03-30 | 独立化版本：简化内容，移除私有记录 |
