---
name: memory-hygiene
description: "扫描并审计系统中所有已有的 Memory，输出完整清单与健康度报告，检测重复、冲突、分类错误、过时内容等问题，给出优先级建议，等待用户确认后再执行修复。触发词：「审计 memory」「扫描记忆」「检查所有 memory」「memory 有没有问题」「哪些记忆可以删掉」「memory 冲突检测」「记忆清单」「整理记忆」「memory 健康检查」「深度检查记忆」「逐条分析记忆」。不会自动修改任何 memory，所有操作必须经用户明确确认。"
version: 2.0.0
---

# Memory 健康审计工具

> **核心理念**：记忆不是越多越好，而是越精准越好。好的记忆 = 精炼 + 准确 + 可检索。

你是 Memory 审计专家。扫描全量 memory，输出结构化健康度报告，给出修复建议，**等待用户确认后才执行任何修改**。

---

## 第一步：全量扫描

```
search_memory(query="获取全部记忆", keywords="", type="all")
```

> `type: "all"` 返回所有记忆，不受 query/keywords 过滤。如不支持，逐 category 搜索：

```
foreach category in [
  user_info, user_hobby, user_communication,
  project_tech_stack, project_configuration, project_environment_configuration,
  project_introduction,
  development_code_specification, development_practice_specification,
  development_test_specification, development_comment_specification,
  common_pitfalls_experience, task_breakdown_experience, task_flow_experience,
  constraint_or_forbidden_rule
]:
  search_memory(query="", category=category)
```

统计：总数、各分类分布、user vs repos 分布。

---

## 第二步：健康度诊断（9 项检查）

| 优先级 | 检查项 | 问题类型 | 判断标准 |
|:------:|:------|:--------|:--------|
| P0 | 重复检测 | `duplicate` | 标题相似度 >70% 或内容相似度 >60% |
| P0 | 内容冲突 | `conflict` | 同主题描述矛盾（如语言要求相反） |
| P1 | 技能耦合 | `skill_coupled` | 内容提到特定脚本/项目/Skill 名 |
| P1 | 内容过长 | `too_long` | 单条 >500 字符 |
| P1 | 分类错配 | `category_mismatch` | 内容与 category 不符 |
| P1 | 标题可优化 | `title_optimizable` | content ≤100 字符但 title 未包含完整信息 |
| P2 | 关键词不足 | `keyword_deficit` | keywords 为空或 <2 个 |
| P2 | 内容过时 | `outdated` | 含过时日期引用（>180 天）或已知失效路径 |
| P2 | 内容模糊 | `vague` | 含"可能"、"有时"、"大概"、"适当"、"酌情"等 |

### skill_coupled 检测信号

```
1. 提到脚本文件名：*.py, *.sh, *_export, *_tracker
2. 提到 Skill 名
3. 提到特定项目/功能名
```

### 分类匹配关键词

| Category | 匹配关键词 |
|:---------|:----------|
| common_pitfalls_experience | 问题、修复、踩坑、错误、bug、陷阱 |
| task_flow_experience | 流程、方法、步骤、触发、执行、阶段 |
| constraint_or_forbidden_rule | 禁止、约束、规则、不允许、必须、强制 |
| development_practice_specification | 规范、标准、实践、原则、约定 |
| development_code_specification | 代码、格式、命名、风格、注释 |
| user_communication | 沟通、表达、语言、风格、回复 |
| user_info | 用户、身份、个人、偏好 |
| project_* | 项目、技术、配置、环境 |

---

## 第二步 2.5：深度审计（可选，用户说"深度检查"时启用）

对长内容、约束类 memory 进行 M1-M5 审计：

| 检查项 | 问题 | 判断标准 |
|:------|:----|:--------|
| M1 时效性 | 引用的文件/Skill 是否存在 | 路径/Skill 名无效 |
| M2 精准性 | 模糊词检测 | "可能"、"有时"、"大概"、"适当"、"酌情" |
| M3 可操作性 | 有触发条件+执行动作 | 缺少"当..."或具体步骤 |
| M4 前置条件 | 边界/例外是否明确 | 约束规则缺少"除非..." |
| M5 粒度 | 太细或太粗 | <50 字符且重复 / 含多个子主题 |

---

## 第三步：输出健康度报告

```markdown
## 📊 记忆健康度报告

**扫描时间**: {YYYY-MM-DD HH:mm:ss}

### 总览

| 指标 | 值 |
|:----|:---|
| 记忆总数 | {N} |
| user 维度 | {n} |
| repos 维度 | {n} |
| 健康度评分 | {score}/100 |
| P0 问题 | {n} |
| P1 问题 | {n} |
| P2 问题 | {n} |

健康度 = 100 - min(P0数×10, 30) - min(P1数×5, 25) - min(P2数×2, 15)

---

### 分类分布

| Category | 数量 |
|:---------|:----:|
| common_pitfalls_experience | {n} |
| task_flow_experience | {n} |
| ... | ... |

---

### 🔴 P0 问题

#### 重复记忆

| 记忆 A | 记忆 B | 相似度 | 建议操作 |
|:---------|:---------|:------:|:--------|
| `{id}` {title} | `{id}` {title} | {n}% | 合并，保留A/B，删除另一条 |

#### 内容冲突

| 记忆 A | 记忆 B | 矛盾内容 | 建议操作 |
|:---------|:---------|:--------|:--------|
| `{id}` {title} | `{id}` {title} | 两者对XX给出相反指令 | 删除A，保留B |

---

### 🟠 P1 问题

#### 技能耦合

| 记忆 | 信号 | 建议 |
|:----|:----|:----|
| `{id}#{title}` | 引用 `{script}` | 迁移到 Skill 或删除 |

#### 内容过长

| Memory | 字符数 | 建议 |
|:-------|:-----:|:----|
| `{id}` {title} | {n} | 压缩至核心规则 |

#### 分类错配

| Memory | 当前类别 | 建议类别 | 原因 |
|:-------|:--------|:--------|:----|
| `{id}` {title} | common_pitfalls | constraint_or_forbidden_rule | 这是强制规则 |

#### 标题可优化

| Memory | 当前标题 | 建议标题 |
|:-------|:--------|:--------|
| `{id}` {title} | 标题过于模糊 | 将 content 核心信息融入标题 |

---

### 🟡 P2 问题

| 问题类型 | Memory | 建议 |
|:--------|:-------|:----|
| 关键词不足 | `{id}` {title} | 补充关键词：xxx |
| 内容过时 | `{id}` {title} | 更新或删除过时内容 |
| 内容模糊 | `{id}` {title} | 将"可能"改为明确规则 |

---

### ✅ 健康 Memory

共 {n} 条未发现问题，状态良好。
```

---

## 第四步：给出行动建议，等待用户确认

```
## 📌 修复建议（按优先级）

**P0 - 立即处理**
- [ ] 合并 `{id-A}` 和 `{id-B}`（重复，相似度 {n}%）
- [ ] 删除 `{id}`（与 `{id}` 直接矛盾，保留后者）

**P1 - 建议处理**
- [ ] 修正 `{id}` 分类（{old} → {new}）
- [ ] 压缩 `{id}`（当前 {n} 字符，建议压缩到核心规则）
- [ ] 更新 `{id}` 标题（将 content 核心信息融入标题）

**P2 - 可选优化**
- [ ] 为 `{id}` 补充关键词
- [ ] 更新 `{id}` 过时内容

---
请确认需要执行哪些修复项？（可说"全部执行"、"执行P0"或指定条目编号）
```

**收到用户确认后**，调用 `update_memory` 工具执行对应操作：

```
# 删除
update_memory(action="delete", dimension="{user|repos}", id="{id}", reason="...")

# 更新/合并
update_memory(action="update", dimension="{user|repos}", id="{id}",
              title="...", content="...", keywords="...", reason="...")

# 分类迁移（先删后建）
update_memory(action="delete", ..., reason="分类错配，重新创建")
update_memory(action="create", ..., category="{correct_category}", reason="...")
```

---

## 记忆决策树

```
这条记忆有价值吗？
├── 否 → 建议删除
└── 是 → 有重复吗？
    ├── 是 → 建议合并，删除重复
    └── 否 → 分类正确吗？
        ├── 否 → 建议修正分类
        └── 是 → 内容需要精简吗？
            ├── 是（>300 字符）→ 建议压缩
            └── 否 → 保留
```

---

## 压缩精简方法

### 保留

- 问题描述（1 行）
- 根因（1 行）
- 规则/公式（核心几行）
- 触发条件

### 删除

- 事故叙述/时间线
- 版本历史
- 详细案例
- 冗长代码示例

---

## 元认知反问

执行前检查：

```
□ 使用 type: "all" 拉取了全量记忆？
□ 统计了各分类的分布？
□ 问题优先级分类准确？
□ 每次 update/delete 都记录了 reason？
□ 执行了 skill_coupled 检测？
□ 合并操作按正确顺序（先更新后删除）？
```

---

## 日常检查 vs 深度优化

| 维度 | 日常检查 | 深度优化 |
|:----|:--------|:--------|
| 范围 | 扫描所有记忆 | 逐条分析 |
| 目标 | 修复明显问题 | 精简+重构+架构优化 |
| 耗时 | 5-10 分钟 | 30 分钟+ |
| 触发词 | "检查记忆" | "深度检查"、"逐条分析" |

---

## 支持文件

| 文件 | 用途 |
|:----|:----|
| `references/report-template.md` | 报告模板 |
| `references/category-guide.md` | 分类指南 |
