---
name: skill-creator
description: Use when creating a new skill from scratch, editing existing skills, or converting proven workflows into reusable skills
version: 1.0.0
requires:
  - writing-skills
---

# Skill Creator

> 将实践经验结晶成可复用的 Skill

---

## 🎯 技能定位

本技能帮助你创建高质量的 Skill，遵循 TDD 方法论和最佳实践。

**核心理念**：
```
Skill = 认知压缩 + 知识结晶 + 执行引擎
```

---

## 🚦 触发场景

**必须使用本 Skill 的情况**：
- ✅ 用户说"创建一个 skill"、"帮我写个 skill"
- ✅ 用户说"这个流程可以做成 skill"
- ✅ 发现某个工作流被重复使用 ≥3 次
- ✅ 需要编辑或优化现有 skill
- ✅ 需要将对话中的经验沉淀为 skill

**不适用的场景**：
- ❌ 一次性的解决方案
- ❌ 项目特定的配置（应该放在 CLAUDE.md）
- ❌ 简单的命令执行（可以自动化的不需要 skill）

---

## 📋 创建前的十问清单

在开始创建 Skill 前，必须回答这 10 个问题：

```markdown
## Skill 需求分析

### 1. 问题领域
- [ ] 这个 Skill 要解决什么具体问题？
- [ ] 目标用户是谁？（AI Agent / 人类用户 / 两者）
- [ ] 现有方案的痛点是什么？

### 2. 功能边界
- [ ] Skill 要做什么？（3-5 条核心功能）
- [ ] Skill **不做**什么？（明确边界）
- [ ] 与现有 Skill 的区别是什么？

### 3. 触发机制
- [ ] 用户什么时候需要这个 Skill？（场景）
- [ ] 用户会用什么话触发？（触发词列表）
- [ ] 如何避免误触发？（反例场景）

### 4. 输入输出
- [ ] 输入：Skill 需要什么信息？（参数/上下文）
- [ ] 输出：Skill 产出什么？（文件/分析/建议）
- [ ] 副作用：Skill 会修改什么？（状态变化）

### 5. 依赖关系
- [ ] 依赖其他 Skill 吗？（requires 字段）
- [ ] 依赖外部工具吗？（Python/Node.js/etc.）
- [ ] 需要特定配置吗？（环境变量/配置文件）

### 6. 质量标准
- [ ] 成功的标准是什么？（如何判断完成）
- [ ] 性能要求是什么？（响应时间/资源消耗）
- [ ] 错误处理策略？（失败后如何恢复）

### 7. 版本规划
- [ ] v1.0.0 包含哪些功能？（MVP）
- [ ] 哪些功能留到后续版本？（Roadmap）
- [ ] 有废弃替代的计划吗？（退出策略）

### 8. 测试策略
- [ ] 如何测试这个 Skill？（测试用例）
- [ ] 需要什么测试数据？（Mock/真实数据）
- [ ] 如何验证质量？（验收标准）

### 9. 文档计划
- [ ] 需要哪些支持文档？（references/）
- [ ] 需要示例吗？（examples/）
- [ ] 需要脚本工具吗？（scripts/）

### 10. 发布计划
- [ ] 发布到哪里？（个人/项目/系统）
- [ ] 目标用户是谁？（自己/团队/公开）
- [ ] 如何收集反馈？（Issue/邮件/聊天）
```

---

## 🔄 TDD 创建流程

### Phase 0: 准备阶段

**强制规则**：
> ⚠️ **必须先加载 `writing-skills` skill**
> 
> 本 skill 依赖 `writing-skills` 的 TDD 方法论。
> 如果尚未加载，现在停止并先加载它。

### Phase 1: RED — 观察失败行为

**目标**：不写 skill，先观察 AI 在没有指引时会犯什么错误

```dot
digraph red_phase {
    rankdir=LR;
    node [shape=box];
    
    Start [label="识别需要\nSkill的场景" shape=ellipse];
    Scenario [label="设计压力\n测试场景"];
    Baseline [label="运行基线测试\n(不加载Skill)"];
    Document [label="记录AI的\n错误行为"];
    Analyze [label="分析根本原因"];
    
    Start -> Scenario;
    Scenario -> Baseline;
    Baseline -> Document;
    Document -> Analyze;
}
```

**具体步骤**：

1. **设计压力场景**：
   ```markdown
   场景描述：
   - 触发条件：[用户说什么/做什么]
   - 预期行为：[AI 应该做什么]
   - 常见错误：[AI 可能犯什么错]
   ```

2. **运行基线测试**：
   ```
   use_subagent(
       subagent_name="test-baseline",
       task="""
       [压力场景描述]
       
       约束：
       - 不要加载任何 skill
       - 按照你的直觉处理
       - 记录你的思考过程
       """,
       background=false
   )
   ```

3. **记录错误行为**：
   ```markdown
   ## 基线测试结果
   
   ### AI 的实际行为
   [记录 AI 做了什么]
   
   ### 错误类型
   - [ ] 跳过关键步骤
   - [ ] 顺序错误
   - [ ] 遗漏验证
   - [ ] 其他：[具体描述]
   
   ### AI 的合理化说辞
   [记录 AI 如何为错误辩护]
   ```

### Phase 2: GREEN — 编写 Skill

**目标**：编写最小化的 skill，让 AI 通过测试

**Skill 结构模板**：

```markdown
---
name: skill-name
description: Use when [具体触发条件，不要总结工作流]
version: 1.0.0
requires:
  - dependency-skill  # 可选
---

# Skill Name

> 一句话说明核心理念

---

## 🎯 技能定位

[一段话说明这个 Skill 是什么，解决什么问题]

---

## 🚦 触发场景

**必须使用的情况**：
- ✅ [场景1]
- ✅ [场景2]

**不适用的场景**：
- ❌ [反例1]
- ❌ [反例2]

---

## 📋 核心流程

### Step 1: [步骤名称]

[具体说明]

**检查清单**：
- [ ] [检查项1]
- [ ] [检查项2]

### Step 2: [步骤名称]

[具体说明]

---

## ⚠️ P0 强制规则

> 🚨 **STOP - 以下规则不可绕过**

- ❌ **禁止**：[明确禁止的行为]
- ✅ **必须**：[强制执行的行为]

---

## 🔍 常见错误

### 错误1：[错误描述]

**症状**：[如何识别]
**原因**：[为什么会发生]
**修复**：[如何避免]

---

## 📚 参考资料

[可选：链接到支持文件]

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | YYYY-MM-DD | 初始版本 |
```

**编写技巧**：

1. **Description 字段**（最重要！）：
   ```yaml
   # ❌ 错误：总结了工作流
   description: Use when creating skills - write test first, then skill, then verify
   
   # ✅ 正确：只描述触发条件
   description: Use when creating new skills, editing existing skills, or converting proven workflows
   ```

2. **使用强制标记**：
   ```markdown
   > 🚨 **STOP - 必须先做X**
   > ❌ **禁止**：跳过Y步骤
   > ✅ **必须**：先执行Z
   ```

3. **提供检查清单**：
   - AI 特别容易跟随清单
   - 每个关键步骤都配清单
   - 用 `- [ ]` 格式

4. **预见常见错误**：
   - 基于基线测试的观察
   - 提供具体的"症状-诊断-修复"

### Phase 3: GREEN — 验证通过

**测试 Skill 是否有效**：

```
use_subagent(
    subagent_name="test-with-skill",
    task="""
    [相同的压力场景]
    
    要求：
    - 加载 skill: [skill-name]
    - 严格遵循 skill 指引
    - 记录是否能正确执行
    """,
    background=false
)
```

**验证标准**：
- ✅ AI 不再犯基线测试中的错误
- ✅ AI 按照 skill 的步骤执行
- ✅ AI 的输出符合预期

### Phase 4: REFACTOR — 查漏补缺

**目标**：发现 AI 绕过 skill 的新方法

**迭代流程**：

```
循环 3-5 次：
  1. 设计新的压力场景（更刁钻）
  2. 运行测试
  3. 发现新的合理化说辞
  4. 更新 skill 堵住漏洞
  5. 验证不破坏之前的测试
```

**常见漏洞类型**：

| 漏洞 | 症状 | 修复 |
|------|------|------|
| **模糊词汇** | "可能"、"建议"、"通常" | 改为"必须"、"禁止" |
| **例外条款** | "除非特殊情况" | 删除例外，或明确定义 |
| **顺序不明** | AI 跳过步骤 | 添加"先...再..."、编号 |
| **缺少验证** | AI 不检查结果 | 添加检查清单 |

---

## 🎯 四种 Skill 类型

### 1.0 工具型 Skill（简单）

**特征**：
- 单一功能
- < 200 行
- 解决单点问题

**示例**：karpathy-guidelines

**适用场景**：
- 个人使用
- 简单规则
- 快速参考

### 2.0 框架型 Skill（中等）

**特征**：
- 多步骤流程
- 200-400 行
- 结构化分析

**示例**：product-thinking, brainstorming

**适用场景**：
- 团队共享
- 标准流程
- 复杂任务

### 3.0 工业化 Skill（复杂）

**特征**：
- 质量保障
- > 400 行
- 自适应优化

**示例**：meta-execution, session-learning

**适用场景**：
- 生产环境
- 高质量要求
- 持续优化

### 4.0 自进化 Skill（未来）

**特征**：
- 自动优化
- 智能触发
- 自我修复

**示例**：evo-* 系列

---

## 📦 文件组织

### 简单 Skill
```
skill-name/
  SKILL.md              # 一个文件搞定
```

### 带工具的 Skill
```
skill-name/
  SKILL.md              # 主文档
  scripts/
    helper.py           # 辅助脚本
  examples/
    example.ts          # 示例代码
```

### 复杂 Skill
```
skill-name/
  SKILL.md              # 主文档
  references/
    api-reference.md    # API 文档
    patterns.md         # 设计模式
  scripts/
    tool1.py
    tool2.sh
  templates/
    template.md         # 模板文件
  examples/
    example1.ts
    example2.py
```

---

## 🚨 铁律：先测试，后编写

```
❌ 没有失败测试就编写 Skill = 删除重来
❌ 编写 Skill 后再补测试 = 删除重来
❌ "这次例外" = 不存在的
```

**为什么这么严格？**

1. **没看到失败，不知道教什么**：你以为 AI 会犯的错，可能不是真实的错
2. **没有基线，无法度量改进**：怎么知道 skill 有用？
3. **跳过测试的 skill 质量差**：100% 相关性

---

## 🎨 10 大设计模式

从已有 skill 中提炼的可复用模式：

### 1. 门禁模式
```markdown
> 🚨 **STOP - 必须先加载 X skill**
```
**用途**：强制依赖和前置条件

### 2. 检查清单模式
```markdown
- [ ] 检查项1
- [ ] 检查项2
```
**用途**：标准化验证流程

### 3. 渐进式披露模式
```markdown
## 快速开始（必读）
...

## 高级用法（按需）
...
```
**用途**：降低学习曲线

### 4. 自适应激活模式
```markdown
评分标准（C1-C7）：
- C1: [条件1]
- C2: [条件2]

触发规则：
命中 ≥ 2 项 → 完整激活
命中 1 项   → 轻量模式
```
**用途**：智能触发，避免过度设计

### 5. 错误重试协议
```markdown
第1次失败: 诊断 & 修复
第2次失败: 换方法
第3次失败: 升级给用户
```
**用途**：容错处理

### 6. 四问框架模式
```markdown
问题1: [从外到内]
问题2: [递进分析]
问题3: [深入本质]
问题4: [输出决策]
```
**用途**：结构化分析

### 7. 反模式文档模式
```markdown
### ❌ 错误1
**症状**：
**诊断**：
**修复**：
```
**用途**：知识沉淀，预防错误

### 8. 并行执行模式
```markdown
tasks = []
for item in items:
    task = use_subagent(item)
    tasks.append(task)
```
**用途**：性能优化（5x+ 加速）

### 9. 检查点模式
```markdown
每2步操作后：
- 记录当前状态
- 验证中间结果
- 确认可继续
```
**用途**：长流程的状态保存

### 10. 依赖声明模式
```yaml
requires:
  - dependency-skill-1
  - dependency-skill-2
```
**用途**：Skill 组合和复用

---

## 🎯 质量评估标准

### P0 级别（必须满足）

- [ ] 有失败的基线测试
- [ ] 有通过的 green 测试
- [ ] Description 只描述触发条件（不总结工作流）
- [ ] 有明确的"触发场景"和"不适用场景"
- [ ] 有强制规则（STOP/禁止/必须）
- [ ] 有检查清单
- [ ] 有常见错误说明

### P1 级别（推荐）

- [ ] 有完整的 10 问清单回答
- [ ] 有代码示例
- [ ] 有版本历史
- [ ] 有依赖声明
- [ ] 有性能优化考虑

### P2 级别（可选）

- [ ] 有支持文档
- [ ] 有辅助脚本
- [ ] 有多语言示例
- [ ] 有迁移指南

---

## 📚 参考资料

### 必读文档（在 knowledge/skill/ 目录下）
- `01-skill-design-principles.md` — 8条黄金法则
- `02-skill-patterns-cookbook.md` — 10个设计模式详解
- `04-skill-lifecycle-management.md` — 完整生命周期
- `05-essence-insights.md` — 本质洞察

### 参考 Skill
- `writing-skills` — 本 skill 的理论基础
- `using-superpowers` — Skill 使用规范
- `meta-execution` — 质量保障范例
- `session-learning` — 性能优化范例

---

## 🚀 快速开始

**5 分钟创建一个简单 Skill**：

1. **确认需求**：回答前 5 个问题
2. **运行基线**：观察 AI 的错误行为
3. **编写 MVP**：只包含核心流程和强制规则
4. **测试验证**：确认 AI 能正确执行
5. **发布使用**：在实践中迭代优化

**记住**：
- 从简单开始（1.0 工具型）
- 在使用中优化（不要一步到位）
- 度量驱动改进（记录效果数据）

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-04-30 | 初始版本，整合设计原则和TDD方法论 |
