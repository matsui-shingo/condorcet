# -*- coding: utf-8 -*-
"""トップページの素案を3案（a/b/c）生成する。

使い方（Claude が実行する。松井さんが手元で動かす必要はない）:
    python tools/build.py            → リポジトリ直下に index.html, a/, b/, c/ を書く
    python tools/build.py --fragments DIR → 同じ内容を <title>+<style>+本文だけの形で DIR に書く
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- themes
THEMES = {
    "a": {
        "name": "A 白と青",
        "mood": "AI・SaaS の会社の作り。白地に鮮やかな青の面、太いゴシックの見出し、白い角丸カード。写真や絵は使わず文字だけで組む",
        "fonts": "Noto+Sans+JP:wght@400;500;700;900",
        "css": """
:root{--bg:#ffffff;--fg:#0f1b33;--accent:#1e40c8;--deep:#0b2a6b;--line:#dbe1ee;--muted:#5b6780;--soft:#eef2fb;
--display:'Noto Sans JP','Hiragino Sans',sans-serif;--body:'Noto Sans JP','Hiragino Sans',sans-serif;--fs:17px}
header.top{border-bottom:1px solid var(--line)}
header.top .brand{font-weight:900;font-size:1.3rem;color:var(--accent);letter-spacing:-.01em}
header.top .right{display:flex;align-items:center;gap:14px}
.cta{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:700;font-size:.85rem;padding:.45em 1.1em;border-radius:999px}
.menu summary{border:0;padding:0;display:flex;flex-direction:column;align-items:center;gap:3px;color:var(--fg)}
.menu summary .ico{display:block;width:26px;height:18px;position:relative}
.menu summary .ico::before,.menu summary .ico::after,.menu summary .ico i{content:"";position:absolute;left:0;right:0;height:2px;background:var(--fg);border-radius:2px}
.menu summary .ico::before{top:0}.menu summary .ico i{top:8px}.menu summary .ico::after{bottom:0}
.menu summary .lbl{font-size:.62rem;letter-spacing:.05em}
.menu nav{border-radius:14px;border:0;box-shadow:0 12px 32px rgba(11,42,107,.18);padding:.6em 0;min-width:240px}
.menu nav a{font-weight:500;padding:.65em 1.4em}
.hero{background:var(--deep);color:#fff;padding-block:64px 96px}
.hero .name{font-weight:900;font-size:2.9rem;letter-spacing:-.02em;line-height:1.1}
.hero .kana{font-size:.9rem;letter-spacing:.35em;opacity:.8;margin-top:.5em}
.hero .catch{font-weight:900;font-size:1.7rem;line-height:1.45;margin-top:1.6em;text-wrap:pretty}
#service{border-top:0;padding-top:0;background:linear-gradient(var(--deep) 0,var(--deep) 56px,var(--bg) 56px)}
#service dl.summary{background:#fff;border-radius:18px;padding:28px 22px;box-shadow:0 18px 44px rgba(11,42,107,.14)}
dl.summary dt{color:var(--accent);font-weight:900;font-size:.9rem;display:flex;align-items:center;gap:.5em}
dl.summary dt::before{content:"";width:10px;height:10px;background:var(--accent);border-radius:2px}
dl.summary dd{padding-left:1.35em}
section{border-top:0;padding-block:56px}
main > section:nth-of-type(odd):not(#service){background:var(--soft)}
h2{font-weight:900;font-size:1.5rem;letter-spacing:-.01em}
h2::before{content:"";display:block;width:32px;height:5px;background:var(--accent);border-radius:3px;margin-bottom:.8em}
.essay p{line-height:2}
.essay .closing{border-top:0;background:var(--soft);border-radius:14px;padding:20px 18px;margin-top:2em}
main > section:nth-of-type(odd) .essay .closing{background:#fff}
.block{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 18px 16px}
main > section:nth-of-type(even) .block{background:var(--soft);border:0}
.block h3{color:var(--accent);font-weight:900;font-size:1rem}
.more{color:var(--accent);border-bottom:0;font-weight:700}
.figure{border:2px dashed var(--line);border-radius:14px;background:#fff}
.price .row{border-bottom:1px solid var(--line)}
.price .row:first-child{border-top:0}
.price .amt{color:var(--accent);font-weight:900;font-size:1.6rem}
footer{background:var(--deep);color:rgba(255,255,255,.75);border-top:0;padding-block:40px 56px}
footer .co{color:#fff}
footer nav a{color:rgba(255,255,255,.75)}
footer .note{color:rgba(255,255,255,.6)}
footer a{color:#fff}
""",
    },
    "b": {
        "name": "B 生成りと藍鉄",
        "mood": "落ち着いた紺（藍鉄）と生成りの地。丸みのある見出しと読みやすいUDフォント。文字は少し大きめ",
        "fonts": "Zen+Maru+Gothic:wght@500;700&family=BIZ+UDPGothic:wght@400;700",
        "css": """
:root{--bg:#f7f5ef;--fg:#1f2d3d;--accent:#1f2d3d;--sub:#3e6b8f;--line:#d9d4c7;--muted:#5f6b78;--soft:#ecebe3;
--display:'Zen Maru Gothic','Hiragino Maru Gothic ProN',sans-serif;--body:'BIZ UDPGothic','Hiragino Sans',sans-serif;--fs:18px}
header.top{background:var(--accent);color:#fff;border-bottom:0}
header.top .brand{color:#fff;font-weight:700}
.menu summary{color:#fff;border-color:rgba(255,255,255,.55);border-radius:999px;padding:.3em 1em}
.menu nav{border-radius:14px}
.hero{padding-block:60px 44px}
.hero .name{font-family:var(--display);font-weight:700;font-size:2.6rem;color:var(--accent)}
.hero .kana{display:inline-block;background:var(--sub);color:#fff;border-radius:999px;padding:.1em .9em;font-size:.85rem;margin-top:.5em}
.hero .catch{font-family:var(--display);font-weight:700;font-size:1.55rem;line-height:1.6;margin-top:1.3em}
section{border-top:0;padding-block:52px}
main > section:nth-of-type(even){background:var(--soft)}
#service dl.summary{background:#fff;border-radius:18px;padding:26px 22px;box-shadow:0 10px 30px rgba(31,45,61,.10)}
h2{font-family:var(--display);font-weight:700;color:var(--accent)}
h2::before{content:"";display:block;width:36px;height:5px;background:var(--sub);border-radius:3px;margin-bottom:.8em}
dl.summary dt{display:inline-block;background:var(--accent);color:#fff;border-radius:6px;padding:.05em .8em;font-size:.85rem;font-weight:700}
.essay .closing{border-top:0;background:#fff;border-radius:14px;padding:20px 18px}
.block{background:#fff;border-radius:14px;padding:18px 18px 16px}
main > section:nth-of-type(odd) .block{background:var(--soft)}
.block h3{font-family:var(--display);color:var(--sub);font-weight:700}
.more{color:var(--sub);border-bottom:0;font-weight:700}
.price .row:first-child{border-top:0}
.price .amt{color:var(--sub);font-family:var(--display);font-weight:700;font-size:1.55rem}
.figure{background:#fff;border:2px dashed var(--line);border-radius:14px}
footer{background:var(--accent);color:rgba(255,255,255,.75);border-top:0;padding-block:40px 56px}
footer .co{color:#fff}
footer nav a{color:rgba(255,255,255,.75)}
footer .note{color:rgba(255,255,255,.6)}
footer a{color:#fff}
""",
    },
    "c": {
        "name": "C 白・黒・山吹",
        "mood": "力強い・現場。白地に黒の太い見出し、黄色の下線。工事看板のようなはっきりした見た目",
        "fonts": "Zen+Kaku+Gothic+New:wght@500;900&family=Noto+Sans+JP:wght@400;700",
        "css": """
:root{--bg:#ffffff;--fg:#111111;--accent:#111111;--line:#111111;--muted:#555555;--soft:#fff7d6;--mark:#f2b705;
--display:'Zen Kaku Gothic New','Hiragino Sans',sans-serif;--body:'Noto Sans JP','Hiragino Sans',sans-serif;--fs:17px}
header.top{background:#111;color:#fff;border-bottom:4px solid var(--mark)}
header.top .brand{color:#fff}
.menu summary{color:#fff;border-color:#fff}
.hero .name{font-family:var(--display);font-weight:900;font-size:2.7rem;letter-spacing:-.01em}
.hero .kana{font-weight:700;font-size:.9rem;letter-spacing:.2em}
.hero .catch{font-family:var(--display);font-weight:900;font-size:1.6rem;line-height:1.5;margin-top:1.2em;
background:linear-gradient(transparent 62%,var(--mark) 62%);display:inline;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.hero .catchwrap{margin-top:1.2em}
section{border-top:2px solid var(--line)}
h2{font-family:var(--display);font-weight:900;font-size:1.5rem}
h2::after{content:"";display:block;width:2.5em;height:6px;background:var(--mark);margin-top:.3em}
dl.summary dt{font-family:var(--display);font-weight:900;font-size:.95rem;background:var(--mark);display:inline-block;padding:0 .5em}
.block h3{font-family:var(--display);font-weight:900}
.price .amt{font-family:var(--display);font-weight:900;background:linear-gradient(transparent 60%,var(--mark) 60%)}
.figure{border:2px dashed var(--line)}
""",
    },
}

BASE_CSS = """
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;color-scheme:light}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:var(--fs);line-height:1.9;
font-feature-settings:"palt" 0;overflow-wrap:anywhere}
.wrap{max-width:640px;margin:0 auto;padding-inline:20px}
header.top{position:fixed;top:0;left:0;right:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);
padding-top:env(safe-area-inset-top,0px)}
header.top .bar{display:flex;align-items:center;justify-content:space-between;height:56px}
header.top .brand{font-family:var(--display);font-weight:700;font-size:1.15rem;color:var(--accent);text-decoration:none;letter-spacing:.03em}
.menu{position:relative}
.menu summary{list-style:none;cursor:pointer;border:1px solid var(--accent);color:var(--accent);padding:.25em .8em;font-size:.85rem;border-radius:3px;user-select:none}
.menu summary::-webkit-details-marker{display:none}
.menu summary .ico{display:none}
.cta{display:none}
header.top .right{display:flex;align-items:center;gap:12px}
.menu nav{position:absolute;right:0;top:calc(100% + 10px);background:var(--bg);border:1px solid var(--line);min-width:220px;
box-shadow:0 8px 24px rgba(0,0,0,.12);padding:.4em 0;border-radius:4px}
.menu nav a{display:block;padding:.55em 1.2em;color:var(--fg);text-decoration:none;font-size:.95rem}
.menu nav a:hover,.menu nav a:focus-visible{background:var(--soft);outline:none}
main{padding-top:calc(56px + env(safe-area-inset-top,0px))}
.hero{padding-block:52px 40px}
.hero .kana{display:block}
.hero .catch{text-wrap:pretty;font-weight:inherit;margin-bottom:0}
section{padding-block:40px;border-top:1px solid var(--line);scroll-margin-top:calc(64px + env(safe-area-inset-top,0px))}
h2{font-size:1.4rem;line-height:1.5;margin:0 0 1em;text-wrap:balance}
h3{font-size:1.05rem;line-height:1.6;margin:0 0 .4em}
p{margin:0 0 1.1em}
p:last-child{margin-bottom:0}
dl.summary{margin:0}
dl.summary dt{margin:0 0 .3em}
dl.summary dd{margin:0 0 1.5em}
dl.summary dd:last-child{margin-bottom:0}
.essay p{text-indent:1em}
.essay .closing{margin-top:2.2em;padding-top:1.6em;border-top:1px dashed var(--line)}
.block{margin-bottom:1.6em}
.block:last-of-type{margin-bottom:0}
.more{display:inline-block;margin-top:.6em;color:var(--muted);font-size:.9rem;border-bottom:1px dotted var(--muted)}
.note{color:var(--muted);font-size:.9rem}
.figure{margin:1.4em 0 0;padding:2.2em 1em;text-align:center;color:var(--muted);font-size:.9rem;border:1px dashed var(--line);border-radius:4px}
.price{margin:0 0 1.2em}
.price .row{display:flex;flex-wrap:wrap;align-items:baseline;gap:.2em .8em;padding:.8em 0;border-bottom:1px solid var(--line)}
.price .row:first-child{border-top:1px solid var(--line)}
.price .item{flex:1 1 100%;}
.price .amt{font-size:1.35rem;font-variant-numeric:tabular-nums}
.price .cond{color:var(--muted);font-size:.85rem}
footer{border-top:1px solid var(--line);padding-block:32px 48px;color:var(--muted);font-size:.85rem}
footer .co{color:var(--fg);font-weight:700;margin-bottom:.4em}
footer nav{margin-top:1.2em;display:flex;flex-wrap:wrap;gap:.3em 1.2em}
footer nav a{color:var(--muted);text-decoration:none}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
"""

MENU_JS = """
document.querySelectorAll('.menu nav a').forEach(function(a){
  a.addEventListener('click',function(){var d=a.closest('details');if(d){d.open=false;}});
});
"""


# ---------------------------------------------------------------- html
def menu_items():
    items = [("#service", "サービス"), ("#essay", "コンドルセの考え")]
    for s in C.SECTIONS:
        if s.get("menu"):
            items.append(("#" + s["id"], s["menu"]))
    return items


def render_section(s):
    out = [f'<section id="{s["id"]}"><div class="wrap">']
    out.append(f"<h2>{esc(s['title'])}</h2>")
    if s.get("note"):
        out.append(f'<p class="note">{esc(s["note"])}</p>')
    for h, body in s.get("blocks", []):
        out.append(f'<div class="block"><h3>{esc(h)}</h3><p>{esc(body)}</p></div>')
    if s.get("price"):
        out.append('<div class="price">')
        for item, amt, cond in s["price"]:
            out.append(f'<div class="row"><span class="item">{esc(item)}</span>'
                       f'<span class="amt">{esc(amt)}</span><span class="cond">{esc(cond)}</span></div>')
        out.append("</div>")
    for p in s.get("paras", []):
        out.append(f"<p>{esc(p)}</p>")
    if s.get("figure"):
        out.append(f'<div class="figure">{esc(s["figure"])}</div>')
    if s.get("more"):
        out.append(f'<span class="more">→ {esc(s["more"])}（別ページ・準備中）</span>')
    out.append("</div></section>")
    return "\n".join(out)


def render_body(theme_key):
    t = THEMES[theme_key]
    parts = []
    parts.append('<header class="top"><div class="wrap bar">'
                 f'<a class="brand" href="#top">{C.SITE_NAME}</a>'
                 '<div class="right"><a class="cta" href="#toiawase">お問い合わせ</a>'
                 '<details class="menu"><summary><span class="ico"><i></i></span><span class="lbl">メニュー</span></summary><nav>')
    for href, label in menu_items():
        parts.append(f'<a href="{href}">{esc(label)}</a>')
    parts.append("</nav></details></div></div></header>")

    parts.append('<main id="top">')
    # ① ②
    parts.append('<div class="hero"><div class="wrap">'
                 f'<div class="name">{C.SITE_NAME}</div><span class="kana">{C.SITE_KANA}</span>'
                 f'<div class="catchwrap"><h1 class="catch">{esc(C.CATCH)}</h1></div></div></div>')
    # ③
    parts.append('<section id="service"><div class="wrap"><dl class="summary">')
    for k, v in C.SUMMARY:
        parts.append(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>")
    parts.append("</dl></div></section>")
    # ④
    parts.append('<section id="essay" class="essay"><div class="wrap">')
    parts.append(f"<h2>{esc(C.ESSAY_TITLE)}</h2>")
    for p in C.ESSAY:
        parts.append(f"<p>{esc(p)}</p>")
    parts.append('<div class="closing">')
    for p in C.ESSAY_CLOSING:
        parts.append(f"<p>{esc(p)}</p>")
    parts.append("</div></div></section>")
    # ⑤〜
    for s in C.SECTIONS:
        parts.append(render_section(s))
    parts.append("</main>")

    parts.append('<footer><div class="wrap">'
                 f'<div class="co">{esc(C.COMPANY)}</div>'
                 '<div>所在地（準備中）</div>'
                 '<nav>')
    for href, label in menu_items():
        parts.append(f'<a href="{href}">{esc(label)}</a>')
    parts.append("</nav>"
                 f'<p class="note" style="margin-top:1.4em">{esc(C.FOOTER_NOTE)}<br>この案：{esc(t["name"])}　'
                 '<a href="../" style="color:inherit">ほかの案を見る</a></p>'
                 "</div></footer>")
    parts.append(f"<script>{MENU_JS}</script>")
    return "\n".join(parts)


def head_parts(theme_key):
    t = THEMES[theme_key]
    title = f"<title>{C.SITE_NAME}（{C.SITE_KANA}）— {esc(C.CATCH)}</title>"
    link = (f'<link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={t["fonts"]}&display=swap">')
    style = f"<style>{BASE_CSS}{t['css']}</style>"
    return title, link, style


def full_page(theme_key):
    title, link, style = head_parts(theme_key)
    return ("<!doctype html>\n<html lang=\"ja\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"{title}\n{link}\n{style}\n</head>\n<body>\n{render_body(theme_key)}\n</body>\n</html>\n")


def fragment(theme_key):
    title, link, style = head_parts(theme_key)
    return f"{title}\n{link}\n{style}\n{render_body(theme_key)}\n"



# ---------------------------------------------------------------- 案D（採用サイト型・文字だけ）
# 書体: 見出しは Zen Old Mincho、本文は端末の書体（ヒラギノ／游ゴシック／メイリオ）。ロゴ（Condorcet）だけ英字の Manrope
D_FONTS = "Zen+Old+Mincho:wght@400;500;700&family=Manrope:wght@600;700"
D_CSS = """
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;color-scheme:light}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
:root{--bg:#e6edf7;--paper:#ffffff;--ink:#141c2b;--ink2:#3f4a5e;--muted:#6f7b90;--accent:#1b57d6;--line:#c5d1e4;--deep:#0f1f3d;--deep-em:#8fb3ff;
--font:'Hiragino Sans','Hiragino Kaku Gothic ProN','Yu Gothic','游ゴシック',YuGothic,Meiryo,'Noto Sans JP',sans-serif;--head:'Zen Old Mincho','Hiragino Mincho ProN','Yu Mincho',serif;--latin:'Manrope','Helvetica Neue',Arial,sans-serif}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-size:16px;font-weight:500;line-height:2;overflow-wrap:anywhere}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;opacity:.055;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
main,footer{position:relative;z-index:1}
.w{max-width:640px;margin:0 auto;padding-inline:24px}
.hd{position:fixed;top:0;left:0;right:0;z-index:30;padding-top:env(safe-area-inset-top,0px);background:transparent;transition:background .3s,box-shadow .3s}
.hd.on{background:rgba(230,237,247,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);box-shadow:0 1px 0 var(--line)}
.hd:not(.on) .logo,.hd:not(.on) .cta{color:#fff;border-color:rgba(255,255,255,.7)}
.hd:not(.on) .mn summary::before,.hd:not(.on) .mn summary::after{background:#fff}
.hd .bar{display:flex;align-items:center;justify-content:space-between;height:60px}
.logo{font-family:var(--latin);font-weight:700;font-size:1.25rem;letter-spacing:-.02em;color:var(--ink);text-decoration:none;display:inline-flex;flex-direction:column;line-height:1.1}
.logo .kana{font-family:var(--font);font-weight:500;font-size:.6rem;letter-spacing:.3em;opacity:.8;margin-top:.25em;transition:opacity .3s,max-height .3s;max-height:1.2em;overflow:hidden}
.hd.on .logo .kana{opacity:0;max-height:0;margin-top:0}
.hd .rt{display:flex;align-items:center;gap:16px}
.hd .cta{font-size:.8rem;font-weight:500;color:var(--ink);text-decoration:none;border:1px solid var(--ink);border-radius:999px;padding:.35em 1em;white-space:nowrap}
.mn{position:relative}
.mn summary{list-style:none;cursor:pointer;width:34px;height:24px;position:relative;display:block}
.mn summary::-webkit-details-marker{display:none}
.mn summary::before,.mn summary::after{content:"";position:absolute;left:0;right:0;height:1.5px;background:var(--ink);transition:transform .3s}
.mn summary::before{top:6px}.mn summary::after{bottom:6px}
.mn[open] summary::before{transform:translateY(5px) rotate(20deg)}.mn[open] summary::after{transform:translateY(-5px) rotate(-20deg)}
.mn nav{position:fixed;left:0;right:0;top:calc(60px + env(safe-area-inset-top,0px));background:var(--bg);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 24px 20px}
.mn nav a{display:block;padding:.5em 0;color:var(--ink);text-decoration:none;font-size:1.05rem;font-weight:500;letter-spacing:.04em}
.mn nav a.cur{color:var(--accent)}
.hero{background:var(--deep);color:#fff;padding:calc(60px + env(safe-area-inset-top,0px) + 88px) 0 64px}
.hero .catch{font-family:var(--head);font-size:2.2rem;font-weight:700;line-height:1.5;letter-spacing:.02em;margin:0;text-wrap:pretty;font-feature-settings:"palt"}
.hero .catch em{font-style:normal;color:var(--deep-em);white-space:nowrap}
.hero .sub{margin:2em 0 0;font-family:var(--head);font-weight:500;font-size:1.06rem;color:rgba(255,255,255,.88);line-height:2.1;max-width:34em;letter-spacing:.04em;font-feature-settings:"palt"}
.cue{margin-top:64px;font-size:.75rem;letter-spacing:.2em;color:rgba(255,255,255,.6);display:flex;align-items:center;gap:12px}
.cue::after{content:"";width:1px;height:40px;background:rgba(255,255,255,.6);animation:cue 1.8s ease-in-out infinite;transform-origin:top}
@keyframes cue{0%{transform:scaleY(0)}50%{transform:scaleY(1)}100%{transform:scaleY(0);transform-origin:bottom}}
@media (prefers-reduced-motion:reduce){.cue::after{animation:none}}
/* ヒーローの写真: スマホでは一番上に写真（右寄りを切り出す）、その下の濃紺に文字。ひと画面に両方が入る大きさ */
.hero{position:relative;overflow:hidden;display:flex;flex-direction:column;padding:0;min-height:100vh;min-height:100svh}
.hero .w{position:relative;z-index:1;order:1;padding-top:20px;padding-bottom:32px}
.hero .catch{font-size:1.55rem;line-height:1.5}
.hero .sub{margin-top:1.1em;font-size:.88rem;line-height:1.85}
.hero .cue{margin-top:24px}
.hero .cue::after{height:28px}
.hero-img{order:0;flex:1 0 auto;min-height:72vw;
background:linear-gradient(to bottom,rgba(15,31,61,.55) 0%,rgba(15,31,61,0) 22%),linear-gradient(to top,var(--deep) 0%,rgba(15,31,61,0) 28%),url(hero.webp) 86% 62%/cover no-repeat,var(--deep)}
section{padding:96px 0;scroll-margin-top:calc(60px + env(safe-area-inset-top,0px))}
section + section .w{border-top:1px solid var(--line);padding-top:96px}
section + section{padding-top:0}
section.paper{background:var(--bg)} /* いったん白の節をなくして全部同じ青に（2026-09-19） */
.lbl{font-size:.75rem;letter-spacing:.25em;color:var(--accent);font-weight:700;margin:0 0 1.6em}
h2{font-family:var(--head);font-size:1.75rem;font-weight:700;line-height:1.5;letter-spacing:.03em;margin:0 0 1.4em;text-wrap:pretty;font-feature-settings:"palt"}
h3{font-family:var(--head);font-size:1.15rem;font-weight:700;margin:0 0 .5em;letter-spacing:.03em}
p{margin:0 0 1.4em}
p:last-child{margin-bottom:0}
.facts{list-style:none;margin:0;padding:0}
.facts li{display:grid;grid-template-columns:4.5em 1fr;gap:0 12px;padding:22px 0;border-top:1px solid var(--line)}
.facts li:last-child{border-bottom:1px solid var(--line)}
.facts .k{font-size:.85rem;font-weight:700;color:var(--accent);letter-spacing:.1em;padding-top:.35em}
.facts p{margin:0;font-size:.98rem;line-height:1.95}
.essay .body p{font-size:1.02rem;line-height:2.15;margin-bottom:1.8em}
.essay .closing{margin-top:3em;padding-left:18px;border-left:2px solid var(--accent)}
.essay .closing p{color:var(--ink);font-weight:600}
.blk{padding:26px 0;border-top:1px solid var(--line)}
.blks .blk:last-child{border-bottom:1px solid var(--line)}
.blk p{font-size:.98rem}
.more{display:inline-block;margin-top:2em;color:var(--accent);font-weight:500;text-decoration:none;font-size:.95rem}
.note{color:var(--muted);font-size:.9rem}
.fig{margin:2em 0 0;padding:44px 16px;text-align:center;color:var(--muted);font-size:.85rem;border:1px dashed var(--line)}
.price{margin:0 0 2em}
.price .row{padding:22px 0;border-top:1px solid var(--line)}
.price .row:last-child{border-bottom:1px solid var(--line)}
.price .item{display:block;font-size:.95rem;color:var(--ink2)}
.price .amt{display:block;font-family:var(--head);font-size:2rem;font-weight:700;letter-spacing:.02em;line-height:1.3;margin:.15em 0;font-variant-numeric:tabular-nums}
.price .cond{display:block;font-size:.85rem;color:var(--muted)}
.big{font-family:var(--head);font-size:1.3rem;font-weight:500;line-height:1.9}
footer{padding:64px 0 72px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line)}
footer .logo{display:inline-block;margin-bottom:.6em}
footer .co{color:var(--ink);font-weight:700;font-size:1rem;margin-bottom:.3em}
footer nav{margin-top:2em;display:flex;flex-wrap:wrap;gap:.2em 1.4em}
footer nav a{color:var(--muted);text-decoration:none}
a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.js .rv{opacity:0;transform:translateY(16px);transition:opacity .8s cubic-bezier(.2,.6,.2,1),transform .8s cubic-bezier(.2,.6,.2,1)}
.js .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none;transition:none}}

/* ---- 画面が広いとき（PC・タブレット横）: 節ごとに横幅の使い方を決める ---- */
@media (min-width:860px){
  .w{max-width:1120px;padding-inline:48px}
  .hd .bar{height:72px}
  .logo{font-size:1.4rem}
  .mn nav{left:auto;right:48px;top:calc(72px + env(safe-area-inset-top,0px));width:280px;border:1px solid var(--line);padding:10px 24px 16px}
  .hero{padding:calc(72px + env(safe-area-inset-top,0px) + 120px) 0 96px}
  .hero .catch{font-size:clamp(2.6rem,4.4vw,4rem);line-height:1.3;letter-spacing:0;max-width:20em}
  .hero .sub{font-size:1.05rem;max-width:40em}
  /* ヒーローの写真: PCでは右に高さいっぱいで置き、左の文字側を濃紺でなじませる */
  .hero-img{flex:none;min-height:0}
  .hero{min-height:clamp(640px,92vh,960px);flex-direction:row;align-items:center;padding:calc(72px + env(safe-area-inset-top,0px) + 120px) 0 96px}
  .hero .w{width:100%;padding-top:0;padding-bottom:0}
  .hero .catch{font-size:clamp(2.4rem,3.4vw,3.2rem);line-height:1.3;max-width:11.5em}
  .hero .sub{margin-top:2em;font-size:1.05rem;line-height:2;max-width:24em}
  .hero .cue{margin-top:64px}
  .hero .cue::after{height:40px}
  .hero-img{position:absolute;inset:0;height:auto;max-height:none;margin:0;
  background:linear-gradient(to right,var(--deep) 0%,var(--deep) 18%,rgba(15,31,61,.6) 32%,rgba(15,31,61,0) 50%),url(hero.webp) right center/auto 100% no-repeat,var(--deep)}
  section{padding:112px 0}
  section + section{padding-top:0}
  section + section .w{padding-top:112px}
  h2{font-size:2rem;line-height:1.4}
  .in.narrow{max-width:720px}
  /* 表: 1列で縦に並べる（2×2はやめた 2026-09-19） */
  #service .in{max-width:820px}
  .facts li{grid-template-columns:6em 1fr;gap:0 28px;padding:28px 0}
  .facts p{font-size:1.02rem}
  /* 横3列 */
  .cols3 .blks,.cols3 .paras{display:grid;grid-template-columns:repeat(3,1fr);gap:0 48px;align-items:start}
  .cols3 .blks .blk{border-top:1px solid var(--line);border-bottom:0;padding:28px 0 0}
  .cols3 .paras p{border-top:1px solid var(--line);padding-top:28px;margin:0}
  /* 左に文章、右に見本 */
  .split .body{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:start}
  .split .fig{margin:0;min-height:260px;display:flex;align-items:center;justify-content:center}
  /* 料金: 2列 */
  .price{display:grid;grid-template-columns:1fr 1fr;gap:0 48px}
  .price .row{border-bottom:1px solid var(--line)}
  .price .amt{font-size:2.4rem}
  .pricenote{max-width:720px}
  /* お問い合わせ: 2列 */
  .cols2 .paras{display:grid;grid-template-columns:1fr 1fr;gap:0 56px;align-items:start}
  .cols2 .paras p{margin:0}
  footer .w{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
  footer nav{margin-top:0;flex-direction:column;gap:.3em}
}
"""

D_JS = """
(function(){
  var root=document.documentElement;root.classList.add('js');
  var hd=document.querySelector('.hd');
  function onS(){hd.classList.toggle('on',window.scrollY>8)}
  onS();window.addEventListener('scroll',onS,{passive:true});
  var rv=document.querySelectorAll('.rv');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(el){io.observe(el)});
  }else{rv.forEach(function(el){el.classList.add('in')})}
  var links=document.querySelectorAll('.mn nav a');
  links.forEach(function(a){a.addEventListener('click',function(){var d=a.closest('details');if(d)d.open=false})});
  var secs=[].map.call(links,function(a){return document.querySelector(a.getAttribute('href'))}).filter(Boolean);
  if('IntersectionObserver' in window){
    var spy=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('cur',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-40% 0px -55% 0px'});
    secs.forEach(function(s){spy.observe(s)});
  }
})();
"""


def d_catch():
    c = esc(C.CATCH)
    if "、" in c:
        a, b = c.rsplit("、", 1)
        # 「AIを、」の途中で改行させない（…任せられる／AIを、一日で。）
        if a.endswith("AIを"):
            return f'{a[:-3]}<span style="white-space:nowrap">AIを、</span><em>{b}</em>'
        # 「、」の位置で改行する。改行するので読点は表示しない（2026-09-19 博彰）
        return f"{a}<br><em>{b}</em>"
    return c


LAYOUT = {"hachinichi": "cols3", "tsukureru": "split", "junbi": "narrow", "ai": "cols3",
          "jirei": "narrow", "ryokin": "price", "okotowari": "narrow", "shokai": "narrow", "toiawase": "cols2"}


def render_body_d():
    P = []
    P.append('<header class="hd"><div class="w bar">'
             f'<a class="logo" href="#top">{C.SITE_NAME}<span class="kana">{C.SITE_KANA}</span></a>'
             '<div class="rt"><a class="cta" href="#toiawase">お問い合わせ</a>'
             '<details class="mn"><summary aria-label="メニュー"></summary><nav>')
    for href, label in menu_items():
        P.append(f'<a href="{href}">{esc(label)}</a>')
    P.append('</nav></details></div></div></header>')

    P.append('<main id="top">')
    P.append('<div class="hero"><div class="w">'
             f'<h1 class="catch">{d_catch()}</h1>'
             f'<p class="sub">{esc(C.HERO_SUB)}</p>'
             '<div class="cue">スクロール</div>'
             '</div><div class="hero-img" role="img" aria-label="夜の机。職人の手が置かれた手書きのノートから光の線が伸び、スマホとノートPCへつながっている"></div></div>')
    # ③ 表: 内容は全幅、残りは2×2
    P.append('<section id="service" class="paper"><div class="w"><div class="in rv">'
             '<p class="lbl">コンドルセとは</p><ul class="facts">')
    for i, (k, v) in enumerate(C.SUMMARY):
        full = ' class="full"' if i == 0 else ''
        P.append(f'<li{full}><span class="k">{esc(k)}</span><p>{esc(v)}</p></li>')
    P.append('</ul></div></div></section>')
    # ④ 長文: 幅を絞る
    P.append('<section id="essay" class="essay"><div class="w"><div class="in narrow rv">'
             f'<p class="lbl">コンドルセの考え</p><h2>{esc(C.ESSAY_TITLE)}</h2><div class="body">')
    for p in C.ESSAY:
        P.append(f'<p>{esc(p)}</p>')
    P.append('<div class="closing">')
    for p in C.ESSAY_CLOSING:
        P.append(f'<p>{esc(p)}</p>')
    P.append('</div></div></div></div></section>')
    # ⑤〜: 節ごとの型
    for i, s_ in enumerate(C.SECTIONS):
        cls = "paper" if i % 2 == 0 else ""
        lay = LAYOUT.get(s_["id"], "narrow")
        P.append(f'<section id="{s_["id"]}" class="{cls}"><div class="w"><div class="in {lay} rv">')
        P.append(f'<h2>{esc(s_["title"])}</h2>')
        if s_.get("note"):
            P.append(f'<p class="note">{esc(s_["note"])}</p>')
        P.append('<div class="body">')
        if lay == "split":
            P.append('<div>')
        blocks = s_.get("blocks", [])
        if blocks:
            P.append('<div class="blks">')
            for h, body in blocks:
                P.append(f'<div class="blk"><h3>{esc(h)}</h3><p>{esc(body)}</p></div>')
            P.append('</div>')
        if s_.get("price"):
            P.append('<div class="price">')
            for item, amt, cond in s_["price"]:
                P.append(f'<div class="row"><span class="item">{esc(item)}</span>'
                         f'<span class="amt">{esc(amt)}</span><span class="cond">{esc(cond)}</span></div>')
            P.append('</div>')
        paras = s_.get("paras", [])
        if paras:
            pcls = "paras pricenote" if lay == "price" else "paras"
            P.append(f'<div class="{pcls}">')
            for j, p in enumerate(paras):
                big = ' class="big"' if (s_["id"] in ("junbi", "okotowari") and j == 0) else ''
                P.append(f'<p{big}>{esc(p)}</p>')
            P.append('</div>')
        if lay == "split":
            P.append('</div>')
        if s_.get("figure"):
            P.append(f'<div class="fig">{esc(s_["figure"])}</div>')
        P.append('</div>')
        if s_.get("more"):
            P.append(f'<span class="more">{esc(s_["more"])} →（別ページ・準備中）</span>')
        P.append('</div></div></section>')
    P.append('</main>')

    P.append('<footer><div class="w"><div>'
             f'<a class="logo" href="#top">{C.SITE_NAME}</a>'
             f'<p class="note" style="margin-top:2em">{esc(C.FOOTER_NOTE)}<br>この案：D 文字と余白　'
             '<a href="../" style="color:inherit">ほかの案を見る</a></p></div><nav>')
    for href, label in menu_items():
        P.append(f'<a href="{href}">{esc(label)}</a>')
    P.append('</nav></div></footer>')
    P.append(f'<script>{D_JS}</script>')
    return "\n".join(P)


def d_head():
    title = f"<title>{C.SITE_NAME}（{C.SITE_KANA}）— {esc(C.CATCH)}</title>"
    link = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={D_FONTS}&display=swap">')
    return title, link, f"<style>{D_CSS}</style>"


def full_page_d():
    title, link, style = d_head()
    return ("<!doctype html>\n<html lang=\"ja\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"{title}\n{link}\n{style}\n</head>\n<body>\n{render_body_d()}\n</body>\n</html>\n")


def fragment_d():
    title, link, style = d_head()
    return f"{title}\n{link}\n{style}\n{render_body_d()}\n"

INDEX_CSS = """
*{box-sizing:border-box}html{color-scheme:light}
body{margin:0;background:#fafafa;color:#222;font-family:'Noto Sans JP','Hiragino Sans',sans-serif;font-size:16px;line-height:1.8}
.wrap{max-width:640px;margin:0 auto;padding:40px 20px 60px}
h1{font-size:1.4rem;margin:0 0 .3em}
.sub{color:#666;margin:0 0 2em}
.card{display:block;border:1px solid #ddd;border-radius:8px;padding:1.1em 1.2em;margin-bottom:1em;text-decoration:none;color:inherit;background:#fff}
.card b{display:block;font-size:1.1rem;margin-bottom:.2em}
.card span{color:#555;font-size:.95rem}
h2{font-size:1.05rem;margin:2.2em 0 .6em}
ul{padding-left:1.3em}li{margin-bottom:.4em}
.note{color:#666;font-size:.9rem}
"""


def index_page(fragment_mode=False):
    body = ['<div class="wrap">',
            f"<h1>{C.SITE_NAME} トップページ 素案</h1>",
            '<p class="sub">同じ文章で、雰囲気の違う3案。スマホで開いて比べてください。</p>']
    for k, t in THEMES.items():
        body.append(f'<a class="card" href="{k}/"><b>{esc(t["name"])}</b><span>{esc(t["mood"])}</span></a>')
    body.append('<a class="card" href="d/"><b>D 文字と余白</b><span>採用サイトの型。薄い灰の地に文字だけ、青は強調したい語にだけ。PCでは節ごとに横幅の使い方を変える（長文は絞る・8日間は3列・料金は2列）。ロゴだけ英字</span></a>')
    body.append("<h2>この素案で確定しているもの</h2><ul>"
                "<li>事業名・キャッチコピー・事業情報の表（内容／対象／日数／料金／誰が）</li>"
                "<li>長文（博彰の清書。一字も変えていません）</li></ul>")
    body.append("<h2>下書き（構成を確かめるための仮の文章）</h2><ul>"
                "<li>「8日間で何が起きるか」以降の各節</li>"
                "<li>見本の画面・連絡先・所在地は準備中</li></ul>")
    body.append("<h2>ここは確認が要る（長文）</h2><ul>"
                "<li>「情報を外に出さずに」— AIはクラウドなので、事実としては「他人に渡さずに済む」が正確</li>"
                "<li>「何度でもお手伝い」— 対応量の上限を約束することになる（内規は合計3時間目安）。手段（チャットと電話）も抜けている</li>"
                "<li>「なくせます」— 結果の保証に近い。「減らしていけます」が線の内側</li></ul>")
    body.append("</div>")
    inner = "\n".join(body)
    title = f"<title>{C.SITE_NAME} トップページ 素案</title>"
    style = f"<style>{INDEX_CSS}</style>"
    if fragment_mode:
        return f"{title}\n{style}\n{inner}\n"
    return ("<!doctype html>\n<html lang=\"ja\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"{title}\n{style}\n</head>\n<body>\n{inner}\n</body>\n</html>\n")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--fragments":
        out = sys.argv[2]
        write(os.path.join(out, "index.html"), index_page(fragment_mode=True))
        for k in THEMES:
            write(os.path.join(out, k, "index.html"), fragment(k))
        write(os.path.join(out, "d", "index.html"), fragment_d())
        print("fragments ->", out)
        return
    write(os.path.join(ROOT, "index.html"), index_page())
    for k in THEMES:
        write(os.path.join(ROOT, k, "index.html"), full_page(k))
    write(os.path.join(ROOT, "d", "index.html"), full_page_d())
    print("written:", ROOT)


if __name__ == "__main__":
    main()
