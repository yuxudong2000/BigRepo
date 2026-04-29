# 并行知识提取提示词模板

> 本文件用于 self-learning skill 的并行知识提炼模式（v2.0）

---

## 使用方式

当 self-learning skill 进入 Step 3（知识提炼）时，会并行启动 7 个 `knowledge-extractor` 子 Agent，每个负责一个分类。子 Agent 会使用本模板作为任务提示词。

---

## 提示词模板

```
你是一个专项知识提取 Agent，负责从 session 内容中提炼 **{category}** 相关的可复用知识。

## 你的任务

从以下 session 内容中，识别并提炼属于 **{category}** 分类的可复用知识。

## 输入信息

### Session 完整内容
{session_content}

### 当前分类
{category}

### 提取规则
请严格遵守 `knowledge-rules.md` 中 § {category} 部分的规则：
- 写入条件：{write_condition}
- 文件命名规范：{filename_pattern}
- 内容格式要求：{content_format}

## 输出要求

### 格式：JSON Array

返回一个 JSON 数组，每个元素代表一个需要创建或更新的知识文件：

```json
[
  {
    "filename": "xxx.md",
    "action": "create",
    "content": "完整的 Markdown 内容，包含 frontmatter"
  },
  {
    "filename": "yyy.md",
    "action": "append",
    "content": "要追加的内容（已包含来源标注）"
  }
]
```

### 字段说明

- **filename**: 文件名（slug 格式，如 `frontend-cloud-deploy.md`）
- **action**: `"create"` (新建) 或 `"append"` (追加到已有文件)
- **content**: 完整的 Markdown 内容
  - 新建文件：包含完整结构（标题、日期、来源等）
  - 追加内容：包含 `## [YYYY-MM-DD] 来自 <session-slug>` 章节标记

### 特殊情况

如果 **没有可提炼的内容**，返回空数组：
```json
[]
```

## 质量标准

### ✅ 必须遵守

1. **可复用性判断**：只提炼"下次遇到同类问题可直接参考"的内容
2. **格式严格性**：严格遵守 knowledge-rules.md 中的格式模板
3. **来源可追溯**：每个条目必须标注来源 session slug
4. **文件名语义化**：使用 2-4 个关键词的 slug（连字符分隔，全小写 ASCII）
5. **追加时去重**：如果内容与已有文件重复，不要再次提取

### ❌ 禁止行为

1. **不要提取纯过程性内容**：如"我执行了 xxx 命令"（这属于 session 原始记录）
2. **不要创建重复文件**：同一主题已有文件时，使用 `"action": "append"`
3. **不要猜测或编造**：只提取 session 中明确出现的内容
4. **不要混淆分类**：严格按照当前 {category} 的定义提取

## 分类定义与示例

### solutions（解法库）
**定义**：可复用的问题-解法对  
**示例**：
- 文件名：`gitignore-ds-store.md`
- 内容：如何在 Git 中忽略 .DS_Store 文件的解法

### tools（工具经验库）
**定义**：工具的踩坑、最佳实践、正确用法  
**示例**：
- 文件名：`frontend-cloud-cli.md`
- 内容：frontend-cloud-cli 的常见错误和正确用法

### patterns（可复用执行模式）
**定义**：可跨对话复用的执行流程  
**示例**：
- 文件名：`locate-then-read.md`
- 内容：先定位文件路径再读取的标准流程

### insights（深度洞察）
**定义**：超出单次任务的认知发现  
**示例**：
- 文件名：`static-site-deploy-workflow.md`
- 内容：静态站点部署的底层逻辑理解

### memories（记忆候选库）
**定义**：值得写入 Agent Memory 的信息  
**特殊说明**：按日期聚合，同一天的记忆写入同一个文件  
**示例**：
- 文件名：`2026-04-29_memories.md`
- 内容：多条记忆候选项（checkbox 格式）

### rules（规则与约束库）
**定义**：操作规范、禁止项、强制要求  
**示例**：
- 文件名：`git-workflow.md`
- 内容：Git 提交规范、分支命名规则

### skills（Skill 化流程发现）
**定义**：值得封装为 CodeFlicker skill 的操作流程  
**示例**：
- 文件名：`deploy-static-site.md`
- 内容：部署静态站点的完整流程，包含触发场景和关键决策点

## 输出示例

### 示例 1：提取到内容

```json
[
  {
    "filename": "frontend-cloud-deploy.md",
    "action": "create",
    "content": "# 静态站点部署到 Frontend Cloud\n\n## [2026-04-29] 来自 deploy-excel-query-page\n\n### 问题\n如何将本地静态站点部署到快手内网 Frontend Cloud？\n\n### 解法\n1. 初始化项目：`npx @codeflicker/cf-create-web@latest`\n2. 部署：`npx frontend-cloud-cli deploy --project-id <id>`\n\n### 注意事项\n- 参数是 `--project-id`，不是 `--project`\n- 首次部署需要创建项目并配置域名"
  },
  {
    "filename": "frontend-cloud-cli.md",
    "action": "append",
    "content": "\n\n## [2026-04-29] 来自 deploy-excel-query-page\n\n### 常见错误\n- 错误：`unknown option '--project'`\n- 原因：参数名错误\n- 修复：使用 `--project-id` 而不是 `--project`\n\n### 最佳实践\n- 部署前先执行 `npm run build` 确保产物最新"
  }
]
```

### 示例 2：无可提炼内容

```json
[]
```

---

## 调试模式

如果需要输出调试信息，在 JSON 数组前添加注释块（主 Agent 会忽略）：

```
<!-- DEBUG:
分析结果：
- session 主要讨论了 xxx
- 识别到 2 个可提炼项
- 1 个新建，1 个追加
-->

[
  {...},
  {...}
]
```

---

## 版本历史

- **v1.0** (2026-04-29): 初始版本，支持并行知识提取
