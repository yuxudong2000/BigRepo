# Skill 生命周期管理完全指南

> **从创建到废弃的全生命周期最佳实践**  
> 调研日期：2026-04-30  
> 基于：knowledge-review, skill-review, writing-skills 等示例深度分析

---

## 目录

1. [Skill 生命周期概览](#一skill-生命周期概览)
2. [创建阶段](#二创建阶段)
3. [测试与验证](#三测试与验证)
4. [版本管理](#四版本管理)
5. [维护与优化](#五维护与优化)
6. [审计与健康检查](#六审计与健康检查)
7. [废弃与迁移](#七废弃与迁移)
8. [最佳实践汇总](#八最佳实践汇总)

---

## 一、Skill 生命周期概览

### 1.1 完整生命周期

```
┌─────────────────────────────────────────────────────────────┐
│                    Skill 生命周期                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Phase 1: 需求分析 & 设计                                    │
│    ├─ 识别问题领域                                          │
│    ├─ 调研现有方案                                          │
│    ├─ 设计核心流程                                          │
│    └─ 编写设计文档                                          │
│                     ↓                                       │
│  Phase 2: 开发与测试                                        │
│    ├─ 创建 SKILL.md                                        │
│    ├─ 编写支持文件                                          │
│    ├─ 单元测试（使用 subagent 测试）                        │
│    └─ 集成测试                                              │
│                     ↓                                       │
│  Phase 3: 发布与部署                                        │
│    ├─ 版本标记（v1.0.0）                                    │
│    ├─ 文档完善                                              │
│    ├─ 安装到目标位置                                        │
│    └─ 宣布可用                                              │
│                     ↓                                       │
│  Phase 4: 使用与反馈                                        │
│    ├─ 实际使用收集反馈                                      │
│    ├─ 记录问题和改进点                                      │
│    ├─ 监控性能和效果                                        │
│    └─ 定期审计                                              │
│                     ↓                                       │
│  Phase 5: 维护与迭代                                        │
│    ├─ Bug 修复（patch 版本）                                │
│    ├─ 新功能（minor 版本）                                  │
│    ├─ 重大重构（major 版本）                                │
│    └─ 文档更新                                              │
│                     ↓                                       │
│  Phase 6: 废弃与迁移（可选）                                │
│    ├─ 标记为废弃                                            │
│    ├─ 提供替代方案                                          │
│    ├─ 迁移指南                                              │
│    └─ 最终删除                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 生命周期阶段统计

| 阶段 | 典型耗时 | 关键产出 | 失败风险 |
|------|---------|---------|---------|
| 需求分析 | 2-4小时 | 设计文档 | 需求理解偏差 |
| 开发测试 | 4-8小时 | SKILL.md | 功能不完整 |
| 发布部署 | 1-2小时 | v1.0.0 | 文档不清晰 |
| 使用反馈 | 持续 | 问题清单 | 无人使用 |
| 维护迭代 | 持续 | 新版本 | 兼容性问题 |
| 废弃迁移 | 1-2小时 | 迁移指南 | 用户损失 |

---

## 二、创建阶段

### 2.1 需求分析清单

**在开始编写 Skill 前，必须回答的 10 个问题：**

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

### 2.2 设计文档模板

在创建 SKILL.md 之前，先写设计文档：

```markdown
# Skill 设计文档：[Skill Name]

> 设计日期：YYYY-MM-DD  
> 设计者：[Your Name]  
> 状态：[草稿 / 审查中 / 已批准]

---

## 1. 概述

### 1.1 目标
[一段话说明这个 Skill 的目标]

### 1.2 用户价值
[用户使用这个 Skill 能获得什么价值？]

### 1.3 非目标
[明确这个 Skill **不做**什么]

---

## 2. 用户场景

### 2.1 主要场景
**场景 1：[场景名称]**
- 用户：[用户类型]
- 触发：[用户说什么/做什么]
- 期望：[用户期望得到什么]
- 流程：[Skill 如何响应]

**场景 2：[场景名称]**
...

### 2.2 边缘场景
[列出不常见但需要考虑的场景]

### 2.3 反例场景
[列出看起来相关但不应该触发的场景]

---

## 3. 功能设计

### 3.1 核心功能列表
1. [功能 1] — [说明]
2. [功能 2] — [说明]
3. [功能 3] — [说明]

### 3.2 执行流程
[使用流程图或步骤列表]

```
Step 1: [步骤描述]
  ├─ 输入：[...]
  ├─ 处理：[...]
  └─ 输出：[...]

Step 2: [步骤描述]
  ...
```

### 3.3 错误处理
[如何处理各种错误情况]

---

## 4. 技术设计

### 4.1 文件结构
```
skill-name/
├── SKILL.md
├── references/
├── scripts/
└── templates/
```

### 4.2 依赖关系
- 依赖 Skill：[...]
- 依赖工具：[...]
- 依赖配置：[...]

### 4.3 性能考虑
[响应时间、资源消耗、并发支持]

---

## 5. 测试计划

### 5.1 测试用例
| 用例ID | 场景 | 输入 | 期望输出 | 优先级 |
|--------|------|------|---------|--------|
| TC-01 | ... | ... | ... | P0 |

### 5.2 测试策略
[如何执行测试]

---

## 6. 版本规划

### 6.1 MVP (v1.0.0)
[最小可用版本包含的功能]

### 6.2 未来版本
- v1.1.0: [功能]
- v2.0.0: [重大变更]

---

## 7. 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| [风险描述] | 高/中/低 | 高/中/低 | [措施] |

---

## 8. 审批记录

| 审批人 | 日期 | 意见 | 状态 |
|--------|------|------|------|
| [Name] | YYYY-MM-DD | [Comments] | 通过/待修改 |
```

---

## 三、测试与验证

### 3.1 测试类型

#### 3.1.1 单元测试（Subagent 测试）

从 `writing-skills/testing-skills-with-subagents.md` 学到的方法：

```markdown
## 使用 Subagent 测试 Skill

### 测试步骤

1. **准备测试用例**
   - 编写测试场景描述
   - 准备测试输入数据
   - 定义期望输出

2. **创建测试 Subagent**
   ```
   use_subagent(
       subagent_name="test-runner",
       task="""
       测试 {skill-name} 的以下场景：
       
       场景：{scenario}
       输入：{input}
       期望：{expected}
       
       验证：
       1. Skill 是否正确触发
       2. 输出是否符合预期
       3. 错误处理是否正确
       """,
       background=false
   )
   ```

3. **收集测试结果**
   - Subagent 返回测试通过/失败
   - 记录错误和边缘情况
   - 生成测试报告

### 测试用例模板

```markdown
## 测试用例：{Case Name}

### 场景描述
[描述测试场景]

### 前置条件
- [条件1]
- [条件2]

### 测试步骤
1. [步骤1]
2. [步骤2]

### 期望结果
- [结果1]
- [结果2]

### 实际结果
- [记录实际输出]

### 通过标准
- [ ] 功能正确
- [ ] 性能达标
- [ ] 错误处理正确
```

#### 3.1.2 集成测试

测试 Skill 与其他组件的交互：

```markdown
## 集成测试清单

### 与依赖 Skill 的集成
- [ ] 依赖的 Skill 能正确加载
- [ ] 数据传递正确
- [ ] 错误能正确传播

### 与系统工具的集成
- [ ] 文件系统操作正确
- [ ] 外部命令执行正确
- [ ] API 调用正确

### 与用户交互的集成
- [ ] 触发词识别准确
- [ ] 输出格式友好
- [ ] 错误提示清晰
```

#### 3.1.3 用户验收测试

```markdown
## 用户验收测试（UAT）

### 可用性测试
- [ ] 用户能理解如何使用
- [ ] 触发词符合直觉
- [ ] 输出易于理解

### 场景覆盖测试
- [ ] 主要场景全覆盖
- [ ] 边缘场景有处理
- [ ] 错误场景能恢复

### 体验测试
- [ ] 响应速度满意
- [ ] 反馈及时
- [ ] 无明显 Bug
```

### 3.2 测试工具

从 `writing-skills/` 示例学到的测试工具：

#### 3.2.1 Anthropic 最佳实践检查器

```markdown
## Anthropic 最佳实践对照

基于 `anthropic-best-practices.md` 检查：

### Prompt 设计
- [ ] 使用清晰的结构
- [ ] 提供示例
- [ ] 明确输出格式

### 错误处理
- [ ] 有明确的错误提示
- [ ] 提供恢复建议
- [ ] 记录错误日志

### 性能优化
- [ ] 避免重复调用
- [ ] 使用缓存机制
- [ ] 并行处理（如适用）
```

#### 3.2.2 说服力原则检查

基于 `persuasion-principles.md`：

```markdown
## Skill 说服力检查

### 明确性（Clarity）
- [ ] Skill 的目的一目了然
- [ ] 步骤清晰易懂
- [ ] 术语有解释

### 相关性（Relevance）
- [ ] 解决真实问题
- [ ] 用户能感受到价值
- [ ] 与现有工作流集成

### 可信度（Credibility）
- [ ] 有实际案例
- [ ] 有数据支持
- [ ] 有版本历史
```

---

## 四、版本管理

### 4.1 语义化版本控制

遵循 [Semantic Versioning 2.0.0](https://semver.org/)：

```
版本格式：MAJOR.MINOR.PATCH

MAJOR：不兼容的 API 变更
MINOR：向后兼容的功能新增
PATCH：向后兼容的 Bug 修复
```

**示例版本演进**：

```
v1.0.0  → 初始发布
v1.0.1  → Bug 修复（修正文档错误）
v1.1.0  → 新功能（增加并行模式）
v1.2.0  → 新功能（增加缓存机制）
v2.0.0  → 重大变更（重构核心流程）
v2.1.0  → 新功能（新增深度分析）
v3.0.0  → 重大变更（完全重写）
```

### 4.2 版本历史记录

在 SKILL.md 底部维护版本历史：

```markdown
## 版本历史

| 版本 | 日期 | 变更类型 | 变更内容 | 破坏性变更 |
|------|------|---------|---------|-----------|
| v3.0.0 | 2026-04-29 | 🔴 重大变更 | 引入根因分析，知识层级提升 | ✅ 是 |
| v2.1.0 | 2026-04-15 | 🟢 新功能 | 增加原子写入保护 | ❌ 否 |
| v2.0.0 | 2026-04-12 | 🔴 重大变更 | 并行执行优化（5.8x加速） | ✅ 是 |
| v1.2.1 | 2026-04-05 | 🔵 Bug修复 | 修复文件路径解析错误 | ❌ 否 |
| v1.2.0 | 2026-04-01 | 🟢 新功能 | 增加流式进度反馈 | ❌ 否 |
| v1.1.0 | 2026-03-25 | 🟢 新功能 | 增加降级兜底机制 | ❌ 否 |
| v1.0.1 | 2026-03-22 | 🔵 Bug修复 | 修正文档示例错误 | ❌ 否 |
| v1.0.0 | 2026-03-20 | 🎉 初始发布 | 基础功能实现 | N/A |
```

**变更类型图例**：
- 🎉 初始发布
- 🔴 重大变更（Major）
- 🟢 新功能（Minor）
- 🔵 Bug修复（Patch）
- 📝 文档更新
- ⚡ 性能优化
- 🔧 重构

### 4.3 变更日志（CHANGELOG.md）

为复杂 Skill 创建独立的 CHANGELOG.md：

```markdown
# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- [功能描述]

### Changed
- [变更描述]

### Fixed
- [修复描述]

## [3.0.0] - 2026-04-29
### Added
- 根因分析引擎（Five-Why 分析）
- 通用原则库（Layer 5 知识架构）
- root-cause-analyzer 子 Agent

### Changed
- 知识层级从 Layer 1-3 提升到 Layer 1-5
- 性能影响：增加 15s 执行时间（可选启用）

### Breaking Changes
- 知识库目录结构变更（新增 root-causes/ 和 principles/）
- frontmatter 新增 `deep_analysis: true` 字段

## [2.0.0] - 2026-04-12
### Added
- 并行执行模式（5.8x 加速）
- 流式进度反馈
- 原子写入保护

### Changed
- 从串行提取改为并行提取
- 自动降级策略优化

### Breaking Changes
- frontmatter 新增 `parallel_mode: true` 字段
- 依赖 `use_subagent` 工具

## [1.0.0] - 2026-03-20
### Added
- 初始发布
- 基础知识提炼功能
- 七分类提取（solutions/tools/patterns/insights/memories/rules/skills）
```

### 4.4 Git 标签管理

为每个版本创建 Git 标签：

```bash
# 创建带注释的标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签到远程
git push origin v1.0.0

# 查看所有标签
git tag -l

# 查看特定标签的详细信息
git show v1.0.0
```

---

## 五、维护与优化

### 5.1 定期维护清单

```markdown
## Skill 维护检查清单（每月执行）

### 1. 功能检查
- [ ] 所有核心功能正常工作
- [ ] 无新增 Bug
- [ ] 性能无明显下降

### 2. 文档检查
- [ ] 文档与代码一致
- [ ] 示例可正常运行
- [ ] 无过时信息

### 3. 依赖检查
- [ ] 依赖的 Skill 版本兼容
- [ ] 依赖的工具版本兼容
- [ ] 无废弃 API 使用

### 4. 兼容性检查
- [ ] 与最新系统版本兼容
- [ ] 与其他 Skill 无冲突
- [ ] 触发词无误触发

### 5. 性能检查
- [ ] 响应时间满足要求
- [ ] 资源消耗合理
- [ ] 无内存泄漏

### 6. 用户反馈
- [ ] 收集用户反馈
- [ ] 识别改进点
- [ ] 规划新功能
```

### 5.2 性能优化策略

从 `session-learning` 学到的优化方法：

#### 5.2.1 并行化

```markdown
## 并行化优化清单

### 识别并行机会
- [ ] 有独立的子任务吗？
- [ ] 子任务之间无依赖吗？
- [ ] 并行能带来明显提升吗？

### 实现并行
- [ ] 使用 use_subagent 并发执行
- [ ] 设置合理的超时时间
- [ ] 实现降级兜底策略

### 性能度量
- [ ] 记录串行模式耗时
- [ ] 记录并行模式耗时
- [ ] 计算加速比
- [ ] 向用户展示性能提升
```

#### 5.2.2 缓存机制

```markdown
## 缓存策略

### 识别缓存机会
- [ ] 有重复计算吗？
- [ ] 有重复查询吗？
- [ ] 缓存能带来收益吗？

### 实现缓存
- [ ] 选择缓存存储（内存/文件/数据库）
- [ ] 设置缓存过期策略
- [ ] 实现缓存失效机制

### 缓存维护
- [ ] 定期清理过期缓存
- [ ] 监控缓存命中率
- [ ] 优化缓存策略
```

### 5.3 重构策略

```markdown
## 重构决策树

### 何时重构？

符合以下任一条件时考虑重构：
- [ ] 代码超过 500 行，难以维护
- [ ] 功能逻辑混乱，难以理解
- [ ] 频繁出现 Bug
- [ ] 性能严重下降
- [ ] 新功能难以添加

### 重构类型

**小型重构（Patch 版本）**
- 提取函数/方法
- 重命名变量
- 简化逻辑
- 不改变功能

**中型重构（Minor 版本）**
- 重组文件结构
- 优化算法
- 改进接口
- 保持向后兼容

**大型重构（Major 版本）**
- 重写核心流程
- 改变数据结构
- 重新设计API
- 可能破坏兼容性

### 重构步骤

1. **评估必要性** — 收益 > 成本
2. **备份现状** — Git 标签/分支
3. **增加测试** — 确保重构不破坏功能
4. **小步迭代** — 每次改动小，频繁提交
5. **持续验证** — 每步都测试
6. **文档更新** — 同步更新文档
7. **用户通知** — 说明变更内容
```

---

## 六、审计与健康检查

### 6.1 Skill 审计流程

从 `skill-review` 学到的审计方法：

```markdown
## Skill 全量审计流程

### Step 1: 扫描所有 Skill

**扫描目录**：
- ~/.codeflicker/skills/（个人级）
- ~/.codeflicker/internal/skills/（系统内置）
- {project}/.codeflicker/skills/（项目级）

**收集信息**：
| # | 名称 | 版本 | 描述 | 路径 | 最后更新 |
|---|------|------|------|------|---------|

### Step 2: 问题检测

#### 检测项 1：YAML 格式错误
- [ ] frontmatter 在文件开头
- [ ] 必填字段完整（name, description）
- [ ] name 符合 kebab-case
- [ ] 目录名与 name 一致

#### 检测项 2：描述质量
- [ ] description 包含触发场景
- [ ] description 长度适中（> 30字）
- [ ] description 明确不适用场景

#### 检测项 3：冲突检测
- [ ] 触发词无重叠
- [ ] 功能范围无重叠
- [ ] 无废弃声明的 Skill

#### 检测项 4：路径问题
- [ ] SKILL.md 文件存在
- [ ] 脚本路径无硬编码
- [ ] 依赖路径正确

#### 检测项 5：版本状态
- [ ] 版本号合理
- [ ] 无冗余旧版本
- [ ] 无未完成的 Skill

### Step 3: 输出问题报告

```
## 🔍 问题检测报告

### ❌ 严重问题（需立即修复）
| Skill | 问题类型 | 问题描述 | 建议 |
|-------|---------|---------|------|

### ⚠️ 冲突/重叠（建议处理）
| Skill A | Skill B | 冲突类型 | 建议 |
|---------|---------|---------|------|

### 🗑️ 建议删除
| Skill | 删除原因 |
|-------|---------|

### 💡 建议优化（可选）
| Skill | 问题 | 优化建议 |
|-------|------|---------|

### ✅ 健康 Skill
共 X 个 Skill 未发现问题。
```

### Step 4: 执行修复
- [ ] 修复 P0 问题
- [ ] 处理 P1 冲突
- [ ] 清理废弃 Skill
- [ ] 优化描述质量
```

### 6.2 知识库健康检查

从 `knowledge-review` 学到的知识库管理：

```markdown
## 知识库健康度评估

### Phase 1: 全量扫描

```bash
python3 scripts/scan_knowledge_base.py "${KB_PATH}"
```

**输出**：
- 总文档数
- 目录分布
- 最近更新
- 最久未更新

### Phase 2: 健康度诊断

#### 五项检查

| 检查项 | 阈值 | 问题类型 | 优先级 |
|--------|------|---------|--------|
| **索引缺失** | 不在任何index中 | `orphan` | P0 |
| **重复文档** | 标题相似>0.7 | `duplicate` | P1 |
| **分类混乱** | 位置与内容不符 | `misplaced` | P1 |
| **过时** | >180天未更新 | `outdated` | P2 |
| **无引用** | 无记忆/技能引用 | `isolated` | P2 |

#### 健康度评分

```
健康度 = 100 - P0问题×20 - P1问题×10 - P2问题×5

| 评级 | 分数 | 标签 |
|------|------|------|
| 健康 | 80-100 | 🟢 健康 |
| 需关注 | 60-79 | 🟡 需关注 |
| 需优化 | 0-59 | 🔴 需优化 |
```

### Phase 3: 节点深度审计

**筛选高风险文档**：
- 文档 > 200行
- 含统计数据/数字
- 外部链接 > 3个
- >120天未更新
- 无内部引用

**五项审计**：
1. **信息时效性** (P0) — 数据是否过时
2. **内部一致性** (P0) — 是否自相矛盾
3. **结构完整性** (P1) — 章节是否完整
4. **链接有效性** (P1) — 链接是否失效
5. **可读性评估** (P2) — 是否易于理解

### Phase 4: 整理优化

```
📋 知识库优化计划

🔴 P0 问题 (2项):
  1. [orphan] research/draft.md — 未被索引
  2. [orphan] notes/temp.md — 未被索引

🟡 P1 问题 (1项):
  1. [misplaced] guides/research.md — 应移至 research/

🟢 P2 问题 (3项):
  1. [outdated] archives/old.md — 200天未更新
  ...

是否执行优化？ [全部 / 仅P0 / 选择 / 跳过]
```

### Phase 5: 产出报告

```markdown
### 知识优化报告 {DATE}

#### 扫描结果
- 总数: N 个文档
- 索引完整性: ✅/❌

#### 问题统计
- P0: N 项
- P1: N 项
- P2: N 项

#### 操作记录
1. [reindex] category — 完成
2. [reclassify] file.md — 移动

#### 健康度变化
- 优化前: X%
- 优化后: Y%
```
```

---

## 七、废弃与迁移

### 7.1 废弃标记

当 Skill 需要废弃时，在 frontmatter 中添加废弃声明：

```yaml
---
name: old-skill
deprecated: true
deprecated_since: "2026-04-30"
deprecated_message: "已被 new-skill 替代，请使用 new-skill"
replacement: new-skill
replacement_url: "https://link-to-new-skill-doc"
version: 1.5.0
---
```

在文档顶部添加醒目警告：

```markdown
> ⚠️ **此 Skill 已废弃**
>
> 自 2026-04-30 起，本 Skill 已被 `new-skill` 替代。
>
> **替代方案**：请使用 [`new-skill`](link) 获得更好的功能和性能。
>
> **迁移指南**：见下方 [迁移说明](#迁移指南)。
>
> **维护状态**：本 Skill 仅修复严重 Bug，不再添加新功能。
>
> **移除计划**：预计于 2026-07-30 完全移除。

# [Skill Name] （已废弃）

[原有内容...]

---

## 迁移指南

### 从 old-skill 迁移到 new-skill

[详细迁移步骤...]
```

### 7.2 迁移指南模板

```markdown
## 迁移指南：从 {old-skill} 到 {new-skill}

### 为什么迁移？

- [原因1：性能提升]
- [原因2：功能增强]
- [原因3：更好的维护]

### 兼容性说明

#### 保持不变
- [功能1] — 完全兼容
- [功能2] — 完全兼容

#### 需要调整
- [功能3] — 轻微调整，见下方说明
- [功能4] — 参数变更，见下方说明

#### 已移除
- [功能5] — 已废弃，无替代
- [功能6] — 由新功能X替代

### 迁移步骤

#### Step 1: 安装新 Skill

```bash
# 使用 skill-manager 安装
skill-manager install new-skill
```

#### Step 2: 更新触发词

| 旧触发词 | 新触发词 | 说明 |
|---------|---------|------|
| "旧词" | "新词" | [变更说明] |

#### Step 3: 迁移配置

```yaml
# 旧配置
old_skill:
  option1: value1
  option2: value2

# 新配置
new_skill:
  option1: value1  # 保持不变
  option2_renamed: value2  # 重命名
  option3: value3  # 新增
```

#### Step 4: 测试新 Skill

[测试步骤...]

#### Step 5: 删除旧 Skill

```bash
# 确认新 Skill 工作正常后
skill-manager remove old-skill
```

### 对照表

| 旧 Skill 功能 | 新 Skill 对应功能 | 变化 |
|--------------|-----------------|------|
| [功能A] | [功能A'] | 名称变更 |
| [功能B] | [功能B] | 无变化 |
| [功能C] | [功能X + 功能Y] | 拆分为两个功能 |
| [功能D] | — | 已移除 |
| — | [功能Z] | 新增 |

### 常见问题

#### Q1: 旧 Skill 的数据会保留吗？
A: [回答]

#### Q2: 迁移需要多长时间？
A: [回答]

#### Q3: 可以同时使用两个 Skill 吗？
A: [回答]

### 获取帮助

- 文档：[链接]
- Issue：[链接]
- 联系：[邮件/聊天]
```

### 7.3 废弃时间表

```markdown
## Skill 废弃时间表

### Phase 1: 废弃公告（T+0）
- [x] 在 Skill 中添加废弃标记
- [x] 发布废弃公告
- [x] 更新文档说明
- [ ] 通知所有用户

### Phase 2: 维护期（T+0 到 T+60天）
- [ ] 仅修复严重 Bug
- [ ] 协助用户迁移
- [ ] 收集迁移反馈
- [ ] 优化新 Skill

### Phase 3: 宽限期（T+60 到 T+90天）
- [ ] 停止所有维护
- [ ] 再次通知用户
- [ ] 确认用户已迁移
- [ ] 准备移除

### Phase 4: 移除（T+90天）
- [ ] 从系统中移除
- [ ] 更新相关文档
- [ ] 归档代码（Git 标签）
- [ ] 发布移除公告
```

---

## 八、最佳实践汇总

### 8.1 创建阶段

✅ **Do**：
- 先写设计文档，再写代码
- 明确定义触发场景和反例
- 提供丰富的示例和说明
- 设置清晰的边界
- 考虑错误处理和降级策略

❌ **Don't**：
- 不要假设用户知道如何使用
- 不要过度设计（从 MVP 开始）
- 不要跳过测试阶段
- 不要忽略文档
- 不要硬编码路径和配置

### 8.2 测试阶段

✅ **Do**：
- 使用 Subagent 进行自动化测试
- 覆盖主要场景和边缘情况
- 测试错误处理
- 收集真实用户反馈
- 记录测试结果

❌ **Don't**：
- 不要只测试happy path
- 不要假设用户会正确使用
- 不要跳过性能测试
- 不要忽略兼容性测试

### 8.3 版本管理

✅ **Do**：
- 遵循语义化版本
- 记录详细的变更日志
- 使用 Git 标签
- 说明破坏性变更
- 提供升级指南

❌ **Don't**：
- 不要随意改变版本号
- 不要忘记更新版本历史
- 不要在小版本中引入破坏性变更
- 不要跳过版本号

### 8.4 维护阶段

✅ **Do**：
- 定期执行健康检查
- 及时修复 Bug
- 收集用户反馈
- 持续优化性能
- 保持文档更新

❌ **Don't**：
- 不要长期不维护
- 不要忽略用户反馈
- 不要让文档过时
- 不要累积技术债
- 不要拒绝重构

### 8.5 废弃阶段

✅ **Do**：
- 提前公告废弃计划
- 提供清晰的迁移指南
- 给予充足的迁移时间
- 协助用户迁移
- 归档历史版本

❌ **Don't**：
- 不要突然移除
- 不要不提供替代方案
- 不要忽略现有用户
- 不要删除历史记录
- 不要强制迁移

---

## 附录：工具和脚本

### A. 健康检查脚本

```python
#!/usr/bin/env python3
"""
Skill 健康检查脚本
"""

import os
import yaml
from pathlib import Path
from datetime import datetime, timedelta

def check_skill_health(skill_path):
    """检查单个 Skill 的健康度"""
    
    issues = []
    score = 100
    
    # 1. 检查 SKILL.md 存在
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        issues.append(("P0", "SKILL.md 文件不存在"))
        score -= 40
        return {"score": score, "issues": issues}
    
    # 2. 解析 frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        issues.append(("P0", "frontmatter 不在文件开头"))
        score -= 20
    
    try:
        # 提取 YAML
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1])
            
            # 3. 检查必填字段
            if "name" not in fm:
                issues.append(("P0", "缺少 name 字段"))
                score -= 20
            
            if "description" not in fm:
                issues.append(("P0", "缺少 description 字段"))
                score -= 20
            
            # 4. 检查描述质量
            desc = fm.get("description", "")
            if len(desc) < 30:
                issues.append(("P1", "description 过短"))
                score -= 10
            
            # 5. 检查版本
            version = fm.get("version")
            if not version:
                issues.append(("P2", "缺少 version 字段"))
                score -= 5
            
            # 6. 检查废弃标记
            if fm.get("deprecated"):
                issues.append(("INFO", "Skill 已标记为废弃"))
            
    except Exception as e:
        issues.append(("P0", f"YAML 解析错误: {e}"))
        score -= 30
    
    # 7. 检查文件更新时间
    mod_time = datetime.fromtimestamp(skill_md.stat().st_mtime)
    days_old = (datetime.now() - mod_time).days
    
    if days_old > 180:
        issues.append(("P2", f"{days_old}天未更新"))
        score -= 5
    
    return {
        "score": max(0, score),
        "issues": issues,
        "days_old": days_old
    }

def main():
    """主函数"""
    skills_dir = Path.home() / ".codeflicker" / "skills"
    
    print("🔍 Skill 健康检查")
    print("=" * 60)
    
    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            result = check_skill_health(skill_path)
            
            # 打印结果
            score = result["score"]
            if score >= 80:
                emoji = "🟢"
                status = "健康"
            elif score >= 60:
                emoji = "🟡"
                status = "需关注"
            else:
                emoji = "🔴"
                status = "需优化"
            
            print(f"\n{emoji} {skill_path.name}")
            print(f"   健康度: {score}/100 ({status})")
            print(f"   最后更新: {result['days_old']}天前")
            
            if result["issues"]:
                print("   问题:")
                for priority, issue in result["issues"]:
                    print(f"     [{priority}] {issue}")

if __name__ == "__main__":
    main()
```

### B. 冲突检测脚本

```python
#!/usr/bin/env python3
"""
Skill 冲突检测脚本
"""

from pathlib import Path
import yaml
from difflib import SequenceMatcher

def extract_trigger_words(description):
    """从描述中提取触发词"""
    triggers = []
    
    # 查找 「...」 和 "..." 中的内容
    import re
    pattern = r'[「"](.*?)[」"]'
    matches = re.findall(pattern, description)
    triggers.extend(matches)
    
    return triggers

def calculate_similarity(text1, text2):
    """计算文本相似度"""
    return SequenceMatcher(None, text1, text2).ratio()

def check_conflicts(skills_dir):
    """检测 Skill 冲突"""
    
    skills = []
    
    # 读取所有 Skill
    for skill_path in Path(skills_dir).iterdir():
        if not skill_path.is_dir():
            continue
        
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue
        
        content = skill_md.read_text()
        parts = content.split("---", 2)
        
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                skills.append({
                    "name": fm.get("name", skill_path.name),
                    "description": fm.get("description", ""),
                    "path": skill_path,
                    "deprecated": fm.get("deprecated", False)
                })
            except:
                pass
    
    # 检测冲突
    conflicts = []
    
    for i, skill_a in enumerate(skills):
        for skill_b in skills[i+1:]:
            # 跳过已废弃的
            if skill_a["deprecated"] or skill_b["deprecated"]:
                continue
            
            # 检查描述相似度
            similarity = calculate_similarity(
                skill_a["description"],
                skill_b["description"]
            )
            
            if similarity > 0.6:
                conflicts.append({
                    "skill_a": skill_a["name"],
                    "skill_b": skill_b["name"],
                    "type": "description_overlap",
                    "similarity": similarity
                })
            
            # 检查触发词重叠
            triggers_a = extract_trigger_words(skill_a["description"])
            triggers_b = extract_trigger_words(skill_b["description"])
            
            common = set(triggers_a) & set(triggers_b)
            if common:
                conflicts.append({
                    "skill_a": skill_a["name"],
                    "skill_b": skill_b["name"],
                    "type": "trigger_overlap",
                    "common_triggers": list(common)
                })
    
    return conflicts

def main():
    """主函数"""
    skills_dir = Path.home() / ".codeflicker" / "skills"
    
    print("🔍 Skill 冲突检测")
    print("=" * 60)
    
    conflicts = check_conflicts(skills_dir)
    
    if not conflicts:
        print("\n✅ 未发现冲突")
        return
    
    print(f"\n⚠️ 发现 {len(conflicts)} 个潜在冲突:\n")
    
    for conflict in conflicts:
        print(f"📌 {conflict['skill_a']} ↔️ {conflict['skill_b']}")
        print(f"   类型: {conflict['type']}")
        
        if conflict["type"] == "description_overlap":
            print(f"   相似度: {conflict['similarity']:.1%}")
        elif conflict["type"] == "trigger_overlap":
            print(f"   重叠触发词: {', '.join(conflict['common_triggers'])}")
        
        print()

if __name__ == "__main__":
    main()
```

---

## 参考资料

- **案例来源**：
  - `knowledge-review` — 知识库健康管理
  - `skill-review` — Skill 审计工具
  - `writing-skills` — Skill 测试方法
  - `session-learning` — 版本演进示例
  - `meta-execution` — 质量保障框架

- **相关文档**：
  - [Semantic Versioning 2.0.0](https://semver.org/)
  - [Keep a Changelog](https://keepachangelog.com/)
  - Anthropic Best Practices

**最后更新**：2026-04-30  
**文档版本**：1.0.0  
**适用范围**：所有 Skill 类型
