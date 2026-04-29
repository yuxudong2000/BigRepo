# 知识库分类写入规则

> 各分类的写入条件、文件命名、格式模板。AI 执行 self-learning skill 时严格遵守本文件。

---

## 总原则

1. **只写可复用内容**：纯过程性、一次性内容留在 `sessions/`，不重复搬运
2. **追加优先于新建**：同主题已有文件时，在文件末尾追加，标注日期
3. **文件名要有语义**：用连字符分隔的 slug，如 `frontend-cloud-cli-deploy.md`
4. **格式统一**：每个条目顶部有 `## [YYYY-MM-DD] <来源 session slug>` 标注来源

---

## § solutions — 解法库

**写入条件**：当对话中产生了可复用的**问题-解法对**（可复用性 ≥ 中）

**什么算"可复用性 ≥ 中"**：
- 下次遇到同类问题可直接参考
- 解法涉及特定工具/API/配置组合

**文件命名**：`solutions/<问题关键词>.md`，如 `solutions/gitignore-ds-store.md`

**文件格式**：
```markdown
# <问题标题>

## [YYYY-MM-DD] 来自 <session-slug>

### 问题
<问题描述 1-3 句>

### 解法
<具体操作步骤或命令>

### 注意事项
- <踩坑点或限制>
```

---

## § tools — 工具经验库

**写入条件**：当对话涉及某工具的**踩坑、最佳实践、正确用法**（具有泛化价值）

**排除**：仅"使用了该工具"的过程性记录，无踩坑或技巧则不写

**文件命名**：`tools/<工具名>.md`，如 `tools/frontend-cloud-cli.md`

**文件格式**：
```markdown
# <工具名> 使用经验

## [YYYY-MM-DD] 来自 <session-slug>

### 正确用法
<命令或调用方式>

### 常见错误
- 错误：`xxx`
- 原因：xxx
- 修复：`yyy`

### 最佳实践
- <技巧点>
```

---

## § patterns — 可复用执行模式

**写入条件**：当对话展示了一个**可跨对话复用的执行流程**（步骤序列有通用价值）

**文件命名**：`patterns/<模式名>.md`，如 `patterns/locate-then-read.md`

**文件格式**：
```markdown
# <模式名>

> 适用场景：<一行描述>

## [YYYY-MM-DD] 来自 <session-slug>

### 流程
1. Step 1：<操作>
2. Step 2：<操作>
...

### 为什么有效
<模式的核心价值>

### 注意事项
- <限制或变体>
```

---

## § insights — 深度洞察

**写入条件**：当对话产生**超出单次任务的认知发现**，如架构理解、技术规律、认知升级

**文件命名**：`insights/<主题关键词>.md`，如 `insights/static-site-deploy-workflow.md`

**文件格式**：
```markdown
# <洞察标题>

## [YYYY-MM-DD] 来自 <session-slug>

### 洞察
<3-6 句，阐述发现的规律或认知>

### 支撑证据
- <来自对话的具体观察>

### 推论/应用
- <下次如何利用这个认知>
```

---

## § memories — 记忆候选库

**写入条件**：当对话中发现**值得写入 Agent Memory 的信息**（用户偏好、项目规范、规律性行为等）

**⚠️ 特别说明**：此目录仅存放**候选项**，AI **不执行** `update_memory`，由用户决定

**文件命名**：`memories/YYYY-MM-DD_memories.md`（按日期聚合，同一天追加）

**文件格式**：
```markdown
# 记忆候选 YYYY-MM-DD

## 来自 <session-slug>

- [ ] **[<category>]** <记忆内容>（建议写入理由：xxx）
- [ ] **[<category>]** <记忆内容>
```

**category 参考**：`user_info` / `project_configuration` / `development_practice_specification` / `development_code_specification` / `common_pitfalls_experience` / `constraint_or_forbidden_rule`

---

## § rules — 规则与约束库

**写入条件**：当对话确认了**操作规范、禁止项、强制要求**（用户明确说明或通过多次交互形成的隐性约定）

**文件命名**：`rules/<规则域>.md`，如 `rules/git-workflow.md`、`rules/file-deletion.md`

**文件格式**：
```markdown
# <规则域> 规则

## [YYYY-MM-DD] 来自 <session-slug>

### 规则
- ✅ MUST：<必须做的>
- ❌ MUST NOT：<禁止做的>
- ⚠️ SHOULD：<建议做的>

### 背景
<规则的来源或原因>
```

---

## § skills — Skill 化流程发现

**写入条件**：当对话中出现**高度重复或值得封装为 CodeFlicker skill 的操作流程**

**文件命名**：`skills/<流程名>.md`，如 `skills/deploy-static-site.md`

**文件格式**：
```markdown
# <Skill 候选名>

## [YYYY-MM-DD] 来自 <session-slug>

### 触发场景
<什么情况下需要这个 skill>

### 核心流程
1. <步骤>
2. <步骤>

### 关键决策点
- <需要用户确认或 AI 判断的地方>

### 成熟度评估
- 复用频率预估：低 / 中 / 高
- 封装优先级：低 / 中 / 高
- 当前状态：💡 想法 / 📝 草稿 / ✅ 可落地
```
