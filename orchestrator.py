import json
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from agents.collector_agent import create_collector_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.marketer_agent import create_marketer_agent
from agents.executor_agent import create_executor_agent
from agents.coo_agent import create_coo_agent
from agents.sns_strategy_agent import create_sns_strategy_agent
from agents.content_planning_agent import create_content_planning_agent

console = Console()
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def run_pipeline(dry_run: bool = False) -> dict:
    started_at = datetime.now()
    console.print(Panel.fit(
        f"[bold]エネルギー情報収集パイプライン[/bold]\n{started_at.strftime('%Y-%m-%d %H:%M:%S')} 開始",
        border_style="green",
    ))

    results = {}

    collector = create_collector_agent()
    collected = collector.run(
        f"現在時刻: {started_at.strftime('%Y年%m月%d日 %H:%M')}\n"
        "すべての情報ソースから最新エネルギー・環境ビジネス情報を収集してください。"
    )
    results["collected"] = collected
    _save_output("1_collected", collected)

    summarizer = create_summarizer_agent()
    summary = summarizer.run(f"以下の収集データを分析してレポートを作成してください。\n\n{collected}")
    results["summary"] = summary
    _save_output("2_summary", summary)

    marketer = create_marketer_agent()
    formatted_raw = marketer.run(f"以下のレポートを各プラットフォーム向けに最適化してください。\n\n{summary}")
    results["formatted_raw"] = formatted_raw
    _save_output("3_formatted", formatted_raw)

    formatted = _parse_formatted(formatted_raw)
    results["formatted"] = formatted

    if dry_run:
        console.print("\n[yellow]⚠ ドライランモード: 投稿をスキップします[/yellow]")
        results["publish"] = {"status": "dry_run"}
    else:
        executor = create_executor_agent()
        pub = executor.run(
            f"Notionタイトル: {formatted.get('notion', {}).get('title', 'エネルギーレポート')}\n"
            f"Notion本文:\n{formatted.get('notion', {}).get('content', summary)}\n\n"
            f"noteタイトル: {formatted.get('note', {}).get('title', 'エネルギーレポート')}\n"
            f"note本文:\n{formatted.get('note', {}).get('content', summary)}"
        )
        results["publish"] = pub
        _save_output("4_publish", pub)

    elapsed = (datetime.now() - started_at).seconds
    note_title = formatted.get("note", {}).get("title", "")
    console.print(Panel.fit(
        f"[bold green]✅ 完了[/bold green] ({elapsed}秒)\nnote: 「{note_title}」",
        border_style="green",
    ))
    return results


def run_strategy(context: str = "") -> str:
    started_at = datetime.now()
    console.print(Panel.fit(
        f"[bold]COO戦略パイプライン（エネルギー）[/bold]\n{started_at.strftime('%Y-%m-%d %H:%M:%S')} 開始",
        border_style="red",
    ))

    recent = _load_latest_output("2_summary")

    sns = create_sns_strategy_agent()
    sns_strategy = sns.run(f"現在の情報:\n{recent}\n\nエネルギー・環境ビジネス分野でのSNS発信戦略を立案してください。")
    _save_output("strategy_sns", sns_strategy)

    planner = create_content_planning_agent()
    content_plan = planner.run(
        f"市場情報:\n{recent}\n\nSNS戦略:\n{sns_strategy}\n\n直近1週間のコンテンツカレンダーを作成してください。"
    )
    _save_output("strategy_content", content_plan)

    coo = create_coo_agent()
    coo_report = coo.run(
        f"【SNS戦略部】\n{sns_strategy}\n\n【コンテンツ企画部】\n{content_plan}\n\n【追加指示】\n{context or 'なし'}"
    )
    _save_output("strategy_coo", coo_report)

    elapsed = (datetime.now() - started_at).seconds
    console.print(Panel.fit(f"[bold red]✅ COO戦略レポート完了[/bold red] ({elapsed}秒)", border_style="red"))
    return coo_report


def _load_latest_output(step_suffix: str) -> str:
    files = sorted(OUTPUT_DIR.glob(f"*_{step_suffix}.txt"), reverse=True)
    return files[0].read_text(encoding="utf-8") if files else "（まだ情報収集が実行されていません）"


def _parse_formatted(raw: str) -> dict:
    try:
        start, end = raw.find("{"), raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except json.JSONDecodeError:
        pass
    return {"note": {"title": "エネルギーレポート", "content": raw}, "notion": {"title": "エネルギーレポート", "content": raw}, "tweets": []}


def _save_output(step: str, content: str):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    (OUTPUT_DIR / f"{ts}_{step}.txt").write_text(content, encoding="utf-8")
