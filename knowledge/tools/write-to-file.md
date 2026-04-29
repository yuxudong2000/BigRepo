# write_to_file 工具使用经验

> 分类：tools  
> 来源：多次对话归档

---

## [2026-04-29] 来自 self-learning-skill-optimization

### 最佳实践：跨目录写入使用绝对路径

**场景**：需要写入文件到非当前工作目录（cwd）的路径

**推荐做法**：
```python
# ✅ 推荐：使用绝对路径
write_to_file(
  path="/Users/yuxudong/.codeflicker/skills/self-learning/references/xxx.md",
  content=...
)
```

**避免做法**：
```python
# ❌ 不推荐：相对路径（依赖 cwd）
write_to_file(
  path="../.codeflicker/skills/self-learning/references/xxx.md",
  content=...
)
```

### 为什么

1. **cwd 不确定性**：当前工作目录可能因 `cd` 命令、环境配置等变化
2. **跨仓库操作**：调研仓库 A，修改仓库 B 的文件，相对路径容易出错
3. **可读性**：绝对路径一目了然，相对路径需要推算

### 什么时候例外

**可以使用相对路径**的场景：
- 文件在当前仓库内（如 `src/utils/xxx.ts`）
- 明确 cwd 不会变化（如单仓库单次操作）

### 排查技巧

如果 `write_to_file` 写入位置不符合预期：
1. 执行 `pwd` 确认当前 cwd
2. 检查目标文件的实际绝对路径
3. 改用绝对路径重写

### 相关工具

同样原则适用于：
- `read_file`
- `replace_in_file`
- `list_files`
