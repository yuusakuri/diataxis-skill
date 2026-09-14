# diataxis-skill

An [Agent Skill](https://agentskills.io/specification) that helps an AI agent
organise documentation using [Diátaxis](https://diataxis.fr/).

Diátaxis sorts documentation by what the reader needs when they arrive:

| The content informs… | …and serves… | …so it is a |
|---|---|---|
| action (doing) | acquisition of skill (studying) | tutorial |
| action (doing) | application of skill (working) | how-to guide |
| cognition (thinking) | application of skill (working) | reference |
| cognition (thinking) | acquisition of skill (studying) | explanation |

The skill applies that split: it decides where a page belongs, sets up a docs
tree, and finds pages that are doing two jobs at once.

## Install

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## Licence

MIT — see [LICENSE](LICENSE). Diátaxis is the work of Daniele Procida and is
applied here, not reproduced.
