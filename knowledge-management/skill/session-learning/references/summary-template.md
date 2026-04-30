# Session 存档模板

> 文件路径：`knowledge/sessions/YYYY-MM-DD_HH-MM_<slug>.md`

---

# [YYYY-MM-DD] <对话主题>

**时间**：YYYY-MM-DD HH:MM  
**工作目录**：<cwd 路径>  
**对话轮次**：约 N 轮

---

## 🎯 对话目标

> 用 2-3 句话概括本次对话的核心任务和期望结果。

- 主要目标：
- 衍生目标（如有）：
- 最终确认状态：✅ 完成 / ⚠️ 部分完成 / ❌ 未完成

---

## 📋 任务拆解

| # | 子任务 | 状态 | 备注 |
|---|--------|------|------|
| 1 | xxx | ✅ | |
| 2 | xxx | ✅ | |
| 3 | xxx | ⚠️ | 原因：xxx |

---

## 🔧 执行过程

> 按子任务逐步复现，包含失败路径，不省略。

### 子任务 1：<名称>

**目标**：

**执行步骤**：

1. ...
2. ...

**遇到的问题**：
- 问题：...
- 原因：...
- 修复：...

**结果**：

---

### 子任务 2：<名称>

（同上结构）

---

## 🛠️ 工具使用清单

| 工具 | 调用次数 | 主要用途 |
|------|---------|---------|
| read_file | N | 读取 xxx 文件 |
| execute_command | N | 执行 xxx 命令 |
| write_to_file | N | 写入 xxx 文件 |
| replace_in_file | N | 修改 xxx |
| grep_search | N | 搜索 xxx |
| browser_agent | N | 操作 xxx 页面 |

---

## ✅ 最终结果

> 列出所有已交付的输出。

- **文件**：`path/to/file.md` — 描述
- **部署**：URL — 描述
- **命令**：`xxx` — 描述

---

## 💡 洞察与经验沉淀

> 本次对话产生的可复用经验和认知。每条注明分类，便于后续提炼到 knowledge/ 目录。

- **[tools]** `frontend-cloud-cli` 的正确参数是 `--project-id`，不是 `--project`。
- **[patterns]** 定位文件先用 `search_file("**/target.html")` 再用 `read_file`，避免路径猜错。
- **[insights]** <深度认知发现>
- **[rules]** <操作约束或规范>
- **[memories]** <值得写入 Agent Memory 的内容（用户决定是否执行）>
- **[skills]** <值得封装为 skill 的流程>

---

## 🌟 海星模型复盘

> 以行动策略为维度复盘，服务于"下次更高效"。

### ✋ 保持（Keep）
> 继续做、效果好的做法

- 

### 🚀 开始（Start）
> 下次应该做但这次没做的

- 

### 🛑 停止（Stop）
> 浪费时间或产生负面效果的行为

- 

### ⬆️ 更多（More）
> 有效但可以加强的行为

- 

### ⬇️ 更少（Less）
> 有价值但占用资源过多的行为

- 

---

## 📌 知识提炼清单

> 本次归档同步提炼到以下知识库文件（供核查）：

- [ ] `solutions/xxx.md` — 新建 / 追加
- [ ] `tools/xxx.md` — 新建 / 追加
- [ ] `patterns/xxx.md` — 新建 / 追加
- [ ] `insights/xxx.md` — 新建 / 追加
- [ ] `memories/YYYY-MM-DD_memories.md` — 包含 N 条候选
- [ ] `rules/xxx.md` — 新建 / 追加
- [ ] `skills/xxx.md` — 新建 / 追加
