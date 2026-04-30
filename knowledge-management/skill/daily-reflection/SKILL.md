---
name: evo-daily-reflection
description: "每日修炼统一入口 — 依次执行记忆优化（evo-memory-hygiene）、知识库优化（evo-knowledge-curator），并输出最终汇总报告。当用户说'每日修炼'、'daily reflection'、'执行修炼'、'开始修炼'、'run daily reflection'、'执行每日复盘'时触发。自动串联两个优化步骤并汇总输出报告。"
version: 1.0.0
---

# 每日修炼（Daily Reflection）

串联执行记忆优化 + 知识库优化，输出最终汇总报告。

---

## 执行流程

```
Step 1: 记忆优化（evo-memory-hygiene）
Step 2: 知识库优化（evo-knowledge-curator）
Step 3: 输出最终报告
```

---

## Step 1: 记忆优化

调用 `evo-memory-hygiene` 执行记忆健康检查与优化：

```
use_skill(skill_name="evo-memory-hygiene")

执行：全量扫描 → 健康度诊断 → 修复 → 输出报告
```

收集以下数据用于最终报告：
- 记忆总数
- 健康度评分（优化前/后）
- P0/P1/P2 问题数
- 执行的修复操作数（删除/更新/合并）

---

## Step 2: 知识库优化

调用 `evo-knowledge-curator` 执行知识库健康检查与优化：

```
use_skill(skill_name="evo-knowledge-curator")

执行：全量扫描 → 健康度诊断 → 整理优化 → 输出报告
```

收集以下数据用于最终报告：
- 知识文档总数
- 健康度评分（优化前/后）
- P0/P1/P2 问题数
- 执行的整理操作数

---

## Step 3: 最终汇总报告

输出格式：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 每日修炼完成 ({TODAY})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 记忆优化
  总数: {N} 条
  健康度: {before} → {after}/100
  问题: P0×{n} P1×{n} P2×{n}
  修复: 删除 {n} | 更新 {n} | 合并 {n}

📚 知识库优化
  总数: {N} 个文档
  健康度: {before} → {after}/100
  问题: P0×{n} P1×{n} P2×{n}
  修复: {n} 项操作

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 支持文件

| 文件 | 用途 |
|:----|:----|
| `references/report-template.md` | 最终报告详细模板 |
