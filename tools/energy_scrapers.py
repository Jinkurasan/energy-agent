"""
エネルギー・環境ビジネス分野の情報ソースから収集するスクレイパー群。
"""
import feedparser
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
from config import SESSION_DIR


def _load_context(playwright, site_name: str, headless: bool = True):
    browser = playwright.chromium.launch(headless=headless)
    session_file = SESSION_DIR / f"{site_name}.json"
    if session_file.exists():
        ctx = browser.new_context(storage_state=str(session_file))
    else:
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    return browser, ctx


# ─── スマートジャパン（ITmedia RSS）────────────────────────────────────────────

def scrape_smartjapan(max_articles: int = 10) -> dict:
    """スマートジャパン（ITmedia）のRSSから電力・エネルギーニュースを取得"""
    try:
        feed = feedparser.parse("https://rss.itmedia.co.jp/rss/2.0/smartjapan.xml")
        articles = []
        for entry in feed.entries[:max_articles]:
            articles.append({
                "title": entry.get("title", ""),
                "summary": entry.get("summary", "")[:300],
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            })
        return {"source": "スマートジャパン", "articles": articles, "status": "success"}
    except Exception as e:
        return {"source": "スマートジャパン", "error": str(e), "status": "failed"}


# ─── 環境ビジネスオンライン ─────────────────────────────────────────────────────

def scrape_kankyo_business(max_articles: int = 10) -> dict:
    """環境ビジネスオンラインから再エネ・省エネ実務情報を取得"""
    browser = None
    try:
        with sync_playwright() as p:
            browser, ctx = _load_context(p, "kankyo")
            page = ctx.new_page()
            page.goto("https://www.kankyo-business.jp/news/", timeout=20000)
            page.wait_for_load_state("domcontentloaded", timeout=10000)

            soup = BeautifulSoup(page.content(), "lxml")
            articles = []

            for item in soup.select("article, .news-item, li.list-item, div.article-item")[:max_articles]:
                title_el = item.select_one("h2, h3, a.title, a")
                date_el = item.select_one("time, .date, span.date")
                if title_el and title_el.get_text(strip=True):
                    articles.append({
                        "title": title_el.get_text(strip=True),
                        "date": date_el.get_text(strip=True) if date_el else "",
                        "link": title_el.get("href", ""),
                    })

            browser.close()
            return {"source": "環境ビジネスオンライン", "articles": articles, "status": "success"}
    except Exception as e:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        return {"source": "環境ビジネスオンライン", "error": str(e), "status": "failed"}


# ─── ソーラージャーナル ─────────────────────────────────────────────────────────

def scrape_solar_journal(max_articles: int = 10) -> dict:
    """ソーラージャーナルから太陽光・再エネ情報を取得"""
    browser = None
    try:
        with sync_playwright() as p:
            browser, ctx = _load_context(p, "solarjournal")
            page = ctx.new_page()
            page.goto("https://solarjournal.jp/", timeout=20000)
            page.wait_for_load_state("domcontentloaded", timeout=10000)

            soup = BeautifulSoup(page.content(), "lxml")
            articles = []

            for item in soup.select("article, .post, .entry")[:max_articles]:
                title_el = item.select_one("h2, h3, .entry-title, a")
                excerpt_el = item.select_one("p, .excerpt")
                if title_el and title_el.get_text(strip=True):
                    articles.append({
                        "title": title_el.get_text(strip=True),
                        "excerpt": excerpt_el.get_text(strip=True)[:200] if excerpt_el else "",
                    })

            browser.close()
            return {"source": "ソーラージャーナル", "articles": articles, "status": "success"}
    except Exception as e:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        return {"source": "ソーラージャーナル", "error": str(e), "status": "failed"}


# ─── ENERGY NEWS DIGITAL JAPAN ─────────────────────────────────────────────────

def scrape_energy_news_digital(max_articles: int = 10) -> dict:
    """ENERGY NEWS DIGITAL JAPANからエネルギー専門ニュースを取得"""
    browser = None
    try:
        with sync_playwright() as p:
            browser, ctx = _load_context(p, "energynews")
            page = ctx.new_page()
            page.goto("https://news.kcsf.co.jp/", timeout=20000)
            page.wait_for_load_state("domcontentloaded", timeout=10000)

            soup = BeautifulSoup(page.content(), "lxml")
            articles = []

            for item in soup.select("article, .news-item, .post, li")[:max_articles]:
                title_el = item.select_one("h2, h3, a")
                if title_el and len(title_el.get_text(strip=True)) > 10:
                    articles.append({
                        "title": title_el.get_text(strip=True),
                        "link": title_el.get("href", ""),
                    })

            browser.close()
            return {"source": "ENERGY NEWS DIGITAL JAPAN", "articles": articles, "status": "success"}
    except Exception as e:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        return {"source": "ENERGY NEWS DIGITAL JAPAN", "error": str(e), "status": "failed"}


# ─── 資源エネルギー庁 ──────────────────────────────────────────────────────────

def scrape_enecho(max_articles: int = 10) -> dict:
    """資源エネルギー庁から政策・制度改正の一次情報を取得"""
    browser = None
    try:
        with sync_playwright() as p:
            browser, ctx = _load_context(p, "enecho")
            page = ctx.new_page()
            page.goto("https://www.enecho.meti.go.jp/category/saving_and_new/", timeout=20000)
            page.wait_for_load_state("domcontentloaded", timeout=10000)

            soup = BeautifulSoup(page.content(), "lxml")
            articles = []

            for item in soup.select("li, .news-item, tr")[:max_articles]:
                title_el = item.select_one("a")
                date_el = item.select_one("time, .date, td.date")
                if title_el and len(title_el.get_text(strip=True)) > 10:
                    articles.append({
                        "title": title_el.get_text(strip=True),
                        "date": date_el.get_text(strip=True) if date_el else "",
                        "link": "https://www.enecho.meti.go.jp" + title_el.get("href", ""),
                    })

            browser.close()
            return {"source": "資源エネルギー庁", "articles": articles, "status": "success"}
    except Exception as e:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        return {"source": "資源エネルギー庁", "error": str(e), "status": "failed"}


# ─── 日経GX（無料部分）─────────────────────────────────────────────────────────

def scrape_nikkei_energy(max_articles: int = 10) -> dict:
    """日経新聞の環境・エネルギー関連ニュースを取得"""
    try:
        feed = feedparser.parse("https://www.nikkei.com/rss/menu.xml")
        articles = []
        energy_keywords = ["エネルギー", "再エネ", "脱炭素", "GX", "蓄電池", "太陽光", "風力", "水素", "カーボン"]
        for entry in feed.entries:
            title = entry.get("title", "")
            if any(kw in title for kw in energy_keywords):
                articles.append({
                    "title": title,
                    "summary": entry.get("summary", "")[:200],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                })
            if len(articles) >= max_articles:
                break
        return {"source": "日経新聞（エネルギー関連）", "articles": articles, "status": "success"}
    except Exception as e:
        return {"source": "日経新聞（エネルギー関連）", "error": str(e), "status": "failed"}


# ─── 経産省プレスリリース ───────────────────────────────────────────────────────

def scrape_meti_press(max_articles: int = 10) -> dict:
    """経産省・資源エネルギー庁のプレスリリースRSSから政策情報を取得"""
    rss_urls = [
        "https://www.meti.go.jp/rss/whatsnew.rdf",
        "https://www.enecho.meti.go.jp/rss/whatsnew.rdf",
    ]
    energy_keywords = ["再エネ", "蓄電", "水素", "GX", "脱炭素", "太陽光", "風力", "電力", "省エネ", "カーボン"]
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                articles = []
                for entry in feed.entries:
                    title = entry.get("title", "")
                    if any(kw in title for kw in energy_keywords) or not energy_keywords:
                        articles.append({
                            "title": title,
                            "summary": entry.get("summary", "")[:300],
                            "link": entry.get("link", ""),
                            "published": entry.get("published", ""),
                        })
                    if len(articles) >= max_articles:
                        break
                if articles:
                    return {"source": "経産省プレスリリース", "articles": articles, "status": "success"}
        except Exception:
            continue
    return {"source": "経産省プレスリリース", "error": "取得失敗", "status": "failed"}


# ─── Reuters エネルギー ────────────────────────────────────────────────────────

def scrape_reuters_energy(max_articles: int = 8) -> dict:
    """Reuters（英語）からエネルギー・環境分野のグローバルニュースを取得"""
    rss_urls = [
        "https://feeds.reuters.com/reuters/environment",
        "https://feeds.reuters.com/reuters/businessNews",
    ]
    energy_keywords = ["energy", "renewable", "solar", "wind", "hydrogen", "battery", "carbon", "climate", "ESG", "green"]
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                articles = []
                for entry in feed.entries:
                    title = entry.get("title", "").lower()
                    if any(kw in title for kw in energy_keywords):
                        articles.append({
                            "title": entry.get("title", ""),
                            "summary": entry.get("summary", "")[:300],
                            "link": entry.get("link", ""),
                            "published": entry.get("published", ""),
                        })
                    if len(articles) >= max_articles:
                        break
                if articles:
                    return {"source": "Reuters（エネルギー）", "articles": articles, "status": "success"}
        except Exception:
            continue
    return {"source": "Reuters（エネルギー）", "error": "取得失敗", "status": "failed"}


# ─── 東洋経済（エネルギー関連）──────────────────────────────────────────────────

def scrape_toyo_keizai_energy(max_articles: int = 8) -> dict:
    """東洋経済オンラインからエネルギー・GX関連記事をRSSで取得"""
    energy_keywords = ["エネルギー", "再エネ", "脱炭素", "GX", "蓄電池", "太陽光", "風力", "水素", "カーボン", "省エネ", "電力"]
    try:
        feed = feedparser.parse("https://toyokeizai.net/list/feed/rss")
        articles = []
        for entry in feed.entries:
            title = entry.get("title", "")
            if any(kw in title for kw in energy_keywords):
                articles.append({
                    "title": title,
                    "summary": entry.get("summary", "")[:300],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                })
            if len(articles) >= max_articles:
                break
        return {"source": "東洋経済（エネルギー）", "articles": articles, "status": "success"}
    except Exception as e:
        return {"source": "東洋経済（エネルギー）", "error": str(e), "status": "failed"}


# ── ツール定義 ───────────────────────────────────────────────────────────────

ENERGY_SCRAPER_TOOLS = [
    {
        "name": "scrape_smartjapan",
        "description": "スマートジャパン（ITmedia）から電力・蓄電池・再エネニュースを取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_kankyo_business",
        "description": "環境ビジネスオンラインから再エネ・省エネ実務情報を取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_solar_journal",
        "description": "ソーラージャーナルから太陽光・再エネ業界情報を取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_energy_news_digital",
        "description": "ENERGY NEWS DIGITAL JAPANから系統用蓄電池・エネルギー専門ニュースを取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_enecho",
        "description": "資源エネルギー庁から政策・制度改正の一次情報を取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_nikkei_energy",
        "description": "日経新聞からエネルギー・GX・脱炭素関連ニュースを取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_meti_press",
        "description": "経産省・資源エネルギー庁の公式プレスリリースから政策・制度情報を取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "scrape_reuters_energy",
        "description": "Reuters（英語）からグローバルエネルギー・ESG・再エネニュースを取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 8}},
        },
    },
    {
        "name": "scrape_toyo_keizai_energy",
        "description": "東洋経済オンラインからエネルギー・GX関連の分析記事を取得します",
        "input_schema": {
            "type": "object",
            "properties": {"max_articles": {"type": "integer", "default": 8}},
        },
    },
]

ENERGY_SCRAPER_EXECUTORS = {
    "scrape_smartjapan": scrape_smartjapan,
    "scrape_kankyo_business": scrape_kankyo_business,
    "scrape_solar_journal": scrape_solar_journal,
    "scrape_energy_news_digital": scrape_energy_news_digital,
    "scrape_enecho": scrape_enecho,
    "scrape_nikkei_energy": scrape_nikkei_energy,
    "scrape_meti_press": scrape_meti_press,
    "scrape_reuters_energy": scrape_reuters_energy,
    "scrape_toyo_keizai_energy": scrape_toyo_keizai_energy,
}
