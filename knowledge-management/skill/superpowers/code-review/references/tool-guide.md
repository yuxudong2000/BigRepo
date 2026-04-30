# Tool Usage Guide

This document describes the available tools in the Code Review Skill and how to use them.

## 1. Script Tools

### 1.1 list-changed-files.sh

**Purpose**: List changed files within a specified scope

**Location**: `{skill_directory}/scripts/list-changed-files.sh`

**Usage**:
```bash
list-changed-files.sh [path] [base_commit]
```

**Parameters**:
| Parameter | Required | Default | Description |
|-----------|:--------:|---------|-------------|
| path | ❌ | `.` | Path filter, e.g. `src/`, `*.ts` |
| base_commit | ❌ | `HEAD` | Base commit, e.g. `HEAD~3`, `main` |

**Examples**:
```bash
# List all uncommitted changes
{skill_directory}/scripts/list-changed-files.sh

# Only show changes in the src directory
{skill_directory}/scripts/list-changed-files.sh src/

# Compare with the main branch
{skill_directory}/scripts/list-changed-files.sh . main
```

**Output format**:
```
# Changed files (base: HEAD)

M   src/foo.ts [staged]
A   src/bar.ts [unstaged]
D   src/old.ts [staged]
??  src/new.ts [unstaged]

# Summary
# Total: 4 files
# Modified: 1 | Added: 1 | Deleted: 1 | Untracked: 1
```

**Status codes**:
| Code | Meaning |
|------|---------|
| `M` | Modified |
| `A` | Added |
| `D` | Deleted |
| `R` | Renamed |
| `??` | Untracked |

**Staging states**:
| Label | Meaning |
|-------|---------|
| `[staged]` | All changes are staged |
| `[unstaged]` | All changes are unstaged |
| `[partial]` | Partially staged |

---

### 1.2 read-diff.sh

**Purpose**: Read the diff content of a specified file (chunked by hunk)

**Location**: `{skill_directory}/scripts/read-diff.sh`

**Usage**:
```bash
read-diff.sh <file_path> [start_chunk_index] [limit]
```

**Parameters**:
| Parameter | Required | Default | Description |
|-----------|:--------:|---------|-------------|
| file_path | ✅ | - | File path |
| start_chunk_index | ❌ | `0` | Starting chunk index (0-indexed) |
| limit | ❌ | `5` | Maximum number of chunks to read |

**Examples**:
```bash
# Read the full diff of a file
{skill_directory}/scripts/read-diff.sh src/foo.ts

# Start reading from chunk 3
{skill_directory}/scripts/read-diff.sh src/foo.ts 3

# Read only the first 2 chunks
{skill_directory}/scripts/read-diff.sh src/foo.ts 0 2
```

**Output format**:
```
# Chunk 0
@@ -10,7 +10,10 @@
 const a = 1;
-const b = 2;
+const b = 3;
+const c = 4;

# Chunk 1
@@ -50,5 +53,8 @@
 function foo() {
-  return null;
+  return bar();
 }

=== Summary ===
File: src/foo.ts
Showing: chunk 0-1 of 2 | +5/-2 lines
Status: complete
```

**Large file handling**:
- Individual chunks exceeding 70 lines will be truncated
- Maximum of 350 lines returned per call
- When truncated, a hint to use `read_file` for full content is provided

---

## 2. Built-in Agent Tools

### 2.1 read_file

**Purpose**: Read file content to understand code context

**Recommended scenarios**:
- View the complete code of changed files
- Understand related but unchanged files
- View full content when diff is truncated

**Example**:
```
read_file("src/foo.ts", start_line=50, end_line=100)
```

### 2.2 list_files

**Purpose**: List directory contents to understand project structure

**Recommended scenarios**:
- Explore project directory structure
- Find related files
- Confirm file existence

**Example**:
```
list_files("src/", recursive=true)
```

### 2.3 grep_search

**Purpose**: Search code patterns to find related code

**Recommended scenarios**:
- Find where functions/classes are used
- Search for specific patterns
- Verify code reference relationships

**Example**:
```
grep_search("src/", "handleClick|onClick")
```

### 2.4 codebase_search

**Purpose**: Semantic search to understand code relationships

**Recommended scenarios**:
- Find code by concept
- Alternative when grep is too literal
- Find related implementations

**Example**:
```
codebase_search("user authentication flow")
```

### 2.5 search_web

**Purpose**: Look up best practices and library documentation

**Recommended scenarios**:
- Verify whether a pattern is best practice
- Consult library documentation
- Research security vulnerability information

**Example**:
```
search_web("TypeScript optional chaining best practice")
```

---

## 3. Tool Selection Strategy

### 3.1 Quick Review

When you need to quickly inspect code changes, prefer script tools:

```
1. Run list-changed-files.sh to get an overview
2. Run read-diff.sh on important files
3. Use read_file for additional context when needed
```

### 3.2 Deep Review

When you need a thorough understanding of the code, use built-in tools:

```
1. Use list_files to understand project structure
2. Use read_file to read core code
3. Use grep_search to find references
4. Use search_web to verify best practices
```

### 3.3 Mixed Usage

In practice, reviews typically combine both:

```
1. list-changed-files.sh → get change list
2. read-diff.sh → view key file diffs
3. read_file → supplement context
4. grep_search → find impact scope
5. Generate report
```

---

## 4. FAQ

### Q: What if script execution fails?

If scripts are unavailable (permission or environment issues), use Git commands directly:

```bash
# Alternative to list-changed-files.sh
git diff --name-status HEAD

# Alternative to read-diff.sh
git diff HEAD -- <file>
```

### Q: What if a large file diff is truncated?

Use `read_file` to view the full content, or call `read-diff.sh` in segments:

```bash
# View chunks 3-7
read-diff.sh src/large-file.ts 3 5
```

### Q: What if there is no Git repository?

Use built-in agent tools to read files directly:

```
read_file("src/foo.ts")
list_files("src/")
```
