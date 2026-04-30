#!/bin/bash
# list-changed-files.sh
# 列出变更文件（HEAD vs Working Directory 或指定范围）
#
# 参考实现：packages/agent/src/tool/tools/list-changed-files/
#
# 用法:
#   list-changed-files.sh [path] [base_commit]
#
# 参数:
#   path        - 路径过滤（可选，默认 "."）
#   base_commit - 基准 commit（可选，默认 "HEAD"）
#
# 输出格式:
#   M  src/foo.ts [staged]
#   A  src/bar.ts [unstaged]
#   D  src/old.ts [staged]
#   R  src/new.ts <- src/old.ts [unstaged]
#   ??  src/new.ts [unstaged]
#
# 限制常量（与 IDE Agent 保持一致）:
#   MAX_FILES_RETURNED = 200

# === 配置常量 ===
MAX_FILES_RETURNED=200

# === 参数解析 ===
PATH_FILTER="${1:-.}"
BASE_COMMIT="${2:-HEAD}"

# === 路径校验 ===
validate_path() {
    local path_input="$1"
    
    # 处理空字符串
    if [ -z "$path_input" ] || [ "$path_input" = "." ]; then
        echo "."
        return 0
    fi
    
    # 检查绝对路径
    case "$path_input" in
        /*)
            echo "Error: Absolute paths are not allowed. Use a relative path under the current working directory." >&2
            return 1
            ;;
    esac
    
    # 检查路径穿越
    case "$path_input" in
        *..*)
            echo "Error: Path traversal (..) is not allowed. Use a relative path under the current working directory." >&2
            return 1
            ;;
    esac
    
    # 规范化路径
    local normalized="$path_input"
    # 移除开头的 ./
    normalized="${normalized#./}"
    # 移除末尾的 /
    normalized="${normalized%/}"
    
    if [ -z "$normalized" ]; then
        normalized="."
    fi
    
    echo "$normalized"
    return 0
}

# === 检查是否在 Git 仓库中 ===
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository. This tool requires a git repository to work."
    exit 1
fi

# === 校验路径参数 ===
NORMALIZED_PATH=$(validate_path "$PATH_FILTER")
if [ $? -ne 0 ]; then
    exit 1
fi

# 构建 git 命令参数
if [ "$NORMALIZED_PATH" = "." ]; then
    GIT_PATH_ARG=""
else
    GIT_PATH_ARG="-- $NORMALIZED_PATH"
fi

# === 检查 base commit 是否有效 ===
if ! git rev-parse "$BASE_COMMIT" > /dev/null 2>&1; then
    echo "Error: Invalid base commit: $BASE_COMMIT"
    exit 1
fi

# === 输出结果 ===
echo "[list_changed_files${PATH_FILTER:+ for \"$PATH_FILTER\"}] Result:"

# 计数器
total_count=0
modified_count=0
added_count=0
deleted_count=0
renamed_count=0
untracked_count=0

# 创建临时文件存储结果
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

# === 获取 git status 信息 ===
# 使用 git status --porcelain 获取所有变更（包括 untracked）
git status --porcelain -uall $GIT_PATH_ARG 2>/dev/null | while IFS= read -r line; do
    [ -z "$line" ] && continue
    [ ${#line} -lt 3 ] && continue
    
    index_status="${line:0:1}"
    worktree_status="${line:1:1}"
    file_info="${line:3}"
    
    # 处理重命名格式: old -> new
    old_path=""
    if echo "$file_info" | grep -q " -> "; then
        old_path="${file_info%% -> *}"
        file_path="${file_info##* -> }"
        # 移除引号
        old_path="${old_path#\"}"
        old_path="${old_path%\"}"
    else
        file_path="$file_info"
    fi
    
    # 移除引号
    file_path="${file_path#\"}"
    file_path="${file_path%\"}"
    
    # 确定变更类型和暂存状态
    status_code=""
    stage_status="unstaged"
    
    if [ "$index_status" = "?" ] && [ "$worktree_status" = "?" ]; then
        status_code="??"
        stage_status="unstaged"
    else
        # 确定暂存状态
        has_index=false
        has_worktree=false
        
        [ "$index_status" != " " ] && [ "$index_status" != "?" ] && has_index=true
        [ "$worktree_status" != " " ] && [ "$worktree_status" != "?" ] && has_worktree=true
        
        if [ "$has_index" = true ] && [ "$has_worktree" = true ]; then
            stage_status="partial"
        elif [ "$has_index" = true ]; then
            stage_status="staged"
        else
            stage_status="unstaged"
        fi
        
        # 确定状态码（优先使用 index 状态）
        if [ "$index_status" != " " ] && [ "$index_status" != "?" ]; then
            status_code="$index_status"
        else
            status_code="$worktree_status"
        fi
    fi
    
    # 格式化输出
    if [ -n "$old_path" ]; then
        echo "$status_code  $file_path <- $old_path [$stage_status]"
    else
        echo "$status_code  $file_path [$stage_status]"
    fi
done | head -n $MAX_FILES_RETURNED > "$TMPFILE"

# 输出结果
cat "$TMPFILE"

# === 统计信息 ===
total_count=$(wc -l < "$TMPFILE" | tr -d ' ')

# 获取完整统计（不受 MAX_FILES_RETURNED 限制）
full_stats=$(git status --porcelain -uall $GIT_PATH_ARG 2>/dev/null)
full_count=$(echo "$full_stats" | grep -c "^" 2>/dev/null || echo "0")
modified_count=$(echo "$full_stats" | grep -c "^.M\|^M" 2>/dev/null || echo "0")
added_count=$(echo "$full_stats" | grep -c "^.A\|^A" 2>/dev/null || echo "0")
deleted_count=$(echo "$full_stats" | grep -c "^.D\|^D" 2>/dev/null || echo "0")
renamed_count=$(echo "$full_stats" | grep -c "^R" 2>/dev/null || echo "0")
untracked_count=$(echo "$full_stats" | grep -c "^??" 2>/dev/null || echo "0")

# === 输出提示信息 ===
if [ "$full_count" -gt "$MAX_FILES_RETURNED" ]; then
    echo ""
    echo "[Result truncated: showing $total_count of $full_count files]"
    
    # 生成 suggestedPaths（简化版：取前 5 个不同的二级目录）
    suggested=$(git status --porcelain -uall $GIT_PATH_ARG 2>/dev/null | \
        awk '{print $2}' | \
        sed 's|[^/]*/[^/]*/.*|\0|; s|\([^/]*/[^/]*/\).*|\1|' | \
        sort | uniq -c | sort -rn | head -5 | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
    
    if [ -n "$suggested" ]; then
        echo "[Suggested paths to narrow down: $suggested]"
    fi
fi

# === 输出统计 ===
echo ""
echo "# Summary"
echo "# Total: $full_count files (showing: $total_count)"
echo "# Modified: $modified_count | Added: $added_count | Deleted: $deleted_count | Renamed: $renamed_count | Untracked: $untracked_count"
