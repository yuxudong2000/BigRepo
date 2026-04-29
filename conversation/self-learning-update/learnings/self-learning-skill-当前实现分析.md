# Hermes-Agent 知识提取与学习架构深度分析

基于完整代码分析，hermes-agent 项目**并没有独立的 self-learning skill**，而是通过一套**模块化的记忆提供者（Memory Provider）插件系统**实现跨会话知识提取和学习能力。以下是完整的架构分析：

---

## 1. 核心架构：MemoryProvider 插件系统

### 1.1 设计哲学
- **单一外部提供者限制**：同时最多运行 1 个外部记忆提供者 + 1 个内置提供者（MEMORY.md/USER.md）
- **无侵入性集成**：所有提供者通过 `MemoryManager` 统一编排，`run_agent.py` 仅需调用 manager 方法
- **失败隔离**：一个提供者失败不会阻塞其他提供者

### 1.2 MemoryProvider ABC 定义的生命周期
```python
# 核心生命周期方法（所有提供者必须实现）:
initialize(session_id, **kwargs)          # 连接资源、创建数据库
system_prompt_block() -> str              # 静态说明文本注入系统提示
prefetch(query, session_id) -> str        # 每轮前从后台线程获取缓存结果
queue_prefetch(query, session_id)         # 每轮后启动后台预加载
sync_turn(user, assistant, session_id)    # 每轮后非阻塞同步
get_tool_schemas() -> List[Dict]          # 工具定义
handle_tool_call(name, args) -> str       # 工具调度
shutdown()                                 # 清理资源

# 可选钩子（重写以启用）:
on_turn_start(turn, message, **kwargs)    # 每轮开始通知
on_session_end(messages)                  # 会话结束时提取知识★
on_pre_compress(messages) -> str          # 压缩前提取待保留见解
on_memory_write(action, target, content)  # 镜像内置记忆写入
on_delegation(task, result, child_sid)    # 子代理完成后观察
```

---

## 2. 三大知识提取模式分析

### 2.1 OpenViking：**服务端自动提取 6 类知识**

#### 工作流程
```
用户输入 ──┐
          ├──► sync_turn() ──► 后台线程 POST /messages (非阻塞)
助手响应 ──┘                         ↓
                                  累积对话轮次
                                      ↓
会话结束 ──► on_session_end() ──► POST /commit ──► 服务端 LLM 提取 ★
                                      ↓
                                  6 类自动分类:
                                  - profile (用户画像)
                                  - preferences (偏好设置)
                                  - entities (实体识别)
                                  - events (事件记录)
                                  - cases (案例库)
                                  - patterns (模式总结)
```

#### 关键特性
- **串行步骤**：
  1. 实时对话同步（后台线程，<5s）
  2. 会话提交（阻塞最多 10s 等待同步完成）
  3. 服务端异步提取（用户无感知）

- **并行化潜力**：
  - ✅ 多个 sync_turn 线程可并发（已实现）
  - ❌ 提取发生在服务端黑盒中（客户端无法并行化）

- **性能瓶颈**：
  - 提交时等待最后的 sync 线程（10s 超时）
  - 服务端提取延迟（用户侧无可见性）

#### 存储结构
```
viking://
├── memories/           # 自动提取的记忆
│   ├── profile/       # 画像：职业、背景
│   ├── preferences/   # 偏好：工具、语言
│   ├── entities/      # 实体：人名、项目名
│   ├── events/        # 事件：时间戳事件
│   ├── cases/         # 案例：问题-解决方案对
│   └── patterns/      # 模式：行为规律
├── resources/          # 手动添加的资源
│   └── docs/          # 文档、代码库
└── skills/            # 技能定义（可选）
```

---

### 2.2 Hindsight：**混合策略知识图谱**

#### 工作流程
```
                    ┌──► recall/reflect 查询 ──► 语义搜索
用户输入 ──┐       │                            + 实体图谱遍历
          ├───────┼──► retain 工具调用 ──────► + 重排序
助手响应 ──┘       │                            ↓
          ↓        │                         结构化事实存储
    auto_retain    │                         (facts/entities/relations)
    (每 N 轮)      │
          ↓        └──► 下次 prefetch 时使用
    后台线程
  Hindsight API
      ↓
  LLM 提取结构化事实
  (异步，可配置)
```

#### 关键特性
- **提取模式**：
  1. **自动提取**：每 N 轮（默认每轮）后台调用 `retain()` API
  2. **显式存储**：Agent 调用 `hindsight_retain` 工具
  3. **会话结束提取**（可选配置）

- **并行化策略**：
  - ✅ `retain_async=True` 时提取完全异步
  - ✅ 预加载（prefetch）在后台线程执行
  - ❌ 反思合成（reflect）必须串行（依赖 LLM 推理）

- **性能瓶颈**：
  - **Cloud 模式**：API 延迟 30-40s（`_DEFAULT_TIMEOUT=120`）
  - **Local 模式**：嵌入式守护进程启动开销
  - 实体解析需要多次数据库查询（N+1 问题）

#### 存储结构
```sql
-- 知识图谱三表结构
facts:        (fact_id, content, timestamp, tags, source)
entities:     (entity_id, name, type, metadata)
relations:    (from_entity, to_entity, fact_id, relation_type)

-- 示例查询：「项目 Alpha 的所有决策」
SELECT f.* FROM facts f
JOIN relations r ON r.fact_id = f.fact_id
JOIN entities e ON e.entity_id = r.from_entity
WHERE e.name = 'project-alpha' AND f.tags LIKE '%decision%'
```

---

### 2.3 Holographic：**本地 HRR 代数记忆**

#### 工作流程
```
用户消息 ──► on_session_end() ──► 正则匹配 ──► add_fact()
                                    ↓
                            I prefer Python
                            my favorite editor is VS Code
                            we decided to use Docker
                                    ↓
                            category="user_pref/project"
                                    ↓
                            ┌─────────────────────┐
                            │ SQLite + NumPy HRR  │
                            │  - facts 表          │
                            │  - entities 表       │
                            │  - hrr_banks 表      │
                            └─────────────────────┘
                                    ↓
                            代数绑定：
                            fact_vector = bind(content, entity, ROLE)
                                    ↓
                            检索时解绑：
                            unbind(bank_vec, entity) ≈ content
```

#### 关键特性
- **完全本地**：无需外部服务，纯 SQLite + NumPy
- **零 LLM 成本**：基于正则规则提取 + 代数检索
- **可选自动提取**：默认关闭（`auto_extract: false`），避免误提取

- **并行化可能性**：
  - ✅ 提取和存储完全本地（<1ms）
  - ✅ HRR 向量计算可批处理
  - ❌ 正则匹配串行（但极快）

- **性能瓶颈**：
  - 大规模实体时的 HRR 重建（O(n²)）
  - 信任分数更新需要全表扫描

---

## 3. 串行 vs 并行分析

### 3.1 必须串行的步骤

| 步骤 | 原因 | 提供者 |
|------|------|--------|
| **会话提交前等待 sync 完成** | 确保所有对话轮次已发送到服务端 | OpenViking |
| **LLM 驱动的反思合成** | 需要推理引擎串行处理上下文 | Hindsight (`reflect`) |
| **实体解析链** | 先提取实体 → 查询图谱 → 创建关系（有依赖） | Hindsight, Holographic |
| **压缩前提取** | 需要完整上下文进行 summarization | 所有提供者 |

### 3.2 可并行化的步骤

| 步骤 | 并行策略 | 已实现？ |
|------|----------|----------|
| **对话轮次同步** | 每轮在独立线程中发送 | ✅ OpenViking, Hindsight |
| **预加载（prefetch）** | 后台线程在前一轮结束时启动 | ✅ 所有提供者 |
| **多类别提取** | 并行提取 profile/preferences/entities | ❌ 服务端黑盒 |
| **向量计算** | 批量计算 embeddings/HRR | ⚠️ 部分（需 NumPy 并行） |
| **工具调用** | Agent 并行调用 `retain` + `search` | ❌ 工具串行执行 |

---

## 4. 知识分类与存储对比

| 维度 | OpenViking | Hindsight | Holographic | Built-in |
|------|------------|-----------|-------------|----------|
| **自动分类** | 6 类（服务端） | 自定义标签 | 4 类（规则） | 无分类 |
| **结构** | 文件树（viking://） | 知识图谱（三元组） | 扁平事实表 | 2 个 .md 文件 |
| **检索方式** | 语义搜索 + 分层加载 | 图遍历 + 语义 + 重排序 | 代数解绑 + 关键词 | 全文匹配 |
| **存储位置** | 远程服务器 | 云/本地数据库 | 本地 SQLite | `~/.hermes/memories/` |
| **容量限制** | 无限（服务端） | 无限（云/本地） | 受限于 SQLite | 2200 + 1375 字符 |

---

## 5. 性能瓶颈定位

### 5.1 网络延迟瓶颈
- **OpenViking commit**: 阻塞等待 sync 线程（最多 10s）
- **Hindsight Cloud**: API 单次调用 30-40s（`_DEFAULT_TIMEOUT=120`）
  ```python
  # plugins/memory/hindsight/__init__.py:50
  _DEFAULT_TIMEOUT = 120  # seconds — cloud API can take 30-40s per request
  ```

### 5.2 计算瓶颈
- **Hindsight 本地嵌入**：NumPy 导入在旧 CPU 上会崩溃（line 77-90）
- **Holographic HRR 重建**：实体增长时 O(n²) 复杂度
  ```python
  # plugins/memory/holographic/store.py:548-553
  for row in rows:
      self._compute_hrr_vector(row["fact_id"], row["content"])  # 串行计算
      categories.add(row["category"])
  for category in categories:
      self._rebuild_bank(category)  # 每个类别全量重建
  ```

### 5.3 数据库瓶颈
- **Hindsight 实体解析**：每个实体触发一次查询（N+1 问题）
- **Holographic 信任分数更新**：需全表扫描 facts

---

## 6. 并行化改进建议

### 6.1 立即可行（Low-Hanging Fruit）
```python
# 1. 批量向量计算（Holographic）
def _batch_compute_hrr(fact_ids: List[int], contents: List[str]):
    vectors = np.array([hrr.encode(c) for c in contents])  # NumPy 向量化
    return vectors

# 2. 异步提交（OpenViking）
async def on_session_end_async(messages):
    tasks = [
        self._client.post_async("/commit"),
        self._mirror_to_backup(),  # 额外备份
    ]
    await asyncio.gather(*tasks)

# 3. 预加载流水线（Hindsight）
class PipelinedPrefetch:
    def __init__(self):
        self._queue = deque(maxlen=3)  # 保留最近 3 次查询
    
    def queue_prefetch(self, query):
        self._queue.append(threading.Thread(target=self._fetch, args=(query,)))
        self._queue[-1].start()  # 立即启动
```

### 6.2 架构级改进（需重构）
1. **分离提取与存储**：
   ```
   LLM 提取 ──┬──► PostgreSQL (结构化)
             ├──► Vector DB (语义检索)
             └──► Graph DB (关系查询)
   ```

2. **流式提取**：
   ```python
   async for extracted_fact in llm_stream_extract(messages):
       await db.upsert_fact(extracted_fact)  # 边提取边存储
   ```

3. **工具并行执行**（需 Agent 支持）：
   ```python
   # run_agent.py 中启用工具并行调用
   tasks = [handle_tool_call(tc) for tc in tool_calls]
   results = await asyncio.gather(*tasks)
   ```

---

## 7. 总结

### 当前实现的优势
- ✅ 模块化设计，易于扩展新提供者
- ✅ 失败隔离，一个提供者崩溃不影响其他
- ✅ 后台同步，不阻塞用户对话流
- ✅ 多种提取策略可选（自动/手动/混合）

### 核心限制
- ❌ **无跨提供者并行**：同时只能运行 1 个外部提供者
- ❌ **工具串行执行**：Agent 逐个调用记忆工具
- ❌ **服务端黑盒**：OpenViking/Hindsight 的提取细节不可见
- ❌ **压缩阻塞**：`on_pre_compress` 必须串行完成

### 性能瓶颈优先级
1. **Hindsight Cloud API 延迟**（30-40s）→ 使用本地模式或缓存
2. **OpenViking commit 等待**（最多 10s）→ 异步提交 + 超时容忍
3. **Holographic 实体重建**（O(n²)）→ 增量更新 + 批处理

### 最佳实践
- **CLI 模式**：选择 Holographic（低延迟，本地）
- **网关模式**：选择 Hindsight（知识图谱适合多用户）
- **高吞吐场景**：选择 OpenViking（服务端提取，客户端无阻塞）