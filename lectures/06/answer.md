# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：　search_materials　[glossary_search_glossary
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3レベル'})
[tool return] glossary_search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…

- STEP 3 の [tool call]：[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
[tool return] fetch_fetch -> Contents of https://modelcontextprotocol.io/:
> ## Documentation Index
> Fetch the complete documentation index at: http…
- STEP 4 の [tool call]：
MCP サーバー（app/mcp_servers.json）
Amazon S3のバージョニングとは、1つのバケット内で同じオブジェクトの複数のバージョンを同時に保持し、上書きや削除が行われた際にも過去のバージョンを保存・復元できるようにする機能です。これにより、誤操作やアプリケーションのエラーによるデータ消失から簡単に回復することができます。

- 気づき・疑問：

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：発展
- やったこと：　普段業務で使用することのある国土交通省の不動産情報ライブラリAPIのデータのMCP サーバーについて調べた。
参考資料：https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/001987144.pdf　(2026年11月28日16時JST：最終アクセス)

- 結果：
　演習の設定が、複数の起動方式（uvからのプロセス起動、fetchからの実行、URLからの接続等）に対応しているのに対し、本ツールの設定はローカルに配置されたPythonプログラムを直接起動する方式を採用していることが大きく異なっていた。
　また、本ツールはMCPサーバーを起動する際に環境変数を渡すための設定が必要な点でも違いがある。具体的には「"LIBRARY_API_KEY": "your_api_key_here",
  "PYTHONUNBUFFERED": "1",  "LOG_LEVEL": "WARNING"」の設定である。
  APIキーを使って外部サービスにアクセスする構成であるが、設定や情報の管理に注意が必要であるといえる。

- 気づき・疑問：
設計思想の違いがあると感じたが、実行環境の構築、依存関係の管理、認証情報の管理、通信方式、運用、保守などの観点からどちらが良いのか。

