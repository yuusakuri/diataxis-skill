# How to install the skill

## Claude Code, as a plugin

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## Any agent, by copying the folder

The skill is a plain [Agent Skills](https://agentskills.io/specification) directory.
Copy it into the directory your agent reads:

```bash
git clone https://github.com/yuusakuri/diataxis-skill
cp -r diataxis-skill/skills/diataxis <target>/
```

| Agent | Target directory |
|---|---|
| Claude Code | `.claude/skills/` |
| Codex, Gemini CLI, OpenCode, Copilot | `.agents/skills/` |
| Cursor | `.cursor/skills/` |

Claude Code reads only `.claude/skills/`.
If you install for several agents, write both directories.

## Check it worked

Ask the agent: *"our docs folder is a mess, where should things go?"* It should answer in terms of tutorials, how-to guides, reference and explanation.

If it does not, the skill is not loaded.
Restart the session, and check the folder you copied into contains `diataxis/SKILL.md`.
