# スキルのインストール方法

このスキルは[Agent Skills](https://agentskills.io/specification)の形式に従ったただのディレクトリである。
インストールとは、そのディレクトリをエージェントが読む場所に置くことを指す。

## フォルダをコピーする

```bash
git clone https://github.com/yuusakuri/diataxis-skill
cp -r diataxis-skill/skills/diataxis <target>/
```

`<target>`は、使っているエージェントが読むディレクトリである。

| 置き場所 | 読むエージェント |
| --- | --- |
| `.agents/skills/` | Codex、Gemini CLI、OpenCode、Copilot、CommandCode |
| `.claude/skills/` | Claude Code |
| `.cursor/skills/` | Cursor |

`.agents/skills/`が共通の置き場である。
Claude CodeとCursorはここを読まないので、これらを使う場合はそれぞれのディレクトリにも書き込む。

## プラグインとして入れる

プラグイン機構を持つエージェントなら、コピーせずに取得できる。
Claude Codeの場合は次のとおり。

```bash
/plugin marketplace add yuusakuri/diataxis-skill
/plugin install diataxis@diataxis-skill
```

## 動作を確認する

エージェントに「docsフォルダがぐちゃぐちゃなんだけど、どう置くべき？」と尋ねる。
チュートリアル、ハウツーガイド、リファレンス、説明という言葉で答えが返るはずである。

返らない場合、スキルが読み込まれていない。
セッションを再起動し、コピー先のディレクトリに`diataxis/SKILL.md`があることを確認する。
