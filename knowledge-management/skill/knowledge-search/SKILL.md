---
name: evo-knowledge-base
vibe: "扫描 → 检索 → 返回"
description: "知识库检索技能 — 快速找到沉淀的知识。【依赖：必须先加载 evo-meta-execution】当用户说'查文档'、'找调研'、'知识库里有什么'、'帮我找一下之前的文档'时自动激活。提供「扫描结构 → 分类检索 → 关键词搜索 → 返回内容」的检索能力。触发词：查知识库、找文档、知识库里有什么、回顾报告。注意：知识库健康管理请使用 knowledge-curator 技能。"
requires:
  - evo-meta-execution
version: 2.0.0
---

> **🚨 STOP - 必须先加载 `evo-meta-execution`**
>
> 本技能依赖 `evo-meta-execution` 进行质量保障。
> **在执行任何操作前，必须先加载 `evo-meta-execution` 技能。**
> 跳过此步骤将导致质量风险和交付问题。

# 个人知识库检索

## 概述

这是一个通用的知识库检索技能，用于快速查找和引用之前沉淀的调研报告、产品方案、投资笔记等知识资产。

## 与 evo-knowledge-curator 的关系

```
evo-knowledge-base（本技能）→ 检索与查询（只读）：帮用户找到内容
evo-knowledge-curator       → 健康管理（读写）：诊断、整理、优化知识库结构
```

## 知识库位置

知识库位置按以下优先级自动检测：

| 优先级 | 路径 | 说明 |
|--------|------|------|
| 1 | `{project}/.knowledge/` | 当前项目的知识库 |
| 2 | `~/.knowledge/` | 用户级知识库 |

**检测逻辑：**
```
IF {project}/.knowledge/ 存在 → 使用项目知识库
ELSE IF ~/.knowledge/ 存在 → 使用用户知识库
ELSE → 提示用户先初始化（使用 evo-knowledge-curator 或 evo-knowledge-acquisition）
```

> 🚨 **强制执行规则：检测必须通过 `list_files` 工具实际执行，禁止假设或推断。**
> 必须先 `list_files("{project}")` 确认 `.knowledge/` 目录是否存在，
> 再 `list_files("~")` 确认 `~/.knowledge/` 是否存在，
> 然后才能决定使用哪个路径。**跳过检测直接使用 = 严重错误。**

### 位置标记文件（快速判断）

知识库初始化后，`init_knowledge_base.py` 会在本技能目录写入一个标记文件：

| 文件名 | 含义 |
|--------|------|
| `.knowledge-base-in-project` | 知识库位于当前项目目录下（如 `{project}/.knowledge/`） |
| `.knowledge-base-in-personal` | 知识库位于个人主目录下（`~/.knowledge/`） |

文件内容是知识库的绝对路径。如果该标记文件存在，可直接读取以跳过 `list_files` 检测步骤；若不存在，则必须执行 `list_files` 检测。

## 知识库结构（动态获取）

> ⚠️ 知识库结构是动态的，**禁止硬编码**。每次使用前需要扫描获取当前结构。

### 首次使用：初始化知识库

如果知识库不存在，提示用户使用 `evo-knowledge-curator` 技能进行初始化，或执行：

```bash
# KB_PATH 由检测逻辑决定
python3 scripts/init_knowledge_base.py "${KB_PATH}"
```

**输出示例**：

```json
{
  "kb_path": "/Users/yourname/clawd/knowledge",
  "created": ["research", "guides", "notes", "deep-research", "archives", "README.md"],
  "categories": ["research", "guides", "notes", "deep-research", "archives"],
  "message": "初始化完成，创建了 6 个目录/文件"
}
```

### 获取当前结构

每次需要了解知识库结构时，执行扫描脚本：

```bash
# 执行技能自带的扫描脚本（如果处于技能根目录下）
python3 scripts/scan_knowledge_base.py "${KB_PATH}"
```

**输出示例**：

```json
{
  "scanned_at": "2026-03-30T01:50:00",
  "root": "/Users/yourname/clawd/knowledge",
  "categories": [
    {
      "name": "research",
      "path": "/Users/yourname/clawd/knowledge/research",
      "file_count": 15,
      "latest_update": "2026-03-28T14:30:00"
    },
    {
      "name": "guides",
      "path": "/Users/yourname/clawd/knowledge/guides",
      "file_count": 8,
      "latest_update": "2026-03-25T10:00:00"
    }
  ],
  "total_files": 23
}
```

## 触发场景

当用户说以下内容时，使用此技能：

- "查知识库"
- "我之前做过什么调研"
- "帮我找一下之前的文档"
- "知识库里有什么"
- "回顾一下我的XXX报告"
- "我之前写过XXX吗"
- "把我的XXX调研找出来"

## 使用流程

### 步骤 1：获取知识库结构

首先执行扫描脚本获取当前知识库状态：

```bash
# 执行扫描脚本（如果处于技能根目录下）
python3 scripts/scan_knowledge_base.py "${KB_PATH}"
```

如果返回 `error` 字段，说明知识库不存在或路径不对。先确认使用的是工作空间路径（如 `$HOME/clawd/knowledge`），并执行初始化：

```bash
python3 scripts/init_knowledge_base.py "${KB_PATH}"
```

### 步骤 2：确定用户需求类型

| 需求类型         | 示例               | 处理方式                  |
| ---------------- | ------------------ | ------------------------- |
| **列出所有内容** | "知识库里有什么"   | 读取 `README.md` 返回索引 |
| **按分类查找**   | "我有哪些产品方案" | 列出对应分类目录内容      |
| **按关键词搜索** | "关于AI的内容"     | 搜索匹配的文件并读取      |
| **读取特定文档** | "帮我回顾XXX报告"  | 直接读取对应文件          |

### 步骤 3：执行检索

#### 列出所有内容

```bash
# 读取知识库索引（默认位于工作区根目录的 knowledge/ 下）
read_file("${KB_PATH}/README.md")
```

#### 按分类查找

```bash
# 先通过扫描脚本获取分类列表，然后列出指定分类下的文件
list_files("${KB_PATH}/${CATEGORY_NAME}/")
```

#### 按关键词搜索

```bash
# 在知识库中搜索关键词
grep_search(path="${KB_PATH}", regex="关键词")
```

#### 读取特定文档

```bash
# 读取具体文档内容
read_file("${KB_PATH}/${CATEGORY}/${FILENAME}.md")
```

### 步骤 4：返回结果

根据用户需求，返回：

- 文档列表（带简要描述）
- 文档内容摘要
- 核心洞察提取
- 完整文档内容

## 新增知识

当用户产出新的调研报告或文档，且希望沉淀到知识库时：

### 步骤 1：确定分类

先扫描当前知识库结构，了解已有分类：

```bash
python3 scripts/scan_knowledge_base.py "${KB_PATH}"
```

根据内容特征选择合适的分类目录，或创建新分类。

### 步骤 2：创建或链接文件

```bash
# 方式一：创建符号链接（推荐，不重复存储）
ln -s /原始文件路径 ${KB_PATH}/分类/文件名.md

# 方式二：直接创建新文件
write_to_file("${KB_PATH}/分类/文件名.md", 内容)
```

### 步骤 3：更新 README.md 索引

在 `${KB_PATH}/README.md` 的对应分类表格中添加新条目。

## 常见查询示例

| 用户说                     | 执行动作                                           |
| -------------------------- | -------------------------------------------------- |
| "知识库里有什么"           | 先扫描结构，然后读取 README.md，列出所有分类和文档 |
| "我之前做过AI方面的调研吗" | 搜索关键词 "AI"，返回匹配的文档列表                |
| "帮我找一下产品方案"       | 列出 `product/` 或相关分类目录并介绍每个文档       |
| "把我的XXX指南找出来"      | 搜索文件名或内容，定位并读取文档                   |

## 内嵌脚本

本技能依赖以下脚本（位于 `scripts/` 子目录）：

| 脚本                     | 功能                                         |
| ------------------------ | -------------------------------------------- |
| `scan_knowledge_base.py` | 扫描知识库目录结构，返回分类/文件数/更新时间 |
| `init_knowledge_base.py` | 首次使用时初始化推荐目录结构                 |

---

## 版本历史

| 版本   | 日期       | 变更                                         |
| ------ | ---------- | -------------------------------------------- |
| v1.0.0 | 2026-03-30 | 独立化版本：去除个人化内容，改为动态结构获取 |
| v2.0.0 | 2026-04-12 | 通用化版本：去除 link 前缀，初始化逻辑优化 |

_知识是最好的复利资产，持续沉淀，越用越值钱。_
