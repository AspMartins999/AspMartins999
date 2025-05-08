import requests, random, re, feedparser, datetime

USERNAME = "AspMartins999"
README_PATH = "README.md"
BLOG_RSS = "https://matheusmartins.dev.br/rss.xml"  # update when blog is ready
MAX_PRS = 5
MAX_POSTS = 3
QUOTES = [
    "Simplicity is the soul of efficiency. — Austin Freeman",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Walking on water and developing software from specs are easy if both are frozen. — Edward V. Berard",
    "Any fool can write code a computer can understand. Good programmers write code humans can understand. — Martin Fowler",
    "In case of fire: git commit, git push, leave building."
]

def get_merged_prs(user: str):
    url = f"https://api.github.com/search/issues?q=is:pr+author:{user}+is:merged"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    total = data.get("total_count", 0)
    prs = []
    emojis = ["🥳", "🎉", "🎊", "🥂", "🙌🏼"]
    for i, item in enumerate(data.get("items", [])[:MAX_PRS]):
        emoji = emojis[i % len(emojis)]
        pr_url = item["html_url"]
        repo_url = re.sub(r'/pull/\d+', '', pr_url)
        prs.append(f"{i+1}. {emoji} Merged PR [{item['number']}]({pr_url}) - [{item['repository_url'][29:]}]({repo_url})")
    return total, "\n".join(prs)

def get_latest_posts(rss_url: str, max_items: int = 3):
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return ""
    posts = []
    for e in feed.entries[:max_items]:
        date = datetime.datetime(*e.published_parsed[:6]).strftime('%Y-%m-%d') if getattr(e, 'published_parsed', None) else ""
        posts.append(f"- [{e.title}]({e.link}) — {date}")
    return "\n".join(posts)

def replace_block(text: str, start: str, end: str, replacement: str):
    pattern = rf'({re.escape(start)}\n)(.*?)(\n{re.escape(end)})'
    return re.sub(pattern, rf'\1{replacement}\3', text, flags=re.DOTALL)

def update_readme():
    total_prs, prs_md = get_merged_prs(USERNAME)
    prs_count_badge = f'<span><img src="https://img.shields.io/badge/Total_Merged_PRs-{total_prs}-1877F2?style=for-the-badge"></span>'
    blog_md = get_latest_posts(BLOG_RSS, MAX_POSTS)
    quote = random.choice(QUOTES)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    content = replace_block(content, "<!--Start Count Merged PRs-->", "<!--Finish Count Merged PRs-->", prs_count_badge)
    content = replace_block(content, "<!--Start Merged PRs-->", "<!--Finish Merged PRs-->", prs_md)
    if blog_md:
        content = replace_block(content, "<!--START_SECTION:blog-->", "<!--END_SECTION:blog-->", blog_md)
    content = replace_block(content, "<!--START_QUOTE-->", "<!--END_QUOTE-->", quote)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()
