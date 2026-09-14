# diataxis-skill

An [Agent Skill](https://agentskills.io/specification) that helps an AI agent organise documentation using [Diátaxis](https://diataxis.fr/).

Diátaxis sorts documentation by what the reader needs when they arrive:

| The content informs | and serves | so it is a |
|---|---|---|
| action (doing) | acquisition of skill (studying) | tutorial |
| action (doing) | application of skill (working) | how-to guide |
| cognition (thinking) | application of skill (working) | reference |
| cognition (thinking) | acquisition of skill (studying) | explanation |

The skill applies that split.
It decides where a page belongs, sets up a docs tree, and finds pages doing two jobs at once.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Install

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

For other agents, copy `skills/diataxis/` into the directory your agent reads.
See [install the skill](docs/how-to/install-the-skill.md).

## Usage

The skill triggers on questions of documentation structure, whether or not Diátaxis is named.
Ask an agent where a page belongs, or why a docs folder is hard to navigate.

It also ships an auditor you can run directly:

```bash
python3 skills/diataxis/scripts/audit_docs.py docs/
```

It reports pages outside any mode, and pages carrying material from a mode they do not belong to, with line numbers.
Findings are candidates, not verdicts: the tool reads the shape of prose, not its meaning.

## Documentation

[`docs/`](docs/) is organised by Diátaxis, so the framework is visible in the directory names.

| | |
|---|---|
| [Tutorial](docs/tutorials/audit-your-first-docs-tree.md) | Run the auditor for the first time |
| [How-to](docs/how-to/) | Install the skill, run the auditor in CI |
| [Reference](docs/reference/) | Command options, finding types |
| [Explanation](docs/explanation/) | Why Diátaxis, what the skill adds |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
Diátaxis is the work of Daniele Procida and is applied here, not reproduced.
