# 并行 Skill 优化通用模式

> 分类：skills  
> 来源：2026-04-29 self-learning-skill-optimization  
> Skill 化潜力：⭐⭐⭐⭐ (高)

---

## [2026-04-29] 来自 self-learning-skill-optimization

### Skill 化流程候选

**场景**：基于开源项目调研，优化现有 skill 的性能（通过并行化）

### 触发词建议

- "优化 XXX skill 的性能"
- "让 XXX skill 并行化"
- "加速 XXX skill"
- "应用并行模式到 XXX skill"

### 核心流程

#### Step 1: 识别瓶颈

**输入**：现有 skill 的执行流程

**分析点**：
- 哪些步骤是串行的？
- 哪些步骤耗时最长？
- 哪些步骤可以并行执行？

**本次案例**：
- 瓶颈：7 个分类串行提炼，每个 5s，总计 35s
- 可并行性：7 个分类独立，无依赖关系

#### Step 2: 拆分任务

**原则**：
- 任务必须**独立**（无共享状态）
- 任务之间**无依赖**（可同时执行）
- 输出格式**标准化**（便于合并）

**本次案例**：
- 拆分：每个分类独立成子任务
- 输入：session 内容 + 分类规则
- 输出：JSON 数组（文件名 + 操作 + 内容）

#### Step 3: 并行委托

**工具选择**：
- ✅ `use_subagent`（适合需要完整 LLM 推理的子任务）
- ⚠️ `delegate_task`（Hermes-agent 专用，MyFlicker 暂无）

**并发模式**：
```python
# 伪代码
results = []
for category in ["solutions", "tools", "patterns", ...]:
    result = use_subagent(
        subagent_name="knowledge-extractor",
        task=f"从 session 中提炼 {category} 相关知识...",
        background=False  # 等待完成
    )
    results.append(result)
```

#### Step 4: 合并结果

**关键操作**：
- 解析每个子任务的输出（JSON）
- 去重（同一文件名的多个条目合并）
- 验证格式（确保符合规范）

**容错机制**：
- 单个子任务失败不影响其他
- 超时保护（30s 自动跳过）

#### Step 5: 降级兜底

**自动降级条件**：
1. 并行工具不可用（如 `use_subagent` disabled）
2. 任务规模太小（如对话轮次 < 10）
3. 子任务超时

**降级逻辑**：
- 回退到原有串行模式
- 显示降级原因和预计耗时
- 输出格式保持一致

### 关键决策点

#### 决策 1：是否值得并行？

**判断标准**：
- 串行耗时 > 20s？✅ 值得
- 任务数量 ≥ 3？✅ 值得
- 子任务独立？✅ 值得

**本次案例**：7 个分类 × 5s = 35s → 并行后 6s（节省 83%）

#### 决策 2：子 Agent vs 批量调用？

**子 Agent 方式**（本次采用）：
- ✅ 每个分类独立推理
- ✅ 容错性强（单个失败不影响全局）
- ❌ 可能增加总 token 消耗

**批量结构化输出**（备选）：
- ✅ 单次 LLM 调用，token 更省
- ❌ 容错性差（一个分类失败可能影响全部）
- ❌ 输出结构复杂

#### 决策 3：流式输出 vs 批量输出？

**流式输出**（推荐）：
```
✅ [solutions] 提炼完成 → 1 个文件
✅ [tools] 提炼完成 → 1 个文件
...
```
- ✅ 用户体验好（实时反馈）
- ✅ 感知速度快

**批量输出**：
```
⏳ 知识提炼中...（等待 35s）
✅ 完成（7 个文件）
```
- ❌ 用户焦虑（黑盒等待）

### 性能预期模板

| 任务规模 | 串行耗时 | 并行耗时 | 加速比 |
|---------|---------|---------|--------|
| 小型 | Xs | Ys | X/Y |
| 中型 | X's | Y's | X'/Y' |
| 大型 | X''s | Y''s | X''/Y'' |

**本次案例**：
- 中型：35s → 10s（3.5x）
- 大型：70s → 12s（5.8x）

### Skill 化建议

**Frontmatter 参数**：
```yaml
name: parallel-skill-optimizer
parallel_mode: true          # 默认启用并行
fallback_to_serial: true     # 自动降级
min_task_count: 3            # 最少任务数（否则不并行）
timeout_per_task: 30         # 单任务超时（秒）
```

**输入**：
- 目标 skill 的执行流程
- 可并行步骤列表
- 子任务提示词模板

**输出**：
- 优化后的 skill SKILL.md
- 子 Agent 定义文件
- 性能测试报告

### 成熟度评估

- ✅ 复用频率：中（每次优化 skill 都可用）
- ✅ 封装优先级：高（模式清晰，可泛化）
- ✅ 技术可行性：已验证（self-learning skill v2.0 实测）
- ⏳ 当前状态：**可落地**（需要编写通用 skill）

### 相关参考

- **Hermes-agent**: `tools/delegate_tool.py` — 并行批量委托
- **Self-learning skill v2.0**: 完整并行化实现案例
