# 環境構築教材・試作版

公開サイト：https://kazuyukit.github.io/seminar-55/

原稿はmainブランチ、生成済みWeb・PDFはgh-pagesブランチで管理します。

学生向け原稿は `index.qmd` と `lesson/environment-setup.qmd` です。Markdown演習、macOS / Windowsの導入、GitHub・Educationの申請を含みます。

## 再生成

Quarto 1.10.18で生成確認。教材のコードは説明用で実行しません。PythonやJupyterはビルドに不要です。

```sh
quarto render --to all
quarto preview
```

生成物は `_book/` にあります。Web版は `_book/index.html`、PDF版は同フォルダのPDFです。Web版はサイト一式を保ったまま利用してください。検索などはHTTPサーバー経由で確認します。

PDFはQuarto内蔵のTypstを使います。今回の環境では日本語フォントHiragino Sansを指定しています。他のOSやGitHub Actionsでは、日本語フォント（例：Noto Sans CJK JP）を導入し、`_quarto.yml` の `mainfont` をそのフォント名に変更してください。フォント一覧は `quarto typst fonts` で確認できます。

## 公開に向けた次の作業

GitHub Pagesはgh-pagesブランチのルートを配信します。更新時は `quarto render --to all` で確認後、`quarto publish gh-pages --no-render` で公開できます。若葉プロファイルが既定で適用されます。著者名、ライセンス、CIでの自動生成は今後の検討事項です。元の参考リポジトリの文章やコードは転載していません。

## 授業担当者向けメモ

Gitのメールを設定する前にGitHubのnoreplyアドレスを取得できるよう、アカウント作成をGit初期設定より先に配置しています。Educationの審査完了は授業内の必須条件にせず、申請状態を記録します。管理PC・未対応OS・証明書不足の学生にはサブゼミで個別対応してください。
