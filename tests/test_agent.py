"""エージェントの配線テスト。

TestModel は実際のLLMを呼ばない偽モデルで、登録されたツールを全部呼んでから
ダミーの回答を返す。APIキーも利用枠も使わずに、
「ツールが登録され、呼ばれ、結果がモデルに戻るか」を確かめられる。
"""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pydantic_ai import DeferredToolRequests
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models.test import TestModel

import app.agent as agent_module
from app.agent import agent

BASE_TOOLS = {"search_glossary", "get_lecture_summary", "make_quiz", "save_learning_log"}


def _parts(result, kind):
    return [p for m in result.all_messages() for p in m.parts if isinstance(p, kind)]


def test_base_tools_are_registered_and_called():
    model = TestModel()
    with agent.override(model=model):
        result = agent.run_sync("LoRAとは？")

    offered = {t.name for t in model.last_model_request_parameters.function_tools}
    assert BASE_TOOLS <= offered  # 演習でツールを足しても壊れないよう「含む」で判定

    called = {p.tool_name for p in _parts(result, ToolCallPart)}
    assert BASE_TOOLS <= called
    # 承認が必要なツール（requires_approval=True）は、実行されずに承認待ちになるので戻り値が無い
    assert isinstance(result.output, DeferredToolRequests)
    waiting = len(result.output.approvals)
    assert {call.tool_name for call in result.output.approvals} == {"save_learning_log"}
    assert len(_parts(result, ToolReturnPart)) + waiting == len(_parts(result, ToolCallPart))
    assert result.output


def test_glossary_result_reaches_the_model():
    model = TestModel(call_tools=["search_glossary"])
    with agent.override(model=model):
        result = agent.run_sync("RAGとは？")
    returns = _parts(result, ToolReturnPart)
    assert returns and returns[0].tool_name == "search_glossary"


@pytest.mark.parametrize(("answer", "approved"), [("y", True), ("n", False)])
def test_cli_resumes_with_the_user_approval(answer, approved, monkeypatch, capsys):
    history = [object()]
    pending = SimpleNamespace(
        output=DeferredToolRequests(
            approvals=[
                ToolCallPart(
                    tool_name="save_learning_log",
                    args={"content": "今日学んだこと"},
                    tool_call_id="call-1",
                )
            ]
        ),
        all_messages=lambda: history,
    )
    finished = SimpleNamespace(output="done")
    run_sync = Mock(side_effect=[pending, finished])
    model = object()

    monkeypatch.setattr(agent, "run_sync", run_sync)
    monkeypatch.setattr(agent_module, "build_model", lambda: model)
    monkeypatch.setattr("sys.argv", ["app.agent", "学習を記録して"])
    monkeypatch.setattr("builtins.input", lambda _: answer)

    agent_module.main()

    assert run_sync.call_count == 2
    resume_call = run_sync.call_args_list[1].kwargs
    assert resume_call["message_history"] == history
    assert resume_call["deferred_tool_results"].approvals == {"call-1": approved}
    assert "done" in capsys.readouterr().out
