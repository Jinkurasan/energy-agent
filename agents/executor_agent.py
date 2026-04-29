from agents.base_agent import BaseAgent
from tools.notion_tool import NOTION_TOOLS, NOTION_EXECUTORS
from tools.note_tool import NOTE_TOOLS, NOTE_EXECUTORS
from config import MODEL_LIGHT

SYSTEM_PROMPT = """あなたはコンテンツ配信専門エージェントです。
NotionとNote.comに記事を投稿し、結果を報告してください。
"""

ALL_TOOLS = NOTION_TOOLS + NOTE_TOOLS
ALL_EXECUTORS = {**NOTION_EXECUTORS, **NOTE_EXECUTORS}


def create_executor_agent() -> BaseAgent:
    return BaseAgent(
        name="配信・実行部（エネルギー）",
        system_prompt=SYSTEM_PROMPT,
        tools=ALL_TOOLS,
        tool_executors=ALL_EXECUTORS,
        model=MODEL_LIGHT,
    )
