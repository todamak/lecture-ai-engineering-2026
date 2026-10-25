import sys
from types import SimpleNamespace
from unittest.mock import Mock

import app.ask as ask_module


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return SimpleNamespace(text=f"回答{len(self.questions)}", usage_metadata=None)


def test_interactive_mode_keeps_chat_and_reports_response_time(monkeypatch, capsys):
    chat = FakeChat()
    client = Mock()
    inputs = iter(["次の質問", "quit"])
    timestamps = iter([10.0, 10.25, 11.0, 12.5])
    monkeypatch.setattr(ask_module, "create_chat", Mock(return_value=(client, chat)))
    monkeypatch.setattr(sys, "argv", ["app.ask", "--interactive", "最初の質問"])
    monkeypatch.setattr("builtins.input", Mock(side_effect=inputs))
    monkeypatch.setattr(ask_module, "perf_counter", lambda: next(timestamps))

    ask_module.main()

    output = capsys.readouterr().out
    assert chat.questions == ["最初の質問", "次の質問"]
    assert "[応答時間] 0.25秒" in output
    assert "[応答時間] 1.50秒" in output
    assert "回答1" in output
    assert "回答2" in output
    client.close.assert_called_once_with()


def test_ask_creates_chat_when_one_is_not_provided(monkeypatch, capsys):
    chat = FakeChat()
    client = Mock()
    monkeypatch.setattr(ask_module, "create_chat", Mock(return_value=(client, chat)))
    monkeypatch.setattr(ask_module, "perf_counter", iter([1.0, 1.1]).__next__)

    result = ask_module.ask("質問", temperature=0.3)

    assert result == "回答1"
    assert chat.questions == ["質問"]
    assert "[応答時間] 0.10秒" in capsys.readouterr().out
    client.close.assert_called_once_with()
