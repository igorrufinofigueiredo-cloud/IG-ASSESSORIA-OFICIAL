# Site oficial da IG Assessoria

Site institucional da IG Assessoria (marca, sites e sistemas), no ar em https://igassessoria.com.br pelo GitHub Pages deste repositório.

## Como ler este projeto sem gastar crédito

1. Ler `MAPA.md` primeiro. Ele diz em qual linha está cada seção, bloco de CSS e função de JS.
2. Abrir só as linhas indicadas (Read com offset e limit). Nunca abrir `index.html` inteiro: são uns 650 mil tokens.
3. Nunca ler as linhas listadas em "Linhas proibidas": são imagens, fontes, vídeos e bibliotecas embutidas.
4. Para achar algo fora do mapa, usar `grep -n` com um termo curto, nunca ler o arquivo para procurar.
5. Depois de editar, rodar o mapa de novo e subir o `MAPA.md` junto:
   `python3 ferramentas/mapa.py index.html contrato/index.html 404.html > MAPA.md`
6. Se a assinatura do arquivo no `MAPA.md` não bater com a do arquivo atual, rodar o mapa antes de qualquer leitura.

## Estrutura

- `index.html`: o site inteiro num arquivo só (texto, CSS, JS, imagens, fonte e vídeos embutidos)
- `contrato/index.html` e `contrato/privacidade.html`: contrato assinável e política de privacidade
- `cases/`: imagens dos cases (Folha & Verso, Pauta, Prumo) em webp, com versão de 900 px
- `404.html`, `robots.txt`, `sitemap.xml`, `CNAME` (domínio igassessoria.com.br)
- `ferramentas/mapa.py`: gera o `MAPA.md`

## Regras do projeto

- Visual editorial monocromático da IG; nada de travessão nem texto com cara de IA.
- Todos os botões abrem o WhatsApp +55 83 9872-8515 com mensagem pronta.
- O site não carrega nada de fora (fonte, imagem, biblioteca): tudo continua embutido.
- Editar só o trecho que muda. Não reescrever o arquivo inteiro.
- Antes de publicar: revisar alinhamento, sobreposição e textos no celular, e conferir formulário e botões de WhatsApp.
- Publicar só quando Igor pedir.
