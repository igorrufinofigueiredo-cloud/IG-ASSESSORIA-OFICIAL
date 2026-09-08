# IG Assessoria — site oficial

Site institucional de criação de sites da IG Assessoria.
No ar em: https://igorrufinofigueiredo-cloud.github.io/IG-ASSESSORIA-OFICIAL/

---

## O que tem nesta pasta

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site inteiro. HTML, CSS, JavaScript e as imagens dos cases, tudo dentro deste arquivo. |
| `404.html` | Página que aparece quando alguém abre um endereço errado do site. O GitHub Pages usa sozinho. |
| `sitemap.xml` | Mapa do site para o Google encontrar as páginas. |
| `robots.txt` | Autoriza os buscadores a indexar o site e aponta para o sitemap. |
| `README.md` | Este arquivo. Não aparece no site, só na página do repositório. |

O site não depende de nenhuma pasta de imagens. Se um dia aparecer uma pasta
`cases-img` no repositório, pode apagar: não é mais usada.

---

## Como subir (pelo navegador, sem linha de comando)

1. Abrir https://github.com/igorrufinofigueiredo-cloud/IG-ASSESSORIA-OFICIAL
2. Se já existir um `index.html` lá, apagar primeiro: clicar no arquivo → ícone de lixeira → **Commit changes**.
   Fazer o mesmo com `styles.css` e `script.js`, que não são mais usados.
3. Voltar para a página inicial do repositório e clicar em **Add file** → **Upload files**.
4. Arrastar os arquivos desta pasta para dentro da área de upload.
5. Clicar em **Commit changes**.
6. Esperar de 1 a 3 minutos e abrir o site em aba anônima para ver a versão nova.

> Se o navegador estiver traduzindo a página do GitHub, os botões aparecem como
> "Adicionar arquivo" e "Confirmar alterações". É o mesmo caminho.

---

## Antes de mandar o link para alguém

- [ ] Abrir o site em aba anônima, no celular, e conferir se os 4 cases aparecem
- [ ] Preencher o formulário até o fim e ver se o WhatsApp abre com a mensagem certa
- [ ] Colar o link no WhatsApp e conferir se a prévia mostra imagem e título
- [ ] Clicar em um botão de WhatsApp e conferir se abre a conversa

---

## Como trocar uma imagem de case depois

As imagens estão embutidas dentro do `index.html` em base64, e por isso não
quebram nunca. Para trocar uma delas, é preciso gerar o novo código base64.
Mais simples: mandar o print novo no chat e pedir o arquivo atualizado.
