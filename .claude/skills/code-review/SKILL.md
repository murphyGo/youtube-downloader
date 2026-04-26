# Code Review Skill

Find real issues in code by reading and understanding it deeply — not by pattern-matching against a checklist. Adapted from aidlc-starter's code-review template, trimmed for personal-scale use.

## Arguments

- `$ARGUMENTS` — one of:
  - `git` — review files changed in git (staged + unstaged), default if no argument
  - `files:<path1>,<path2>` — review specific files
  - `dir:<path>` — review all source files in a directory

If no argument is given, behave as `git`.

## Objective

Surface correctness, safety, reliability, and maintainability issues in code under review. Use the project's `BRIEF.md` to align with project intent (e.g., don't flag missing auth as an issue if `BRIEF.md` lists "no auth" in out-of-scope).

---

## Pre-Review: Automated Checks

Detect the project's lint/test commands from `BRIEF.md` (Tech section), `PLAN.md` (Commands section), and project files (`package.json` scripts, `Makefile`, `pyproject.toml`, `go.mod`, etc.). If found, run them first:

```bash
# examples — actual commands depend on detected stack
npm run lint && npm test
ruff check . && pytest
go vet ./... && go test ./...
```

If any automated check fails, **report the failures at the top of the review and continue with the manual pass.** Lint/type errors don't block the deeper read — they're context. Surface them as issues in their own pre-review section so the user sees them alongside any manual findings.

If no commands are configured, skip this step and note it in the report.

---

## Execution Steps

### Step 1: Identify files to review

| Argument | Behavior |
|----------|----------|
| `git` (or empty) | `git diff --name-only HEAD` + `git diff --name-only --cached`, deduped |
| `files:<paths>` | Comma-separated, validate each exists |
| `dir:<path>` | Recursively glob source files (skip `node_modules`, `vendor`, `dist`, `build`, `__pycache__`, `.venv`) |

Separate test files from source files — they get different review focus.

### Step 2: Read and understand code

Read each file fully. Build mental model of:
- What the code does and why
- How it interacts with other components
- What invariants it maintains
- What happens when things go wrong

Cross-reference with `BRIEF.md` (project intent, out-of-scope) and `DECISIONS.md` (past decisions — don't flag a decision that was already made).

### Step 2a: Protocol selection (triage)

Read `protocols/INDEX.md` (sibling of this SKILL.md). Scan the code under review for each signal category. For each match, load the corresponding protocol file and apply its full analysis steps in Step 3.

Only load protocols whose signals are actually present. When in doubt, include the protocol.

### Step 3: Review with focus areas

Analyze in priority order:

1. **Correctness** — logic bugs, edge cases, off-by-one, nil/empty handling, spec non-compliance
2. **Safety** — resource leaks, concurrency bugs, security vulnerabilities, data loss risks
3. **Reliability** — error handling quality, failure scenarios, graceful degradation
4. **Maintainability** — unnecessary complexity, unclear naming, missing abstractions or over-abstraction

For each protocol loaded in Step 2a, execute its full steps. Don't skip steps — each builds on the previous.

### Step 4: Language & framework reference

Detect the language(s) in the changed files and consult the relevant tables below. **Don't go through every table** — focus on what's actually present.

#### Language patterns

##### Go
| Pattern | Issue | Severity |
|---------|-------|----------|
| `err` assigned but not checked | Ignored error | High |
| `return err` without wrapping | Missing context | Medium |
| `go func()` without sync | Goroutine leak | High |
| Missing `defer` for `Close()` | Resource leak | High |

##### Python
| Pattern | Issue | Severity |
|---------|-------|----------|
| Bare `except:` clause | Catches too much | Medium |
| Missing type hints on public funcs | Type ambiguity | Low |
| `open()` without context manager | Resource leak | Medium |
| Mutable default argument | Shared state bug | High |

##### TypeScript / JavaScript
| Pattern | Issue | Severity |
|---------|-------|----------|
| `any` type usage | Type safety loss | Medium |
| Missing null/undefined check | Runtime error risk | High |
| Unhandled promise rejection | Silent failure | High |
| `==` instead of `===` | Type coercion bug | Medium |

##### Rust
| Pattern | Issue | Severity |
|---------|-------|----------|
| `.unwrap()` on user input or I/O | Panic on edge cases | High |
| `clone()` in hot path | Performance issue | Medium |
| `?` swallowing context | Hard to debug | Medium |

#### Framework patterns

##### FastAPI (Python)
| Pattern | Issue | Severity |
|---------|-------|----------|
| Sync function in async endpoint | Blocking event loop | High |
| Missing `response_model` | Type safety loss | Medium |
| Pydantic model without validation | Data integrity | Medium |
| No request body validation | Security risk | High |
| Hardcoded CORS origins | Security misconfiguration | Medium |

##### Express (Node.js)
| Pattern | Issue | Severity |
|---------|-------|----------|
| No `helmet` middleware | Security headers missing | High |
| Callback without error handling | Silent failure | High |
| Missing body-parser limits | DoS via large payload | High |
| No input sanitization | XSS / injection risk | Critical |

##### React (TypeScript / JavaScript)
| Pattern | Issue | Severity |
|---------|-------|----------|
| `useEffect` missing dependencies | Stale closure | High |
| State mutation directly | React won't re-render | High |
| Missing `key` prop in lists | Reconciliation issues | Medium |
| `dangerouslySetInnerHTML` usage | XSS vulnerability | Critical |
| No error boundary | Crash propagation | Medium |

##### Next.js
| Pattern | Issue | Severity |
|---------|-------|----------|
| Server secrets used in client component | Credential exposure | Critical |
| `getServerSideProps` doing heavy compute on every req | Performance issue | Medium |
| Missing `loading.tsx` / suspense boundary | Poor UX | Low |

##### Other frameworks (Django, Flask, NestJS, Gin/Echo, Spring, Actix, …)
Apply universal patterns: input validation at the boundary, authorization gates on sensitive routes, structured error handling, resource cleanup, no secrets in code, no debug mode in production. Consult the loaded protocols (especially security-boundary) for the specific signals in the diff.

### Step 5: Test coverage check

For each new/modified function:

| Check | Method | Severity if missing |
|-------|--------|---------------------|
| Test file exists | Find corresponding test file | Medium |
| Function has test | Find test for function name | Medium |
| Error paths tested | Find test with error assertions | Medium |

If the project has no tests at all, note it once at the top of the report — don't flag every function. Only escalate to High severity if `BRIEF.md` mentions testing as an explicit goal.

### Step 6: Generate report

Keep it short. One header line, optional pre-review block, optional protocols line, then issues grouped by severity. No summary tables.

```markdown
## Code Review — N files, <languages>, YYYY-MM-DD

**Pre-review**: <"clean" | summary of lint/type/test failures with file:line, or "no commands configured">

**Protocols applied**: <protocol names, or "none triggered">

### 🔴 Critical / High
- `src/auth.py:45` — hardcoded secret. Use environment variable.
- `src/api.py:12` — missing input validation on user_id. Validate as int + range.

### 🟡 Medium
- `src/db.py:78` — bare `except:` catches too much. Catch specific exception.

### 🟢 Low
- `src/utils.py:12` — magic number `86400`. Extract as `SECONDS_PER_DAY`.

### Decisions worth logging (optional)
- (only if a non-obvious choice came out of the review, e.g., "deferred SQL injection fix on internal-only column"). Skip if nothing fits.
```

If no issues at any severity, the report is one line: `## Code Review — N files, <languages>, YYYY-MM-DD: clean`.

---

## Severity definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 Critical | Security vulnerability or data loss risk | Must fix before commit |
| 🔴 High | Likely bug or resource leak | Should fix before commit |
| 🟡 Medium | Code quality issue | Fix if cheap, else log to `DECISIONS.md` and move on |
| 🟢 Low | Style / convention | Fix if easy, else ignore |

---

## Language style guides (reference)

### Python
- `snake_case` for functions/variables; `PascalCase` for classes; `UPPER_CASE` for constants
- Imports: stdlib → third-party → local
- Type hints on public functions
- Catch specific exceptions, not bare `except:`
- Wrap with `raise X from e` to preserve cause

### TypeScript
- `camelCase` variables; `PascalCase` types/interfaces
- Strict mode (`"strict": true`); avoid `any`, prefer `unknown`
- `interface` for object shapes; `type` for unions/intersections
- Always handle promise rejections

### Go
- `camelCase` unexported; `PascalCase` exported
- Group imports: stdlib → external → internal
- `defer` immediately after resource acquisition
- Wrap errors with `fmt.Errorf("context: %w", err)`
- Accept interfaces, return structs

### JavaScript
- `camelCase` variables; `PascalCase` classes/components
- Prefer named exports
- Always handle promise rejections; never `console.log` errors and continue

---

## Project alignment

Always read the project's `BRIEF.md` and `DECISIONS.md` before reporting issues:
- Don't flag features as "missing" if they're in `BRIEF.md` Out of scope
- Don't flag a choice as wrong if it's documented in `DECISIONS.md` with rationale
- Do flag inconsistencies between code and `BRIEF.md`/`DECISIONS.md` — these are real issues

---

## Example invocations

```
/code-review              # implicit "git" — review pending changes
/code-review git
/code-review files:src/auth.py,src/db.py
/code-review dir:src/services
```
