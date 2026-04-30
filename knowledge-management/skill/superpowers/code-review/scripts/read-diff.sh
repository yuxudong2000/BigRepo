#!/bin/bash
# read-diff.sh
# 读取指定文件的 diff 内容（按 chunk/hunk 分段）
#
# 参考实现：packages/agent/src/tool/tools/read-diff/
#
# 用法:
#   read-diff.sh <file_path> [start_chunk_index] [limit]
#
# 参数:
#   file_path         - 文件路径（必填）
#   start_chunk_index - 从第几个 chunk 开始（可选，默认 0）
#   limit             - 最多读取几个 chunk（可选，默认 5）
#
# 限制常量（与 IDE Agent 保持一致）:
#   MAX_LINES_PER_CHUNK = 70   单个 Chunk 最大保留行数
#   MAX_TOTAL_LINES = 350      单次返回最大总行数
#   MAX_CHUNKS_PER_CALL = 5    单次返回最大 Chunk 数

# === 配置常量 ===
MAX_LINES_PER_CHUNK=70
MAX_TOTAL_LINES=350
MAX_CHUNKS_PER_CALL=5

# === 参数解析 ===
FILE_PATH="$1"
START_CHUNK="${2:-0}"
LIMIT="${3:-$MAX_CHUNKS_PER_CALL}"

# === 参数校验 ===
if [ -z "$FILE_PATH" ]; then
    echo "Error: File path required"
    echo "Usage: read-diff.sh <file_path> [start_chunk_index] [limit]"
    exit 1
fi

# === 检查是否在 Git 仓库中 ===
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository. This tool requires a git repository to work."
    exit 1
fi

# === 检查文件是否是 untracked ===
is_untracked() {
    local file="$1"
    local status=$(git status --porcelain -- "$file" 2>/dev/null | head -1)
    case "$status" in
        "??"*) return 0 ;;
        *) return 1 ;;
    esac
}

# === 获取 diff 内容 ===
get_diff() {
    local file="$1"
    
    if is_untracked "$file"; then
        # 对于 untracked 文件，使用 git diff --no-index
        git diff --no-index /dev/null "$file" 2>/dev/null || true
    else
        # 对于已跟踪文件，使用 git diff HEAD
        git diff HEAD -- "$file" 2>/dev/null
    fi
}

# === 主逻辑 ===
echo "[read_diff for \"$FILE_PATH\"] Result:"

# 获取完整 diff
FULL_DIFF=$(get_diff "$FILE_PATH")

# 检查是否有变更
if [ -z "$FULL_DIFF" ]; then
    # 检查文件是否存在
    if [ ! -e "$FILE_PATH" ]; then
        # 检查是否在 HEAD 中存在（被删除的文件）
        if git show HEAD:"$FILE_PATH" > /dev/null 2>&1; then
            echo "Deleted file: $FILE_PATH"
            echo "This file has been deleted from the working directory."
        else
            echo "Error: File not found: $FILE_PATH"
        fi
    else
        echo "No changes in file: $FILE_PATH"
    fi
    exit 0
fi

# 检查是否是二进制文件
if echo "$FULL_DIFF" | grep -q "Binary files"; then
    echo "Binary file: $FILE_PATH (cannot display diff)"
    exit 0
fi

# === 使用 awk 解析和处理 diff ===
echo "$FULL_DIFF" | awk -v start_chunk="$START_CHUNK" \
                        -v limit="$LIMIT" \
                        -v max_lines="$MAX_LINES_PER_CHUNK" \
                        -v max_total="$MAX_TOTAL_LINES" \
                        -v file_path="$FILE_PATH" '
BEGIN {
    chunk_index = -1
    in_chunk = 0
    chunk_count = 0
    output_count = 0
    total_lines = 0
    total_additions = 0
    total_deletions = 0
    truncated_list = ""
    new_start = 1
    new_lines = 1
}

# 检测 hunk 头部
/^@@ -[0-9]+(,[0-9]+)? \+[0-9]+(,[0-9]+)? @@/ {
    # 保存上一个 chunk
    if (in_chunk && chunk_index >= start_chunk && output_count < limit) {
        output_chunk()
    }
    
    chunk_index++
    chunk_count++
    in_chunk = 1
    chunk_lines = ""
    chunk_line_count = 0
    chunk_additions = 0
    chunk_deletions = 0
    
    # 解析位置信息 - 使用兼容的方式
    header = $0
    # 提取 +N,M 部分
    gsub(/.*\+/, "", header)
    gsub(/ @@.*/, "", header)
    # 分离 start 和 lines
    n = split(header, parts, ",")
    new_start = parts[1] + 0
    if (n > 1) {
        new_lines = parts[2] + 0
    } else {
        new_lines = 1
    }
    
    chunk_header = $0
    chunk_lines = $0 "\n"
    chunk_line_count = 1
    next
}

# 收集 chunk 内容
in_chunk {
    chunk_lines = chunk_lines $0 "\n"
    chunk_line_count++
    
    if (/^\+/ && !/^\+\+\+/) {
        chunk_additions++
        total_additions++
    } else if (/^-/ && !/^---/) {
        chunk_deletions++
        total_deletions++
    }
}

function output_chunk() {
    # 检查总行数限制
    if (output_count > 0 && total_lines + chunk_line_count > max_total) {
        return
    }
    
    print ""
    print "# Chunk " chunk_index
    
    # 检查是否需要截断
    if (chunk_line_count > max_lines) {
        # 输出截断后的内容
        split(chunk_lines, lines, "\n")
        for (i = 1; i <= max_lines; i++) {
            print lines[i]
        }
        
        # 计算截断后的统计
        truncated_add = 0
        truncated_del = 0
        for (i = 1; i <= max_lines; i++) {
            if (lines[i] ~ /^\+/ && lines[i] !~ /^\+\+\+/) truncated_add++
            if (lines[i] ~ /^-/ && lines[i] !~ /^---/) truncated_del++
        }
        
        print ""
        print "=== Chunk " chunk_index " (lines " new_start "-" (new_start + new_lines - 1) " in current file): TRUNCATED ==="
        print "Original: " chunk_line_count " lines (+" chunk_additions "/-" chunk_deletions ") | Showing: first " max_lines " lines (+" truncated_add "/-" truncated_del ")"
        print "[Chunk " chunk_index " Hint] Use read_file(\"" file_path "\", start_line=" new_start ", end_line=" (new_start + new_lines - 1) ") to view full changes"
        
        if (truncated_list != "") truncated_list = truncated_list ","
        truncated_list = truncated_list chunk_index
        
        total_lines += max_lines
    } else {
        # 输出完整内容（去掉末尾换行）
        sub(/\n$/, "", chunk_lines)
        print chunk_lines
        total_lines += chunk_line_count
    }
    
    output_count++
}

END {
    # 输出最后一个 chunk
    if (in_chunk && chunk_index >= start_chunk && output_count < limit) {
        output_chunk()
    }
    
    # 计算实际范围
    actual_start = start_chunk
    if (start_chunk >= chunk_count && chunk_count > 0) {
        actual_start = chunk_count - 1
        print ""
        print "=== Warning: chunk index out of range ==="
        print "Requested: start_chunk_index=" start_chunk
        print "Available: 0-" (chunk_count - 1) " (" chunk_count " chunks total)"
        print "Returning: chunk " actual_start " (last chunk)"
    }
    
    if (output_count == 0) {
        actual_end = actual_start
    } else {
        actual_end = actual_start + output_count - 1
    }
    remaining = chunk_count - actual_end - 1
    if (remaining < 0) remaining = 0
    
    # 输出 Summary
    print ""
    print "=== Summary ==="
    print "File: " file_path
    
    if (actual_end >= chunk_count - 1 && truncated_list == "") {
        print "Chunks: " chunk_count " | +" total_additions "/-" total_deletions " lines"
        print "Status: complete"
    } else {
        print "Showing: chunk " actual_start "-" actual_end " of " chunk_count " | +" total_additions "/-" total_deletions " lines"
        
        if (truncated_list != "") {
            msg = "Status: partial (chunk " truncated_list " truncated"
            if (remaining > 0) msg = msg "; " remaining " chunks remaining"
            print msg ")"
        } else if (remaining > 0) {
            print "Status: partial (" remaining " chunks remaining)"
        } else {
            print "Status: complete"
        }
        
        if (remaining > 0) {
            print "Next: read-diff.sh \"" file_path "\" " (actual_end + 1) " " limit
        }
    }
}
'
