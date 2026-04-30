# Large Diff Handling (Edge Cases)

When encountering a large number of changes, follow these strategies:

## File Count Limits

- If changed files > 50, prioritize reviewing high-risk files (security, core logic)
- Review in batches of 20-30 files each

## Single File Diff Too Large

- If a single file diff > 500 lines, read it in segments
- Use `git diff HEAD -- <file>` to get the full diff, then analyze by hunk
- Or use `read_file` to view the current version and understand changes in context with git diff info

## Token Limits

- Keep single tool call output under 20,000 tokens
- If the report is too long, consider splitting or condensing

## Risk Priority

When narrowing the review scope, prioritize by the following order:

| Priority | File Type | Description |
|----------|-----------|-------------|
| P0 | Security-related | Authentication, authorization, encryption, sensitive data handling |
| P1 | Core business logic | Main feature implementations, data models |
| P2 | API/Interfaces | Externally exposed interfaces, protocol definitions |
| P3 | Tooling/Config | Build scripts, configuration files |
| P4 | Docs/Tests | README, test cases |

## Batch Review Strategy

When there are too many changed files:

```
Batch 1: P0 + P1 files (Security + Core logic)
Batch 2: P2 files (API/Interfaces)
Batch 3: P3 + P4 files (Tooling/Docs)
```

After each batch, output an intermediate report. The user can choose whether to continue.
