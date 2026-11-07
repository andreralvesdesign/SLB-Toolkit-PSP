#!/usr/bin/env python3
"""Cut the English PDF extracts (downloads/en/) from the English Toolkit (the DeepL translation of v20261020).

Source: Guiões/MC Sonae_Toolkit Psychological First Aid at Work_V1_EN-draft.pdf (148 pages: DeepL re-flowed three pages into two and added two blank pages).
Page n of the Portuguese Toolkit is page en_abs(n) of the English one (checked against the printed page numbers).
Writes downloads/en/*.pdf and _src/i18n/en/downloads.json ({portuguese file name: {file, pages, mb}}), which apply.py uses to re-point the download buttons of the English pages.
Run from the course root:  python _src/i18n/build_docs.py   (needs PyMuPDF)
"""
import json, pathlib
import fitz

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
EN_PDF = ROOT.parent.parent / 'Guiões' / 'MC Sonae_Toolkit Psychological First Aid at Work_V1_EN-draft.pdf'
OUT = ROOT / 'downloads' / 'en'

# Portuguese file -> (English file, Portuguese page numbers). Ranges come from the Portuguese extracts (see README).
R = lambda a, b: list(range(a, b + 1))
DOCS = {
    'autocheck-do-lider-10-perguntas': ('leader-self-check-10-questions', [105]),
    'cartao-de-bolso-psp': ('pfa-pocket-card', [25]),
    'checklist-devo-intervir': ('checklist-should-i-intervene', R(79, 81)),
    'checklist-o-que-observar-na-equipa': ('checklist-what-to-look-for-in-the-team', [13]),
    'estudos-de-caso-intervencao-do-lider': ('case-studies-leader-intervention', R(90, 93)),
    'ficha-1-burnout': ('sheet-1-burnout', R(109, 111)),
    'ficha-2-luto': ('sheet-2-grief', R(112, 113)),
    'ficha-3-ataques-de-panico': ('sheet-3-panic-attacks', R(114, 116)),
    'ficha-4-situacoes-de-calamidade': ('sheet-4-disaster-situations', R(117, 119)),
    'ficha-5-comportamento-agressivo': ('sheet-5-aggressive-behaviour', R(120, 122)),
    'ficha-6-crise-pessoal-grave': ('sheet-6-serious-personal-crisis', R(123, 124)),
    'ficha-7-conflito-na-equipa': ('sheet-7-conflict-in-the-team', R(125, 127)),
    'ficha-8-apoio-a-cliente-em-sofrimento': ('sheet-8-supporting-a-customer-in-distress', R(128, 129)),
    'ficha-9-suicidio': ('sheet-9-suicide', R(130, 133)),
    'fluxograma-1-psp-no-momento': ('flowchart-1-pfa-in-the-moment', [24]),
    'fluxograma-2-acao-rapida': ('flowchart-2-rapid-action', [44]),
    'fluxograma-3-reflexao-estruturada': ('flowchart-3-structured-reflection', [45]),
    'fluxograma-4-o-que-fazer-no-momento': ('flowchart-4-what-to-do-in-the-moment', [64]),
    'frases-uteis-e-o-que-evitar': ('useful-phrases-and-what-to-avoid', R(52, 53)),
    'guia-de-acao-devo-aproximar-me': ('action-guide-should-i-approach', [48]),
    'guia-rapido-como-apoiar-um-colega': ('quick-guide-how-to-support-a-colleague', R(62, 63)),
    'linhas-de-apoio': ('support-lines-contact-sheet', [140, 144]),
    'mini-seccao-psp-para-lideres': ('pfa-mini-section-for-leaders', R(94, 95)),
    'radar-de-risco-psicossocial-da-equipa': ('team-psychosocial-risk-radar', R(69, 70)),
    'recomendacoes-para-lideres': ('recommendations-for-leaders', R(96, 102)),
    'toolkit-psp-capitulo-1': ('pfa-toolkit-chapter-1', R(8, 10)),
    'toolkit-psp-capitulo-2': ('pfa-toolkit-chapter-2', R(11, 15)),
    'toolkit-psp-capitulo-3': ('pfa-toolkit-chapter-3', R(16, 25)),
    'toolkit-psp-completo': ('pfa-toolkit-complete', R(1, 145)),
    'toolkit-psp-parte-1': ('pfa-toolkit-part-1', R(4, 6)),
    'toolkit-psp-parte-3a-autorregulacao': ('pfa-toolkit-part-3a-self-regulation', R(36, 45)),
    'toolkit-psp-parte-3a-sinais-de-alerta': ('pfa-toolkit-part-3a-warning-signs', R(27, 35)),
    'toolkit-psp-parte-3b-apoiar-durante-a-conversa': ('pfa-toolkit-part-3b-supporting-during-the-conversation', R(49, 54)),
    'toolkit-psp-parte-3b-limites-e-guia-de-conversa': ('pfa-toolkit-part-3b-limits-and-conversation-guide', R(54, 64)),
    'toolkit-psp-parte-3b-reconhecer-e-aproximar': ('pfa-toolkit-part-3b-recognising-and-approaching', R(46, 48)),
    'toolkit-psp-parte-4-o-papel-do-lider': ('pfa-toolkit-part-4-role-of-the-leader', R(66, 70)),
    'toolkit-psp-parte-4a-devo-intervir': ('pfa-toolkit-part-4a-should-i-intervene', R(76, 86)),
    'toolkit-psp-parte-4a-identificar-sinais': ('pfa-toolkit-part-4a-identifying-signs', R(70, 75)),
    'toolkit-psp-parte-4b-como-abordar-um-colaborador': ('pfa-toolkit-part-4b-how-to-approach-an-employee', R(87, 95)),
    'toolkit-psp-parte-4b-liderar-para-a-seguranca-psicologica': ('pfa-toolkit-part-4b-leading-for-psychological-safety', R(96, 107)),
    'toolkit-psp-parte-5-situacoes-sensiveis': ('pfa-toolkit-part-5-sensitive-situations', R(108, 133)),
    'toolkit-psp-parte-6-quando-encaminhar': ('pfa-toolkit-part-6-when-to-refer', R(135, 136)),
    'toolkit-psp-parte-6-recursos': ('pfa-toolkit-part-6-resources', R(137, 145)),
}


def en_abs(p):
    """absolute page (1-based) of the English draft that holds Portuguese page p"""
    if p <= 29: return p
    if p <= 58:
        q = p - 29
        return 29 + (q if q <= 5 else q + 1 if q <= 24 else q + 2)   # EN part-2 page 6 is blank, page 26 is an overflow
    if p <= 87: return p + 2
    if p <= 116:
        q = p - 87
        return 89 + (q if q <= 15 else q + 1)                         # EN part-4 page 16 is blank
    return p + 3


def patch_overflow(doc):
    """EN page 54 (table "What to avoid", last row) ran onto an extra page: redraw that row on the page itself"""
    pg = doc[53]
    bg = pg.get_pixmap(dpi=20, clip=fitz.Rect(0, 830, 10, 840)).pixel(2, 2)
    fill = tuple(c / 255 for c in bg)
    pg.add_redact_annot(fitz.Rect(100, 814, 590, 836), fill=fill)
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    F = pathlib.Path('C:/Windows/Fonts')   # a font with the curly quotes (the built-in Helvetica has none)
    def put(xy, text, face, bold=False, italic=False):
        pg.insert_text(xy, text, fontname=face, fontfile=str(F / face_file[face]), fontsize=9.5, color=(0, 0, 0))
    face_file = {'arb': 'arialbd.ttf', 'ari': 'ariali.ttf', 'ar': 'arial.ttf'}
    put((109, 824), 'Focusing on oneself', 'arb')
    put((236, 820), '“That’s happened to me before…”', 'ari')
    put((236, 831), '“If I were you…”', 'ari')
    put((416, 820), 'Takes the focus away from', 'ar')
    put((416, 831), 'the other person', 'ar')


def main():
    src = fitz.open(str(EN_PDF))
    assert len(src) == 148, len(src)
    patch_overflow(src)
    src.subset_fonts()  # the Arial files added by the patch are embedded whole otherwise
    OUT.mkdir(parents=True, exist_ok=True)
    info = {}
    for pt_name, (en_name, pages) in DOCS.items():
        out = fitz.open()
        for p in pages:
            i = en_abs(p) - 1
            out.insert_pdf(src, from_page=i, to_page=i)
        out.set_metadata({'title': en_name.replace('-', ' ').capitalize(), 'author': 'MC Sonae', 'subject': 'English translation (DeepL draft)'})
        f = OUT / (en_name + '.pdf')
        out.save(str(f), garbage=4, deflate=True)
        info[pt_name] = {'file': en_name + '.pdf', 'pages': len(out), 'mb': round(f.stat().st_size / 1048576, 1)}
        print(pt_name, '->', en_name, len(out), 'pages', info[pt_name]['mb'], 'MB')
    (ROOT / '_src' / 'i18n' / 'en' / 'downloads.json').write_text(json.dumps(info, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
