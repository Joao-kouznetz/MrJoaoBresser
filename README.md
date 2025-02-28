# Documentação de Deploy com MkDocs

Essa documentação explica os comandos necessários para construir e publicar a documentação do projeto usando MkDocs.

## 1. Construção da Documentação

Para gerar a documentação localmente, use o comando:

```
mkdocs build
```

## Publicando no git hub -pages

```
mkdocs gh-deploy --remote-branch Docs
```

O que este comando faz?

- gh-deploy: Faz o deploy da documentação no GitHub Pages.

- --remote-branch Docs: Especifica que a documentação será enviada para a branch Docs do repositório remoto.

Isso faz com que a versão mais recente da documentação gerada seja publicada na branch Docs, tornando-a acessível online.
