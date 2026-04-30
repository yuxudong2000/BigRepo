# Issue Categories

This document describes the issue categories used in Code Review reports.

> **Core principle**: Code Review should focus on **design soundness, business logic completeness, and architecture decisions** — not low-level coding errors that linters can catch. Each category focuses on "is the approach right?" rather than "is this line of code correct?"

## Category Overview

| Code | Full Name | Description | Typical Focus |
|------|-----------|-------------|---------------|
| **DESIGN** | Design & Architecture | Design decisions and architecture choices | Module boundaries, responsibility allocation, abstraction levels, extensibility |
| **LOGIC** | Business Logic | Business logic completeness | Flow coverage, state transitions, business rule correctness |
| **COMPAT** | Compatibility & Impact | Compatibility and blast radius | Backward compatibility, cross-module impact, migration risks |
| **EDGE** | Edge Cases & Robustness | Edge cases and fault tolerance | Exception paths, degradation strategies, race conditions, data consistency |
| **SEC** | Security Boundary | Security boundaries | Permission models, trust boundaries, data isolation |
| **API** | Contract & Interface | Interface contracts and protocols | Protocol design, versioning strategy, call chains |
| **MAINT** | Maintainability | Maintainability | Testability, observability, tech debt, cognitive complexity |

---

## Detailed Descriptions

### DESIGN - Design & Architecture

**Definition**: Architecture choices, module decomposition, responsibility allocation, and abstraction-level design decisions.

**Core questions**:
- Is this approach a reasonable way to solve this problem?
- Are the responsibility boundaries between modules clear?
- Is the abstraction level appropriate — over-engineered or under-designed?
- Are new modules/classes/interfaces consistent with the existing architecture?
- Is this approach easy to extend when requirements change?

**Typical scenarios**:
- Logic that belongs in the Service layer is placed in the Controller
- A "god class" takes on too many responsibilities, violating single responsibility
- An existing module could be reused but a new one was built from scratch
- Unclear data flow with implicit dependencies between modules
- The approach solves the current requirement but blocks future extension

**Examples**:

```
❌ DESIGN issue: BundledSync handles version comparison, file copying, and orphan cleanup all in sync()

Three concerns are coupled in one method. When you need to trigger "cleanup" or "check updates"
independently, there's no way to reuse them.
Suggestion: Split into checkUpdates(), applyUpdate(), cleanupOrphans() as independent methods.
```

```
❌ DESIGN issue: New SkillLoader directly depends on fs and path

Other Skill-related modules access the filesystem through a FileSystem abstraction layer.
SkillLoader directly importing fs breaks the existing testability design.
Suggestion: Inject the FileSystem interface to stay consistent.
```

---

### LOGIC - Business Logic

**Definition**: Completeness of business flows, correctness of state transitions, coverage of business rules.

**Core questions**:
- Are all paths in the business flow covered?
- Is the state machine complete — are there "supposedly unreachable but actually reachable" states?
- Do the business rules correctly reflect product requirements?
- In multi-step flows, how does the system roll back when an intermediate step fails?

**Typical scenarios**:
- Order flow only handles the "success" path, missing "payment timeout" and "partial refund"
- State machine allows transitioning from "completed" back to "in progress", but product logic forbids it
- Permission check misses a role — admin can operate but super-admin cannot
- No defined behavior for partial success in batch operations

**Examples**:

```
❌ LOGIC issue: Skill sync flow lacks "partial failure" handling

BundledSync.sync() loops through all skills, but if the 3rd skill fails,
subsequent syncs and orphan cleanup are skipped entirely.
Suggestion: Independent try-catch per skill sync, collect failures, report at the end.
```

```
❌ LOGIC issue: Version comparison logic doesn't cover the "downgrade" scenario

shouldUpdate() only returns true when bundledVersion > installedVersion.
If a user manually installed a higher version and the plugin upgrade wants to "roll back"
to the bundled version, the current logic can't handle it.
Need to confirm if this is by design or an oversight.
```

---

### COMPAT - Compatibility & Impact

**Definition**: Impact of changes on existing functionality, other modules, and external consumers.

**Core questions**:
- Will this change break existing users' functionality?
- Do other modules/services depend on the modified interface?
- Are data format changes backward compatible?
- Do configuration changes require migration logic?
- Are cross-repo dependencies updated in sync?

**Typical scenarios**:
- An RPC interface field was renamed but consumers still use the old name
- Database schema change has no migration script
- A public exported method was removed but other packages still reference it
- A config key was renamed without backward-compatible reading of the old key

**Examples**:

```
❌ COMPAT issue: VERSION_FILE_PREFIX format change affects installed skills

Changing VERSION_FILE_PREFIX from ".version-" to ".v" means skills already installed
in ~/.claw/internal/skills/ using the old prefix won't be recognized by
extractVersion(), causing a full re-sync.
Suggestion: Make extractVersion() support both prefixes.
```

```
❌ COMPAT issue: ide-agent loadSkill RPC depends on source field enum values

New source: "bundled" value was added, but ide-agent's SkillSource type only defines
"personal" | "project" | "internal". Need to confirm if ide-agent needs a sync update.
```

---

### EDGE - Edge Cases & Robustness

**Definition**: Exception paths, race conditions, data consistency, and degradation strategies.

**Core questions**:
- What happens on network timeout, disk full, or insufficient permissions?
- Can concurrent operations cause data races?
- Is behavior correct with large data volumes or empty data?
- Can the system recover to a consistent state after an interrupted operation?
- Is there a degradation plan when external dependencies are unavailable?

**Typical scenarios**:
- File copy interrupted mid-way, leaving the target directory in a half-finished state
- Two plugin instances running sync() simultaneously, causing file corruption via race condition
- No write permission on the user's home directory, entire skill system silently fails
- External API timeout with no retry and no degradation

**Examples**:

```
❌ EDGE issue: copyDirectory has no atomicity guarantee

syncSkill() removes the old directory then copies the new one.
If copyDirectory fails mid-way (disk full), the user loses that skill with no auto-recovery.
Suggestion: Copy to a temp directory first, then rename to replace on success.
```

```
❌ EDGE issue: getBundledSkills() silently returns empty array on failure

If the bundled-skills directory exists but has no read permissions, getBundledSkills()
catches the error and returns []. Subsequent cleanupOrphanedSkills() would then
delete ALL installed internal skills.
Suggestion: Skip the entire sync flow on read failure.
```

---

### SEC - Security Boundary

**Definition**: Permission models, trust boundaries, and data isolation at the security architecture level. This is NOT about single-line input validation — it's about **security design** considerations.

**Core questions**:
- Where are the trust boundaries — which inputs come from untrusted sources?
- Does the permission model follow the principle of least privilege?
- Is sensitive data protected throughout the transmission and storage chain?
- Could User A's data be accessed by User B?
- Do third-party dependencies introduce additional attack surfaces?

**Typical scenarios**:
- Skill script files can be downloaded from remote and executed directly without signature verification
- Plugin stores API Key in plaintext config instead of SecretStorage
- Missing message origin validation between Webview and Extension Host
- User-uploaded files processed directly in the main process without sandbox isolation

**Examples**:

```
❌ SEC issue: Shell scripts in bundled skills get execution permissions after sync

copyDirectory() preserves original permission bits when copying files.
If an attacker can modify .sh files in the bundled-skills directory,
these scripts will execute with user privileges in the user's environment.
Suggestion: Re-set script permissions after sync, or verify file hashes.
```

```
❌ SEC issue: execute_command instructions in SKILL.md have no sandbox

SKILL.md can instruct the Agent to execute arbitrary shell commands.
Project-level skills (Project source) may come from untrusted repository contributors.
Suggestion: Add command whitelist or user confirmation for Project source skills.
```

---

### API - Contract & Interface

**Definition**: Interface design, protocol agreements, and data format contracts between modules and services.

**Core questions**:
- Is the interface semantics clear — can callers use it correctly from the type definition alone?
- Is the error handling contract explicit — throw exceptions or return error codes?
- Is the interface granularity reasonable — are there "god interfaces"?
- What's the versioning strategy — how to evolve without breaking existing consumers?

**Typical scenarios**:
- A method accepts 10 parameters but callers only use 3, indicating poor granularity
- Same type of error: some methods throw exceptions, others return null — inconsistent contract
- Externally exposed interface lacks type definitions, callers must read implementation to understand
- Data flows through multiple layers but intermediate layers have no explicit DTO definitions

**Examples**:

```
❌ API issue: syncSkill() has no return value for success/failure

Callers can't know if sync succeeded or which skills were updated.
The entire sync() method returns Promise<void>, with logging as the only feedback channel.
Suggestion: Return SyncResult { updated: string[], failed: string[], unchanged: string[] }.
```

```
❌ API issue: shouldUpdate() semantics depend on call order

shouldUpdate(bundledVersion, installedVersion) requires callers to first check
if the skill is installed, then decide whether to pass undefined or the actual version.
This precondition isn't expressed in the type signature.
Suggestion: Split into isInstalled() + needsUpgrade() for clearer semantics.
```

---

### MAINT - Maintainability

**Definition**: Testability, observability, cognitive complexity, and tech debt from a long-term maintenance perspective.

**Core questions**:
- Can the next person to work on this code understand the intent?
- Is this logic easy to unit test? If not, why?
- Can issues be quickly located through logs/monitoring in production?
- Does this introduce unnecessary tech debt?
- Is there a more idiomatic way that follows existing project patterns?

**Typical scenarios**:
- A 200-line method doing 5 things with no decomposition or intent comments
- Critical business flow has no logging — can only guess when production issues occur
- Tests require mocking the entire filesystem, indicating tight dependency coupling
- Uses a pattern unfamiliar to the team (e.g., monads), adding cognitive load with little benefit

**Examples**:

```
❌ MAINT issue: sync() method has no observability

The entire sync flow (version check → file copy → orphan cleanup) produces no logs.
When a user reports "a certain internal skill didn't update", it's impossible to tell
if the version check skipped it or the copy failed.
Suggestion: Add info/warn level logging at key decision points.
```

```
❌ MAINT issue: compareVersions() doesn't handle non-standard version strings

Input like "1.0.0-beta.1" or "latest" leads to unpredictable behavior (NaN in comparisons).
While there's no such input currently, this is an implicit assumption without explicit assertion.
Suggestion: Add version format validation, warn and return a safe default for invalid formats.
```

---

## Category Selection Guide

### Priority Order

When an issue could belong to multiple categories, choose the **most fundamental** one:

1. **DESIGN > Others**: If the root cause is a design decision error, mark as DESIGN
2. **LOGIC > EDGE**: Missing business flow is LOGIC; exception handling in existing flows is EDGE
3. **COMPAT > API**: If it impacts existing users/consumers, prefer COMPAT
4. **SEC independent**: Security issues regardless of scale are marked as SEC

### Issues Outside Code Review Scope

The following should be left to **linter/formatter**, not Code Review:

- Indentation and formatting → ESLint/Prettier
- Unused variables → TypeScript compiler
- Simple null checks → TypeScript strict mode
- Naming style (camelCase vs snake_case) → ESLint rules
- Import ordering → ESLint plugin

> **Principle**: If an issue can be automatically detected and fixed by configuring a tool, it should not appear in a Code Review report.
