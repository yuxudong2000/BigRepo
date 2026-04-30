# Parallel Extractor Implementation Notes

> This directory contains optional Python scripts for parallel knowledge extraction.
> These are reference implementations - the actual Skill uses `use_subagent` tool.

## Purpose

Provides standalone Python implementations of:
1. **Parallel extraction coordinator** - launches multiple subagents
2. **Batch file writer** - concurrent atomic file writes

## Why Python scripts?

While the SKILL.md uses CodeFlicker's `use_subagent` tool directly, these scripts serve as:
- Reference implementations for the algorithm
- Debugging utilities
- Fallback if `use_subagent` is unavailable

## Usage

**Not directly called by the Skill**. The Skill executes parallel extraction via:

```markdown
use_subagent(
  subagent_name="knowledge-extractor",
  task="从 session 中提炼 {category}...",
  background=false
)
```

## Files

- `parallel_extractor.py` - Coordination logic (theoretical)
- `batch_writer.py` - Atomic batch file writing (theoretical)

## Note

These are **design references**, not executable code in the current implementation.
The actual parallel execution is handled by CodeFlicker's subagent system.
