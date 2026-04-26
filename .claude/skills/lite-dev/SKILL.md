# Lite Dev Skill

The development driver. Picks the next unchecked `PLAN.md` task, implements it, checks it off.

## Arguments

- `$ARGUMENTS` — (optional)
  - empty: pick the next unchecked task in `PLAN.md`
  - a task title or partial match: jump to that task
  - `next` / `continue`: same as empty
  - `status`: print PLAN.md progress and stop (don't implement anything)

## Objective

One commit-sized unit of work per invocation. Read context, implement, mark done. **No approval gates** — the user reviews via `git diff` and commits when satisfied.

## Execution Steps

### Step 1: Read context

Read in this order, every invocation:
1. `BRIEF.md` — what we're building, tech stack, out-of-scope
2. `PLAN.md` — task list
3. `DECISIONS.md` — past decisions (so you don't contradict them)

If any of the three is missing, stop and tell the user to run `/lite-init` first.

### Step 2: Pick the task

| `$ARGUMENTS` | Behavior |
|--------------|----------|
| empty / `next` / `continue` | First unchecked `[ ]` item in `PLAN.md`, top to bottom |
| `status` | Print "X of Y tasks done" + the next unchecked task, then stop |
| a string | Find the unchecked task whose text contains the string (case-insensitive). If multiple match, list them and ask which |

If all tasks are checked, congratulate the user and suggest either `/lite-init` (to refine direction) or wrapping up.

### Step 3: Implement

Implement the task. Keep it scoped — if the task is "Set up project structure," do that, not "set up project structure plus add a CI pipeline."

**Scope rules:**
- One task = one commit's worth of changes (rough heuristic: < 200 LOC diff)
- If a task turns out to be much bigger than expected, split it: implement the first half, edit `PLAN.md` to break the task in two (check off the half you finished, leave the other unchecked), report the split.
- If the task is blocked by a missing decision, stop, write a question to the user, and offer to record the answer in `DECISIONS.md`.

**Out-of-scope rules:**
- If the task description conflicts with `BRIEF.md` "Out of scope," ask the user before proceeding.
- Do not silently add features that aren't in `PLAN.md`. If you spot a missing related task, mention it after the implementation and offer to append it to `PLAN.md`.

### Step 4: Check the box

Edit `PLAN.md` and change `- [ ]` to `- [x]` on the task you completed. Same commit, same change set.

### Step 5: Log a decision (only if non-obvious)

Append to `DECISIONS.md` only if you made a choice that:
- Future-you would wonder about
- Differs from the obvious default
- Locks in a constraint (e.g., "chose JWT over sessions because we want stateless")

Format:
```markdown
## YYYY-MM-DD: <short title>

**Why**: <2-4 lines>
```

If the decision is obvious or fully derived from BRIEF.md, skip this step. Do not log routine choices.

### Step 6: Report

Print a short summary:

```
✓ Implemented: <task title>
  Files changed: <list>
  Decisions logged: <yes/no>

Next task: <next unchecked title, or "all tasks done">

Run `git diff` to review, then commit.
```

**Do not** run `git add` or `git commit`. That's the user's gate.

## Guidelines

- **The commit is the only gate.** No "Continue?" prompts. No multi-stage approval.
- **One task per invocation.** If the user wants two tasks, they run `/lite-dev` twice.
- **Resist over-engineering.** If `BRIEF.md` says "personal CLI tool, ~500 LOC," don't introduce dependency injection, plugin systems, or microservices.
- **Trust BRIEF.md.** If the user said "no auth" in out-of-scope, don't add auth even if it would be nice.
- **PLAN.md is mutable.** Splitting tasks, reordering, or adding tasks is fine — just keep it flat and short.

## Example invocations

- `/lite-dev` — work on the next task
- `/lite-dev status` — show progress without doing anything
- `/lite-dev "search endpoint"` — jump to the task whose title contains "search endpoint"
- `/lite-dev next` — same as bare invocation
