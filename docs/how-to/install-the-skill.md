# スキルのインストール方法

このスキルは[Agent Skills](https://agentskills.io/specification)の形式に従ったディレクトリです。エージェントが読む場所にそのディレクトリを置けば、インストールは完了します。

## ディレクトリをコピーする

リポジトリを取得し、`skills/diataxis`をコピーします。

```bash
git clone https://github.com/yuusakuri/diataxis-skill
cp -r diataxis-skill/skills/diataxis <コピー先>/
```

コピー先は、使っているエージェントによって次のように決まります。

| コピー先 | 読むエージェント |
| --- | --- |
| `.agents/skills/` | Codex、Gemini CLI、OpenCode、GitHub Copilot、CommandCode |
| `.claude/skills/` | Claude Code |
| `.cursor/skills/` | Cursor |

`.agents/skills/`は共通の置き場所です。Claude CodeとCursorはこの場所を読まないため、これらを使うときはそれぞれのディレクトリにもコピーしてください。

## プラグインとして取得する

プラグインの仕組みを持つエージェントでは、コピーの代わりに取得できます。Claude Codeでは次のコマンドを実行します。

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## 動作を確認する

エージェントに「docsフォルダが散らかっているので、どこに何を置けばいいか教えてほしい」と尋ねます。

Tutorial、How-to guide、Reference、Explanationという言葉を使った答えが返れば、スキルは読み込まれています。

返らないときは、コピー先のディレクトリに`diataxis/SKILL.md`があることを確認し、セッションを再起動してください。
