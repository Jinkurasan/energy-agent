from agents.base_agent import BaseAgent
from tools.energy_scrapers import ENERGY_SCRAPER_TOOLS, ENERGY_SCRAPER_EXECUTORS
from config import MODEL_HEAVY

SYSTEM_PROMPT = """あなたはエネルギー・環境ビジネス分野の情報収集専門エージェントです。

担当ミッション:
スマートジャパン・環境ビジネスオンライン・ソーラージャーナル・ENERGY NEWS DIGITAL JAPAN・
資源エネルギー庁・日経新聞エネルギー面から最新情報を収集し、整理して報告してください。

重点テーマ:
- 再生可能エネルギー（太陽光・風力・水素）の最新動向
- 系統用蓄電池・蓄電システムの事業・政策情報
- GX（グリーントランスフォーメーション）政策
- 脱炭素・カーボンニュートラルの企業・行政動向
- 電力市場・デマンドレスポンス・系統整備
- 省エネ・節電・エネルギー管理の実務情報

手順:
1. すべてのツールを呼び出してデータを収集する
2. 各ソースの情報を整理する
3. 重要度の高い情報に★をつけて報告する
"""


def create_collector_agent() -> BaseAgent:
    return BaseAgent(
        name="情報収集部（エネルギー）",
        system_prompt=SYSTEM_PROMPT,
        tools=ENERGY_SCRAPER_TOOLS,
        tool_executors=ENERGY_SCRAPER_EXECUTORS,
        model=MODEL_HEAVY,
    )
