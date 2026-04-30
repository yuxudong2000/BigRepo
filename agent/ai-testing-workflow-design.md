# AI Testing Workflow — Spec-Driven + DeepAgent 模式设计规范

**版本**: v1.0  
**日期**: 2026-04-24  
**作者**: zhangtao17  
**模式**: Spec-Driven Development + DeepAgent Orchestration

---

## 1. 概述

### 1.1 目标

构建一套由 AI Agent 全程驱动的自动化测试工作流（AI Testing Workflow），以 **Spec 文档** 为输入起点，通过多个专职 DeepAgent 协作完成从需求理解到覆盖率统计的全链路测试闭环，最终输出完整的测试报告与质量度量数据。

### 1.2 核心设计原则

| 原则 | 说明 |
|------|------|
| **Spec 驱动** | 所有 Agent 行为以 Spec 文档（PRD/接口文档/设计文档）为唯一输入源 |
| **DeepAgent 模式** | 每个阶段由独立 Agent 负责，Agent 可递归调用子 Agent 完成复杂任务 |
| **单向数据流** | 前一阶段产物作为后一阶段输入，形成有向无环图（DAG）流水线 |
| **可观测性** | 每个 Agent 产出结构化 JSON/Markdown 报告，供下游消费和人工 Review |
| **幂等重试** | 每个阶段支持独立重跑，失败不影响已完成阶段 |

---

## 2. Workflow 全局架构

```
Spec 输入层
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                           │
│  （调度中心：DAG 规划 / 阶段触发 / 结果聚合 / 异常处理）            │
└─────────────┬───────────────────────────────────────────────────┘
              │
    ┌─────────┴──────────────────────────────────────────────┐
    │                   Pipeline Stages                       │
    │                                                         │
    │  Stage 1: RequirementsAnalyzerAgent                    │
    │      ↓                                                  │
    │  Stage 2: TestStrategyAgent                            │
    │      ↓                                                  │
    │  Stage 3: TestCaseGeneratorAgent                       │
    │    ↙       ↘                                           │
    │  Stage 4   Stage 8a: TestDataBuilderAgent (UI)         │
    │  (链路分析)      ↓                                      │
    │    ↙    ↘   Stage 8: UITestAgent                       │
    │  Stage 5  Stage 7a: TestDataBuilderAgent (API)         │
    │  (缺陷)        ↓                                        │
    │           Stage 7: APITestAgent                        │
    │                 ↓                                      │
    │  Stage 9: CoverageReporterAgent (汇总 5+7+8)           │
    └─────────────────────────────────────────────────────────┘
              │
    ┌─────────▼─────────┐
    │  Final Report      │
    │  (HTML + JSON)     │
    └───────────────────┘
```

---

## 3. 各阶段 Agent 详细设计

### Stage 1 — RequirementsAnalyzerAgent（需求分析 Agent）

**职责**: 解析 Spec 文档，提取结构化需求信息。

**输入**:
- PRD 文档（Markdown / Confluence / Docs 链接）
- 接口文档（OpenAPI / Swagger YAML）
- UI 原型图（可选）

**行为**:
1. 读取并解析 Spec 文档全文
2. 抽取功能模块列表、用户故事、业务规则、边界条件
3. 识别模糊需求，生成 "需求澄清问题列表"
4. 输出结构化需求树（JSON）

**输出产物**:
```json
{
  "requirements": [
    {
      "id": "REQ-001",
      "module": "用户登录",
      "description": "...",
      "acceptance_criteria": ["...", "..."],
      "risk_level": "high | medium | low",
      "ambiguities": ["..."]
    }
  ],
  "modules": ["用户管理", "订单", "..."],
  "open_questions": ["..."]
}
```

---

### Stage 2 — TestStrategyAgent（测试策略生成 Agent）

**职责**: 基于需求分析结果，制定整体测试策略。

**输入**: Stage 1 产物 + 项目元信息（技术栈、团队规模、上线时间）

**行为**:
1. 评估各模块风险等级
2. 决定测试类型分配（单测 / 集成 / E2E / 性能 / 安全）
3. 确定测试优先级矩阵（重要性 × 复杂度）
4. 生成测试覆盖目标（行覆盖率 / 分支覆盖率 / 接口覆盖率）
5. 输出测试策略文档

**输出产物**:
```json
{
  "strategy": {
    "unit_test_target": "80%",
    "integration_test_target": "60%",
    "e2e_coverage": "核心流程 100%",
    "priority_matrix": [...],
    "risk_areas": ["支付模块", "权限校验"]
  }
}
```

---

### Stage 3 — TestCaseGeneratorAgent（测试用例生成 Agent）

**职责**: 依据需求和策略，自动生成结构化测试用例。

**输入**: Stage 1 产物 + Stage 2 产物

**行为**:
1. 对每个需求生成正向 / 反向 / 边界测试用例
2. 生成等价类和边界值覆盖用例
3. 为高风险模块生成场景测试用例（多步骤）
4. 输出 Gherkin（BDD）格式 + 表格格式双版本

**输出产物**:
```gherkin
Feature: 用户登录
  Scenario: 正常登录
    Given 用户在登录页
    When 输入正确的用户名和密码
    Then 跳转到首页并显示欢迎信息

  Scenario: 密码错误超过5次
    Given 用户在登录页
    When 连续输入错误密码5次
    Then 账号被锁定并提示联系管理员
```

---

### Stage 4 — CallChainAnalyzerAgent（代码链路分析 Agent）

**职责**: 静态分析代码库，建立功能模块与代码路径的映射关系。

**输入**: 代码仓库（Git URL / 本地路径）+ Stage 3 测试用例

**行为**:
1. 解析代码 AST，构建函数调用图（Call Graph）
2. 将测试用例映射到代码入口（Controller / Handler）
3. 追踪完整调用链路（Controller → Service → Repository → DB）
4. 识别未被测试覆盖的关键路径
5. 标注高风险代码路径（复杂度高、修改频繁）

**输出产物**:
```json
{
  "call_chains": [
    {
      "test_case_id": "TC-001",
      "entry_point": "UserController.login",
      "chain": ["AuthService.authenticate", "UserRepo.findByUsername", "PasswordUtil.verify"],
      "risk_score": 8.5,
      "uncovered_branches": ["UserRepo.findByUsername#L45"]
    }
  ]
}
```

---

### Stage 5 — DefectAnalyzerAgent（缺陷分析 Agent）

**职责**: 结合历史缺陷数据和代码静态分析，预测高风险缺陷区域。

**输入**: Stage 4 产物 + 历史 Bug 数据（Jira / 禅道导出）+ 代码变更记录（Git Diff）

**行为**:
1. 分析历史 Bug 模式（高频缺陷模块、缺陷类型分布）
2. 对 Git 变更文件进行缺陷风险评分
3. 识别常见缺陷模式（NPE、并发问题、SQL 注入等）
4. 输出缺陷热图和优先关注区域

**输出产物**:
```json
{
  "defect_predictions": [
    {
      "file": "src/service/OrderService.java",
      "risk_score": 9.2,
      "predicted_defect_types": ["NPE", "并发竞争"],
      "historical_bug_count": 12,
      "changed_in_current_sprint": true
    }
  ],
  "hotspot_summary": "支付模块变更量大，历史缺陷密度高，建议重点覆盖"
}
```

---

### Stage 7a — TestDataBuilderAgent（接口测试数据构造 Agent）

**职责**: 在接口测试执行前，依据链路分析结果构造接口测试所需的基础数据。

**输入**: Stage 4 链路分析结果 + Stage 3 测试用例 + 测试环境配置

**行为**:
1. 解析测试用例中的数据依赖（用户账号、订单、权限角色等）
2. 结合链路分析中的高风险路径，补充构造对应的边界数据
3. 调用测试环境数据构造接口或直接写入数据库生成基础数据
4. 生成数据快照，确保测试可重复执行
5. 输出数据 ID 映射表，供 Stage 7 注入测试参数

**输出产物**:
```json
{
  "test_data_snapshot": {
    "users": [{"id": "u001", "role": "admin", "token": "..."}],
    "orders": [{"id": "o001", "status": "pending"}]
  },
  "cleanup_script": "teardown.sql"
}
```

---

### Stage 7 — APITestAgent（接口测试用例生成及执行 Agent）

**职责**: 基于 OpenAPI Spec 自动生成并执行接口测试。

**输入**: OpenAPI / Swagger YAML + Stage 2 测试策略 + **Stage 4 链路分析结果** + **Stage 7a 测试数据快照** + 测试环境配置

**子 Agent**:
- `APITestGeneratorSubAgent`: 生成测试脚本（Python pytest / Postman Collection）
- `APITestRunnerSubAgent`: 执行测试并收集结果
- `APITestReporterSubAgent`: 生成测试报告

**行为**:
1. 解析所有 API 端点（path、method、参数、响应 schema）
2. **读取 Stage 4 调用链路图**，识别高风险接口路径和未覆盖分支
3. 优先为高风险链路上的接口生成更细粒度的测试用例（含链路上下游参数联动）
4. 生成正常 / 异常 / 边界值测试用例
5. 生成认证 / 鉴权测试用例
6. 执行测试，收集响应状态码、响应时间、响应体校验结果
7. 统计接口覆盖率（含链路级覆盖率）

**输出产物**:
- `api_test_cases.json`：生成的接口测试用例
- `api_test_report.html`：执行结果报告
```json
{
  "total_apis": 45,
  "tested_apis": 43,
  "pass": 38,
  "fail": 5,
  "coverage": "95.6%",
  "failures": [...]
}
```

---

### Stage 8a — TestDataBuilderAgent（UI 测试数据构造 Agent）

**职责**: 与 Stage 4 并行，为 E2E UI 测试提前构造页面所需基础数据。

**输入**: Stage 3 测试用例（E2E 场景）+ 测试环境配置

**行为**:
1. 解析 E2E 场景中的数据依赖（登录账号、页面展示所需数据等）
2. 调用测试环境数据构造接口或直接写入数据库生成基础数据
3. 生成数据快照，确保测试可重复执行
4. 输出数据 ID 映射表，供 Stage 8 注入测试参数

**输出产物**:
```json
{
  "test_data_snapshot": {
    "users": [{"id": "u002", "role": "buyer", "token": "..."}],
    "products": [{"id": "p001", "name": "示例商品"}]
  },
  "cleanup_script": "teardown_ui.sql"
}
```

---

### Stage 8 — UITestAgent（UI 测试脚本生成及执行验证 Agent）

**职责**: 基于需求和 UI 原型，生成并执行 E2E UI 自动化测试。

**输入**: Stage 3 测试用例（E2E 场景）+ **Stage 8a 测试数据构造结果** + UI 原型图 / 页面 URL + 测试环境配置

**子 Agent**:
- `UIScriptGeneratorSubAgent`: 生成 Playwright / Cypress 测试脚本
- `UITestRunnerSubAgent`: 执行 E2E 测试，截图记录
- `UITestValidatorSubAgent`: 校验页面元素、交互行为、视觉回归

**行为**:
1. 解析 E2E 测试场景，生成页面操作序列
2. 生成 Playwright TypeScript 测试脚本
3. 在 Headless 浏览器中执行测试
4. 截图记录关键步骤
5. 校验页面元素存在性、文本内容、导航结果

**输出产物**:
- `ui_test_scripts/`: 生成的 Playwright 脚本
- `ui_test_report.html`: 执行报告（含截图）
```json
{
  "total_scenarios": 20,
  "pass": 17,
  "fail": 3,
  "pass_rate": "85%",
  "screenshots": ["login_success.png", "..."]
}
```

---

### Stage 9 — CoverageReporterAgent（覆盖率统计 Agent）

**职责**: 汇总前端和后端代码覆盖率，生成综合覆盖率报告。

**输入**: 
- 后端覆盖率数据（JaCoCo XML / Istanbul JSON）
- 前端覆盖率数据（Istanbul / V8 Coverage JSON）
- Stage 7 / Stage 8 执行结果

**行为**:
1. 解析后端覆盖率（行 / 分支 / 方法覆盖率）
2. 解析前端覆盖率（语句 / 函数 / 分支覆盖率）
3. 与 Stage 2 覆盖目标对比，标记 Gap
4. 生成模块级覆盖率热图
5. 输出最终综合报告

**输出产物**:
```json
{
  "backend_coverage": {
    "line": "78.5%",
    "branch": "65.2%",
    "method": "82.1%",
    "target_met": false,
    "gap_modules": ["支付服务", "消息推送"]
  },
  "frontend_coverage": {
    "statement": "85.3%",
    "function": "79.8%",
    "branch": "71.2%",
    "target_met": true
  },
  "overall_quality_score": 76,
  "recommendations": ["增加支付模块单测", "补充消息推送异常路径测试"]
}
```

---

## 4. Orchestrator Agent 设计

Orchestrator 是整个 Workflow 的调度大脑，负责：

### 4.1 DAG 执行计划

```
Stage 1 (需求分析)
    └──→ Stage 2 (测试策略)
             └──→ Stage 3 (用例生成)
                      ├──→ Stage 4 (链路分析) ──┬──→ Stage 5 (缺陷分析) ──────────────┐
                      │                         └──→ Stage 7a (测试数据构造-API)        │
                      │                                      └──→ Stage 7 (接口测试) ───┤
                      └──→ Stage 8a (测试数据构造-UI)                                   │
                                     └──→ Stage 8 (UI 测试) ───────────────────────────┤
                                                                                         ▼
                                                                              Stage 9 (覆盖率汇总)
```

**并行策略**: Stage 3 完成后，Stage 4（链路分析）和 Stage 8a（测试数据构造-UI）并行启动；Stage 4 完成后，Stage 5（缺陷分析）和 Stage 7a（测试数据构造-API）并行启动；Stage 7a 完成后启动 Stage 7（接口测试），Stage 8a 完成后启动 Stage 8（UI 测试）；Stage 9 等待 Stage 5、7、8 全部完成后汇总。

### 4.2 状态管理

```json
{
  "workflow_id": "wf-20260424-001",
  "status": "running | completed | failed | paused",
  "stages": {
    "stage_1": { "status": "completed", "duration_s": 45, "artifact_path": "..." },
    "stage_2": { "status": "completed", "duration_s": 30, "artifact_path": "..." },
    "stage_3": { "status": "running", "started_at": "...", "artifact_path": null },
    "stage_4": { "status": "pending" }
  }
}
```

### 4.3 异常处理策略

| 场景 | 处理策略 |
|------|---------|
| 单阶段失败 | 自动重试 3 次，失败后暂停并通知人工介入 |
| 输入数据不完整 | 降级执行（跳过依赖数据的子任务，标记为 N/A） |
| 外部服务超时 | 指数退避重试，超过阈值后熔断 |
| Agent 输出不满足 schema | 触发修复子 Agent 重新生成 |

---

## 5. Agent 交互协议

### 5.1 标准 Agent 接口

每个 Agent 遵循统一的接口规范：

```typescript
interface AgentInput {
  workflow_id: string;
  stage_id: string;
  spec: SpecDocument;         // 原始 Spec 文档（始终携带）
  upstream_artifacts: Record<string, Artifact>;  // 上游产物
  config: StageConfig;        // 阶段配置参数
}

interface AgentOutput {
  stage_id: string;
  status: "success" | "failure" | "partial";
  artifacts: Artifact[];
  metrics: Record<string, number | string>;
  human_review_required: boolean;
  next_stage_hints: string[];  // 给下游 Agent 的提示
}
```

### 5.2 Spec 文档格式规范

所有阶段始终携带原始 Spec，格式：

```yaml
spec:
  type: prd | openapi | design_doc
  source_url: "https://docs.corp.example.com/spec/xxx"
  content: |
    # 功能需求
    ...
  attachments:
    - type: openapi
      path: "./api/openapi.yaml"
    - type: ui_prototype
      path: "./design/figma-export.png"
```

---

## 6. 人工审查节点（Human-in-the-Loop）

Workflow 在以下节点默认暂停，等待人工确认后继续：

| 节点 | 审查内容 | 可跳过 |
|------|---------|--------|
| Stage 1 → Stage 2 | 需求分析结果 + 需求澄清问题 | 是（CI 模式） |
| Stage 2 → Stage 3 | 测试策略文档 | 是（CI 模式） |
| Stage 9 完成后 | 覆盖率未达标时的决策 | 否（需人工批准发布） |

---

## 7. 工具依赖清单

| Agent | 所需工具/服务 |
|-------|-------------|
| RequirementsAnalyzerAgent | LLM（GPT-4 / Claude）, 文档读取 API |
| TestStrategyAgent | LLM |
| TestCaseGeneratorAgent | LLM, Gherkin Parser |
| CallChainAnalyzerAgent | AST 解析器（tree-sitter）, 代码仓库访问 |
| DefectAnalyzerAgent | LLM, Jira API / Git API |
| TestDataBuilderAgent | 数据库客户端, 测试环境 API, 数据快照工具 |
| APITestAgent | LLM, pytest / Postman, 测试环境网络 |
| UITestAgent | LLM, Playwright, Headless Chrome |
| CoverageReporterAgent | JaCoCo / Istanbul, 覆盖率数据收集工具 |
| Orchestrator | 消息队列（可选）, 状态存储（SQLite / Redis）|

---

## 8. 最终报告结构

Workflow 完成后输出统一的综合报告：

```
ai-testing-report/
├── index.html                    # 综合 Dashboard
├── 01-requirements-analysis.md  # 需求分析报告
├── 02-test-strategy.md          # 测试策略文档
├── 03-test-cases.md             # 测试用例清单（Gherkin）
├── 04-call-chain-analysis.json  # 代码链路分析
├── 05-defect-prediction.md      # 缺陷预测报告
├── 06-test-data-snapshot.json   # 测试数据快照
├── 07-api-test-report.html      # 接口测试报告
├── 08-ui-test-report.html       # UI 测试报告（含截图）
└── 09-coverage-summary.html     # 覆盖率综合报告
```

---

## 9. 实施路径建议

### Phase 1 — 核心链路（MVP）
实现 Stage 1 → 2 → 3 → 7 → 9（后端），验证 Spec 驱动的基础流水线。

### Phase 2 — 深度分析
加入 Stage 4（链路分析）+ Stage 5（缺陷分析）+ Stage 6（测试数据构造）。

### Phase 3 — 全链路
实现 Stage 8（UI 测试）+ 覆盖率全面统计 + Orchestrator 完整状态机。

### Phase 4 — 智能化增强
- Agent 间反馈回路（下游失败反哺上游用例补充）
- 基于历史 Workflow 数据的策略优化
- 与 CI/CD 系统深度集成（GitHub Actions / Jenkins）

---

*文档版本: v1.0 | 状态: Draft | 下一步: 转入 writing-plans 制定实施计划*
