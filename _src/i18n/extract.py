#!/usr/bin/env python3
"""Find every Portuguese string of the course that has to be translated.

Units (all by character offsets in the fragment, so apply.py can swap them without touching the markup):
  html   inner HTML of a leaf block (p, li, h2, button…) that holds text
  text   a loose text node next to block children
  attr   alt / aria-label / title / data-title / data-k / data-cta / data-front / data-back / aria-roledescription …
  js     a string literal inside <script> that reads like prose
  meta   "title" and "crumb" of the JSON front-matter comment

Run from the course root:  python _src/i18n/extract.py
Writes _src/i18n/units.json  ({file: [unit…]}) and _src/i18n/pt.json ({pt text: [files]}).
"""
import json, pathlib, re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = pathlib.Path(__file__).resolve().parent

INLINE = {'b', 'i', 'em', 'strong', 'span', 'a', 'br', 'small', 'sup', 'sub', 'u', 'mark', 'abbr', 'code', 'img', 'label', 'input', 'wbr'}
VOID = {'img', 'br', 'input', 'hr', 'meta', 'link', 'wbr', 'source', 'track'}
ATTRS = {'alt', 'aria-label', 'title', 'data-title', 'data-k', 'data-cta', 'data-front', 'data-back', 'aria-roledescription', 'placeholder', 'data-tip'}
LETTERS = re.compile(r'[A-Za-zÀ-ÿ]{2}')


class P(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.t = text
        self.lines = [0] + [i + 1 for i, c in enumerate(text) if c == '\n']
        self.stack = []
        self.units = []
        self.skip = 0
        self.script = None

    def off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        s = self.off(); raw = self.get_starttag_text(); e = s + len(raw)
        if tag in ('script', 'style'):
            self.script = (tag, e); return
        for a in ATTRS:
            m = re.search(r'(?<![\w-])' + re.escape(a) + r'\s*=\s*"([^"]*)"', raw)
            if m and LETTERS.search(m.group(1)) and 'svg' not in tag:
                self.units.append({'kind': 'attr', 'start': s + m.start(1), 'end': s + m.end(1), 'text': m.group(1)})
        if tag == 'svg':
            self.skip += 1
        if tag in VOID or raw.rstrip().endswith('/>'):
            if tag not in INLINE and self.stack:
                self.stack[-1]['block'] = True
            return
        if tag not in INLINE and self.stack:
            for en in self.stack:  # every open block above has a block child now
                pass
            self.stack[-1]['block'] = True
        self.stack.append({'tag': tag, 'cs': e, 'block': False, 'texts': [], 'inline': tag in INLINE})

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.script:
            s = self.off()
            if tag == 'script':
                self.units += js_units(self.t, self.script[1], s)
            self.script = None; return
        if tag == 'svg':
            self.skip = max(0, self.skip - 1); return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                break
        else:
            return
        ce = self.off()
        while len(self.stack) > i:
            en = self.stack.pop()
            if en['inline']:
                # text of an inline element belongs to the nearest block ancestor
                if self.stack:
                    self.stack[-1]['texts'] += en['texts']
                continue
            body = self.t[en['cs']:ce]
            if not en['block'] and LETTERS.search(re.sub(r'<[^>]+>', '', body)):
                self.units.append({'kind': 'html', 'start': en['cs'], 'end': ce, 'text': body})
            else:
                for (a, b, txt) in en['texts']:
                    if LETTERS.search(txt):
                        self.units.append({'kind': 'text', 'start': a, 'end': b, 'text': txt})
            ce = en['cs']  # parents end later; ce is re-read below for the next pop
            ce = self.off()

    def handle_data(self, data):
        if self.script or self.skip or not self.stack:
            return
        s = self.off()
        e = self.t.find('<', s)
        e = len(self.t) if e < 0 else e
        raw = self.t[s:e]
        st = raw.strip()
        if st:
            a = s + raw.index(st)
            self.stack[-1]['texts'].append((a, a + len(st), st))


def js_units(text, a, b):
    """String literals of a script that read like prose."""
    out = []
    i = a
    prev = ''
    while i < b:
        c = text[i]
        if text.startswith('//', i):
            j = text.find('\n', i); i = b if j < 0 else j; continue
        if text.startswith('/*', i):
            j = text.find('*/', i); i = b if j < 0 else j + 2; continue
        if c in '\'"`':
            q = c; j = i + 1
            while j < b:
                if text[j] == '\\': j += 2; continue
                if text[j] == q: break
                if q == '`' and text.startswith('${', j):
                    depth = 1; j += 2
                    while j < b and depth:
                        if text[j] == '{': depth += 1
                        elif text[j] == '}': depth -= 1
                        j += 1
                    continue
                j += 1
            s = text[i + 1:j]
            if prose(s):
                out.append({'kind': 'js', 'start': i + 1, 'end': j, 'text': s, 'q': q})
            i = j + 1; prev = 'x'; continue
        if c == '/' and prev in '(,=:[!&|?{};' + '\n':
            j = i + 1
            while j < b and text[j] != '/' or text[j - 1] == '\\':
                if text[j] == '\n': break
                j += 1
            i = j + 1; continue
        if not c.isspace():
            prev = c
        i += 1
    return out


PT_HINT = re.compile(r'[ãáàâéêíóôõúçÃÁÀÂÉÊÍÓÔÕÚÇ]|\b(?:de|da|do|das|dos|que|não|para|com|uma|um|se|em|na|no|as|os|o|a|é|ou|e|à|ao|por|mais|sem|já|há|me|te|tu|eu)\b')

# short display words inside JS data arrays that the prose() heuristic cannot tell from code tokens
EXTRA = {'Abordar', 'Absentismo', 'Afastamento', 'Ansiedade', 'Apatia', 'Apoiar', 'Apoio direto.', 'Baixa energia', 'Boca seca', 'Cognitivas',
         'Comparar', 'Comportamentais', 'Continuar', 'Corpo ativado', 'Culpa', 'Desespero', 'Emocionais', 'Encaminhamento', 'Encaminhar',
         'Erro grave', 'Escuta', 'Escuta ativa', 'Escutar', 'Estigma social', 'Evitamento', 'Exemplo', 'Exemplos', 'Expira', 'Factos', 'Fadiga',
         'Feito ✓', 'Follow-up', 'Impacto', 'Implica:', 'Importa', 'Inclui', 'Inspira', 'Intervir cedo', 'Irritabilidade', 'Julgar', 'Ligar',
         'Maior foco', 'Manter confidencialidade', 'Manter disponibilidade.', 'Medo', 'Minimizar', 'Necessidades', 'Neste momento', 'Observar',
         'Para fechar', 'Parar', 'Peri-crise', 'Pode incluir', 'Prazos', 'Preparar', 'Previsibilidade', 'Raiva', 'Recompensa', 'Retraimento',
         'Risco', 'Risco elevado', 'Rotatividade', 'Se quer falar', 'Sim', 'Sofrimento', 'Sudorese', 'Taquicardia', 'Tempo', 'Tonturas',
         'Tremores', 'Tristeza', 'Validar', 'Valores', 'Vergonha', 'Vulnerabilidade', 'fico presente', 'gerais', 'laborais'}


def prose(s):
    if s in EXTRA or '<span>Pergunta:</span>' in s:
        return True
    if not s.strip() or not LETTERS.search(s):
        return False
    if re.fullmatch(r'[\w\-\.\#\[\]=:>\s,*~+()"\'/%$]+', s) and not PT_HINT.search(s) and ' ' not in s.strip():
        return False
    if re.search(r'[{};]|=>|\.querySelector|function|\bclass=|<\w+[^>]*class=\"[^\"]*\"[^>]*>$', s) and not PT_HINT.search(s):
        return False
    if s.startswith(('assets/', '#', '.', 'http', 'tel:', 'rgb', 'M', 'sec', '--')) and not PT_HINT.search(s):
        return False
    return bool(PT_HINT.search(s)) or (' ' in s.strip() and len(s) > 14)


SVG = re.compile(r'<svg\b.*?</svg>', re.S)


def view(text):
    """Unit text with every inline <svg> swapped for a short placeholder that the translation keeps as it is."""
    svgs = SVG.findall(text); k = [0]

    def r(m):
        k[0] += 1
        return '<svg#%d/>' % k[0]
    return SVG.sub(r, text), svgs


def main():
    units = {}
    pt = {}
    for f in sorted((ROOT / '_src' / 'lessons').glob('*.html')) + [ROOT / '_src' / 'shell.html']:
        text = f.read_text(encoding='utf-8')
        us = []
        m = re.match(r'\s*<!--(\{.*?\})-->', text, re.S)
        if m:
            meta = json.loads(m.group(1))
            for k in ('title', 'crumb'):
                a = text.index(json.dumps(meta[k], ensure_ascii=False)[1:-1].replace('\\"', '"').replace('"', '\\"')) if False else None
            blk = m.group(1)
            for k in ('title', 'crumb'):
                mm = re.search(r'"' + k + r'"\s*:\s*"((?:[^"\\]|\\.)*)"', blk)
                if mm and LETTERS.search(mm.group(1)):
                    us.append({'kind': 'meta', 'start': m.start(1) + mm.start(1), 'end': m.start(1) + mm.end(1), 'text': mm.group(1)})
        p = P(text); p.feed(text); p.close()
        us += p.units
        us.sort(key=lambda u: (u['start'], -u['end']))
        # attrs that sit inside an html leaf (an <img alt> in a button, a link title) are translated as part of that leaf's markup
        spans = [(u['start'], u['end']) for u in us if u['kind'] in ('html', 'text', 'js')]
        keep = [u for u in us if u['kind'] != 'attr' or not any(a <= u['start'] and u['end'] <= b for a, b in spans)]
        units[f.name] = keep
        for u in keep:
            u['view'] = view(u['text'])[0]
            pt.setdefault(u['view'], []).append(f.name)
    (OUT / 'units.json').write_text(json.dumps(units, ensure_ascii=False, indent=0), encoding='utf-8')
    (OUT / 'pt.json').write_text(json.dumps(pt, ensure_ascii=False, indent=0), encoding='utf-8')
    # frozen order: translations are keyed by position, so new strings are only ever appended
    lst = OUT / 'pt_list.json'
    old = json.loads(lst.read_text(encoding='utf-8')) if lst.exists() else []
    have = set(old)
    old += [k for k in pt if k not in have]
    lst.write_text(json.dumps(old, ensure_ascii=False, indent=0), encoding='utf-8')
    n = sum(len(v) for v in units.values())
    print('units', n, 'unique', len(pt), 'chars(unique)', sum(len(k) for k in pt))


if __name__ == '__main__':
    main()
