# How to install the skill

The skill is a plain [Agent Skills](https://agentskills.io/specification) directory.
Installing it means putting that directory where your agent looks.

## Copy the folder

```bash
git clone https://github.com/yuusakuri/diataxis-skill
cp -r diataxis-skill/skills/diataxis <target>/
```

`<target>` is the directory your agent reads.

| Target | Read by |
|---|---|
| `.agents/skills/` | Codex, Gemini CLI, OpenCode, Copilot, CommandCode |
| `.claude/skills/` | Claude Code |
| `.cursor/skills/` | Cursor |

`.agents/skills/` is the shared convention.
Claude Code and Cursor do not read it, so write their directories too if you use them.

## Install as a plugin

Agents with a plugin system can fetch the skill instead of copying it.
In Claude Code:

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## Check it worked

Ask the agent: *"our docs folder is a mess, where should things go?"*
It should answer in terms of tutorials, how-to guides, reference and explanation.

If it does not, the skill is not loaded.
Restart the session, and check the directory you copied into contains `diataxis/SKILL.md`.
