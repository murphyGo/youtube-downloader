# aidlc-lite (template repo)

This is the **aidlc-lite template repo itself**, not a project using it. After cloning, the user runs `/lite-init` and this file is replaced with a project-specific CLAUDE.md.

## Purpose

Lightweight personal AIDLC starter. Three files (`BRIEF.md`, `PLAN.md`, `DECISIONS.md`) and two skills (`/lite-init`, `/lite-dev`).

## Skills

| Skill | Purpose |
|-------|---------|
| `/lite-init` | One-shot 5-question idea capture → generates BRIEF, PLAN, DECISIONS, project CLAUDE.md |
| `/lite-dev` | Picks next unchecked PLAN.md item, implements, checks it off |

## Files

| File | Role |
|------|------|
| `README.md` | What aidlc-lite is, quick start, design principles |
| `templates/BRIEF.md` | Template for the project's one-page brief |
| `templates/PLAN.md` | Template for the project's flat checklist |
| `templates/DECISIONS.md` | Template for the project's ADR log |
| `.claude/skills/lite-init/SKILL.md` | Init skill definition |
| `.claude/skills/lite-dev/SKILL.md` | Dev driver skill definition |

## When developing aidlc-lite itself

- Skills must stay short. `/lite-init` ≤ 200 lines, `/lite-dev` ≤ 120 lines. If a skill grows, you're rebuilding full AIDLC.
- Templates must stay prose-friendly. No FR-001/NFR-001 numbering schemes. No fill-in-the-blank forms.
- Resist adding stages. The whole value prop is "no stages."
- Resist adding `audit.md`, `aidlc-state.md`, refinement-log, cross-check. Git and checklists replace all of these.
- If a feature is "useful for handoff to others" — it belongs in aidlc-starter, not here.

## Promotion path

Out of scope for now. If a user's project grows past ~3k LOC and they want full AIDLC, they manually copy `BRIEF.md` content into an aidlc-starter `IDEA.md` and run `/init-project` there. We do not maintain a migration tool.
