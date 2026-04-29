# 验证死循环排查模式

> 分类：patterns  
> 来源：2026-04-29 self-learning-skill-optimization

---

## [2026-04-29] 来自 self-learning-skill-optimization

### 问题现象

验证 agent（或任何检查机制）不断报告文件 "missing" 或 "not found"，但文件实际存在。

### 排查步骤

#### Step 1: 明确当前工作目录
```bash
pwd
# 输出：/Users/yuxudong/Documents/hermes-agent
```

#### Step 2: 确认实际文件位置
```bash
ls -la /Users/yuxudong/.codeflicker/skills/self-learning/SKILL.md
# 输出：文件存在
```

#### Step 3: 检查验证逻辑的查找路径

观察验证 agent 的查找逻辑：
```
验证 agent 查找: ./skills/self-learning/SKILL.md
实际路径拼接: /Users/yuxudong/Documents/hermes-agent/skills/self-learning/SKILL.md
结果: 文件不存在（路径错误）
```

#### Step 4: 识别路径不一致

**根本原因**：验证逻辑使用相对路径，但基于错误的 cwd。

**本次案例**：
- 调研仓库：`/Users/yuxudong/Documents/hermes-agent`（cwd）
- 实际文件：`/Users/yuxudong/.codeflicker/skills/self-learning/`
- 验证查找：`./skills/self-learning/`（相对于调研仓库）
- 结果：路径不匹配

### 解决方案

**方案 A：切换工作目录**
```bash
cd /Users/yuxudong/.codeflicker/
# 然后验证相对路径 ./skills/self-learning/SKILL.md
```

**方案 B：使用绝对路径**（推荐）
```python
# 验证逻辑改用绝对路径
verify_file("/Users/yuxudong/.codeflicker/skills/self-learning/SKILL.md")
```

**方案 C：明确告知验证 agent 正确路径**
```
"请在 /Users/yuxudong/.codeflicker/skills/self-learning/ 路径下验证文件"
```

### 通用模式

```
现象：验证/查找失败
  ↓
检查三要素：
  1. 当前 cwd
  2. 实际文件路径（绝对）
  3. 查找逻辑使用的路径（相对 vs 绝对）
  ↓
识别不一致
  ↓
修复：统一路径基准（cwd 或绝对路径）
```

### 适用场景

- 跨仓库文件验证
- CI/CD 脚本路径问题
- 工具链查找配置文件失败
- linter 报告文件不存在但实际存在

### 防御性编程建议

在验证逻辑中，始终：
1. 打印实际查找的完整路径（调试信息）
2. 优先使用绝对路径
3. 如果必须用相对路径，明确 log 当前 cwd
