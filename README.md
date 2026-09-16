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

## Install

See [install the skill](docs/how-to/install-the-skill.md).

## Usage

The skill triggers on documentation structure, whether or not Diátaxis is named.
It answers questions — where does this page belong, why is this folder hard to navigate — and it carries out requests: sort out the docs folder, split this page, decide whether we need a tutorial here.

## Why Diátaxis

See [why Diátaxis](docs/explanation/why-diataxis.md), which also covers what it does not apply to.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE).
