"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask --temperature 0.2 "LoRAとは何ですか？"
    uv run python -m app.ask --interactive
    uv run python -m app.ask --interactive "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールを持たない「素の」呼び出し。--interactive では会話履歴を保って質問できる。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
from time import perf_counter

from google import genai
from google.genai.chats import Chat
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_chat(temperature: float = 1.0) -> tuple[genai.Client, Chat]:
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(
        model=MODEL, config=types.GenerateContentConfig(temperature=temperature)
    )
    return client, chat


def ask(question: str, temperature: float = 1.0, *, chat: Chat | None = None) -> str:
    client = None
    if chat is None:
        client, chat = create_chat(temperature)

    try:
        started_at = perf_counter()
        response = chat.send_message(question)
        elapsed = perf_counter() - started_at
        print(f"[応答時間] {elapsed:.2f}秒")

        usage = response.usage_metadata
        if usage is not None:
            print(f"[トークン数] 入力: {usage.prompt_token_count}, 出力: {usage.candidates_token_count}")

        return response.text
    finally:
        if client is not None:
            client.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="生成時の temperature（0.0〜2.0、既定値: 1.0）",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="会話履歴を保ちながら対話する（終了: exit または quit）",
    )
    args = parser.parse_args()
    if not 0.0 <= args.temperature <= 2.0:
        parser.error("--temperature は 0.0〜2.0 の範囲で指定してください")

    print(f"[model] {MODEL}")
    print(f"[temperature] {args.temperature}")
    client = None
    try:
        client, chat = create_chat(temperature=args.temperature)
        if args.interactive:
            question = args.question
            while True:
                if question is None:
                    question = input("質問 (終了: exit/quit): ").strip()
                if question.lower() in {"exit", "quit"}:
                    break
                if question:
                    print(f"[質問] {question}\n")
                    print(ask(question, chat=chat))
                question = None
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question, chat=chat))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()
