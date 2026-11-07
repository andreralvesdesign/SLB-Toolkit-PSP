# Toolkit PSP · e-learning (versão de demonstração)

Curso e-learning de **Primeiros Socorros Psicológicos no Trabalho**, construído a partir de um toolkit em PDF. Seis módulos em formato scroll (cada módulo é uma página), em português e inglês. HTML, CSS e JavaScript simples, sem framework.

> **Versão de demonstração para portfólio.** Os documentos para download não estão incluídos: os botões continuam visíveis, mas mostram "Ação não disponível nesta versão de demonstração".

## Abrir
Abrir `index.html`, que leva ao ecrã de idioma. Funciona a partir do disco (`file://`) ou de qualquer servidor estático. Publicado em GitHub Pages com o domínio `sonaetoolkit.andrealvesdesign.com` (ficheiro `CNAME`).

## Endereços
Cada página tem um nome curto, em português na raiz e em inglês em `en/`: `/idioma`, `/inicio`, `/contextualizacao` … e `/en/language`, `/en/start`, `/en/context` … A lista está em `_src/pages.json`. Online, o `.html` não aparece no endereço (o GitHub Pages serve `/contextualizacao` a partir de `contextualizacao.html`); aberto do disco, os links mantêm o `.html`. O separador do browser diz sempre "Sonae Toolkit PSP" (inglês: "Sonae PFA Toolkit").

## Estrutura
```
index.html                                   reencaminha para idioma.html
idioma.html, inicio.html                     escolha de idioma; capa e as seis partes
como-utilizar.html                           Módulo 1
contextualizacao.html … primeiros-socorros.html          Módulo 2
sinais-de-alerta.html … limites-e-confidencialidade.html Módulo 3 · Se eu sou um Colaborador
papel-do-lider.html … seguranca-psicologica.html         Módulo 4 · Se eu sou um Líder
situacoes-sensiveis.html, burnout.html … suicidio.html   Módulo 5 · Situações Sensíveis
quando-encaminhar.html, recursos.html                    Módulo 6 · Encaminhamento e Recursos
en/                                          versão em inglês (nomes traduzidos)
assets/css/course.css                        estilos (tokens de cor, layout, componentes, responsivo)
assets/js/player.js                          leitor partilhado: navegação, menu, gate, componentes
assets/js/captions.js                        legendas de todos os vídeos (gerado)
assets/img, assets/video                     imagens, vídeos (H.264) e legendas .vtt (PT e EN)
_src/                                        fontes: editar aqui, nunca nos .html gerados
```

## Construir
1. Editar `_src/lessons/<módulo>.html` (secções + `<script>` opcional) ou `_src/shell.html` (cabeçalho, rodapé, menu, diálogos).
2. Correr `python3 _src/build.py` nesta pasta. Reescreve os `.html` da raiz e de `en/` com os nomes de `_src/pages.json`, `slides.json`, `assets/js/pages.js` e `assets/js/captions.js`, e apaga páginas com nomes antigos.
3. Módulo novo: acrescentar o fragmento em `_src/lessons/`, dar-lhe os nomes PT e EN em `_src/pages.json` e registá-lo em `COURSE`, no topo de `assets/js/player.js`.

## Como funciona
- **Scroll por módulo.** As secções seguem-se na mesma página; cabeçalho fixo com barra de progresso; no fim, "A seguir", Anterior e Seguinte.
- **Gate.** O Seguinte só abre depois de explorar tudo na página (separadores, passos, cartões, fluxogramas, exercícios). Um ponto vermelho marca o que falta abrir. `?gate=off` desliga o bloqueio.
- **Componentes genéricos** em `player.js`: `[data-vtabs]`, `[data-steps]`, `[data-segtabs]`, `[data-reveal]`, `[data-goto]`, cartões que viram (`PSP.flips`), árvores de decisão em conversa e em fluxograma visual (`PSP.flow`), confetis no fim do módulo.
- **Telemóvel.** Separadores e checklists passam a acordeão; vídeos por cima do texto; hovers só em `@media (hover:hover)`.
- **Vídeos.** Só um toca de cada vez; legendas PT/EN embutidas em `captions.js` para funcionarem também a partir do disco.
- **Progresso** em `localStorage` (nada é enviado). Clicar 3 vezes no logótipo ou Shift+Alt+R apaga o progresso.
- **Links diretos.** Um hash com o id da secção (`#m2-3-s14`) abre a secção certa, mesmo noutro módulo; depois o hash sai do endereço.

## Acessibilidade
- Todo o texto é texto real (nada em imagem); cartões que viram com o verso num parágrafo ligado por `aria-controls` e anunciado.
- Conversas em `role="log"`, com reprodução automática e versão completa em texto.
- Separadores com setas, foco visível, `aria-live` nos resultados, títulos sem saltos de nível, contraste 4,5:1, alvos de 44 px, movimento reduzido, texto alternativo nas ilustrações.

## Inglês
As traduções ficam em `_src/i18n/en/c*.json`, por número de frase (`pt_list.json` só se acrescenta, nunca se reordena). O `build.py` corre `_src/i18n/apply.py`, que troca o texto dos fragmentos PT por posição, confere etiquetas, atributos e código, e escreve `_src/lessons-en/` e `_src/shell.en.html`. Se uma frase PT mudar, o build pára até haver tradução. Os textos do `player.js` usam `L('pt', 'en')`.
