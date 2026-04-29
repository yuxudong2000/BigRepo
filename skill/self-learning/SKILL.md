---
name: self-learning
description: 对话知识沉淀技能。当用户说「总结一下」「写个总结」「生成对话总结」「存档本次对话」「session summary」「把这次对话总结写下来」「归档」时触发。分析当前对话的目标、任务拆解、执行过程（含工具使用）、最终结果、洞察与经验，并使用海星模型（保持/开始/停止/更多/更少）进行复盘，直接写入本地 sessions/ 存档，同时自动提炼可复用知识写入 knowledge/ 对应分类，更新 index.md 和 log.md。
version: 1.0.0
---

# Self-Learning — 对话知识沉淀

## 功能定位

将对话完整归档为 session 存档，同时自动提炼可复用知识（解法/工具/模式/洞察/记忆/规则/skill创意）写入个人知识库，形成持久化、可复利的个人知识资产。

## 触发词

「总结一下」「写个总结」「生成对话总结」「存档本次对话」「session summary」「把这次对话总结写下来」「归档」

---

## 知识库路径

```
/Users/yuxudong/Documents/BigRepo/knowledge/
├── index.md          ← 全库目录索引（每次归档更新）
├── log.md            ← 时间线日志（append-only）
├── sessions/         ← 原始对话完整存档
├── solutions/        ← 问题解法库
├── tools/            ← 工具使用经验
├── patterns/         ← 可复用执行模式
├── insights/         ← 深度洞察与新知识
├── memories/         ← 记忆候选项（用户决定是否执行 update_memory）
├── rules/            ← 操作规则与约束
└── skills/           ← 可 skill 化的流程发现
```

---

## 执行流程

### Step 1：分析对话上下文

从以下来源提取信息：
1. **用户消息序列**：识别对话目标、中途需求变化、最终确认的结果
2. **工具调用历史**：统计使用的工具、调用次数、执行的命令和操作
3. **thread 上下文摘要**（如有）：补充跨轮次的历史背景
4. **错误与修正记录**：识别失败操作、走错路径、最终修复方案

---

### Step 2：生成 Session 存档

**输出路径**：`knowledge/sessions/YYYY-MM-DD_HH-MM_<slug>.md`

Slug 规则：从对话目标提取 2-4 个关键词，用连字符连接，全小写 ASCII。

格式参考 `references/summary-template.md`，包含：
- 🎯 对话目标
- 📋 任务拆解（完成状态表格）
- 🔧 执行过程（每个子任务完整复现，包含失败路径）
- 🛠️ 工具使用清单（表格）
- ✅ 最终结果
- 💡 洞察与经验沉淀
- 🌟 海星模型复盘（保持/开始/停止/更多/更少）

---

### Step 3：自动知识提炼

从 session 内容中提炼**可复用、对后续有帮助**的内容，写入对应分类：

| 分类 | 写入条件 | 详细规则见 |
|------|---------|-----------|
| `solutions/` | 有可复用解法（可复用性 ≥ 中） | knowledge-rules.md § solutions |
| `tools/` | 有工具踩坑或最佳实践（有泛化价值） | knowledge-rules.md § tools |
| `patterns/` | 有可泛化的执行流程（跨对话适用） | knowledge-rules.md § patterns |
| `insights/` | 有超出单次对话的认知发现 | knowledge-rules.md § insights |
| `memories/` | 有记忆候选项 | knowledge-rules.md § memories |
| `rules/` | 有操作约束/规范/禁止项 | knowledge-rules.md § rules |
| `skills/` | 检测到值得封装为 skill 的流程 | knowledge-rules.md § skills |

**提炼原则**：
- 只写"可复用"内容，纯过程记录留在 sessions/
- 每个提炼条目写入独立文件（除 memories/ 按日期聚合）
- 如该主题已有文件，**追加更新**，不重新创建

---

### Step 4：更新 index.md 和 log.md

**index.md** — 追加新文件到对应分类条目：
```markdown
## solutions/
- [文件名](solutions/xxx.md) — 一行描述 · YYYY-MM-DD
```

**log.md** — append-only，追加一条记录：
```markdown
## [YYYY-MM-DD] archive | <session 主题>
新增/更新：solutions/xxx · tools/xxx · sessions/xxx
```

---

### Step 5：输出归档摘要

写入完成后，在对话中输出：

```
✅ Session 已存档：knowledge/sessions/YYYY-MM-DD_HH-MM_topic.md

📚 知识库更新：
  - solutions/xxx.md（新建）— <一行描述>
  - tools/xxx.md（新建）— <一行描述>
  - memories/YYYY-MM-DD_memories.md（新建）— 含 N 条记忆候选，待你决定是否执行 update_memory

💡 记忆候选项（需要你决定）：
  - [ ] [<类别>] <记忆内容>
  - [ ] [<类别>] <记忆内容>
```

---

## 注意事项

1. **Step 2 和 Step 3 都要做**，不能只做其一
2. **完整复现每一步**，包括失败的尝试和回退，不省略
3. **记忆候选只列出，不自动执行**，由用户决定
4. **确保目录存在再写入**：`mkdir -p <path>` 再 write_to_file
5. **追加优先于新建**：同主题文件已存在时追加，不覆盖
6. **index.md 和 log.md 必须更新**，这是知识库可检索性的基础

## 支持文件

- `references/summary-template.md` — Session 存档完整模板
- `references/knowledge-rules.md` — 各分类写入规则 + 文件格式模板
- `references/starfish-model.md` — 海星模型详解与示例
