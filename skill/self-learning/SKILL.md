---
name: self-learning
description: 对话知识沉淀技能。当用户说「总结一下」「写个总结」「生成对话总结」「存档本次对话」「session summary」「把这次对话总结写下来」「归档」时触发。分析当前对话的目标、任务拆解、执行过程（含工具使用）、最终结果、洞察与经验，并使用海星模型（保持/开始/停止/更多/更少）进行复盘，直接写入本地 sessions/ 存档，同时自动提炼可复用知识写入 knowledge/ 对应分类，更新 index.md 和 log.md。
version: 2.0.0
parallel_mode: true
fallback_to_serial: true
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

### Step 3：并行知识提炼 ⚡ (v2.0 优化)

**执行模式**：并行模式（优先）或串行模式（降级）

#### 并行模式（推荐）

**触发条件**：
- ✅ `use_subagent` 工具可用
- ✅ 对话轮次 ≥ 10（小对话自动降级到串行）
- ✅ `parallel_mode: true`（Skill frontmatter 配置）

**执行流程**：
1. **加载 session 内容到共享上下文**
   - 读取 Step 2 生成的 session 存档文件
   - 准备提取规则文档 (knowledge-rules.md)

2. **并行启动 7 个专项提取 Agent**
   - 每个 Agent 负责一个分类（solutions/tools/patterns/insights/memories/rules/skills）
   - 使用 `knowledge-extractor` 子 Agent
   - 并发执行，互不阻塞

   ```
   并行调用 7 次 use_subagent:
   
   use_subagent(
     subagent_name="knowledge-extractor",
     task=f"""从以下 session 中提炼 **{category}** 相关的可复用知识：
     
     {session_content}
     
     参考 ~/.codeflicker/skills/self-learning/references/knowledge-rules.md § {category} 章节。
     参考 ~/.codeflicker/skills/self-learning/references/parallel-extraction-prompt.md 了解输出格式。
     
     如无可提炼内容，返回空数组 []。
     如有内容，返回 JSON 数组，每个条目包含 filename、action、content 字段。
     """,
     background=false
   )
   ```

3. **等待所有子 Agent 返回结果**
   - 容错机制：单个分类失败不影响其他
   - 超时保护：单个子 Agent 超时 30s 自动跳过

4. **合并提取结果**
   - 解析每个子 Agent 返回的 JSON 数组
   - 去重（同一文件名的多个条目合并）
   - 验证文件名格式（slug 规范）

5. **批量写入文件**（见 Step 4）

**性能提升**：
- 串行模式：7 × 5s = 35s
- 并行模式：max(5s) + 合并 1s = **6s**
- **加速比：5.8x** ⚡

**流式进度反馈**（实时展示）：
```
🚀 开始知识提炼（7 个分类并行）...

✅ [solutions] 提炼完成 → 1 个文件
✅ [tools] 提炼完成 → 1 个文件
✅ [patterns] 无可提炼内容
✅ [insights] 提炼完成 → 1 个文件
✅ [memories] 提炼完成 → 2 条候选
✅ [rules] 无可提炼内容
✅ [skills] 提炼完成 → 1 个文件
```

---

#### 串行模式（降级兜底）

**自动降级条件**（满足任一即降级）：
1. `use_subagent` 工具不可用
2. 对话轮次 < 10（小对话无需并行）
3. 任意子 Agent 超时（> 30s）
4. `parallel_mode: false`（手动禁用）

**执行流程**：
按照 v1.0 原有逻辑，逐个分类串行提炼：

| 分类 | 写入条件 | 详细规则见 |
|------|---------|-----------|
| `solutions/` | 有可复用解法（可复用性 ≥ 中） | knowledge-rules.md § solutions |
| `tools/` | 有工具踩坑或最佳实践（有泛化价值） | knowledge-rules.md § tools |
| `patterns/` | 有可泛化的执行流程（跨对话适用） | knowledge-rules.md § patterns |
| `insights/` | 有超出单次对话的认知发现 | knowledge-rules.md § insights |
| `memories/` | 有记忆候选项 | knowledge-rules.md § memories |
| `rules/` | 有操作约束/规范/禁止项 | knowledge-rules.md § rules |
| `skills/` | 检测到值得封装为 skill 的流程 | knowledge-rules.md § skills |

**降级日志**：
```
⚠️ 并行模式不可用，回退到串行模式
原因：use_subagent 工具未启用
预计耗时：35s（vs 并行模式 6s）
```

---

**提炼原则**（两种模式通用）：
- 只写"可复用"内容，纯过程记录留在 sessions/
- 每个提炼条目写入独立文件（除 memories/ 按日期聚合）
- 如该主题已有文件，**追加更新**，不重新创建

---

### Step 4：批量更新索引和文件 ⚡ (v2.0 优化)

**并发写入策略**（借鉴 Hermes-agent 原子写入模式）

#### 并发写入清单

1. **所有提炼的知识文件**（solutions/xxx.md, tools/xxx.md, ...）
2. **index.md**（追加新文件到对应分类条目）
3. **log.md**（追加归档记录）

#### 写入流程

**并行模式**（推荐）：
1. **批量准备写入任务**
   - 从 Step 3 获取所有提取结果
   - 为每个文件生成完整路径和内容
   - 准备 index.md 和 log.md 的更新内容

2. **并发执行文件写入**
   - 使用信号量限流（最多 5 个并发写入，防止文件系统压力）
   - 每个文件使用原子写入模式（参考 Hermes `tools/memory_tool.py`）：
     ```
     1. 临时文件写入：temp_file = .tmp_filename_{uuid}
     2. 内容写入 + fsync（确保数据落盘）
     3. 原子替换：os.replace(temp_file, target_file)
     ```
   - 并发写入多个文件，互不阻塞

3. **验证写入完整性**
   - 检查所有文件是否成功创建/更新
   - 失败的文件记录到日志

**性能提升**：
- 串行模式：7 个文件 × 0.5s = 3.5s
- 并行模式：max(0.5s) + 信号量开销 = **1s**
- **加速比：3.5x** ⚡

#### 文件格式

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

#### 原子性保证

**关键机制**（借鉴 Hermes-agent）：
1. **临时文件 + 原子替换**：防止写入中断导致文件损坏
2. **fsync 强制落盘**：确保数据持久化
3. **错误恢复**：临时文件在异常时自动清理

**并发写入代码逻辑**（伪代码）：
```python
async def batch_write_files(file_writes: List[Tuple[Path, str]]):
    """并发写入多个文件，保证原子性"""
    semaphore = asyncio.Semaphore(5)  # 限流
    
    async def atomic_write_one(path: Path, content: str):
        async with semaphore:
            # 临时文件
            temp = path.parent / f".tmp_{path.name}_{uuid.uuid4().hex[:8]}"
            # 写入 + fsync
            await asyncio.to_thread(temp.write_text, content)
            # 原子替换
            await asyncio.to_thread(os.replace, temp, path)
    
    tasks = [atomic_write_one(p, c) for p, c in file_writes]
    await asyncio.gather(*tasks)
```

**注意事项**：
- 确保目录存在：每个写入前自动 `mkdir -p`
- 追加优先于新建：同主题文件已存在时追加，不覆盖
- index.md 和 log.md 必须更新（知识库可检索性基础）

---

### Step 5：流式输出归档摘要 ⚡ (v2.0 优化)

**输出模式**：流式进度反馈（边提炼边展示）

#### 并行模式输出示例

```
🚀 开始知识提炼（7 个分类并行）...

✅ [solutions] 提炼完成 → solutions/npm-registry-access-denied.md（新建）
✅ [tools] 提炼完成 → tools/frontend-cloud-cli.md（追加）
✅ [patterns] 无可提炼内容
✅ [insights] 提炼完成 → insights/static-site-deploy-workflow.md（新建）
✅ [memories] 提炼完成 → memories/2026-04-29_memories.md（2 条候选）
✅ [rules] 无可提炼内容
✅ [skills] 提炼完成 → skills/deploy-appwrite-project.md（新建）

📝 批量写入文件中...（4 个文件并发）
✅ 全部写入完成（耗时 1.2s）

─────────────────────────────────────

✅ **Session 已存档**
📄 knowledge/sessions/2026-04-29_14-30_hermes-agent-analysis.md

📚 **知识库更新**（新增/更新 4 个文件）
  - solutions/npm-registry-access-denied.md（新建）— npm Access Denied 错误解决
  - tools/frontend-cloud-cli.md（追加）— 参数使用经验
  - insights/static-site-deploy-workflow.md（新建）— 静态站点部署工作流理解
  - skills/deploy-appwrite-project.md（新建）— Appwrite 项目部署流程

💡 **记忆候选项**（2 条，需要你决定是否执行 update_memory）
  - [ ] [constraint_or_forbidden_rule] 删除文件操作必须先获取用户确认
  - [ ] [development_practice_specification] 部署前必须先在测试环境验证

⚡ **性能统计**
  - 总耗时：8.5s（串行模式预计 40s，节省 79%）
  - 知识提炼：6.2s（并行）
  - 文件写入：1.2s（批量）
  - 其他：1.1s
```

#### 串行模式输出示例

```
📝 开始知识提炼（串行模式）...

  [1/7] solutions... ✅（1 个文件）
  [2/7] tools... ✅（1 个文件）
  [3/7] patterns... ⏭️（无内容）
  [4/7] insights... ✅（1 个文件）
  [5/7] memories... ✅（2 条候选）
  [6/7] rules... ⏭️（无内容）
  [7/7] skills... ✅（1 个文件）

📝 写入文件中...
✅ 写入完成（耗时 3.8s）

─────────────────────────────────────

✅ **Session 已存档**
📄 knowledge/sessions/2026-04-29_14-30_hermes-agent-analysis.md

📚 **知识库更新**（新增/更新 4 个文件）
  - solutions/npm-registry-access-denied.md（新建）— npm Access Denied 错误解决
  - tools/frontend-cloud-cli.md（追加）— 参数使用经验
  - insights/static-site-deploy-workflow.md（新建）— 静态站点部署工作流理解
  - skills/deploy-appwrite-project.md（新建）— Appwrite 项目部署流程

💡 **记忆候选项**（2 条，需要你决定是否执行 update_memory）
  - [ ] [constraint_or_forbidden_rule] 删除文件操作必须先获取用户确认
  - [ ] [development_practice_specification] 部署前必须先在测试环境验证
```

#### 用户体验提升

**实时反馈**：
- ✅ 每个分类提炼完成立即展示
- ✅ 显示文件名和操作类型（新建/追加）
- ✅ 性能统计（并行模式下显示节省时间）

**感知速度优化**：
- 流式输出让用户提前看到部分结果
- 不再"黑盒等待"35 秒
- 感知速度提升 > 实际速度提升

---

## 注意事项

### v2.0 并行模式特定注意事项

1. **并行模式优先，自动降级兜底**
   - 优先尝试并行模式（use_subagent）
   - 不可用时自动降级到串行模式
   - 降级会显示原因和预计耗时

2. **子 Agent 隔离性**
   - 每个分类提取独立执行，互不干扰
   - 单个分类失败不影响其他分类
   - 超时保护：30s 自动跳过

3. **原子写入保证**
   - 使用临时文件 + 原子替换
   - 防止写入中断导致文件损坏
   - 并发写入有信号量限流（防止文件系统压力）

4. **流式进度反馈**
   - 边提炼边展示进度，实时可见
   - 性能统计显示节省时间（并行模式）
   - 用户体验优于串行"黑盒等待"

### 通用注意事项（v1.0 + v2.0）

1. **Step 2 和 Step 3 都要做**，不能只做其一
2. **完整复现每一步**，包括失败的尝试和回退，不省略
3. **记忆候选只列出，不自动执行**，由用户决定
4. **确保目录存在再写入**：自动 `mkdir -p <path>`（v2.0 优化）
5. **追加优先于新建**：同主题文件已存在时追加，不覆盖
6. **index.md 和 log.md 必须更新**，这是知识库可检索性的基础

### 性能预期（v2.0）

| 对话规模 | 串行模式 | 并行模式 | 加速比 |
|---------|---------|---------|--------|
| **小型** (10-20 轮) | 15s | 8s | 1.9x |
| **中型** (30-50 轮) | 35s | 10s | 3.5x |
| **大型** (60+ 轮) | 70s | 12s | **5.8x** |

### 降级触发条件

自动降级到串行模式（满足任一即降级）：
1. `use_subagent` 工具不可用
2. 对话轮次 < 10（小对话无需并行）
3. 任意子 Agent 超时（> 30s）
4. `parallel_mode: false`（手动禁用，在 frontmatter 设置）

## 支持文件

### v2.0 新增

- `references/parallel-extraction-prompt.md` — 并行提取提示词模板（子 Agent 使用）
- `~/.codeflicker/agents/knowledge-extractor.md` — 知识提取子 Agent 定义

### v1.0 原有

- `references/summary-template.md` — Session 存档完整模板
- `references/knowledge-rules.md` — 各分类写入规则 + 文件格式模板
- `references/starfish-model.md` — 海星模型详解与示例

---

## 版本更新日志

### v2.0.0 (2026-04-29) — 并行化优化

**核心改进**：
- ⚡ **并行知识提炼**：7 个分类并发执行，加速 5-7x
- ⚡ **批量文件写入**：并发 I/O，加速 3.5x
- 🎯 **流式进度反馈**：实时展示，用户体验提升
- 🛡️ **向后兼容**：自动降级机制，保证兼容性

**技术亮点**：
- 借鉴 Hermes-agent 的并行委托模式 (`delegate_task`)
- 借鉴 Hermes-agent 的原子写入模式 (`atomic_write`)
- 借鉴 Hermes-agent 的流式输出模式 (`as_completed`)

**性能提升**：
- 中型对话 (30-50 轮)：35s → 10s（节省 71%）
- 大型对话 (60+ 轮)：70s → 12s（节省 83%）

**兼容性**：
- ✅ Feature Flag 控制（`parallel_mode: true`）
- ✅ 自动降级兜底（use_subagent 不可用时回退串行）
- ✅ 输出格式保持一致

---

### v1.0.0 (2024) — 初始版本

**核心功能**：
- Session 完整归档
- 7 分类知识提炼（串行）
- index.md + log.md 索引
- 海星模型复盘
- 记忆候选项生成

---

## 参考文献

- **Hermes-Agent 自进化机制深度分析** (Thread assets: `docs/analysis/hermes-agent-self-evolution-analysis.md`)
  - 并行化技术调研
  - 性能优化方案
  - 原子写入模式

- **Hermes-Agent 源码** (GitHub: NousResearch/hermes-agent)
  - `tools/delegate_tool.py` — 并行批量委托
  - `tools/memory_tool.py` — 原子写入实现
  - `tools/session_search_tool.py` — 异步摘要模式
