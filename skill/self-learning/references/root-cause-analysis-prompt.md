# Five-Why 根因分析提示词模板

> 本文档用于指导 `root-cause-analyzer` 子 Agent 执行高质量根因分析

---

## 一、Five-Why 执行规范

### 1.1 核心原则

**目标**: 从表面症状挖掘到可操作的系统性根因

**关键规则**:
1. ✅ **基于事实,非猜测**: 每个答案必须有可验证证据
2. ✅ **追问到系统性问题**: 不停在"人为错误"
3. ✅ **保持因果链完整**: 每个Why针对上一个答案
4. ✅ **识别流程缺陷**: 指向可改进的机制

### 1.2 追问模板

```
Why {N}: 为什么 {上一层的答案}?
→ {基于证据的回答}
→ 证据: {具体证据来源}
```

### 1.3 何时停止追问

**停止信号**:
- ✅ 触及可操作的系统性改进点
- ✅ 继续追问开始循环/同义反复
- ✅ 超出组织控制范围
- ✅ 无法获得更深洞察

**不应停止的情况**:
- ❌ 仅因为到了第5次就停止
- ❌ 停在"人为疏忽"/"技能不足"等表面原因
- ❌ 未触及流程/机制层面

---

## 二、症状 vs 根因识别标准

### 2.1 判断标准表

| 维度 | 症状(Symptom) | 根因(Root Cause) |
|------|--------------|-----------------|
| **定义** | 问题的表现形式 | 问题的深层来源 |
| **解决效果** | 暂时缓解 | 永久消除 |
| **可操作性** | 修补性措施("用绝对路径") | 系统性改进("建立显式依赖检查") |
| **指向** | 具体事件("这次路径混淆") | 流程缺陷("缺少上下文消歧机制") |
| **层级** | Layer 1-2(数据/信息) | Layer 4-5(知识/智慧) |

### 2.2 根因的三个必要标志

#### ✅ 标志 1: 消除它能防止问题再次发生

**示例对比**:
```
❌ 症状级方案: "修复这个Bug"
   → 下次可能出现类似Bug

✅ 根因级方案: "建立自动化回归测试"
   → 系统性预防该类Bug
```

#### ✅ 标志 2: 指向流程或系统性问题

**示例对比**:
```
❌ 症状: "开发者技能不足"
   → 指责个人,无可操作改进点

✅ 根因: "入职培训流程缺少实战演练,新员工无导师制"
   → 指向可改进的流程
```

#### ✅ 标志 3: 继续提问无法获得更深洞察

**示例**:
```
Why 5: 为什么缺少消歧机制?
→ 工具设计时未考虑多上下文场景

Why 6: 为什么设计时未考虑?
→ 需求分析阶段未识别该场景
   (继续追问开始重复,已触及根因)
```

---

## 三、DIKW 层级判断指南

### 3.1 DIKW 金字塔映射

```
Layer 5: Wisdom(智慧)
    ↑ 通用原则(跨领域适用)
    ↑ 例: "显式依赖原则"
    ↑
Layer 4: Knowledge(知识)
    ↑ 领域洞察(领域内跨场景)
    ↑ 例: "隐式上下文依赖问题"
    ↑
Layer 3: Information(信息)
    ↑ 模式识别(可复用流程)
    ↑ 例: "多上下文操作前确认模式"
    ↑
Layer 2: Information(信息)
    ↑ 经验总结(具体经验)
    ↑ 例: "使用绝对路径"
    ↑
Layer 1: Data(数据)
    ↑ 原始事实
    ↑ 例: "文件路径验证失败"
```

### 3.2 层级判断清单

#### Layer 1: 数据(原始事实)
- [ ] 具体事件记录
- [ ] 日志/监控数据
- [ ] 测试结果

#### Layer 2: 信息(经验总结)
- [ ] "应该这样做"
- [ ] 单一场景的解法
- [ ] 具体操作步骤

#### Layer 3: 信息(模式识别)
- [ ] "这类问题这样做"
- [ ] 可复用流程/检查清单
- [ ] 跨多个案例的模式

#### Layer 4: 知识(领域洞察)
- [ ] "为什么会发生"
- [ ] 领域内跨场景适用
- [ ] 揭示问题本质

#### Layer 5: 智慧(通用原则)
- [ ] "根本性原则"
- [ ] 跨领域适用
- [ ] 2-4词精炼命名
- [ ] 可指导架构设计

### 3.3 抽象层级提升方法

**从具体到抽象的提炼路径**:

```
具体案例(Layer 1)
    ↓ "这个问题是什么?"
具体解法(Layer 2)
    ↓ "这类问题有什么共性?"
可复用模式(Layer 3)
    ↓ "为什么会发生这类问题?"
领域洞察(Layer 4)
    ↓ "背后的通用原则是什么?"
通用原则(Layer 5)
```

**示例**:
```
Layer 1: "self-learning skill路径验证失败"
    ↓
Layer 2: "使用绝对路径"
    ↓
Layer 3: "多上下文操作前确认目标路径"
    ↓
Layer 4: "隐式上下文依赖导致行为不确定"
    ↓
Layer 5: "显式依赖原则 — 操作结果只依赖显式参数"
```

---

## 四、输出格式要求

### 4.1 标准 JSON Schema

```json
{
  "type": "object",
  "required": ["why_chain", "root_cause", "abstraction_level", "principle", "applicable_domains", "preventive_measures"],
  "properties": {
    "why_chain": {
      "type": "array",
      "minItems": 3,
      "maxItems": 7,
      "items": {
        "type": "object",
        "required": ["level", "question", "answer", "evidence"],
        "properties": {
          "level": {"type": "integer", "minimum": 1, "maximum": 7},
          "question": {"type": "string", "minLength": 5},
          "answer": {"type": "string", "minLength": 10},
          "evidence": {"type": "string", "minLength": 10}
        }
      }
    },
    "root_cause": {
      "type": "string",
      "minLength": 20,
      "description": "根本原因陈述,必须指向系统性问题"
    },
    "abstraction_level": {
      "type": "integer",
      "minimum": 3,
      "maximum": 5,
      "description": "DIKW层级,根因分析应达到Layer 4-5"
    },
    "principle": {
      "type": "object",
      "required": ["name", "statement"],
      "properties": {
        "name": {
          "type": "string",
          "minLength": 4,
          "maxLength": 20,
          "description": "原则名称(中文),2-4词,如'显式依赖原则'"
        },
        "statement": {
          "type": "string",
          "minLength": 15,
          "description": "原则陈述,一句话核心定义"
        },
        "english_name": {
          "type": "string",
          "description": "原则名称(英文),可选"
        }
      }
    },
    "applicable_domains": {
      "type": "array",
      "minItems": 3,
      "items": {
        "type": "string",
        "minLength": 5
      },
      "description": "适用领域列表,至少3个不同场景"
    },
    "preventive_measures": {
      "type": "array",
      "minItems": 3,
      "items": {
        "type": "string",
        "minLength": 10
      },
      "description": "预防性措施列表,可操作的改进建议"
    }
  }
}
```

### 4.2 字段填写指南

#### `why_chain` (Why链条)

**要求**:
- 至少3层,最多7层
- 每层包含: level(层级), question(提问), answer(回答), evidence(证据)
- 保持因果链完整(每个Why针对上一个答案)

**示例**:
```json
{
  "level": 1,
  "question": "为什么在错误路径验证?",
  "answer": "验证逻辑使用相对路径,依赖当前cwd",
  "evidence": "当前cwd=/Users/xxx/hermes-agent, 验证路径=./skills/xxx.md"
}
```

#### `root_cause` (根本原因)

**要求**:
- 至少20字符
- 必须指向系统性问题(流程/机制缺陷)
- 不能是"人为错误"/"技能不足"

**优秀示例**:
```
✅ "隐式上下文依赖 — 操作结果依赖未显式声明的状态(cwd、环境变量等),导致行为不确定"
✅ "缺少系统化的性能工程培训体系和自动化护栏,新成员无法识别性能隐患"
```

**不良示例**:
```
❌ "开发者疏忽" (指责个人)
❌ "路径写错了" (停在表面症状)
```

#### `abstraction_level` (抽象层级)

**要求**:
- 取值范围: 3-5
- 根因分析应达到 Layer 4-5

**层级对照**:
- 3: 模式识别(可复用流程)
- 4: 领域洞察(揭示本质)
- 5: 通用原则(跨领域适用)

#### `principle` (通用原则)

**要求**:
- `name`: 2-4词的名词短语,如"显式依赖原则"
- `statement`: 一句话核心定义
- `english_name`: 可选,英文名称

**示例**:
```json
{
  "name": "显式依赖原则",
  "statement": "操作结果应只依赖显式参数,不依赖隐式状态",
  "english_name": "Explicit Dependency Principle"
}
```

#### `applicable_domains` (适用领域)

**要求**:
- 至少3个不同场景
- 跨领域验证(不同技术栈/业务场景)

**示例**:
```json
[
  "文件系统操作(路径解析)",
  "API调用(环境变量依赖)",
  "配置管理(默认值假设)",
  "时间处理(时区依赖)",
  "编码处理(charset依赖)"
]
```

#### `preventive_measures` (预防性措施)

**要求**:
- 至少3条
- 可操作的具体改进建议
- 对应不同层面(技术/流程/文化)

**示例**:
```json
[
  "技术层面: 使用绝对路径而非相对路径",
  "流程层面: 操作前增加上下文确认步骤",
  "机制层面: 工具设计要求显式传递所有依赖",
  "文化层面: 建立'显式优于隐式'的团队共识"
]
```

---

## 五、质量检查清单

### 执行前检查

- [ ] 理解了问题和完整语境
- [ ] 识别了所有初步症状
- [ ] 准备了追问的起点

### 执行中检查

- [ ] 每个Why都针对上一个答案提问
- [ ] 每个答案都有可验证证据
- [ ] 未停在"人为错误"
- [ ] 追问到系统性问题

### 输出质量检查

#### ✅ 必须满足(合格标准)

- [ ] Why链至少3层
- [ ] 每层有清晰证据
- [ ] 根因指向流程/机制缺陷
- [ ] 原则命名清晰(2-4词)
- [ ] 至少3个适用领域

#### 🌟 优秀标准

- [ ] Why链5层以上
- [ ] 根因触及组织/架构层面
- [ ] 原则可跨领域(不限于单一技术栈)
- [ ] 适用领域覆盖5+场景
- [ ] 预防措施涵盖技术/流程/文化多层面

---

## 六、实战案例模板

### 案例结构

```markdown
### 案例 N: {问题标题}

**输入**:
```
问题: {具体问题描述}
语境: {完整上下文}
症状: [{症状列表}]
```

**分析过程**:
{分析思路说明}

**输出**:
```json
{...完整JSON输出...}
```

**关键洞察**:
- {洞察1}
- {洞察2}
```

---

## 七、常见错误与纠正

### 错误 1: 过早停止

**错误示例**:
```
Why 1: 为什么文件不存在?
→ 路径写错了
[停止] ❌
```

**纠正**:
```
Why 1: 为什么文件不存在?
→ 路径写错了
Why 2: 为什么路径会写错?
→ 使用了相对路径,依赖cwd
Why 3: 为什么使用相对路径?
→ 操作未显式指定目标上下文
[继续深挖]
```

### 错误 2: 指责个人

**错误示例**:
```
Why 3: 为什么代码有Bug?
→ 开发者不够仔细 ❌
```

**纠正**:
```
Why 3: 为什么代码有Bug?
→ 代码审查流程未捕获该类错误
Why 4: 为什么审查流程未捕获?
→ Checklist缺少该项检查
Why 5: 为什么Checklist缺少?
→ 流程更新时未同步维护Checklist
```

### 错误 3: 缺少证据

**错误示例**:
```
Why 2: 为什么性能差?
→ 我觉得是因为数据库慢 ❌
```

**纠正**:
```
Why 2: 为什么性能差?
→ 数据库查询耗时4.8s
→ 证据: 慢查询日志显示SELECT语句执行时间4815ms
```

### 错误 4: 原则过于具体

**错误示例**:
```json
{
  "principle": {
    "name": "self-learning skill必须使用绝对路径",
    "statement": "在优化skill时要用绝对路径"
  }
}
❌ 过于具体,仅适用于单一场景
```

**纠正**:
```json
{
  "principle": {
    "name": "显式依赖原则",
    "statement": "操作结果应只依赖显式参数,不依赖隐式状态"
  }
}
✅ 通用原则,跨领域适用
```

---

## 八、参考资料

### 理论基础

1. **Five-Why 方法论**
   - Sakichi Toyoda (1930s) — 发明者
   - Taiichi Ohno (1988) — Toyota Production System
   - Alan J. Card (2017) — Five-Why批判性分析(BMJ Quality & Safety)

2. **DIKW 金字塔**
   - Russell Ackoff (1989) — From Data to Wisdom
   - Jennifer Rowley (2007) — The wisdom hierarchy

3. **抽象梯度**
   - Alfred Korzybski (1933) — Science and Sanity
   - S.I. Hayakawa (1939) — Ladder of Abstraction

### 最佳实践

1. **系统思考**
   - Peter Senge (1990) — The Fifth Discipline
   - Donella Meadows (2008) — Thinking in Systems

2. **事故分析**
   - Nancy Leveson (2011) — STAMP/CAST方法
   - Sidney Dekker (2006) — The Field Guide to Understanding Human Error

---

## 版本历史

- **v1.0.0** (2026-04-29): 初始版本,配合self-learning skill v3.0
