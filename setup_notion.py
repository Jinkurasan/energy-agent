"""
energy-agent用のNotionデータベースを自動作成するセットアップスクリプト。
"""
from notion_client import Client

key = input("Notionシークレットキー(secret_xxx... または ntn_xxx...)を貼り付けてEnter: ").strip()
page_url = input("NotionページのURLを貼り付けてEnter: ").strip()

# URLからページIDを抽出
page_id = page_url.split("/")[-1].split("?")[0]
if "-" in page_id:
    page_id = page_id.replace("-", "")
page_id = page_id[-32:] if len(page_id) >= 32 else page_id

print(f"\nデータベース作成中... (Page ID: {page_id})")

try:
    notion = Client(auth=key)
    db = notion.databases.create(
        parent={"type": "page_id", "page_id": page_id},
        title=[{"text": {"content": "エネルギーレポート"}}],
        properties={
            "タイトル": {"title": {}},
            "カテゴリ": {"select": {}},
            "公開日": {"date": {}},
            "ステータス": {"select": {}},
        },
    )
    db_id = db["id"]
    print(f"\n✅ 作成完了！")
    print(f"\n以下を energy-agent/.env の NOTION_DATABASE_ID に設定してください：")
    print(f"NOTION_DATABASE_ID={db_id}")

except Exception as e:
    print(f"\n❌ エラー: {e}")
