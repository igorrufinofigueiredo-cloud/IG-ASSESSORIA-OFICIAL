# IG Assessoria — site oficial

Site institucional da IG Assessoria, publicado pelo GitHub Pages em
https://igorrufinofigueiredo-cloud.github.io/IG-ASSESSORIA-OFICIAL/

## Arquivos do repositório

| Arquivo | Para que serve | Precisa mexer? |
|---|---|---|
| `index.html` | O site inteiro: texto, estilo, script, imagens, fontes e o vídeo do hero, tudo dentro de um arquivo só | Sim, é o único que muda no dia a dia |
| `404.html` | Página mostrada quando alguém abre um endereço que não existe, com botão de voltar para a home | Raramente |
| `robots.txt` | Libera o site para os buscadores e aponta o sitemap | Só se mudar o domínio |
| `sitemap.xml` | Lista de páginas para o Google, com a data da última atualização | Atualizar a data quando publicar uma mudança grande |
| `.nojekyll` | Impede o GitHub de processar os arquivos antes de publicar | Nunca |

O site não depende de nada externo. Não carrega fonte do Google, não carrega imagem de outro servidor e não usa biblioteca de terceiros. Se o repositório estiver no ar, o site está completo.

## Como atualizar sem linha de comando

1. Abrir o repositório no navegador.
2. Clicar no arquivo que vai trocar, por exemplo `index.html`.
3. Clicar no ícone da lixeira para apagar e confirmar em **Commit changes**.
4. Voltar para a raiz do repositório e clicar em **Add file**, depois **Upload files**.
5. Arrastar o arquivo novo e confirmar em **Commit changes**.
6. Esperar de 1 a 2 minutos e abrir o site em aba anônima para ver a versão nova.

O nome do arquivo precisa ser exatamente `index.html`, tudo em minúsculo. Se o navegador estiver traduzindo a página do GitHub, desligue a tradução antes de subir, para não confundir os nomes.

## Antes de publicar

- Abrir o site em um celular de verdade, não só no simulador do navegador.
- Enviar o formulário uma vez e confirmar que a mensagem chegou.
- Clicar em um botão de WhatsApp e ver se abre a conversa com o texto já preenchido.
- Colar o link no WhatsApp e conferir se a prévia aparece com imagem e título.

## Domínio próprio

Quando o domínio do Registro.br estiver pronto:

1. Em **Settings**, **Pages**, campo **Custom domain**, escrever o domínio e salvar. Isso cria um arquivo `CNAME` no repositório.
2. No Registro.br, apontar os registros para o GitHub Pages.
3. Marcar **Enforce HTTPS** depois que o certificado for emitido.
4. Trocar o endereço antigo pelo novo dentro do `index.html`, nas linhas de `canonical`, `og:url` e do bloco de dados estruturados, e também no `robots.txt`, no `sitemap.xml` e no botão da `404.html`.

## Observações técnicas

- O arquivo `index.html` tem cerca de 1,8 MB porque o vídeo do hero e as imagens estão embutidos nele. É o preço de não depender de servidor externo. O carregamento inicial mostra a imagem estática do vídeo antes de ele começar.
- As animações respeitam a preferência de movimento reduzido do sistema.
- Não há chave, token ou senha no código. Tudo que está no arquivo é público.
