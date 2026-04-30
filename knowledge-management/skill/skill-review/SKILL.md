---
name: claw-skill-review
description: 扫描并审计系统中所有已安装的 skill，生成完整清单，检测错误、冲突与冗余，给出更新或删除建议。当用户说「审计 skill」「扫描 skill」「检查所有技能」「skill 有没有问题」「哪些 skill 可以删掉」「skill 冲突检测」「skill 清单」时触发。不负责 skill 的具体创建/更新/删除操作（交由 skill-manager 执行）。
version: 1.0.0
---

# Skill 全量审计工具

你是 Skill 审计专家。你的目标是对当前系统中所有已安装的 skill 进行全面扫描，输出结构化清单，并识别需要更新或删除的问题 skill。

---

## 第一步：扫描所有 Skill 目录

依次扫描以下目录，收集所有 skill 的基础信息：

### 个人级 Skill（Personal）
```bash
ls ~/.codeflicker/skills/
ls ~/.codeflicker/internal/skills/
```
> 也可能存在于：`~/.cursor/skills/`、`~/.claude/skills/`、`~/.codex/skills/`

### 项目级 Skill（Project）
```bash
ls {project_root}/.codeflicker/skills/
```

### 系统内置 Skill（Internal）
直接从 agent 上下文的 `<available_skills>` 列表中获取，无需手动扫描。

**扫描规则**：
- 每个 skill 目录下必须有 `SKILL.md` 文件
- 读取 `SKILL.md` 的 YAML frontmatter 提取：`name`、`description`、`version`
- 记录 skill 的来源路径（用于后续定位问题）

---

## 第二步：输出完整 Skill 清单

以分组方式展示：

```
## 📋 Skill 全量清单

### 🏠 个人级 Skill（Personal）— ~/.codeflicker/skills/
| # | 名称 | 版本 | 描述摘要 | 路径 |
|---|------|------|----------|------|
| 1 | skill-name | v1.0.0 | 描述前50字... | ~/.codeflicker/skills/skill-name |

### 🏢 系统内置 Skill（Internal）— ~/.codeflicker/internal/skills/
| # | 名称 | 版本 | 描述摘要 |
|---|------|------|----------|

### 📁 项目级 Skill（Project）— .codeflicker/skills/
| # | 名称 | 版本 | 描述摘要 |
|---|------|------|----------|

**统计：个人级 X 个 / 内置 X 个 / 项目级 X 个 / 合计 X 个**
```

---

## 第三步：问题检测

对每个 skill 逐一执行以下检测，输出问题报告：

### 检测项 1：YAML 格式错误
- `SKILL.md` 中 YAML frontmatter 是否以 `---` 开头（必须是文件第一行）
- 是否包含必填字段：`name`、`description`
- `name` 是否符合 kebab-case 格式
- 路径中的目录名与 `name` 字段是否一致

### 检测项 2：描述质量问题
- `description` 是否包含明确的触发场景（关键词/触发句）
- `description` 是否过于简短（< 30字）或过于通用（如"通用工具"、"万能助手"）
- `description` 是否缺少"不适用场景"的说明（会导致误触发）

### 检测项 3：Skill 间冲突与重叠
逐对比较所有 skill 的 `description`，检测：

**冲突类型 A：触发词重叠**
- 两个 skill 的触发词语义相同或高度相似（例如两个都响应"生成图片"）
- 优先级不明确时用户会随机触发其中之一

**冲突类型 B：功能范围重叠**
- 两个 skill 的核心功能几乎完全相同（如两个"代码审查"类 skill）
- 建议合并或明确分工

**冲突类型 C：已废弃/迁移声明**
- description 中明确说明"已废弃"、"请使用 X 替代"的 skill（例如 `cf-web-artifacts`、`session-summary`）
- 这类 skill 可以直接标记为"建议删除"

### 检测项 4：路径与目录问题
- 是否存在 SKILL.md 文件（目录存在但文件缺失）
- 脚本路径引用是否使用了 `$HOME` 或硬编码绝对路径（应使用 `<skill_directory>` 占位符）

### 检测项 5：版本过时判断
- 若 skill 版本为 `1.0.0` 且内容极少（< 200字），标记为"可能未完成"
- 若与同功能的更新版 skill 共存，标记为"可能冗余"

---

## 第四步：输出问题报告

```
## 🔍 问题检测报告

### ❌ 严重问题（需立即修复）
| skill 名称 | 问题类型 | 问题描述 | 建议操作 |
|-----------|---------|---------|---------|
| xxx-skill | YAML格式错误 | frontmatter 不在文件开头 | 更新 |

### ⚠️ 冲突/重叠（建议处理）
| skill A | skill B | 冲突类型 | 重叠内容 | 建议 |
|---------|---------|---------|---------|-----|
| cf-web-artifacts | website-builder | 功能重叠 | 两者均构建静态网页... | 删除A，保留B |

### 🗑️ 建议删除
| skill 名称 | 删除原因 |
|-----------|---------|
| session-summary | description 明确标注"已废弃，请使用 self-learning" |

### 💡 建议优化（可选）
| skill 名称 | 问题 | 优化建议 |
|-----------|-----|---------|
| xxx-skill | description 无触发词 | 补充「当用户说...时使用」 |

### ✅ 健康 Skill
共 X 个 skill 未发现问题，状态良好。
```

---

## 第五步：给出行动建议

根据问题报告，按优先级输出 TODO 列表：

```
## 📌 行动建议（按优先级）

**P0 - 立即处理**
- [ ] 修复 [skill-name] 的 YAML 格式错误
- [ ] 删除已明确废弃的 [skill-name]

**P1 - 建议处理**
- [ ] 合并/区分 [skill-A] 和 [skill-B]（功能重叠）
- [ ] 更新 [skill-name] 的 description，补充触发场景

**P2 - 可选优化**
- [ ] 为 [skill-name] 添加「不适用场景」说明
```

询问用户：「是否需要我帮你执行以上操作？（可调用 skill-manager 完成更新/删除）」

---

## 执行规则

1. **只读扫描，不自动修改**：本 skill 仅负责分析和报告，不直接修改任何 skill 文件
2. **禁止操作内置目录**：`~/.codeflicker/internal/skills/` 为只读，不建议删除内置 skill
3. **删除需二次确认**：所有删除建议都必须经用户明确确认后，再调用 skill-manager 执行
4. **优先使用 available_skills 上下文**：系统提示词中的 `<available_skills>` 已包含当前加载的 skill 列表，优先用于冲突检测，减少文件系统扫描
5. **报告格式简洁**：问题少时直接列出，问题多时按严重程度分组，避免信息过载

---

## 快速命令参考

扫描个人级 skill 目录：
```bash
ls -la ~/.codeflicker/skills/
ls -la ~/.codeflicker/internal/skills/
```

读取某个 skill 的 frontmatter：
```bash
head -10 ~/.codeflicker/skills/{skill-name}/SKILL.md
```

检查 description 字段：
```bash
grep -A2 "^description:" ~/.codeflicker/skills/{skill-name}/SKILL.md
```
