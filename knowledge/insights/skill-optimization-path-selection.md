# Skill 优化的路径选择

> 分类：insights  
> 来源：2026-04-29 self-learning-skill-optimization

---

## [2026-04-29] 来自 self-learning-skill-optimization

### 洞察

当要优化一个 skill 时，首先要明确**优化哪里的 skill**，避免路径混淆导致工作白费。

### 背景问题

本次对话中，初始目标是"基于 Hermes-agent 调研结果优化 self-learning skill"，但存在两层歧义：

1. **来源歧义**：
   - Hermes-agent 开源仓库没有独立的 self-learning skill
   - 用户的 `.codeflicker/skills/self-learning/` 已存在完整实现

2. **路径歧义**：
   - 当前工作目录：`/Users/yuxudong/Documents/hermes-agent`（调研仓库）
   - 实际目标文件：`/Users/yuxudong/.codeflicker/skills/self-learning/`
   - 验证 agent 在错误路径查找文件，导致"死循环"

### 解决方案

**路径前置明确原则**：在调研阶段就明确三个问题：
1. 优化的是**哪个仓库**的 skill？
2. 目标文件的**绝对路径**是什么？
3. 是**调研 + 提案**，还是**直接修改**？

### 通用模式

```
调研开源项目 → 形成优化方案 → 明确应用目标
                                   ↓
                              选项 A: 修改用户自己的 skill
                              选项 B: 在调研仓库创建示例
                              选项 C: 仅输出方案文档
```

**决策点**：在"形成优化方案"之后，立即与用户确认选项 A/B/C。

### 应用场景

- 基于开源项目的 best practice 优化自己的实现
- 学习新技术后应用到现有项目
- 迁移设计模式到不同代码库

### 相关问题

如果用户说"优化 XXX skill"，但未明确路径，优先询问：
```
"我注意到您提到优化 XXX skill，请问您是想：
A. 修改您现有的 .codeflicker/skills/XXX/
B. 在当前仓库创建示例实现
C. 仅输出优化方案文档
？"
```
