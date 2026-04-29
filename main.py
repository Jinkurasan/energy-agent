"""
使い方:
  python main.py              # 本番実行
  python main.py --dry-run    # テスト実行（投稿なし）
  python main.py --strategy   # COO戦略レポート生成
  python main.py --show       # 最後の記事を表示
"""
import argparse
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def main():
    parser = argparse.ArgumentParser(description="エネルギー情報収集・配信パイプライン")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strategy", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if args.strategy:
        from orchestrator import run_strategy
        report = run_strategy()
        console.print(Markdown(report))
        return

    if args.show:
        output_dir = Path(__file__).parent / "output"
        summaries = sorted(output_dir.glob("*_2_summary.txt"), reverse=True)
        if summaries:
            console.print(Markdown(summaries[0].read_text(encoding="utf-8")))
        else:
            console.print("[yellow]まだ記事がありません[/yellow]")
        return

    from orchestrator import run_pipeline
    run_pipeline(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
