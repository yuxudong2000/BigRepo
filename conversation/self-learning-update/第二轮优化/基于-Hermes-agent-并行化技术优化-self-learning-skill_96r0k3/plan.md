# 基于 Five-Why 的知识提炼深度优化方案

<!-- anchor:overview -->
## 一、问题诊断

### 1.1 当前知识提炼的根本问题

通过对刚才归档的知识进行 Five-Why 分析:

**表面问题**：提炼的知识过于具体,复用性低

**Five-Why 分析**:
```
Why 1: 为什么知识过于具体?
→ 停留在"做了什么"层面,未追问"为什么"

Why 2: 为什么未追问"为什么"?
→ 提炼流程中缺少根因分析步骤

Why 3: 为什么缺少根因分析?
→ knowledge-extractor 子 Agent 的提示词只要求提取"what",未要求"why"

Why 4: 为什么提示词设计不足?
→ 设计时参考 Hermes-agent 的并行模式,但未深入研究知识管理理论

Why 5: 为什么未研究理论?
→ 缺少"知识提炼深度"的评估标准和优化意识
```

**根本原因**: self-learning skill 的知识提炼机制缺少**抽象层级提升**和**根因追溯**的设计。

### 1.2 具体表现(基于刚才的归档)

| 文件 | 当前抽象层级 | 问题 | 应达到层级 |
|------|-------------|------|-----------|
| skill-optimization-path-selection.md | Layer 2(症状) | 只记录"要明确路径",未解释"为什么会路径混淆" | Layer 4(原则) |
| write-to-file.md | Layer 2(经验) | 只说"用绝对路径",未解释"隐式依赖的危害" | Layer 4(原则) |
| verification-deadlock-debugging.md | Layer 3(流程) | 提供排查步骤,但未分析"为什么会死循环" | Layer 4(原理) |
| parallel-skill-optimization-pattern.md | Layer 3(模式) | 较好,但缺少理论基础(阿姆达尔定律) | Layer 5(理论) |

### 1.3 知识层次理论视角

**DIKW 金字塔映射**:

当前状态:
```
Wisdom(智慧) —— 缺失
    ↑
Knowledge(知识) —— 部分(仅 Layer 3)
    ↑
Information(信息) —— 主要停留于此(Layer 1-2)
    ↑
Data(数据) —— 原始对话记录
```

目标状态:
```
Wisdom(智慧) —— Layer 5:通用原则("显式优于隐式")
    ↑
Knowledge(知识) —— Layer 4:领域洞察("上下文歧义消解")
    ↑
Information(信息) —— Layer 2-3:模式识别("路径混淆模式")
    ↑
Data(数据) —— Layer 1:具体案例("self-learning skill 路径问题")
```

---

<!-- anchor:design-principles -->
## 二、设计原则

### 2.1 核心设计原则(基于调研)

#### **原则 1: 抽象层级提升原则**

**来源**: DIKW 理论 + Nature 知识跨界研究

**核心洞察**:
> "知识层级(抽象级别)能够调节知识跨界的惩罚效应。当知识处于更高抽象层级时(>8),跨领域整合的阻力会显著降低。"

**实践要求**:
- 每个知识条目必须包含**至少两个层级**:
  - Layer 1-2: 具体案例(保留语境)
  - Layer 4-5: 通用原则(跨领域适用)
- 通过 **Five-Why 根因分析** 实现层级跃迁

#### **原则 2: 根因导向提炼原则**

**来源**: Five-Why 方法论

**核心洞察**:
> "好的知识不是记录'我们做了什么',而是揭示'为什么这样做有效,以及何时可以复用'。"

**实践要求**:
- 对每个问题执行 **Five-Why 分析**
- 识别症状 vs 根因:
  - ❌ 症状: "路径混淆" / "使用绝对路径"
  - ✅ 根因: "隐式上下文依赖" / "显式依赖原则"

#### **原则 3: 可复用性优先原则**

**来源**: Gang of Four 设计模式方法论

**核心洞察**:
> "模式必须在多个情境可应用(不是一次性方案),且能用简短名词短语(2-3词)精准表达。"

**实践要求**:
- **复现性验证**: 至少 3 个不同案例支撑
- **命名明确**: 使用名词短语(如"上下文歧义消解模式")
- **边界清晰**: 包含"何时适用" + "何时不适用"

#### **原则 4: 渐进式抽象原则**

**来源**: Progressive Summarization + Zettelkasten

**核心洞察**:
> "不要一次性强求抽象,允许笔记'从具体→模糊→重新抽象'。"

**实践要求**:
- 保留**多层级语境**(避免过度压缩)
- 允许知识条目**随时间演化**(可拆分/合并/重构)
- 定期审计(周/月/年)识别可抽象模式

---

<!-- anchor:solution-architecture -->
## 三、解决方案架构

### 3.1 整体架构升级

**从"单层提取"到"三层提炼"**:

```
┌─────────────────────────────────────────────────────┐
│          Layer 5: 通用原则库 (Principles)            │
│  - 跨领域适用                                        │
│  - 回答"Why"问题                                     │
│  - 例: "显式依赖原则"                                │
└──────────────────────┬──────────────────────────────┘
                       ↑ Five-Why 提炼
┌──────────────────────┴──────────────────────────────┐
│          Layer 4: 领域洞察库 (Insights)              │
│  - 领域内跨场景                                      │
│  - 回答"What causes"                                 │
│  - 例: "上下文歧义消解模式"                          │
└──────────────────────┬──────────────────────────────┘
                       ↑ 模式识别
┌──────────────────────┴──────────────────────────────┐
│          Layer 2-3: 模式库 (Patterns)                │
│  - 可复用流程                                        │
│  - 回答"How"问题                                     │
│  - 例: "多上下文操作确认模式"                        │
└──────────────────────┬──────────────────────────────┘
                       ↑ 案例提取
┌──────────────────────┴──────────────────────────────┐
│          Layer 1: 案例库 (Sessions + Solutions)      │
│  - 完整语境                                          │
│  - 回答"What happened"                               │
│  - 例: "self-learning skill 路径混淆事件"            │
└─────────────────────────────────────────────────────┘
```

### 3.2 知识提炼流程重构

**从 7 分类提取 → 3 阶段深化**:

#### **阶段 1: 案例提取(L1-L2)** — 现有流程保持

7 个分类并行提取:
- solutions / tools / patterns / insights / memories / rules / skills
- 输出: 具体解法、工具经验、执行流程

#### **阶段 2: 根因分析(L2→L4)** — **新增**

对 Step 1 提取的每个条目执行 Five-Why:
- 输入: 具体问题(如"路径混淆")
- 过程: 追问 5 次"为什么"
- 输出: 根本原因(如"隐式上下文依赖")

#### **阶段 3: 原则提炼(L4→L5)** — **新增**

跨案例模式识别:
- 输入: 多个根因分析结果
- 过程: 横向对比,识别共性
- 输出: 通用原则(如"显式依赖原则")

### 3.3 数据流与存储结构

```
Session 对话
    ↓
【阶段 1】并行案例提取(现有)
    ├→ knowledge/solutions/*.md
    ├→ knowledge/tools/*.md
    ├→ knowledge/patterns/*.md
    └→ knowledge/insights/*.md  (停留在 Layer 2-3)
    ↓
【阶段 2】串行根因分析(新增)
    ├→ 对每个 insight 执行 Five-Why
    └→ knowledge/root-causes/*.md  (Layer 4)
    ↓
【阶段 3】原则库提炼(新增)
    ├→ 跨 session 模式识别
    └→ knowledge/principles/*.md  (Layer 5)
```

**新增目录结构**:
```
knowledge/
├── sessions/          # 完整对话存档(Layer 1)
├── solutions/         # 具体解法(Layer 2)
├── tools/             # 工具经验(Layer 2)
├── patterns/          # 执行模式(Layer 3)
├── insights/          # 领域洞察(Layer 3-4)
├── root-causes/       # **新增**: 根因分析(Layer 4)
├── principles/        # **新增**: 通用原则库(Layer 5)
├── memories/          # 记忆候选
├── rules/             # 规则约束
├── skills/            # Skill 化候选
├── index.md           # 全库索引
└── log.md             # 时间线日志
```

---

<!-- anchor:implementation-plan -->
## 四、实施计划

### Phase 1: 创建 Five-Why 分析子 Agent(3 小时)

#### 任务 1.1: 定义 `root-cause-analyzer` 子 Agent

**文件**: `~/.codeflicker/agents/root-cause-analyzer.md`

**核心能力**:
1. 对输入的问题执行 Five-Why 分析
2. 识别症状 vs 根因
3. 输出结构化根因报告(JSON 格式)

**输入格式**:
```json
{
  "problem": "具体问题描述",
  "context": "问题发生的完整语境",
  "initial_symptoms": ["症状1", "症状2"]
}
```

**输出格式**:
```json
{
  "why_chain": [
    {"level": 1, "question": "为什么 X?", "answer": "因为 Y", "evidence": "..."},
    {"level": 2, "question": "为什么 Y?", "answer": "因为 Z", "evidence": "..."},
    ...
  ],
  "root_cause": "最终根本原因",
  "abstraction_level": 4,  // DIKW 层级
  "applicable_domains": ["文件操作", "API 调用", "配置管理"],
  "principle": "提炼的通用原则(如'显式依赖原则')"
}
```

#### 任务 1.2: 创建提示词模板

**文件**: `/Users/yuxudong/.codeflicker/skills/self-learning/references/root-cause-analysis-prompt.md`

**核心内容**:
- Five-Why 执行规范
- 症状 vs 根因识别标准
- DIKW 层级判断指南
- 输出格式要求

### Phase 2: 升级 knowledge-extractor(2 小时)

#### 任务 2.1: 增强 knowledge-extractor 的分析深度

**修改**: `~/.codeflicker/agents/knowledge-extractor.md`

**新增章节**:
```markdown
## Step 2.5: 深度分析(在提取后执行)

对每个提炼的条目,追问:
1. **为什么会发生这个问题?**(Why 1-3)
2. **这个问题的本质是什么?**(问题分类)
3. **什么通用原则可以预防这类问题?**(原则提炼)

输出格式:
```json
{
  "surface_issue": "具体问题",
  "why_chain": [...],
  "root_cause": "根本原因",
  "principle": "通用原则",
  "applicable_beyond": ["场景1", "场景2"]
}
```
```

### Phase 3: 修改 SKILL.md 主流程(3 小时)

#### 任务 3.1: 在 Step 3 后增加 Step 3.5(根因分析阶段)

**文件**: `/Users/yuxudong/.codeflicker/skills/self-learning/SKILL.md`

**新增内容** (插入在当前 Step 3 和 Step 4 之间):

```markdown
### Step 3.5: 根因分析与原则提炼 🔍 (v3.0 新增)

**执行模式**: 串行分析(需要深度推理)

#### 输入
从 Step 3 获取提炼的 insights 清单

#### 执行流程

**1. 对每个 insight 执行 Five-Why 分析**

使用 `root-cause-analyzer` 子 Agent:

```python
for insight in insights:
    analysis = use_subagent(
        subagent_name="root-cause-analyzer",
        task=f"""
        对以下问题执行 Five-Why 根因分析:
        
        问题: {insight.problem}
        语境: {insight.context}
        初步症状: {insight.symptoms}
        
        输出:
        1. Why 链条(至少 3 层,最多 5 层)
        2. 根本原因
        3. 通用原则
        4. 适用领域
        """
    )
    root_causes.append(analysis)
```

**2. 写入根因分析结果**

```
knowledge/root-causes/YYYY-MM-DD_<topic-slug>.md
```

**3. 跨 session 原则提炼(可选,每月执行)**

```python
# 扫描 root-causes/ 目录
all_root_causes = load_all_root_causes()

# 识别重复出现的原则
principles = identify_common_principles(all_root_causes)

# 写入原则库
for principle in principles:
    write_principle(
        filename=f"knowledge/principles/{principle.name}.md",
        content=principle.generate_markdown()
    )
```

#### 输出示例

**root-causes/2026-04-29_skill-optimization.md**:
```markdown
# 根因分析: Skill 优化路径混淆问题

## 问题描述
优化 self-learning skill 时,Agent 在错误路径(hermes-agent 仓库)验证文件。

## Five-Why 分析

### Why 1: 为什么在错误路径验证?
→ 验证逻辑使用相对路径,依赖当前 cwd

### Why 2: 为什么依赖 cwd?
→ 操作未显式指定目标上下文

### Why 3: 为什么未显式指定?
→ 用户指令"优化 skill"存在歧义(调研 vs 修改)

### Why 4: 为什么存在歧义?
→ 指令隐式依赖上下文假设(用户以为指自己的目录)

### Why 5: 为什么会有隐式假设?
→ 缺少"多上下文操作前必须消歧"的设计原则

## 根本原因
**隐式上下文依赖** — 操作结果依赖未显式声明的状态(cwd、环境变量等)

## 通用原则
**显式依赖原则(Explicit Dependency Principle)**:
> 操作结果应只依赖显式参数,不依赖隐式状态。

## 适用领域
- 文件系统操作(路径)
- API 调用(环境变量)
- 配置管理(默认值)
- 时间处理(时区)
- 编码处理(charset)

## 关联原则
- 最小惊讶原则
- 不变式约束
- 操作前确认原则
```

#### 性能影响
- 根因分析为串行(需要深度推理)
- 预计每个 insight 分析耗时: 3-5s
- 总增加耗时: 3-5 个 insights × 4s ≈ **15s**
- 可接受(收益 >> 成本)
```

#### 任务 3.2: 更新 frontmatter 和版本号

```yaml
version: 3.0.0
deep_analysis: true  # 启用根因分析
```

### Phase 4: 创建原则库模板(2 小时)

#### 任务 4.1: 定义原则库文件格式

**模板文件**: `/Users/yuxudong/.codeflicker/skills/self-learning/references/principle-template.md`

```markdown
# [原则名称]

> **定义**: 一句话核心定义

---

## 根本问题

描述这个原则解决的根本问题(非表面症状)

## 为什么会发生

### 理论基础
- 引用相关理论(如 DIKW、设计模式、系统动力学)

### 历史案例
- 案例 1: [标题](链接)
- 案例 2: [标题](链接)
- 案例 3: [标题](链接)

## 原则内容

### 核心主张
1. 子原则 1
2. 子原则 2
3. 子原则 3

### 实践检查清单
- [ ] 检查项 1
- [ ] 检查项 2

### 反模式(何时违反)
- ❌ 反模式 1
- ❌ 反模式 2

## 适用边界

### 适用场景
- ✅ 场景 1
- ✅ 场景 2

### 不适用场景
- ❌ 场景 1(理由)
- ❌ 场景 2(理由)

## 相关原则
- [原则 A](链接) — 关系说明
- [原则 B](链接) — 关系说明

## 参考资料
- [文献 1](链接)
- [文献 2](链接)

---

**抽象层级**: Layer 5(通用原则)  
**首次提出**: YYYY-MM-DD from [session](链接)  
**验证案例数**: N  
**最后更新**: YYYY-MM-DD
```

#### 任务 4.2: 创建第一个原则库文件

**文件**: `knowledge/principles/explicit-dependency-principle.md`

**内容**: 基于刚才提炼的"显式依赖原则",按模板填写

### Phase 5: 测试与验证(2 小时)

#### 任务 5.1: 回溯测试

对刚才归档的 4 个文件执行:
1. 读取原始 insight
2. 调用 `root-cause-analyzer` 执行 Five-Why
3. 生成根因分析报告
4. 验证输出质量

#### 任务 5.2: 端到端测试

选择一个新的中型对话(30-50 轮):
1. 执行完整 self-learning skill v3.0 流程
2. 检查生成的根因分析文件
3. 验证原则库是否有更新
4. 评估知识深度提升效果

#### 任务 5.3: 质量评估

使用以下标准评估提炼的知识:
```markdown
- [ ] **场景独立性**: 不看原始对话能否理解?
- [ ] **指导价值**: 遇到类似问题能否帮我少走弯路?
- [ ] **泛化适用**: 能否用于其他项目/领域?
- [ ] **原理深度**: 解释了"为什么",还是只说了"怎么做"?
- [ ] **可验证性**: 有具体案例支撑?
- [ ] **边界清晰**: 明确何时适用、何时不适用?
```

---

<!-- anchor:success-criteria -->
## 五、成功标准

### 5.1 定量指标

| 指标 | 当前(v2.0) | 目标(v3.0) |
|------|-----------|-----------|
| **抽象层级** | Layer 2-3 | Layer 4-5 |
| **可复用性评分** | 3/10 | 8/10 |
| **根因覆盖率** | 0%(无根因分析) | 80%(主要 insights 有根因) |
| **原则库条目数** | 0 | 初期 5-10 条 |
| **跨领域适用性** | 低(仅 skill 优化场景) | 高(文件/API/配置等) |

### 5.2 定性标准

**知识条目质量要求**:

#### ✅ 合格标准
- 包含"为什么会发生"章节
- 提炼出通用原则(非具体操作)
- 标注适用边界
- 至少 3 个案例支撑

#### 🌟 优秀标准
- 链接到理论基础(DIKW、设计模式、系统理论)
- 跨领域验证(至少 2 个不同领域)
- 包含反模式警示
- 有量化评估(如并行加速比)

### 5.3 用户体验指标

- **查找效率**: 30 秒内定位相关原则 (>90%)
- **理解成本**: 重读时无需额外查询 (>80%)
- **复用成功率**: 原则能在新情境直接应用 (>60%)

---

<!-- anchor:risks-and-mitigation -->
## 六、风险与缓解

### 风险 1: 根因分析耗时过长

**风险描述**: Step 3.5 串行执行,可能显著增加总耗时

**缓解措施**:
1. **并行优化**: 根因分析可并行(多个 insights 独立分析)
2. **条件触发**: 仅对"重要 insights"执行根因分析(通过重要性评分筛选)
3. **异步执行**: 根因分析可异步执行,不阻塞归档完成

### 风险 2: 过度抽象导致丢失语境

**风险描述**: 追求高层级原则,可能丢失具体案例的语境

**缓解措施**:
1. **多层级存储**: 保留 Layer 1-5 所有层级
2. **双向链接**: 原则链接到支撑案例,案例链接到原则
3. **渐进式抽象**: 允许知识条目随时间演化

### 风险 3: 原则库膨胀难以维护

**风险描述**: 原则数量过多,难以查找和维护

**缓解措施**:
1. **定期审计**: 每季度审查原则库,合并相似原则
2. **使用频率跟踪**: 记录每个原则的引用次数,淘汰低频原则
3. **MOC 索引**: 创建 Map of Content 组织原则(按领域/主题)

### 风险 4: Five-Why 分析质量不稳定

**风险描述**: AI 执行 Five-Why 可能停在表面或过度深入

**缓解措施**:
1. **质量检查**: 根因分析后增加验证步骤(检查是否触及系统性问题)
2. **人工审查**: 每周回顾根因分析结果,标注优秀/待改进案例
3. **提示词迭代**: 基于质量反馈持续优化 root-cause-analyzer 的提示词

---

<!-- anchor:expected-outcomes -->
## 七、预期成果

### 7.1 知识库质量提升

**从"经验日记"到"可复用原则库"**:

**改进前**:
```
knowledge/insights/skill-optimization-path-selection.md
内容: "优化 skill 前要明确是调研还是实际修改"
层级: Layer 2(经验总结)
复用性: 仅限 skill 优化场景
```

**改进后**:
```
knowledge/root-causes/2026-04-29_skill-optimization.md
内容: "隐式上下文依赖导致操作目标歧义"
层级: Layer 4(根因)

↓ 提炼

knowledge/principles/explicit-dependency-principle.md
内容: "显式依赖原则 — 操作结果应只依赖显式参数"
层级: Layer 5(通用原则)
复用性: 文件/API/配置/时间/编码等所有隐式依赖场景
```

### 7.2 跨领域知识迁移能力

**示例**: 基于"显式依赖原则",未来遇到以下问题可直接应用:

| 问题 | 表面症状 | 根因 | 原则应用 |
|------|---------|------|---------|
| API 调用环境依赖 | 本地通过测试失败 | 依赖 `$ENV` 变量 | 显式传参而非读环境变量 |
| 时间处理 Bug | 不同时区结果不同 | 依赖系统时区 | 显式传入时区参数 |
| 编码错误 | Windows 下乱码 | 依赖默认编码 | 显式指定 charset |

### 7.3 知识库结构优化

**新增 MOC(Map of Content)**:

```
knowledge/maps/
├── context-management.md       # 上下文管理主题
│   ├→ principles/explicit-dependency-principle.md
│   ├→ patterns/multi-context-disambiguation.md
│   └→ root-causes/2026-04-29_skill-optimization.md
├── performance-optimization.md  # 性能优化主题
│   ├→ principles/amdahls-law.md
│   ├→ patterns/parallel-skill-optimization.md
│   └→ insights/...
└── system-debugging.md          # 系统调试主题
```

---

## 八、后续演进方向

### 8.1 短期(1-3 个月)

1. **建立原则库基础**: 积累 10-15 条通用原则
2. **跨 session 模式识别**: 每月执行一次原则提炼
3. **质量评估机制**: 建立原则库评分体系

### 8.2 中期(3-6 个月)

1. **自动化原则发现**: AI 自动识别重复模式
2. **关联网络构建**: 原则之间的依赖/冲突关系
3. **领域知识图谱**: 按技术领域组织原则库

### 8.3 长期(6-12 个月)

1. **知识迁移引擎**: 给定新问题,自动推荐适用原则
2. **原则验证系统**: 跟踪原则的实际应用效果
3. **社区知识共享**: 将原则库开源,形成通用知识库

---

## 九、参考文献

### 理论基础
1. **Five-Why 方法论**: Taiichi Ohno (1988) — Toyota Production System
2. **DIKW 金字塔**: Russell Ackoff (1989) — Knowledge Hierarchy
3. **抽象梯度**: Hayakawa — Ladder of Abstraction
4. **设计模式**: Gang of Four (1994) — Design Patterns

### 实践指南
1. **Progressive Summarization**: Tiago Forte — 渐进式总结法
2. **Zettelkasten**: Niklas Luhmann — 卡片盒笔记法
3. **PARA**: Tiago Forte — Projects-Areas-Resources-Archives

### 学术研究
1. **Nature**: Knowledge hierarchy and cross-domain integration (2023)
2. **BMJ Quality & Safety**: Alan J. Card — Five-Why 批判性分析 (2017)

---

**方案版本**: v1.0  
**创建时间**: 2026-04-29  
**预计实施周期**: 12 小时  
**优先级**: P0(高优先级重构)