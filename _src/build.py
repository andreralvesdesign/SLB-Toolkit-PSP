#!/usr/bin/env python3
"""Assemble course chapters: shared shell (header, footer, menu, dialogs) + chapter fragment.

Each fragment in _src/lessons/<file>.html starts with a JSON front-matter comment:
<!--{"chapter":"2.1","title":"…","crumb":"Parte 2 · <b>2.1 Contextualização</b>"}-->
followed by the <section class="slide"> elements, then optionally a <script> block
with chapter-specific code. The script must end with PSP.start(); if absent, it is added.

Page names: the fragments keep their file names; the built pages get the short names of _src/pages.json
(Portuguese in the course root, English in en/), and every link between pages is re-pointed to them.
index.html is cut in two: the language screen (idioma / language) and the home page (inicio / start);
index.html itself only forwards to the language screen. Online, player.js leaves ".html" out of the address.
The browser tab reads "Sonae Toolkit PSP" (English: "Sonae PFA Toolkit"), with the module in front inside a module: "Módulo 3 - Sonae Toolkit PSP".

English: _src/i18n/apply.py turns the Portuguese fragments into _src/lessons-en/ + _src/shell.en.html (see _src/i18n/).
This script builds both: Portuguese into the course root, English into en/ (assets/ is shared, so its links get a "../" in front).
Run: python3 _src/build.py   (from the course root; add --no-en to skip the English pages)
"""
import html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = {k: v for k, v in json.loads((ROOT / '_src' / 'pages.json').read_text(encoding='utf-8')).items() if not k.startswith('_')}
TITLE = ('Sonae Toolkit PSP', 'Sonae PFA Toolkit')
LANG_SEC = re.compile(r'\s*(?:<!--[^>]*-->\s*)?<section class="slide s-lang\b.*?</section>', re.S)
REDIRECT = '''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><title>{title}</title>
<meta http-equiv="refresh" content="0; url={page}.html">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/img/favicon-32.png">
<script>location.replace(/^https?:$/.test(location.protocol) ? '{page}' : '{page}.html');</script>
</head><body><a href="{page}.html">{title}</a></body></html>
'''


def pages_js():
    """assets/js/pages.js = the page names, for player.js (menu, Anterior/Seguinte, language switch)"""
    (ROOT / 'assets' / 'js' / 'pages.js').write_text('window.PAGES=' + json.dumps(PAGES, ensure_ascii=False) + ';\n', encoding='utf-8', newline='\n')


def relink(out, li):
    """links between pages: fragment file name -> short page name of this language"""
    for src, names in PAGES.items():
        if src.endswith('.html'):
            out = re.sub(r'(?<=["\'/])' + re.escape(src) + r'(?=["\'#?])', names[li] + '.html', out)
    return out


def build(shell_file, lessons, dest, shared_prefix=''):
    li = 1 if shared_prefix else 0
    shell = shell_file.read_text(encoding='utf-8')
    dest.mkdir(exist_ok=True)
    built = set()
    slides = []   # for slides.json (review tool): hash id = m<chapter>-<data-id>, global order
    for frag in sorted(lessons.glob('*.html'), key=lambda f: (f.name != 'index.html', f.name)):
        src = frag.read_text(encoding='utf-8')
        m = re.match(r'\s*<!--(\{.*?\})-->', src, re.S)
        meta = json.loads(m.group(1))
        body = src[m.end():]
        script = ''
        sm = re.search(r'<script>(.*?)</script>\s*$', body, re.S)
        if sm:
            script = sm.group(1).strip()
            body = body[:sm.start()]
        if 'PSP.start()' not in script:
            script += '\nPSP.start();'
        parts = [(PAGES[frag.name][li], meta['chapter'], body)]
        if frag.name == 'index.html':
            lang = LANG_SEC.search(body)
            parts = [(PAGES['idioma'][li], 'lang', lang.group(0)), (PAGES['index.html'][li], meta['chapter'], body[:lang.start()] + body[lang.end():])]
        for name, chapter, part in parts:
            out = (shell.replace('{{TITLE}}', meta['title'])
                        .replace('{{CHAPTER}}', chapter)
                        .replace('{{CRUMB}}', meta['crumb'])
                        .replace('{{SLIDES}}', part.strip())
                        .replace('{{SCRIPT}}', script))
            mod = chapter.split('.')[0] if re.match(r'[1-9]', chapter) else ''
            title = (('Módulo ', 'Module ')[li] + mod + ' - ' if mod else '') + TITLE[li]
            out = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, out, count=1, flags=re.S)
            # header path: the dots get room of their own
            out = re.sub(r'<p class="crumb">.*?</p>', lambda m: m.group(0).replace(' · ', ' <span class="csep">·</span> '), out, count=1)
            out = relink(out, li)
            if shared_prefix:
                # assets/ and downloads/ stay in the course root: every reference that opens a quote, a backtick or a url( gets the prefix
                out = re.sub(r'''(?<=["'`(])((?:assets|downloads)/)''', shared_prefix + r'\1', out)
            (dest / (name + '.html')).write_text(out, encoding='utf-8')
            built.add(name + '.html')
            for sec in re.finditer(r'<section class="slide[^"]*"([^>]*)>', part):
                a = sec.group(1)
                sid = re.search(r'data-id="([^"]+)"', a).group(1)
                ttl = re.search(r'data-title="([^"]*)"', a)
                slides.append({'id': 'm%s-%s' % (chapter.replace('.', '-'), sid), 'module': meta['title'], 'title': html.unescape(ttl.group(1)) if ttl else sid, 'order': len(slides) + 1})
            print('built', dest.relative_to(ROOT) if dest != ROOT else '.', name + '.html', len(out))
    # the address without a page name opens the language screen
    (dest / 'index.html').write_text(REDIRECT.format(lang=('pt-PT', 'en-GB')[li], title=TITLE[li], page=PAGES['idioma'][li], pre=shared_prefix), encoding='utf-8')
    built.add('index.html')
    # pages left over from older names
    for old in dest.glob('*.html'):
        if old.name not in built:
            old.unlink(); print('removed', old.relative_to(ROOT))
    (dest / 'slides.json').write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding='utf-8')


def captions_js():
    """assets/js/captions.js = every .vtt inside one script, so captions also work when the course is opened from disk
    (browsers refuse <track src> on file://); player.js builds the text tracks from it."""
    caps = {lang: {f.stem.replace('video-', ''): f.read_text(encoding='utf-8').replace('\r', '')
                   for f in sorted((ROOT / 'assets' / 'video' / sub).glob('video-*.vtt'))} for lang, sub in (('pt', ''), ('en', 'en'))}
    (ROOT / 'assets' / 'js' / 'captions.js').write_text('window.CAPS=' + json.dumps(caps, ensure_ascii=False) + ';\n', encoding='utf-8', newline='\n')


captions_js()
pages_js()
build(ROOT / '_src' / 'shell.html', ROOT / '_src' / 'lessons', ROOT)
if '--no-en' not in sys.argv:
    r = subprocess.run([sys.executable, str(ROOT / '_src' / 'i18n' / 'apply.py')], cwd=ROOT)
    if r.returncode:
        sys.exit('English fragments not built (see the messages above); the Portuguese pages are done.')
    build(ROOT / '_src' / 'shell.en.html', ROOT / '_src' / 'lessons-en', ROOT / 'en', '../')
