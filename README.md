# diataxis-skill

AIエージェントが[Diátaxis](https://diataxis.fr/)にもとづいてドキュメントを整理するためのAgent Skillです。

Diátaxisは、読者がそのページを開いた時点で何を必要としているかによって、ドキュメントを4つのモードに分けます。

| 内容が扱うもの | 読者の状況 | モード |
| --- | --- | --- |
| 行動 | 学んでいる | Tutorial |
| 行動 | 作業している | How-to guide |
| 認識 | 作業している | Reference |
| 認識 | 学んでいる | Explanation |

このスキルは、新しいページをどのモードに置くかを判断し、4つのモードにもとづいたディレクトリ構成を作り、複数のモードが混ざったページを見つけます。

## Install

[スキルのインストール方法](docs/how-to/install-the-skill.md)を参照してください。

## Usage

ドキュメントの構成が問題になったときに動きます。Diátaxisという語を出す必要はありません。

「このページはどこに置けばいいか」「なぜこのフォルダは目的のものを探しにくいのか」といった質問に答えます。「docsフォルダを整理してほしい」「このページを分割してほしい」「ここにTutorialが必要かどうか判断してほしい」といった依頼にも応えます。

## Contributing

貢献の手順は[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## License

ライセンスは[LICENSE](LICENSE)を参照してください。
