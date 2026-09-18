# コントリビュート

## スキルを変更する

4つのモードに関わる部分を変更するときは、先に一次情報である[Diátaxis](https://diataxis.fr/)を読んでください。このリポジトリはDiátaxisを適用するものであり、解釈を加えるものではありません。

Diátaxisに書かれていない運用上の優先順位を規則にしないでください。「このモードから手を付けると効果が大きい」のような判断は、根拠がなければ書きません。

`SKILL.md`と`references/`はDiátaxisの翻案を含むため、CC BY-SA 4.0です。詳細は[NOTICE](NOTICE)にあります。

`SKILL.md`は500行未満に保ちます。詳細は`references/`に置いてください。エージェントは必要になったときだけそれを読みます。

変更したら、次の2つで検証します。

```bash
claude plugin validate . --strict
claude plugin validate ./skills --strict
python3 tests/check_repo.py
```

`claude plugin validate`は仕様準拠の確認です。frontmatterの形式、必須フィールド、`name`とディレクトリ名の一致などは、こちらが正です。

`tests/check_repo.py`はこのリポジトリ固有の確認です。同梱ファイルの実在、2つのmanifestの整合、Markdownの相対リンク、evalの構造を見ます。仕様の再実装はここには書かないでください。

## スキルの判断を変更する

スキルが下す判断を変えるときは、変更前なら失敗したはずのcaseを`evals/diataxis/`に足してください。どの採点器にも引っかからない変更は、判断ではなく文言の変更です。

```bash
claude plugin eval .
```

`Δ`が0のcaseは、スキルを読み込まなくても同じ結果になるcaseです。測っている対象を見直してください。

`SKILL.md`や`references/`に載っている例をcaseの題材にしないでください。例の再現を測ることになります。

## 問題を報告する

与えたプロンプト、与えたドキュメントの構成、返ってきた答えを添えてissueを作成してください。

このスキルが出すのは判断です。納得できない判断そのものが、何が起きたかの説明よりも多くを伝えます。
