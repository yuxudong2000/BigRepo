# 基于 Hermes-agent 并行化技术优化 self-learning skill

<!-- anchor:overview -->
## 1. 背景与目标

### 当前实现分析

`self-learning` skill 当前采用**串行执行模式**:

```
Step 1: 分析对话上下文 (串行)
   ↓
Step 2: 生成 Session 存档 (单次 LLM 调用)
   ↓
Step 3: 知识提炼 (串行遍历 7 个分类)
   ↓
Step 4: 更新 index.md + log.md (串行写入)
   ↓
Step 5: 输出归档摘要
```

**性能瓶颈**:
- ❌ Step 3 串行遍历 7 个分类 (solutions/tools/patterns/insights/memories/rules/skills)
- ❌ 每个分类独立调用 LLM 分析可提炼内容
- ❌ 文件写入串行执行
- ❌ 长对话 (50+ 轮) 分析耗时 > 60s

### 优化目标

应用 Hermes-agent 中验证的并行化模式:
1. **并行知识提炼** (借鉴 `delegate_task` 并行批量模式)
2. **异步文件写入** (借鉴原子写入 + 并发 I/O)
3. **流式输出** (借鉴 `as_completed` 模式)
4. **智能缓存** (避免重复分析)

**预期收益**:
- ⚡ 知识提炼阶段加速 **5-7x** (7 个分类并行)
- ⚡ 总体执行时间缩短 **60-70%**
- ✅ 保持结果一致性和原子性

---

<!-- anchor:bottleneck-analysis -->
## 2. 瓶颈分析与可并行化点

### 2.1 当前串行瓶颈

| 阶段 | 耗时占比 | 瓶颈点 |
|------|---------|--------|
| **Step 1 上下文分析** | 5% | 单次 LLM 调用,可接受 |
| **Step 2 Session 存档** | 15% | 单次 LLM 生成,不可避免 |
| **Step 3 知识提炼** | **70%** | 🔴 **7 个分类串行调用 LLM** |
| **Step 4 索引更新** | 8% | 串行文件写入 |
| **Step 5 摘要输出** | 2% | 可忽略 |

### 2.2 Hermes-agent 可借鉴模式

从调研报告中提取的关键技术:

#### ✅ 模式 1: 子 Agent 并行委托

**Hermes 实现** (`tools/delegate_tool.py`):
```python
def delegate_batch(tasks: List[str]):
    """并行启动多个子 Agent"""
    with ProcessPoolExecutor() as executor:
        results = executor.map(_run_child_agent, tasks)
    return list(results)
```

**应用到 self-learning**:
```python
# 7 个分类并行提炼
categories = ["solutions", "tools", "patterns", "insights", "memories", "rules", "skills"]
tasks = [
    f"从 session 内容中提炼 {cat} 相关的可复用知识"
    for cat in categories
]
results = delegate_batch(tasks)  # 并行执行
```

#### ✅ 模式 2: 异步文件写入

**Hermes 实现** (`tools/memory_tool.py`):
```python
# 原子写入模式
fd, temp_path = tempfile.mkstemp(dir=target.parent)
os.write(fd, content.encode())
os.fsync(fd)
os.replace(temp_path, target)  # 原子替换
```

**应用到 self-learning**:
```python
async def batch_write_files(file_contents: Dict[str, str]):
    """并发写入多个文件"""
    tasks = [
        _atomic_write_async(path, content)
        for path, content in file_contents.items()
    ]
    await asyncio.gather(*tasks)
```

#### ✅ 模式 3: 流式结果返回

**Hermes 实现** (`tools/session_search_tool.py`):
```python
async def adaptive_summarize(snippets):
    for coro in asyncio.as_completed(tasks):
        yield await coro  # 流式返回
```

**应用到 self-learning**:
```python
async def stream_knowledge_extraction():
    """提炼结果流式返回,边提炼边写入"""
    for category in categories:
        result = await extract_category(category)
        yield result
        await write_to_knowledge_base(result)  # 立即写入
```

---

<!-- anchor:optimization-design -->
## 3. 优化方案设计

### 3.1 架构改造

**优化前 (串行)**:
```
┌─────────────────────────────────────────┐
│  Step 3: 知识提炼 (串行)                │
│  ┌──────────────────────────────────┐  │
│  │ solutions  → LLM Call → Write    │  │
│  │ tools      → LLM Call → Write    │  │
│  │ patterns   → LLM Call → Write    │  │
│  │ insights   → LLM Call → Write    │  │
│  │ memories   → LLM Call → Write    │  │
│  │ rules      → LLM Call → Write    │  │
│  │ skills     → LLM Call → Write    │  │
│  └──────────────────────────────────┘  │
│  总耗时: 7 × t_llm ≈ 35-70s             │
└─────────────────────────────────────────┘
```

**优化后 (并行)**:
```
┌─────────────────────────────────────────┐
│  Step 3: 知识提炼 (并行)                │
│  ┌──────────┬──────────┬──────────┐    │
│  │solutions │  tools   │ patterns │    │
│  │→ LLM Call│→ LLM Call│→ LLM Call│    │
│  └──────────┴──────────┴──────────┘    │
│  ┌──────────┬──────────┬──────────┐    │
│  │ insights │ memories │  rules   │    │
│  │→ LLM Call│→ LLM Call│→ LLM Call│    │
│  └──────────┴──────────┴──────────┘    │
│  ┌──────────┐                           │
│  │  skills  │                           │
│  │→ LLM Call│                           │
│  └──────────┘                           │
│  ↓ (异步并发写入)                       │
│  总耗时: max(t_llm) ≈ 5-10s             │
└─────────────────────────────────────────┘
```

### 3.2 核心实现策略

#### 策略 1: 并行提炼子 Agent

使用 `use_subagent` 并行启动 7 个专项提炼 Agent:

```markdown
**子 Agent 配置**:
- `subagent_name`: "knowledge-extractor"
- `task`: "从 session 内容中提炼 {category} 相关的可复用知识,遵循 knowledge-rules.md"
- `allowed_tools`: ["read_file"]  # 仅读权限,不写入
- `background`: false  # 等待结果
```

**优点**:
- ✅ 隔离性: 每个子 Agent 独立上下文
- ✅ 并行度: 7 个子 Agent 并发执行
- ✅ 容错性: 单个失败不影响其他

#### 策略 2: 批量 LLM 调用优化

**当前**: 7 次独立 LLM 调用  
**优化**: 单次批量调用 + 结构化输出

```json
{
  "model": "gpt-4",
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "knowledge_extraction",
      "schema": {
        "type": "object",
        "properties": {
          "solutions": {"type": "array", "items": {"type": "object"}},
          "tools": {"type": "array"},
          "patterns": {"type": "array"},
          "insights": {"type": "array"},
          "memories": {"type": "array"},
          "rules": {"type": "array"},
          "skills": {"type": "array"}
        }
      }
    }
  }
}
```

**优点**:
- ⚡ HTTP 请求开销从 7 次 → 1 次
- ⚡ 总延迟从 `7 × t_llm` → `1.2 × t_llm` (略增加 tokens)

#### 策略 3: 异步文件写入池

```python
async def atomic_write_pool(writes: List[Tuple[Path, str]]):
    """
    并发写入多个文件,保证原子性
    """
    semaphore = asyncio.Semaphore(5)  # 限流防止文件系统压力
    
    async def _write_one(path: Path, content: str):
        async with semaphore:
            # 原子写入模式 (借鉴 Hermes)
            temp = path.parent / f".tmp_{path.name}_{uuid.uuid4().hex[:8]}"
            await asyncio.to_thread(temp.write_text, content)
            await asyncio.to_thread(os.replace, temp, path)
    
    tasks = [_write_one(p, c) for p, c in writes]
    await asyncio.gather(*tasks)
```

---

<!-- anchor:implementation-plan -->
## 4. 实施计划

### Phase 1: 扩展 Skill 结构 (准备工作)

**目标**: 增加支持文件,不改动现有逻辑

**新增文件**:
```
self-learning/
├── SKILL.md (保持不变)
├── references/
│   ├── knowledge-rules.md (保持不变)
│   ├── summary-template.md (保持不变)
│   ├── starfish-model.md (保持不变)
│   └── 🆕 parallel-extraction-prompt.md  # 并行提取提示词模板
└── 🆕 scripts/
    ├── parallel_extractor.py  # 并行提取器 (可选,若 Skill 支持 Python)
    └── batch_writer.py        # 批量写入器
```

**parallel-extraction-prompt.md 内容**:
```markdown
# 并行知识提取提示词

你是一个专项知识提取 Agent,负责从 session 内容中提炼 **{category}** 相关的可复用知识。

## 输入
- Session 完整内容 (Markdown)
- 当前分类: {category}
- 提取规则: knowledge-rules.md § {category}

## 输出格式
JSON Array,每个条目包含:
{
  "filename": "xxx.md",
  "action": "create" | "append",
  "content": "完整 Markdown 内容"
}

## 要求
1. 严格遵守 knowledge-rules.md 中的写入条件
2. 如无可提炼内容,返回空数组 []
3. 文件名必须语义化 (slug 格式)
4. 追加时注明来源 session slug
```

### Phase 2: 实现并行提取逻辑 (核心改造)

**修改 SKILL.md Step 3**:

```markdown
### Step 3：并行知识提炼 ⚡ (已优化)

**执行模式**: 使用 `use_subagent` 并行启动 7 个专项提取 Agent

**流程**:
1. 加载 session 内容到共享上下文
2. 并行启动 7 个子 Agent (每个负责一个分类):
   ```
   use_subagent(
     subagent_name="knowledge-extractor",
     task=f"从 session 中提炼 {category},遵循 knowledge-rules.md",
     background=false
   )
   ```
3. 等待所有子 Agent 返回结果
4. 合并提取结果
5. 批量异步写入文件

**性能提升**: 
- 串行模式: 7 × 5s = 35s
- 并行模式: max(5s) + 合并 1s = **6s**
- **加速比: 5.8x** ⚡

**容错机制**:
- 单个分类提取失败不影响其他
- 失败的分类回退到串行重试
```

### Phase 3: 优化文件写入 (I/O 优化)

**目标**: 并发写入多个文件,减少 I/O 等待

**实现**:
```markdown
### Step 4：批量更新索引和文件 (已优化)

**并发写入清单**:
1. 所有提炼的知识文件 (solutions/xxx.md, tools/xxx.md, ...)
2. index.md (追加新条目)
3. log.md (追加归档记录)

**写入策略**:
- 使用异步 I/O (asyncio.to_thread)
- 信号量限流 (Semaphore=5)
- 原子写入保证 (temp file + os.replace)

**性能提升**:
- 串行模式: 7 个文件 × 0.5s = 3.5s
- 并行模式: max(0.5s) + 信号量开销 = **1s**
- **加速比: 3.5x** ⚡
```

### Phase 4: 流式输出 (用户体验优化)

**目标**: 边提炼边展示进度,不等待全部完成

**实现**:
```markdown
### Step 5：流式输出归档摘要 (已优化)

**输出模式**: 使用 `asyncio.as_completed` 流式返回

示例输出:
```
🚀 开始知识提炼 (7 个分类并行)...

✅ [solutions] 提炼完成 → solutions/frontend-cloud-deploy.md (新建)
✅ [tools] 提炼完成 → tools/frontend-cloud-cli.md (追加)
✅ [patterns] 无可提炼内容
✅ [insights] 提炼完成 → insights/static-site-workflow.md (新建)
✅ [memories] 提炼完成 → memories/2026-04-29_memories.md (2 条候选)
✅ [rules] 无可提炼内容
✅ [skills] 提炼完成 → skills/deploy-appwrite-project.md (新建)

📝 写入文件中... (4 个文件并发)
✅ 全部写入完成 (耗时 1.2s)

📚 知识库更新摘要: ...
```

**用户体验提升**:
- 实时进度反馈 (不再黑盒等待)
- 可提前看到部分结果
- 感知速度提升 > 实际速度提升
```

---

<!-- anchor:backward-compatibility -->
## 5. 向后兼容与降级方案

### 5.1 Feature Flag 控制

在 SKILL.md 顶部增加配置:

```yaml
---
name: self-learning
version: 2.0.0  # 升级版本号
parallel_mode: true  # Feature Flag: 并行模式开关
fallback_to_serial: true  # 失败时回退到串行
---
```

### 5.2 降级触发条件

```markdown
## 自动降级到串行模式

以下情况自动回退:
1. `use_subagent` 工具不可用
2. 对话轮次 < 10 (小对话无需并行)
3. 任意子 Agent 超时 (> 30s)
4. 用户环境不支持并发 (检测 asyncio 可用性)

**降级日志**:
```
⚠️ 并行模式不可用,回退到串行模式
原因: use_subagent 工具未启用
预计耗时: 35s (vs 并行模式 6s)
```
```

---

<!-- anchor:metrics -->
## 6. 性能评估与监控

### 6.1 基准测试场景

| 场景 | 对话轮次 | 工具调用 | 预期提炼项 |
|------|---------|---------|-----------|
| **小型** | 10-20 | < 15 | 1-2 个分类有内容 |
| **中型** | 30-50 | 20-40 | 3-5 个分类有内容 |
| **大型** | 60+ | 50+ | 5-7 个分类有内容 |

### 6.2 性能指标对比

| 指标 | 串行模式 (v1.0) | 并行模式 (v2.0) | 提升 |
|------|----------------|----------------|------|
| **小型对话** | 15s | 8s | 1.9x |
| **中型对话** | 35s | 10s | 3.5x |
| **大型对话** | 70s | 12s | **5.8x** |
| **I/O 写入** | 3.5s | 1s | 3.5x |
| **总体加速** | - | - | **3-6x** |

### 6.3 监控埋点

在 SKILL.md 中增加调试日志:

```markdown
## 性能日志 (调试模式)

```json
{
  "session_slug": "hermes-agent-analysis",
  "total_time": "12.3s",
  "breakdown": {
    "step1_context_analysis": "0.8s",
    "step2_session_archive": "2.1s",
    "step3_parallel_extraction": "6.2s",
    "step4_batch_write": "1.0s",
    "step5_summary_output": "0.2s"
  },
  "parallel_stats": {
    "subagents_launched": 7,
    "subagents_succeeded": 6,
    "subagents_failed": 1,
    "fallback_triggered": false
  },
  "extracted_files": 4,
  "total_tokens": 12500
}
```
```

---

<!-- anchor:rollout-plan -->
## 7. 上线策略

### 7.1 灰度发布

| 阶段 | 流量占比 | 监控指标 | 回滚条件 |
|------|---------|---------|---------|
| **Alpha** | 10% | 成功率 > 95% | 成功率 < 90% |
| **Beta** | 50% | 加速比 > 3x | 用户投诉 > 2 |
| **GA** | 100% | 稳定运行 7 天 | 严重 Bug |

### 7.2 A/B 测试指标

**主要指标**:
- ⏱️ 总执行时间 (Target: < 15s for 中型对话)
- ✅ 提炼质量 (人工抽检,一致性 > 95%)
- 🚀 用户满意度 (完成后调查)

**次要指标**:
- 🔄 子 Agent 成功率
- 💾 文件写入完整性
- 🐛 错误率

---

## 8. 风险与应对

### 8.1 技术风险

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| 子 Agent 并发限制 | 中 | 中 | 动态调整并发度 (7 → 3) |
| LLM 批量调用失败 | 低 | 高 | 回退到逐个调用 |
| 文件系统竞争 | 低 | 中 | 信号量限流 + 重试 |
| 提炼质量下降 | 低 | 高 | A/B 测试验证,人工抽检 |

### 8.2 兼容性风险

**不支持并行的环境**:
- Windows 上 ProcessPoolExecutor 限制
- 低内存环境 (< 2GB)
- 旧版 Python (< 3.10)

**应对**: 自动检测环境,降级到串行模式

---

## 9. 后续优化方向

### 9.1 智能缓存层

**场景**: 相似对话避免重复提炼

```python
# 检测 session 相似度
if similarity(current_session, cached_session) > 0.85:
    reuse_extraction(cached_session)
    only_extract_diff()
```

### 9.2 增量提炼

**场景**: 长对话中途归档

```markdown
## 增量归档模式

当对话超过 50 轮时,支持:
- 中途归档 (保存检查点)
- 仅提炼新增部分
- 合并到最终归档
```

### 9.3 多模态支持

**未来**: 支持提炼图片、代码截图中的知识

---

## 10. 总结

### 核心改进

1. ⚡ **并行知识提炼**: 7 个分类并发 → **5-7x 加速**
2. ⚡ **异步文件写入**: 批量并发 I/O → **3.5x 加速**
3. 🎯 **流式进度反馈**: 实时展示 → 用户体验提升
4. 🛡️ **向后兼容**: Feature Flag + 自动降级

### 技术债务清理

- [ ] 移除 `session-summary` skill (已被 `self-learning` 取代)
- [ ] 统一知识库路径配置 (当前硬编码)
- [ ] 增加单元测试 (提炼逻辑验证)

### 成功标准

- ✅ 中型对话 (30-50 轮) 归档时间 < 15s
- ✅ 提炼质量一致性 > 95%
- ✅ 无文件损坏或丢失
- ✅ 用户满意度 > 4.5/5

---

**参考文献**:
- Hermes-Agent 自进化机制深度分析 (`hermes-agent-self-evolution-analysis.md`)
- Hermes `delegate_tool.py` 并行批量模式
- Hermes `session_search_tool.py` 异步摘要模式
- Hermes `memory_tool.py` 原子写入模式
