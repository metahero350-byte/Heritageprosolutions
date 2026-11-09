#!/usr/bin/env python3
"""Build the Heritage blog from blog-src/*.md.

Each post is a Markdown file with front matter:
    ---
    title: "Post title"
    slug: "post-url-slug"
    date: "2026-11-08"
    description: "One or two sentences for Google and the cards (optional)."
    cover: "https://... or assets/blog/file.webp"
    ---
    Body in Markdown.

Run:  python3 tools/build_blog.py
Writes post/<slug>/index.html, blog/index.html, blog/posts.json, sitemap-blog.xml.
Post URLs match the old Wix URLs (/post/<slug>) so links keep working after the domain moves.
"""
import json, os, re, glob, html, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.heritageprosolutions.com"          # canonical domain
FORM = "https://api.leadconnectorhq.com/widget/form/G5TdPLSdrlG2OJXl467W"
CLARITY = "https://calendly.com/heritage-protection/complimentary-financial-needs-analysis"
PHONE = "951-236-0684"
LEGAL = ("Educational content only, not individual financial, tax, or legal advice. Strategies and product "
         "availability vary by state, carrier, and individual circumstances. Aaron Duchane Sr. · Heritage "
         "Protection Solutions · Powered by Global Financial Impact · CA Lic# 0K48492 · NV Lic# 4135418. "
         "Outside CA or NV? Reach out, I can expand to serve your state.")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    _, fm, body = raw.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = json.loads(v.strip())
    meta["body_md"] = body.strip()
    return meta


def excerpt(md_text, n=170):
    for para in md_text.split("\n\n"):
        p = para.strip()
        if not p or p.startswith(("#", "!", "-", "1.", ">")):
            continue
        p = re.sub(r"[*_`]", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p))
        if len(p) < 60:
            continue
        return p if len(p) <= n else p[:n].rsplit(" ", 1)[0] + "…"
    return ""


def asset(url, depth):
    """Local repo paths become relative to the page; full URLs pass through."""
    return url if re.match(r"https?://", url) else "../" * depth + url


def fmt_date(d):
    return datetime.date.fromisoformat(d).strftime("%b %-d, %Y")


def page(title, desc, canonical, body, depth, og_image="", extra_head=""):
    css = "../" * depth + "blog/blog.css"
    logo = "../" * depth + "assets/heritage-logo.webp"
    r = "../" * depth or "./"
    blog = r + "blog/"
    og = f'<meta property="og:image" content="{html.escape(og_image)}">' if og_image else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}">{og}
<link rel="icon" href="{logo}">
<link rel="stylesheet" href="{css}">{extra_head}
</head><body>
<header class="hdr"><div class="wrap nav">
  <a class="brand" href="{r}"><img src="{logo}" alt="Heritage Protection Solutions"></a>
  <nav class="links"><a href="{r}">Home</a><a href="{r}about-us/">About</a><a href="{r}faqs/">FAQs</a><a href="{blog}">Blog</a><a href="{r}contact/">Contact</a></nav>
  <a class="btn" href="{FORM}" target="_blank" rel="noopener">Find Your Path →</a>
</div></header>
{body}
<footer class="ftr"><div class="wrap">
  <img src="{logo}" alt="Heritage Protection Solutions" class="flogo">
  <p class="tag">Guardian of Generational Wealth · <a href="tel:+1{PHONE.replace('-', '')}">{PHONE}</a></p>
  <p class="flinks"><a href="{r}">Home</a><a href="{r}about-us/">About</a><a href="{r}about-us/#team">Our Team</a><a href="{r}faqs/">FAQs</a><a href="{r}testimonials/">Client Stories</a><a href="{blog}">Blog</a><a href="{r}contact/">Contact</a><a href="{CLARITY}" target="_blank" rel="noopener">Book a Clarity Session</a></p>
  <p class="legal">{LEGAL}</p>
</div></footer>
</body></html>
"""


def build():
    posts = [parse(p) for p in glob.glob(os.path.join(ROOT, "blog-src", "*.md"))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    index_items = []
    for i, p in enumerate(posts):
        md.reset()
        body_html = md.convert(p["body_md"])
        words = len(re.sub(r"<[^>]+>", " ", body_html).split())
        p["minutes"] = max(1, round(words / 230))
        d = (p.get("description") or "").strip()
        glued = re.search(r"[.!?”\"][“\"A-Z]", d)  # Wix glues sentences/lines together
        p["desc"] = d if d and not glued and len(d) <= 200 else excerpt(p["body_md"])
        p["url"] = f"post/{p['slug']}/"
        canonical = f"{SITE}/post/{p['slug']}"
        # images: lazy-load and make local paths relative to post/<slug>/
        body_html = re.sub(r'<img ([^>]*?)src="([^"]+)"',
                           lambda m: f'<img loading="lazy" onerror="this.remove()" {m.group(1)}src="{asset(m.group(2), 2)}"', body_html)
        cover = p.get("cover", "")
        cover_tag = f'<img class="cover" src="{asset(cover, 2)}" alt="" onerror="this.remove()">' if cover else ""
        nxt = posts[i + 1] if i + 1 < len(posts) else None
        prv = posts[i - 1] if i > 0 else None
        nav = '<nav class="pn">' + \
            (f'<a href="../{prv["slug"]}/">← {html.escape(prv["title"])}</a>' if prv else "<span></span>") + \
            (f'<a href="../{nxt["slug"]}/">{html.escape(nxt["title"])} →</a>' if nxt else "<span></span>") + "</nav>"
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
              "datePublished": p["date"], "description": p["desc"], "mainEntityOfPage": canonical,
              "author": {"@type": "Person", "name": "Aaron Duchane Sr."},
              "publisher": {"@type": "Organization", "name": "Heritage Protection Solutions", "url": SITE}}
        if cover.startswith("http"):
            ld["image"] = cover
        body = f"""<main class="wrap post">
<a class="back" href="../../blog/">← All articles</a>
<div class="kicker">{fmt_date(p['date'])} · {p['minutes']} min read</div>
<h1>{html.escape(p['title'])}</h1>
{cover_tag}
<article class="prose">{body_html}</article>
<aside class="cta"><div><div class="kicker">Your next step can be simple</div>
<h2>Want to see how this applies to your family?</h2>
<p>Start with where you are. We’ll help you understand what deserves attention next.</p></div>
<div class="ctab"><a class="btn" href="{FORM}" target="_blank" rel="noopener">Find Your Path →</a>
<a class="btn ghost" href="{CLARITY}" target="_blank" rel="noopener">Book a Clarity Session</a></div></aside>
{nav}
</main>"""
        head = f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        out = os.path.join(ROOT, "post", p["slug"])
        os.makedirs(out, exist_ok=True)
        og_img = cover if cover.startswith("http") else (f"{SITE}/{cover}" if cover else "")
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(
            page(f"{p['title']} | Heritage Protection Solutions", p["desc"], canonical, body, 2, og_img, head))
        card_img = f'<div class="ci" style="background-image:url(\'{asset(cover, 1)}\')"></div>' if cover else ""
        index_items.append(f"""<a class="card" href="../{p['url']}">{card_img}<div class="cb">
<div class="kicker">{fmt_date(p['date'])} · {p['minutes']} min</div><h3>{html.escape(p['title'])}</h3>
<p>{html.escape(p['desc'])}</p><span class="more">Read article →</span></div></a>""")

    body = f"""<main class="wrap">
<section class="bhead"><div class="kicker">The Heritage Blog</div><h1>Protect today. Prepare for tomorrow.</h1>
<p>Plain-language articles on family protection, retirement, legacy, and building something worth passing on.</p></section>
<div class="grid">{''.join(index_items)}</div></main>"""
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8").write(
        page("Blog | Heritage Protection Solutions",
             "Articles on family protection, retirement, legacy, and financial clarity from Heritage Protection Solutions.",
             f"{SITE}/blog", body, 1))
    feed = [{"title": p["title"], "slug": p["slug"], "date": p["date"], "dateLabel": fmt_date(p["date"]),
             "minutes": p["minutes"], "excerpt": p["desc"], "url": p["url"], "cover": p.get("cover", "")}
            for p in posts]
    json.dump(feed, open(os.path.join(ROOT, "blog", "posts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pages = build_pages(md)
    urls = [f"{SITE}/"] + [f"{SITE}/{s}" for s in pages] + [f"{SITE}/blog"] + [f"{SITE}/post/{p['slug']}" for p in posts]
    sm = "".join(f"<url><loc>{u}</loc></url>" for u in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    old = os.path.join(ROOT, "sitemap-blog.xml")
    if os.path.exists(old):
        os.remove(old)
    print(f"built {len(posts)} posts, {len(pages)} pages, {len(REDIRECTS)} redirects")


# Old Wix addresses that should keep working after the domain moves.
REDIRECTS = {
    "home": "", "team-3": "about-us/#team", "the-heritage-blueprint": "#blueprint",
    "interactive-guide-2": "#wealth-building", "business-succession-protection": "#goals",
    "services": "#goals", "services-5": "#goals", "items": "#goals", "inquiry-services-page": "#goals",
}


def build_pages(md):
    built = []
    for path in sorted(glob.glob(os.path.join(ROOT, "pages-src", "*.md"))):
        p = parse(path)
        body_md = p["body_md"].replace("(FORM)", f"({FORM})").replace('"FORM"', f'"{FORM}"') \
            .replace('"CLARITY"', f'"{CLARITY}"') \
            .replace('"REVIEW"', '"https://calendly.com/heritage-protection/existing-client-policy-review"')
        md.reset()
        body_html = md.convert(body_md)
        body = f"""<main class="wrap post page">
<div class="kicker">{html.escape(p['kicker'])}</div>
<h1>{html.escape(p['heading'])}</h1>
<article class="prose">{body_html}</article>
<aside class="cta"><div><div class="kicker">Your next step can be simple</div>
<h2>You don’t need to have everything figured out before we talk.</h2>
<p>Start with where you are. We’ll help you understand what deserves attention next.</p></div>
<div class="ctab"><a class="btn" href="{FORM}" target="_blank" rel="noopener">Find Your Path →</a>
<a class="btn ghost" href="{CLARITY}" target="_blank" rel="noopener">Book a Clarity Session</a></div></aside>
</main>"""
        out = os.path.join(ROOT, p["slug"])
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(
            page(p["title"], p["description"], f"{SITE}/{p['slug']}", body, 1))
        built.append(p["slug"])
    for old, target in REDIRECTS.items():
        out = os.path.join(ROOT, old)
        os.makedirs(out, exist_ok=True)
        rel = "../" + target
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Heritage Protection Solutions</title>
<link rel="canonical" href="{SITE}/{target}"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={rel}">
<script>location.replace({json.dumps(rel)});</script></head>
<body><p><a href="{rel}">Continue to Heritage Protection Solutions</a></p></body></html>
""")
    return built


if __name__ == "__main__":
    build()
