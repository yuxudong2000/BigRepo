# 显式依赖原则

> **一句话定义**: 操作结果应只依赖显式参数，不依赖隐式状态

---

## 元信息

| 属性 | 值 |
|------|---|
| **原则名称（中文）** | 显式依赖原则 |
| **原则名称（英文）** | Explicit Dependency Principle |
| **首次提出** | 2026-04-29 from self-learning skill 优化 session |
| **抽象层级** | Layer 5 (通用原则 / Wisdom) |
| **验证案例数** | 1 个（初始版本，待扩充） |
| **最后更新** | 2026-04-29 |

---

## 根本问题

### 这个原则解决什么问题？

**核心问题**：当操作结果依赖于未显式声明的状态（如当前工作目录、环境变量、系统配置、时区等）时，会导致行为不确定、难以预测、难以调试、难以测试。

**问题本质**：
- **不可预测性**：同一操作在不同环境/时间/状态下产生不同结果
- **隐式耦合**：操作与执行环境之间存在隐藏的依赖关系
- **认知负担**：使用者需要额外了解隐式依赖才能正确使用

**为什么会发生**：
- **理论基础**: 违反了函数式编程的"引用透明性"原则 — 相同输入应产生相同输出
- **心智模型缺陷**: 开发者通常假设"默认行为"是确定的，忽略了执行环境的差异性
- **系统性原因**: 工具设计追求"便利性"而非"明确性"，允许依赖隐式状态以减少参数数量

---

## 历史案例

### 案例 1: Skill 优化路径混淆问题

**来源**: [session] self-learning skill 优化 | [root-cause] 待生成  
**日期**: 2026-04-29  
**问题**: 优化 self-learning skill 时，Agent 在错误路径（/hermes-agent 仓库）验证文件，而实际文件在 ~/.codeflicker/skills/  
**根因**: 文件操作依赖隐式的 `cwd`（当前工作目录），用户指令"优化 skill"存在上下文歧义  
**原则应用**: 如果文件操作使用绝对路径而非相对路径，或在执行前显式确认目标路径，可避免此问题

### 案例 2: npm registry 配置问题（预期扩展）

**来源**: 未来归档  
**日期**: TBD  
**问题**: npm install 在不同环境报 Access Denied 错误  
**根因**: npm 依赖隐式的 registry 配置（环境变量或全局配置）  
**原则应用**: 如果在 package.json 或 .npmrc 中显式声明 registry，或在命令中显式指定 `--registry`，可避免环境差异

### 案例 3: 时区处理错误（预期扩展）

**来源**: 未来归档  
**日期**: TBD  
**问题**: 时间计算结果在不同地区不一致  
**根因**: 时间处理依赖系统时区设置  
**原则应用**: 显式传递时区参数（如 `datetime.now(tz=timezone.utc)`），而非依赖 `datetime.now()`

---

## 原则内容

### 核心主张

**任何操作（函数、API、命令、工具）的结果应该是确定性的，只依赖于显式传递的参数，而不依赖于执行时的隐式状态。**

**三个关键要素**：
1. **确定性**: 相同的显式输入 → 相同的输出（无论在何时何地执行）
2. **可追溯性**: 所有依赖关系都在参数列表中可见
3. **可控性**: 调用者可以完全控制操作行为，无需修改全局状态

### 实践检查清单

在设计/开发/审查时，使用以下清单检查是否遵守此原则：

- [ ] **文件路径**: 使用绝对路径而非相对路径，或显式传递 `base_dir` 参数
- [ ] **环境变量**: 显式传递配置参数，不直接读取 `os.getenv()`
- [ ] **时间处理**: 显式传递时区参数，不依赖系统时区
- [ ] **编码处理**: 显式指定 charset（如 `encoding="utf-8"`），不依赖系统默认编码
- [ ] **API 调用**: 显式传递所有必需参数（API key、endpoint 等），不依赖全局配置
- [ ] **配置读取**: 显式传递配置文件路径，不依赖"约定优于配置"的默认路径

### 反模式（何时违反）

识别和避免以下反模式：

#### ❌ 反模式 1: 依赖相对路径

**表现**：
```python
# 不推荐
with open("./config.yaml") as f:
    config = yaml.load(f)
```

**危害**：行为取决于 `cwd`，换个目录执行就失败  
**纠正**：
```python
# 推荐
config_path = Path(__file__).parent / "config.yaml"
with open(config_path) as f:
    config = yaml.load(f)
```

#### ❌ 反模式 2: 隐式读取环境变量

**表现**：
```python
# 不推荐
def call_api():
    api_key = os.getenv("API_KEY")
    return requests.get(url, headers={"Authorization": api_key})
```

**危害**：依赖环境变量设置，换个环境（Docker、CI、本地）行为不同  
**纠正**：
```python
# 推荐
def call_api(api_key: str):
    return requests.get(url, headers={"Authorization": api_key})
```

#### ❌ 反模式 3: 依赖系统默认值

**表现**：
```python
# 不推荐
with open(file_path) as f:  # 编码依赖系统默认（Windows: GBK, Linux: UTF-8）
    content = f.read()
```

**危害**：跨平台不一致  
**纠正**：
```python
# 推荐
with open(file_path, encoding="utf-8") as f:
    content = f.read()
```

---

## 适用边界

### ✅ 适用场景

以下场景**强烈推荐**应用此原则：

1. **跨环境执行的代码**
   - 为什么适用: 不同环境的隐式状态（cwd、环境变量、系统配置）可能不同
   - 示例: CI/CD 脚本、Docker 容器、多人协作项目

2. **长期维护的系统**
   - 为什么适用: 隐式依赖会在时间推移中积累，导致"为什么以前能跑现在不能跑"的困惑
   - 示例: 核心业务逻辑、公共库、基础设施代码

3. **测试代码**
   - 为什么适用: 测试需要可重复执行，隐式依赖会导致测试不稳定（flaky tests）
   - 示例: 单元测试、集成测试、E2E 测试

### ❌ 不适用场景

以下场景**不推荐或禁止**应用此原则：

1. **一次性脚本（临时工具）**
   - 为什么不适用: 成本 > 收益，追求便利性优于稳定性
   - 替代方案: 在脚本开头注释说明依赖的隐式状态（如"需要在项目根目录执行"）

2. **配置文件约定**
   - 为什么不适用: 行业惯例（如 `.gitignore`, `package.json` 必须在项目根目录）
   - 替代方案: 遵循行业约定，但在文档中显式说明

### ⚠️ 权衡取舍

应用此原则时需要注意的权衡：

- **权衡 1**: **便利性 vs 明确性** — 显式传递参数会增加函数签名长度，降低便利性
  - **建议**: 优先保证明确性，通过合理的默认参数和配置对象来平衡便利性
  
- **权衡 2**: **向后兼容 vs 正确性** — 已有的依赖隐式状态的 API 修改成本高
  - **建议**: 新 API 严格遵守，旧 API 通过 deprecation warning 逐步迁移

- **权衡 3**: **参数数量 vs 可读性** — 过多显式参数会降低可读性
  - **建议**: 使用配置对象封装相关参数，或使用 Builder 模式

---

## 跨领域适用性

### 技术领域

| 领域 | 具体应用 | 示例 |
|------|---------|------|
| **文件系统** | 使用绝对路径 | `Path(__file__).parent / "data.json"` |
| **API 设计** | 显式传递认证信息 | `api.call(api_key="xxx", endpoint="https://...")` |
| **数据库** | 显式传递连接参数 | `connect(host="...", port=5432, db="...")` |
| **配置管理** | 显式传递配置文件路径 | `load_config(path="/etc/app/config.yaml")` |
| **时间处理** | 显式传递时区 | `datetime.now(tz=timezone.utc)` |
| **编码处理** | 显式指定 charset | `open(file, encoding="utf-8")` |

### 流程领域

| 领域 | 具体应用 | 示例 |
|------|---------|------|
| **需求分析** | 显式列出依赖的外部系统和配置 | 需求文档包含"环境依赖"章节 |
| **代码审查** | 检查是否有隐式依赖 | CR Checklist: "是否使用相对路径？" |
| **测试设计** | Mock 所有隐式状态 | 测试中显式设置 cwd、环境变量、时区 |
| **部署运维** | 显式声明运行时依赖 | Dockerfile 中显式设置 ENV、WORKDIR |

### 组织领域

| 领域 | 具体应用 | 示例 |
|------|---------|------|
| **团队协作** | 文档中显式说明操作前提 | "执行前需要 cd 到项目根目录" |
| **知识传承** | 新人培训强调显式依赖 | 入职培训包含"隐式依赖陷阱"案例 |
| **决策机制** | 决策文档显式列出假设 | 技术方案包含"假设与依赖"章节 |

---

## 实施指南

### 技术层面

**工具支持**：
- **静态分析**: `pylint` — 检测 `os.getenv()` 无默认值的调用
- **Linter 规则**: `ruff` — 规则 PTH123（禁止 `open()` 不带 `encoding`）
- **CI/CD 集成**: Pre-commit hook 检查相对路径使用

**代码示例**：

#### ✅ 推荐写法

```python
# 文件操作 — 使用绝对路径
from pathlib import Path

def load_config(config_path: Path | None = None):
    if config_path is None:
        config_path = Path(__file__).parent / "default_config.yaml"
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)

# API 调用 — 显式传递凭证
def fetch_data(api_key: str, endpoint: str):
    headers = {"Authorization": f"Bearer {api_key}"}
    return requests.get(endpoint, headers=headers)

# 时间处理 — 显式传递时区
from datetime import datetime, timezone

def get_utc_now():
    return datetime.now(tz=timezone.utc)
```

#### ❌ 不推荐写法

```python
# 文件操作 — 依赖 cwd
def load_config():
    with open("./config.yaml") as f:  # 问题：依赖 cwd
        return yaml.safe_load(f)

# API 调用 — 依赖环境变量
def fetch_data():
    api_key = os.getenv("API_KEY")  # 问题：隐式依赖
    return requests.get(endpoint, headers={"Authorization": api_key})

# 时间处理 — 依赖系统时区
def get_now():
    return datetime.now()  # 问题：不同时区结果不同
```

---

### 流程层面

**融入现有流程**：

1. **需求评审阶段**
   - [ ] 需求文档包含"环境依赖"章节，列出所有隐式依赖
   - [ ] 明确"跨环境一致性"是否为需求

2. **设计评审阶段**
   - [ ] API 设计文档列出所有必需参数
   - [ ] 检查是否有"约定优于配置"的隐式依赖

3. **代码审查阶段**
   - [ ] 检查文件操作是否使用相对路径
   - [ ] 检查是否直接读取环境变量
   - [ ] 检查时间/编码处理是否依赖系统默认值

4. **测试阶段**
   - [ ] 测试用例显式设置所有隐式依赖（cwd、环境变量、时区）
   - [ ] 在不同环境（Docker、CI、本地）运行测试验证一致性

---

### 文化层面

**团队共识建立**：

1. **培训新成员**
   - 入职培训包含"隐式依赖陷阱"专题
   - 提供真实案例分析练习（如本案例）
   - 代码审查时主动指出违反情况

2. **持续强化**
   - 周会分享隐式依赖导致的线上问题
   - 每季度回顾原则应用效果
   - 在团队编码规范文档中强调此原则

3. **激励机制**
   - 表彰主动发现和消除隐式依赖的优秀案例
   - 代码质量评分包含"显式依赖"维度

---

## 相关原则

### 支撑关系

这些原则**支撑**本原则：

- **最小惊讶原则** (Principle of Least Astonishment) — 显式依赖让行为更可预测
- **依赖注入原则** (Dependency Injection) — 技术实现层面的显式依赖

### 协同关系

这些原则与本原则**协同应用**效果更好：

- **不变式约束** (Invariant Constraints) — 显式依赖是保证不变式的前提
- **单一职责原则** (Single Responsibility Principle) — 减少隐式依赖有助于职责分离

### 冲突关系

这些原则可能与本原则**冲突**，需要权衡：

- **约定优于配置** (Convention over Configuration) — 追求便利性可能引入隐式依赖
  - **权衡建议**: 在稳定性要求高的场景优先显式依赖，在便利性优先的场景（如 CLI 工具）可适度依赖约定

---

## 理论基础

### 学术文献

1. **Referential Transparency in Functional Programming**
   - 作者: Christopher Strachey
   - 年份: 1967
   - 相关性: 显式依赖是实现引用透明性的前提

2. **The Law of Demeter**
   - 作者: Karl Lieberherr
   - 年份: 1987
   - 相关性: "只与直接朋友交谈"的原则要求依赖显式化

### 经典书籍

1. **《代码大全》(Code Complete)**
   - 作者: Steve McConnell
   - 出版年: 2004
   - 章节: Chapter 5.3 "Defensive Programming"
   - 引用: "Anticipate errors and handle them explicitly"

2. **《设计模式》(Design Patterns)**
   - 作者: Gang of Four
   - 出版年: 1994
   - 章节: Dependency Injection Pattern
   - 引用: "Depend on abstractions, not concretions"

### 行业最佳实践

1. **The Twelve-Factor App** (Heroku)
   - 描述: "Store config in the environment, but inject it explicitly at startup"
   - 链接: https://12factor.net/config

2. **Google's Software Engineering Practices**
   - 描述: "Make dependencies explicit in BUILD files"
   - 链接: https://abseil.io/resources/swe-book

---

## 度量与评估

### 定量指标

**如何衡量原则遵守程度**：

| 指标 | 计算方法 | 目标值 | 当前值 |
|------|---------|--------|--------|
| 相对路径使用率 | `grep -r "\./.*\.md" / 总文件数` | < 5% | TBD |
| 环境变量直接读取率 | `grep -r "os\.getenv" / 总代码行数` | < 10% | TBD |
| 编码未声明率 | `open(.*) [^encoding]` 命中数 | 0% | TBD |

### 定性指标

**原则应用成熟度等级**：

- **Level 1 (认知)**: 团队知道此原则存在
- **Level 2 (理解)**: 团队理解原则含义和适用场景
- **Level 3 (应用)**: 部分项目开始应用
- **Level 4 (规范)**: 所有新项目强制要求遵守
- **Level 5 (内化)**: 成为团队默认做法，无需提醒

**当前成熟度**: Level 1 (初始提出阶段)

---

## 演进历史

### v1.0.0 (2026-04-29)

**首次提出**：
- 来源: self-learning skill 优化 session
- 触发事件: Agent 在错误路径验证文件，发现依赖 cwd 的隐式依赖问题
- 初始范围: 文件系统操作

---

## 常见问题

### Q1: 是否所有函数都要显式传递所有参数？

**回答**: 不是。关键在于区分"配置参数"和"业务参数"：
- **业务参数**: 每次调用可能不同（如用户输入），应显式传递
- **配置参数**: 在应用生命周期内固定（如 API endpoint），可以在初始化时注入，避免每次调用都传递

示例：
```python
# 推荐：配置在初始化时注入
class ApiClient:
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint
    
    def fetch_user(self, user_id: int):  # user_id 是业务参数
        return requests.get(f"{self.endpoint}/users/{user_id}",
                          headers={"Authorization": self.api_key})
```

### Q2: 如何处理遗留代码中的隐式依赖？

**回答**: 渐进式重构策略：
1. **第一步**: 添加 deprecation warning，提示用户未来将移除隐式依赖
2. **第二步**: 提供新 API（显式参数），保留旧 API（标记为 deprecated）
3. **第三步**: 在主版本升级时移除旧 API

示例：
```python
import warnings

def load_config(config_path: str | None = None):
    if config_path is None:
        warnings.warn("Implicit config path is deprecated, please pass config_path explicitly",
                     DeprecationWarning, stacklevel=2)
        config_path = "./config.yaml"  # 旧行为
    ...
```

### Q3: 是否与"约定优于配置"原则冲突？

**回答**: 不冲突，但需要权衡：
- **约定优于配置**适用于**稳定的、行业公认的约定**（如 `.gitignore` 位于项目根目录）
- **显式依赖原则**适用于**不稳定的、团队内部的假设**（如"相对路径从哪里开始计算"）

**判断标准**: 如果违反"约定"会导致 100% 的新手犯错，说明这个"约定"不够稳定，应该显式化。

---

## 参考来源

### 直接来源（根因分析）

- 待生成根因分析文件

### 相关 Sessions

- self-learning skill 优化 session (2026-04-29) — Skill 路径混淆问题

### 相关 Insights

- skill-optimization-path-selection.md — 路径选择问题
- write-to-file.md — 文件操作工具经验

---

**最后审查**: 2026-04-29  
**审查人**: 初始版本，无人工审查  
**下次审查**: 2026-07-29（建议每季度审查一次）
