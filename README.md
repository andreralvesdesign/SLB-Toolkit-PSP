# Toolkit PSP · Sport Lisboa e Benfica · versão scroll

Adaptação do curso "Primeiros Socorros Psicológicos no Trabalho" (feito para a Sonae) ao contexto de quem trabalha no Benfica. Fase 1: **conteúdo pedagógico**. Fase 2: **parte gráfica** (identidade do Benfica; estrutura e interações iguais). As ilustrações de pessoas (`av-*.webp`) ainda são as da versão Sonae.

## Parte gráfica (fase 2)
Inspirada no site oficial (slbenfica.pt, valores medidos no próprio site) e no emblema. O Brandfetch não abriu (verificação anti-bot).

| Elemento | Antes (MC) | Agora (Benfica) |
|---|---|---|
| Tipo de letra | Instrument Sans | **Roboto** (a do slbenfica.pt), 400/500/700, embebida no CSS como WOFF para funcionar a partir do disco |
| Vermelho | #DC3228 + variantes (escuro, rosado) | **um só vermelho, #C30000** (o da interface do site). Sem vermelho-escuro, rosados, transparências nem sombras sobre vermelho. Os botões vermelhos ficam pretos ao passar o rato |
| Blocos escuros (slides de destaque, regras, citações, verso dos cartões, vídeo) | azul-marinho #000F64 | **vermelho #C30000 liso com texto branco**; o que era vermelho por cima passa a branco |
| Texto e controlos pequenos | azul-marinho #000F64 | **#242424** (preto do site). A variável continua a chamar-se `--navy` |
| Fundo / linhas | #F0F0EB quente | **alternância** entre cinza-claro #F4F4F4 e branco puro, slide a slide (os vermelhos não contam). O `build.py` põe a classe `s-white` num slide claro sim, num não. Nos slides brancos, os cartões passam a cinza-claro e o que estava dentro deles a branco. Linhas #DCDCDC |
| Cores de apoio | verde, azul, amarelo MC | cores do emblema: verde #12814B, azul #1074BC, dourado #FFD432 |
| Partes 0–6 (Índice) | 7 cores MC | preto, azul, vermelho, verde, cinzento, dourado, preto |
| Botões e cartões | redondos (pílula) | **cantos retos**, contorno de 1px preto; ação principal ("Seguinte", "Apoio") a vermelho cheio |
| Etiquetas | maiúsculas vermelho-escuro | maiúsculas vermelhas, como as do site ("ASSEMBLEIA GERAL") |
| Logótipo | `logo-mc.png` | `emblema-slb.svg` (o emblema entregue em `../assets/emblema`) |
| Aquarela da capa e dos módulos | `aquarela.webp` (círculo marinho + mancha vermelha) | `motivo.svg`: a **roda de bicicleta do emblema**, o círculo vermelho com a faixa do escudo e a bola dourada. **Já não é usado:** a capa inicial passou a ter a ilustração Storyset "Team goals" (`av-team-goals.svg`) |
| Ícones (`ic-*.svg`) | marinho + pincel vermelho (desenho Sonae) | substituídos por Tabler Icons (licença MIT, @tabler/icons 3.19.0): linhas #242424 com uma só parte em #C30000, sem pincel. Os PNG da Sonae estão arquivados em `../escolha-icones/sonae-originais/` e já não são usados |
| Ilustrações de pessoas (`av-*.svg`) | `av-*.webp`, personagens multicolores (desenho Sonae) | substituídas por ilustrações **Storyset, estilo Pana** (storyset.com, Freepik; feitas por ilustradores, não IA). Cor principal trocada para #C30000, tinta para #242424, sombreados translúcidos retirados (não há rosados) e `viewBox` recortado ao conteúdo. Ao contrário da versão Sonae, **cada sítio do curso tem a sua ilustração** (49 usos, 49 ilustrações diferentes): as 18 que substituíram as da Sonae mantêm o nome `av-NN.svg`; as restantes têm o nome da ilustração Storyset (`av-stress.svg`, `av-deadline.svg`…). O prefixo `av-` tem de ficar, porque o `player.js` usa-o para não pôr o emblema nessas secções. Cada SVG diz no topo de que ilustração veio. **Licença gratuita com atribuição: "Illustrations by Storyset"** (tem de aparecer nos créditos do curso/plataforma). Os WebP da Sonae estão em `../escolha-ilustracoes/sonae-originais/` |
| Confetti do fim de módulo | cores MC | cores do emblema |

**Texturas desportivas (muito suaves, só decoração):**
- **Slides claros:** grão de filme e uma sombra neutra num canto. Alternam dois tipos de riscas diagonais de velocidade, em cinzento e nunca em vermelho: umas finas a sair do canto superior esquerdo e outras na diagonal contrária, mais espaçadas e um pouco mais grossas, a sair do canto inferior direito. As do canto inferior direito nunca ficam numa secção imediatamente antes ou depois de uma secção com emblema (aí o fundo fica liso).
- **Capa:** riscas de relvado cortado atrás do motivo.
- **Slides e blocos vermelhos:** vermelho liso, sem textura, para o tom nunca mudar.

Ficam em `::before`/`::after` atrás do conteúdo, sem bloquear cliques, e desaparecem em impressão e no modo de alto contraste. Estão na secção "Benfica · texturas desportivas" do CSS.

**Espaçamento:** mais ar em todo o curso, para facilitar a leitura:
- entrelinha do texto +0,12;
- intervalos entre caixas e elementos ×1,35;
- margens entre blocos ×1,3;
- padding de caixas e botões ×1,2;
- botões um pouco mais altos.

O cabeçalho mantém os intervalos originais, para o nome do módulo caber. Está na secção "Benfica · espaçamento" do CSS.

**Fotografias:**
- **Onde estão:** as capas de 25 módulos têm uma fotografia de pessoas no lugar do motivo gráfico (incluindo a abertura do 5.9, com uma imagem de apoio sereno). A página inicial tem uma ilustração (`av-team-goals.svg`), não uma foto. A 5.0 (índice) fica sem fotografia.
- **Formato:** no computador, quase quadradas (6:5) e com a largura da coluna, com um bloco vermelho reto atrás. No telemóvel ficam por baixo do título, a toda a largura, em 3:2, como as fotografias dentro dos módulos. Ficheiros: `capa-<módulo>-d.webp` (computador) e `-h.webp` (telemóvel).
- **Ficheiros:** o original está em `../assets/imagens/` e as versões do curso, em WebP, em `assets/img/fotos/`.
- **Capas, posição:** começam no topo, com a fotografia mais baixa (até 54 % da altura do ecrã).
- **Dentro dos módulos:** 13 secções de uma só coluna (listas "O que fazer?" e "O que evitar?", citações, comparações) têm uma fotografia numa coluna à direita, fixa (não acompanha o scroll). No telemóvel passa para baixo do título, em horizontal. Cada uma tem duas versões: `<módulo>-<secção>-v.webp` (vertical) e `-h.webp` (horizontal).
- **Emblema:** nunca entra numa secção com fotografia.

**Emblema em marca de água:** o emblema só com as linhas, como no slbenfica.pt, e **apenas como fundo de secções**: nunca dentro de blocos nem de botões.
- **Encaixe:** o topo (a águia) fica fixo no topo da secção, nunca cortado. O emblema estica para baixo, sem distorcer, e passa sempre do fundo. Fica à direita e pode ser cortado na lateral.
- **Escala:** varia de secção para secção. Nunca desce dos 135 % da altura e é maior nas secções pequenas (até 260 %).
- **Onde:** é o `player.js` que escolhe, com a página já montada. Nunca usa secções com vídeo ou ilustração, nem secções em que o lado direito tenha muito texto, caixas ou interações (mede o que lá está).
- **Quantas vezes:** pelo menos uma vez por página, e nunca em duas secções seguidas. Nas secções claras, com moderação (uma em cada quatro, no máximo). Nas secções vermelhas, sempre que o lado direito estiver livre. Se uma página não tiver nenhuma secção livre, usa a menos ocupada e, em último caso, a secção final.
- **Opacidade:** 50 % no cinza-claro, 25 % no branco e 16 % no vermelho (linhas brancas). No vermelho, a pedido, isto dá linhas ligeiramente rosadas.
- **Excluir uma secção:** `data-nowm` na secção.

A versão de linhas está em `assets/img/emblema-linhas.svg`, gerada a partir do emblema entregue: são as partes pretas do original. No CSS vai embebida, para funcionar a partir do disco.

**Sem círculos decorativos:** não há círculos no fundo das secções nem dos blocos.
- As regras e as citações vermelhas ficam lisas, sem decoração.
- O ícone dos slides vermelhos está num quadrado, sem anéis. No 1.4 (O que não substitui) e na Ideia-chave do 2.1, o quadrado é uma fotografia (`fotos/nao-substitui-*`, `fotos/ideia-chave-*`; e em "O que NÃO são" do 2.3, `fotos/nao-sao-*`. A foto tem a altura do conteúdo da coluna esquerda no computador, 3:2 por cima do texto em ecrãs estreitos).
- Ficam redondos só os elementos com função: pontos, números, avatares, a roda dos 7 princípios e o exercício de respiração. As regras novas estão no fim de `assets/css/course.css` ("Benfica skin").

## Abrir e construir
- Abrir `index.html` (funciona a partir do disco ou de um servidor).
- Editar sempre `_src/lessons/*.html` e `_src/shell.html`, nunca os `.html` da raiz. Depois, `python _src/build.py` (a partir desta pasta) reescreve as páginas e o `slides.json`.
- **Sem bloqueio:** nesta versão o "Seguinte" está sempre ativo (`GATE = false` em `assets/js/player.js`). Os pontos vermelhos e as linhas "Clica…" continuam a guiar, mas não obrigam. Um módulo conta como concluído quando todas as secções foram vistas.
- O resto da mecânica (pontos vermelhos, fluxogramas, acessibilidade, ids de slide estáveis para a ferramenta de revisão) é a do curso scroll da Sonae. Ver o README desse projeto.

## O que mudou em relação à versão Sonae
| Tema | Sonae | Benfica |
|---|---|---|
| Organização | Sonae, MC, "colaborador(a) MC" | Sport Lisboa e Benfica ("o Benfica") |
| Contextos de trabalho | loja, armazém, secção de frutas e legumes, "Loja Wells" | Estádio da Luz em dia de jogo, loja do Benfica, Museu Benfica, Campus do Seixal, Benfica TV, serviços centrais |
| Ficha 5.8 | Apoio a cliente em sofrimento | **Apoio a sócio ou adepto em sofrimento** (ficheiro renomeado; o id `m5-8-…` mantém-se) |
| Recursos internos (6.2) | Somos Sonae (Cruz Vermelha), Seguro Multicare, Medicina no Trabalho Sonae | Marcadores **[A CONFIRMAR]**; Medicina no Trabalho em texto genérico; novo separador com o **Código de Conduta e o canal de denúncias** |
| Botão Apoio | Linha Somos Sonae 800 100 025 | "Apoio ao colaborador do Benfica: por definir" |
| Vídeos | 15 vídeos | **Todos indisponíveis**: o player mostra o aviso "Vídeo ainda não disponível nesta versão do curso." |
| PDFs | "Ler no Toolkit" + 43 descarregáveis | **Retirados** (não existe ainda um Toolkit do Benfica). O Fluxograma 3, que só existia em PDF, passou a texto no módulo 3.2 |
| Idioma | PT + EN com ecrã de escolha | **Só português** (sem pasta `en/`, sem seletor) |
| Marca de formação | Faixa "Eu escolho aprender" | Retirada |

Não foi copiada a versão slides da Sonae. O projeto `sonae_version` ficou intacto (incluindo `output/slides`).

## Endereços curtos
Cada página é uma pasta com o seu `index.html`, para os endereços não terem `.html` nem o nome longo:
`/` (Introdução), `/2-1/`, `/3-2/` … `/6-2/`, e em inglês `/en/`, `/en/2-1/` … O build gera esta estrutura a partir dos fragmentos de `_src/lessons/` (que mantêm os nomes longos) e reescreve todas as ligações entre páginas. Depois do `#` fica a secção (`/2-1/#m2-1-ideia`), que serve para voltar ao ponto onde se ficou.
Para ver localmente é preciso um servidor (`python -m http.server` na pasta `curso/`): aberto com duplo clique, o browser não abre `2-1/` sozinho. No GitHub Pages funciona sem configuração; com o domínio `slbtoolkit.andrealvesdesign.com` fica `slbtoolkit.andrealvesdesign.com/2-1/`.

## Camada moderna (só estética)
No fim do `course.css` ("Benfica · camada moderna"): gradientes suaves só em brancos e cinzentos (secções, cartões, botões neutros, Índice), contorno fino e sombra leve nos cartões das secções claras, cabeçalho em vidro fosco (com recurso para quem pede menos transparência), traço vermelho liso antes das etiquetas, sombra neutra nas fotos das secções claras, seleção de texto e anel de foco a vermelho. O vermelho continua liso: nada de gradiente, sombra ou transparência sobre o vermelho. Sem bibliotecas novas (só CSS). Cópia do CSS anterior no scratchpad da sessão (`course.before-modern.css`).

## Versão inglesa (en/)
- **Como se gera:** `python _src/build.py` constrói o português na raiz e o inglês em `en/` (mesmos nomes de ficheiro; `assets/` é partilhado). Com `--no-en` salta o inglês.
- **Traduções:** `_src/i18n/extract.py` lista todos os textos portugueses (`pt_list.json`, por ordem fixa); `_src/i18n/en/c*.json` tem o inglês de cada um. Os ficheiros `c00`–`c33` vêm da versão Sonae (textos iguais reaproveitados); `c90.json` tem os 297 textos novos ou adaptados ao Benfica. Se um texto português mudar ou for novo, o build do inglês pára e lista o que falta traduzir. `en/overrides.json` permite outra tradução para o mesmo texto num ficheiro (ex.: o tooltip do botão de idioma).
- **Termos:** Module (Módulo), page, Contents (Índice), Support (Apoio), PFA (PSP), member / fan (sócio / adepto), Occupational Medicine / Occupational Physician.
- **Capa de idioma:** primeira secção do `index.html` (emblema + "Escolhe o idioma / Choose your language", bandeiras). Aparece uma vez por sessão; depois abre a capa.
- **Botão de idioma no cabeçalho:** "EN" nas páginas portuguesas, "PT" nas inglesas. Abre a mesma página e a mesma secção na outra língua (os ids das secções são iguais nas duas).

## Nomes: módulos e páginas
O que antes se chamava **Parte** chama-se agora **Módulo** (Módulo 1 · Introdução … Módulo 6 · Encaminhamento e Recursos): no Índice, no cabeçalho, nas etiquetas das capas, nos cartões e nos textos ("ir para o Módulo 3 · A", "Módulo 4 concluído"). Cada 2.1, 3.2… é uma **página** do módulo: os botões Anterior / Seguinte dizem "Página anterior / seguinte", o Índice mostra "Nesta página: x de y secções vistas" e conta "x de 6 módulos concluídos" (um módulo conta quando todas as suas páginas estão concluídas). As subdivisões "Parte A / Parte B" dentro dos módulos 3 e 4 mantêm o nome.

## Estrutura: Início e Introdução num só módulo
O antigo "Início" (capa + lista das partes) e o módulo 1.1 "Como utilizar este Toolkit" são agora **um só módulo, a Introdução** (`index.html`, capítulo `0`, que no Índice aparece como Parte 1 · 1.1 Introdução). Passou de 10 secções para 6: capa · o que é e para quem é · o que não substitui · quando utilizar · as cinco partes e como navegar · fim. Saíram os cartões "A quem lidera / A cada colaborador", a lista de ferramentas de consulta rápida e a visita guiada aos botões (o essencial dela passou para o texto das cinco partes). O ficheiro `1-1-como-utilizar.html` deixou de existir; as cópias de segurança estão no scratchpad da sessão.

## Versão de demonstração
- Vídeos: só "Vídeo não disponível nesta versão de demonstração." (sem o título do vídeo). Por baixo: "Legendas não disponíveis nesta versão de demonstração."
- Dados internos: "(Informação não disponível nesta versão de demonstração)".
- O último módulo (6.2) fecha com "Terminaste o Toolkit…" e o botão **Terminar** (abre o diálogo de sair). Cada **parte** conta como um módulo: só a última página de cada parte tem a secção de fecho ("Parte N concluída · Terminaste este módulo · Utiliza o botão Seguinte para avançar para o próximo módulo."), ou seja Introdução, 2.3, 3.5, 4.5, 5.9 (depois do "Para saber mais", sem confetti) e 6.2. As outras páginas acabam no último conteúdo, seguido do rodapé Anterior / Seguinte.

## Conteúdo criativo acrescentado (Benfica)
- **Introdução, para quem é:** do Estádio da Luz ao Campus do Seixal, do Museu às lojas, da bilheteira aos serviços centrais, da Benfica TV à Fundação Benfica.
- **2.1 Exemplos:** a Ana e a Rita passam a trabalhar no atendimento ao público do Estádio numa semana de jogo grande.
- **Role plays (contexto, sem vídeo):** 1.º armazém de logística do Estádio; 3.º loja do Benfica em hora de pico antes do jogo; 4.º serviços centrais na véspera de um jogo grande; 5.º Museu Benfica – Cosme Damião, visitante com ataque de pânico.
- **4.4 Estudos de caso:** Benfica TV (prazos), loja em campanha de sócios (reatividade), organização de dia de jogo (sobrecarga), Campus do Seixal (isolamento).
- **4.5:** picos de calendário (dias de jogo, jogos europeus, final de época, campanhas de sócios).
- **Parte 5:** luto coletivo na comunidade benfiquista (5.2); incidente grave no Estádio com público (5.4); emoção do resultado e segurança do Estádio com adeptos (5.5, 5.8).
- **6.2:** o Código de Conduta da Benfica SAD e o canal de denúncias; fecho com "E pluribus unum".

## O que o Benfica tem de confirmar antes de publicar
A pesquisa pública não encontrou nenhum programa de apoio psicológico ou de saúde do Benfica para os seus colaboradores. Por isso **não se inventou nenhum**: onde a Sonae tinha um serviço interno, há um marcador `[A CONFIRMAR]`. No curso, esses marcadores aparecem agora como "(dados ocultados desta versão)", e os "por definir" foram retirados. Procurar por "dados ocultados" para encontrar todos os sítios a preencher.

1. **Apoio psicológico interno (6.2, ecrã 2):** quem presta, nº de consultas, custo, presencial/online, quem pode usar, contacto e se funciona 24h. Perguntar também se cobre quem trabalha nos dias de jogo (incluindo prestadores).
2. **Seguro de saúde e bem-estar (6.2, ecrã 3 e separador "Serviços de saúde"):** se existe, seguradora, consultas de psicologia, como marcar.
3. **Medicina no Trabalho (6.2):** contacto e local no Estádio e no Campus; a alternativa 24h quando não há resposta no prazo (aparece também em 3.5 e 4.3).
4. **Botão Apoio (`_src/shell.html`) e ficha 5.9:** onde entra o contacto interno de apoio.
5. **Ficha 5.9, "Para saber mais":** manual ou página interna de prevenção do suicídio.
6. **Código de Conduta (6.2):** o texto cita o da **Benfica SAD**; confirmar se código e canal valem para o Clube e para as restantes entidades do Grupo Benfica (Benfica TV, Benfica Estádio, Fundação, Clínica do SLB, etc.).
7. **Clínica do SLB:** entidade do Grupo Benfica; confirmar se presta apoio a colaboradores (não está mencionada no curso).
8. **Nomes das estruturas** usados nos exemplos (bilheteira, loja do Estádio, serviços centrais, Benfica TV): confirmar que refletem a realidade.

## Linhas públicas: o que foi verificado
| Linha | Estado |
|---|---|
| 112 | conhecido |
| 1411, Prevenção do Suicídio, 24h | confirmado (lançada a 10 set 2025) |
| CITE 800 204 684, atendimento às segundas e terças, 14h30–16h00 | confirmado no site da CITE (o horário da Sonae estava certo) |
| APAV 116 006, dias úteis 08h–23h | confirmado no site da APAV (a Sonae tinha 09h–21h, desatualizado) |
| ACT 300 069 300, dias úteis 09h–12h30 | encontrado em gov.pt; a Sonae tinha 707 228 448. **Confirmar** em act.gov.pt |
| SOS Voz Amiga, 4 números, 15h30–00h30 | confirmado em notícias recentes |
| SNS 24 808 24 24 24, opção 4 | herdado da Sonae; **não confirmado** nesta pesquisa |
| Conversa Amiga, Voz de Apoio, Telefone da Amizade | herdados da Sonae; **não confirmados** (números e horários) |
| Linha de violência doméstica 800 202 148 e SMS 3060; Linha Internet Segura 800 219 090; ILGA | herdados da Sonae; **não confirmados** |

## Factos do Benfica usados (com fonte)
- Código de Conduta da Sport Lisboa e Benfica – Futebol, SAD: versão 01, em vigor desde 23 de novembro de 2022; secção 6.2 (igualdade, assédio); canal de denúncias em `slbenficasad.integrityline.com`. (`media.slbenfica.pt`, `codigo-conduta.pdf`)
- Entidades do Grupo Benfica (Benfica TV, Benfica Estádio, Clínica do SLB, Fundação Benfica, …) e sede no Estádio SL Benfica, Avenida Eusébio da Silva Ferreira, Lisboa: Política de Privacidade do Grupo Benfica.
- Museu Benfica – Cosme Damião no Estádio da Luz; Benfica Campus no Seixal.
- "E pluribus unum" é o lema que consta do emblema do clube.

## Ainda por fazer
- Vídeos (e legendas) e a respetiva versão Benfica dos role plays.
- Parte gráfica: pôr a atribuição "Illustrations by Storyset" num sítio visível do curso (o curso ainda não tem página de créditos). Confirmar com o Benfica se o emblema pode ser usado neste curso interno e se há manual de marca (tipo de letra própria, regras do emblema).
- Guião/PDF do Toolkit do Benfica e, depois, os descarregáveis.
- Versão em inglês.
- Revisão pedagógica por psicólogos do Benfica; revisão de linguagem (tratamento por tu mantido).
- SCORM e regras de conclusão.
