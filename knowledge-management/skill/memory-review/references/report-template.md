# 记忆健康度报告模板

---

## 报告格式

```markdown
# 记忆健康度报告

**生成时间**: {YYYY-MM-DD HH:mm:ss}

---

## 📊 总览

| 指标 | 值 |
|:----|:---|
| 记忆总数 | {N} |
| user 维度 | {n} |
| repos 维度 | {n} |
| 健康度评分 | {score}/100 |
| P0 问题 | {n} |
| P1 问题 | {n} |
| P2 问题 | {n} |

---

## 📁 分类分布

| Category | 数量 | 占比 |
|:---------|:----:|:----:|
| user_info | {n} | {p}% |
| user_hobby | {n} | {p}% |
| user_communication | {n} | {p}% |
| project_tech_stack | {n} | {p}% |
| project_configuration | {n} | {p}% |
| project_environment_configuration | {n} | {p}% |
| project_introduction | {n} | {p}% |
| development_code_specification | {n} | {p}% |
| development_practice_specification | {n} | {p}% |
| development_test_specification | {n} | {p}% |
| development_comment_specification | {n} | {p}% |
| common_pitfalls_experience | {n} | {p}% |
| task_breakdown_experience | {n} | {p}% |
| task_flow_experience | {n} | {p}% |
| constraint_or_forbidden_rule | {n} | {p}% |

---

## 🔴 P0 问题（严重）

### 重复记忆

| 记忆 A | 记忆 B | 相似度 | 建议操作 |
|:------|:------|:-----:|:--------|
| `{id}` {title} | `{id}` {title} | {n}% | 合并到 A，删除 B |

### 内容冲突

| 记忆 A | 记忆 B | 冲突点 | 建议操作 |
|:------|:------|:------|:--------|
| `{id}` {title} | `{id}` {title} | {描述} | 保留正确的，删除错误的 |

---

## 🟠 P1 问题（中等）

### 技能耦合

| 记忆 ID | 标题 | 耦合信号 | 建议 |
|:-------|:----|:--------|:----|
| `{id}` | {title} | 引用 `{script/skill}` | 迁移到对应 Skill |

### 内容过长

| 记忆 ID | 标题 | 字符数 | 建议 |
|:-------|:----|:-----:|:----|
| `{id}` | {title} | {n} | 压缩到 <300 字符 |

### 分类错配

| 记忆 ID | 标题 | 当前分类 | 建议分类 |
|:-------|:----|:--------|:--------|
| `{id}` | {title} | {current} | {suggested} |

---

## 🟡 P2 问题（轻微）

| 问题类型 | 数量 | 记忆 ID 列表 |
|:--------|:----:|:------------|
| 关键词不足 | {n} | {id1}, {id2}, ... |
| 过时 | {n} | {id1}, {id2}, ... |
| 内容模糊 | {n} | {id1}, {id2}, ... |
| 无价值 | {n} | {id1}, {id2}, ... |

---

## ✅ 建议清单（等待用户确认）

| 操作 | 数量 | 详情 |
|:----|:----:|:----|
| 建议删除 | {n} | {id1}, {id2}, ... |
| 建议更新 | {n} | {id1}, {id2}, ... |
| 建议合并 | {n} | {id_a}+{id_b} → {id_a} |
| 建议修正分类 | {n} | {id}: {old} → {new} |

> 以上均为建议，需用户确认后才执行。

---

## 📌 建议

1. **短期**：{立即需要处理的问题}
2. **中期**：{近期应该关注的优化}
3. **长期**：{架构层面的建议}

---

## 📈 历史趋势（可选）

| 日期 | 总数 | 健康度 | 变化 |
|:----|:----:|:-----:|:----:|
| {date1} | {n} | {score} | - |
| {date2} | {n} | {score} | +{n}/-{n} |
```

---

## 操作模板

### 删除记忆

```
update_memory(
  action: "delete",
  dimension: "{user|repos}",
  id: "{memory_id}",
  reason: "删除原因：{具体原因}"
)
```

### 更新/精简记忆

```
update_memory(
  action: "update",
  dimension: "{user|repos}",
  id: "{memory_id}",
  category: "{category}",
  title: "精简后的标题",
  content: "精简后的内容（问题+根因+规则）",
  keywords: "关键词1, 关键词2, 关键词3",
  reason: "精简原因：内容过长，从 {n} 字符压缩到 {m} 字符"
)
```

### 合并重复记忆

```
# Step 1: 更新保留的记忆
update_memory(
  action: "update",
  dimension: "{dimension}",
  id: "{keep_id}",
  content: "{合并后的完整内容}",
  reason: "合并重复记忆 {delete_id}"
)

# Step 2: 删除被合并的记忆
update_memory(
  action: "delete",
  dimension: "{dimension}",
  id: "{delete_id}",
  reason: "已合并到 {keep_id}"
)
```

### 修正分类（删除+重建）

```
# Step 1: 删除错误分类的记忆
update_memory(
  action: "delete",
  dimension: "{dimension}",
  id: "{old_id}",
  reason: "分类错配，从 {old_category} 迁移到 {new_category}"
)

# Step 2: 在正确分类创建
update_memory(
  action: "create",
  dimension: "{dimension}",
  category: "{correct_category}",
  title: "{title}",
  content: "{content}",
  keywords: "{keywords}",
  reason: "从 {old_category} 迁移"
)
```

### 补充关键词

```
update_memory(
  action: "update",
  dimension: "{dimension}",
  id: "{memory_id}",
  keywords: "关键词1, 关键词2, 关键词3, 关键词4",
  reason: "补充关键词，提升可检索性"
)
```
