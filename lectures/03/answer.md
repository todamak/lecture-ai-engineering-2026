# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：

[tool call]   search_glossary({'query': 'LoRA'}) 

[tool call]   search_glossary({'query': 'QLoRA'})

- 1つの質問での LLM 呼び出し回数（`requests`）：
2

- 追加したツールと、docstring に書いた説明：

　make_quiz

  """指定した回の用語から1つを選び、
    確認問題と答えを返す。
 
    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """
    # 1. load_glossary() から lecture が一致する用語を集める
    # 2. 1 つ選ぶ（random.choice）
    # 3. 問題と答えを文字列で返す（json.dumps など）


## 宿題

- 取り組んだレベル：発展
- やったこと：
宿題の基礎の中で「用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」を
「必要に応じて search_glossary で用語集を確認する」とすることで「search_glossary」の確認を任意としていた。
そのうえでPydanticAI版で使用していた学習支援エージェントを 、エージェントを組み立てる部分だけを ADK で書き直した場合の挙動を確認した。
用語集にある質問1とない質問2でそれぞれ検証を行った。


- 結果：

1. 質問1「LoRA とQLoRAの違いは？」について

1.1  Pydantic
uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"
[model] gemini-3.5-flash-lite
**LoRA**と**QLoRA**の主な違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを大幅に節約するかにあります。

* **LoRA（Low-Rank Adaptation）**
  * 事前学習済みの重みは固定したまま、重みの更新分（低ランク行列）だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習パラメータを大きく減らすことができます。

* **QLoRA（Quantized LoRA）**
  * LoRAの仕組みをベースにしつつ、**ベースモデルの重みを4ビットなどに量子化**してメモリ消費を極限まで抑えたうえで学習を行う手法です。これにより、より大きなモデルをより小さなGPUメモリで扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0009381'), details={'text_prompt_tokens': 1352}, input_text_tokens=1352, input_tokens=1352, output_tokens=213, requests=2, tool_calls=2)

1.2 ADK:

[user]: uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"
[glossary_agent]: **LoRA**と**QLoRA**の主な違いは、ベースモデルの重みを量子化するかどうか（およびそのビット数）にあります。

* **LoRA（Low-Rank Adaptation）**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな低ランク行列の積として表し、その小さな行列だけを学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。学習パラメータや保存ファイルを大幅に削減できます。

* **QLoRA（Quantized LoRA）**
  ベースモデルの重みを4ビットなどに量子化（Quantization）してメモリをさらに節約した状態で固定し、その上でLoRAによるファインチューニングを行う手法です。これにより、より大きなモデルを限られたVRAM（GPUメモリ）の環境でも効率よく学習できるようになります。


2. 質問2「AIE2026のlec02-startタグとは？」

2.1  Pydantic

$ uv run python -m app.agent --trace "AIE2026のlec02-startタグとは？"

[model] gemini-3.5-flash-lite用語集には「lec02-startタグ」という言葉は登録されていません。推測や不確実な情報でお答えすることはできませんが、おそらく第2回（lec02）の演習やハンズオンを開始する際に関連するGitのタグ、ブランチ、またはソースコードの目印などを指している可能性が高いと考えられます。第2回の内容や詳細については、該当回の講義を確認してみてください。
第2回

--- trace ---[tool call]   search_glossary({'query': 'lec02-startタグ'})[tool return] search_glossary -> 用語集に「lec02-startタグ」は見つかりませんでした。…[usage] RunUsage(cost=Decimal('0.0005499'), details={'text_prompt_tokens': 858}, input_text_tokens=858, input_tokens=858, output_tokens=117, requests=2, tool_calls=1)　

2.2 ADK

[user]: uv run python -m app.agent --trace "AIE2026のlec02-startタグとは？"
[glossary_agent]: 用語集には「lec02-start」という用語は登録されていません。

講座の第2回の内容や特定のタグについてお知りになりたい場合は、関連する用語（例：Gitや環境構築に関する用語など）で改めてお調べするか、第2回の講義内容についてご確認ください。

（第2回）

- 気づき・疑問：

質問１は、ADKでも、回答内容は用語集の定義と整合しており、LoRA、QLoRA、第2回が正しく説明されていた。
ただしツール呼び出し履歴が表示されないため、search_glossary が実際に呼ばれたかを直接確認することはできなかった。

また「必要に応じて」の変更だけでは大きな変化は見られなかった。
LoRA/QLoRA のようなの一般的な用語については、依然として用語集ベースの回答を生成したことから必要と判断し参考にしているようである。

質問2は用語集に見つからないことは、推測で断定せず「用語集にはない」と伝えるは概ね守られていた。
一方で、基礎で設定を変えていた影響で、Gitタグやブランチ名の可能性が高いという推測はそれぞれ行っていた。