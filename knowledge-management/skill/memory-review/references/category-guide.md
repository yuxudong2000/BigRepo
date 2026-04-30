# 记忆分类指南

---

## 分类说明

### User 维度（用户级）

与特定用户相关的记忆，跨项目通用。

| Category | 说明 | 典型内容 |
|:---------|:----|:--------|
| `user_info` | 用户基本信息 | 姓名、身份、角色、工号 |
| `user_hobby` | 用户爱好 | 兴趣、偏好的技术栈、喜欢的工具 |
| `user_communication` | 沟通偏好 | 语言、回复风格、表达习惯 |

### Repos 维度（仓库级）

与特定项目/仓库相关的记忆。

| Category | 说明 | 典型内容 |
|:---------|:----|:--------|
| `project_tech_stack` | 项目技术栈 | 使用的框架、语言、库 |
| `project_configuration` | 项目配置 | 构建配置、部署配置 |
| `project_environment_configuration` | 环境配置 | 开发/测试/生产环境设置 |
| `project_introduction` | 项目介绍 | 项目目的、架构概述 |
| `development_code_specification` | 代码规范 | 命名规则、格式要求、代码风格 |
| `development_practice_specification` | 开发实践 | 工作流程、最佳实践、设计原则 |
| `development_test_specification` | 测试规范 | 测试策略、覆盖率要求 |
| `development_comment_specification` | 注释规范 | 注释风格、文档要求 |
| `common_pitfalls_experience` | 踩坑经验 | 常见错误、问题解决方案 |
| `task_breakdown_experience` | 任务拆解 | 如何分解复杂任务 |
| `task_flow_experience` | 任务流程 | 工作流、触发条件、执行步骤 |
| `constraint_or_forbidden_rule` | 约束规则 | 禁止的操作、必须遵守的规则 |

---

## 分类匹配关键词

用于诊断「分类错配」问题：

| Category | 匹配关键词 |
|:---------|:----------|
| `user_info` | 用户、身份、个人、名字、姓名、角色 |
| `user_hobby` | 爱好、喜欢、偏好、兴趣 |
| `user_communication` | 沟通、表达、语言、风格、回复、中文、英文 |
| `project_tech_stack` | 技术栈、框架、语言、库、React、Vue、Python |
| `project_configuration` | 配置、config、build、构建、webpack、vite |
| `project_environment_configuration` | 环境、env、开发环境、测试环境、生产 |
| `project_introduction` | 项目、介绍、目的、架构、概述 |
| `development_code_specification` | 代码、格式、命名、风格、lint、ESLint |
| `development_practice_specification` | 实践、规范、原则、约定、流程 |
| `development_test_specification` | 测试、test、覆盖率、单测、集成测试 |
| `development_comment_specification` | 注释、文档、JSDoc、comment |
| `common_pitfalls_experience` | 问题、错误、bug、踩坑、陷阱、修复、解决 |
| `task_breakdown_experience` | 拆解、分解、子任务、步骤 |
| `task_flow_experience` | 流程、工作流、触发、执行、阶段、方法 |
| `constraint_or_forbidden_rule` | 禁止、约束、规则、不允许、必须、强制、不要 |

---

## 分类决策流程图

```
这条记忆是关于用户个人的吗？
├── 是 → 是基本信息、爱好还是沟通偏好？
│   ├── 基本信息 → user_info
│   ├── 爱好/偏好 → user_hobby
│   └── 沟通相关 → user_communication
└── 否 → 是关于项目的吗？
    ├── 是 → 是技术/配置还是开发规范？
    │   ├── 技术栈 → project_tech_stack
    │   ├── 项目配置 → project_configuration
    │   ├── 环境配置 → project_environment_configuration
    │   ├── 项目介绍 → project_introduction
    │   ├── 代码规范 → development_code_specification
    │   ├── 开发实践 → development_practice_specification
    │   ├── 测试规范 → development_test_specification
    │   └── 注释规范 → development_comment_specification
    └── 是经验/规则吗？
        ├── 踩坑经验 → common_pitfalls_experience
        ├── 任务拆解 → task_breakdown_experience
        ├── 任务流程 → task_flow_experience
        └── 禁止/约束 → constraint_or_forbidden_rule
```

---

## 边界案例处理

### "使用 TypeScript 时，必须定义接口类型"

- **问题**：是代码规范还是约束规则？
- **判断**：如果是「必须」的强制要求 → `constraint_or_forbidden_rule`；如果是推荐的最佳实践 → `development_code_specification`

### "调用 API 前先检查参数"

- **问题**：是开发实践还是踩坑经验？
- **判断**：如果来自一次具体的错误 → `common_pitfalls_experience`；如果是通用的设计原则 → `development_practice_specification`

### "用户喜欢简洁的回复"

- **问题**：是 user_hobby 还是 user_communication？
- **判断**：关于沟通方式 → `user_communication`；关于技术/工具偏好 → `user_hobby`

---

## 维度选择

| 场景 | 维度 |
|:----|:----:|
| 用户的个人偏好、身份信息 | user |
| 特定项目的配置、规范 | repos |
| 通用的开发经验（不绑定项目） | repos（默认） |
| 不确定时 | repos |
