# Onde acessar

[https://joao-kouznetz.github.io/MrJoaoBresser/]

# Documentação de Deploy com MkDocs

Essa documentação explica os comandos necessários para construir e publicar a documentação do projeto usando MkDocs.

## 1. Construção da Documentação

Para so ver como ela fica rode:

```
mkdocs serve --livereload
```

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

# Documentação do Plugin para Incorporar Vídeos do YouTube no MkDocs

Este documento explica como criar e usar um plugin personalizado para o MkDocs que converte links de imagens do YouTube (`![texto](https://www.youtube.com/watch?v=ID)`) em iframes incorporados, permitindo que vídeos do YouTube sejam exibidos diretamente em sua documentação.

## Visão Geral

O plugin transforma a sintaxe markdown de imagem apontando para um vídeo do YouTube:

```markdown
![Título do vídeo](https://www.youtube.com/watch?v=GjZo2On_oOI)
```

Em um iframe HTML que incorpora o vídeo diretamente na página:

```html
<iframe width="560" height="315" 
  src="https://www.youtube.com/embed/GjZo2On_oOI" 
  title="YouTube video player" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen>
</iframe>
```

## Estrutura do Plugin

O plugin é composto por três partes principais:

1. **YouTubeEmbedProcessor**: Processa links de imagem do YouTube e os converte em iframes.
2. **YouTubeEmbedExtension**: Extensão do Markdown que registra o processador.
3. **YouTubePlugin**: Classe principal do plugin que configura a extensão Markdown para o MkDocs.

## Implementação Passo a Passo

### 1. Estrutura de Arquivos

Primeiro, crie a seguinte estrutura de arquivos:

```
seu-projeto/
├── mkdocs.yml
├── docsmd/
├── plugins/
│   ├── __init__.py
│   └── youtube.py
└── setup.py
```

### 2. Código do Plugin

No arquivo `plugins/youtube.py`, implemente o código do plugin:

```python
import re
from markdown.inlinepatterns import ImageInlineProcessor
from markdown.extensions import Extension
from xml.etree import ElementTree as etree
import mkdocs.plugins

# Expressão regular para detectar ![texto](https://www.youtube.com/watch?v=ID)
YOUTUBE_RE = r"!\[(?P<alt>[^\]]*)\]\((?P<url>https?://www\.youtube\.com/watch\?v=(?P<id>[\w-]+)[^\)]*)\)"

class YouTubeEmbedProcessor(ImageInlineProcessor):
    def handleMatch(self, m, data):
        # Extrai o id do vídeo
        video_id = m.group("id")
        
        # Cria o elemento iframe
        iframe = etree.Element("iframe")
        iframe.set("width", "560")
        iframe.set("height", "315")
        iframe.set("src", f"https://www.youtube.com/embed/{video_id}")
        iframe.set("title", "YouTube video player")
        iframe.set("frameborder", "0")
        iframe.set(
            "allow", 
            "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
        )
        iframe.set("allowfullscreen", "allowfullscreen")
        
        return iframe, m.start(0), m.end(0)

class YouTubeEmbedExtension(Extension):
    def extendMarkdown(self, md):
        pattern = YouTubeEmbedProcessor(YOUTUBE_RE, md)
        # Registra a extensão com prioridade 175 (maior que a do padrão de imagens)
        md.inlinePatterns.register(pattern, "youtube_embed", 175)

class YouTubePlugin(mkdocs.plugins.BasePlugin):
    def on_config(self, config):
        # Adicione a extensão à lista de extensões markdown
        config['markdown_extensions'].append(YouTubeEmbedExtension())
        return config

# Função necessária para registro do plugin
def get_plugin_class():
    return YouTubePlugin
```

### 3. Arquivo de Configuração de Instalação

No arquivo `setup.py` na raiz do projeto, adicione:

```python
from setuptools import setup, find_packages

setup(
    name='mkdocs-youtube-plugin',
    version='0.1.0',
    description='Plugin para embutir vídeos do YouTube em documentação MkDocs',
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'youtube = plugins.youtube:YouTubePlugin',
        ]
    },
)
```

### 4. Instalação do Plugin

Instale o plugin localmente executando:

```bash
pip install -e .
```

Isso instala o plugin em modo de desenvolvimento, permitindo que você faça alterações sem precisar reinstalá-lo.

### 5. Configuração do MkDocs

Atualize o arquivo `mkdocs.yml` para incluir o plugin:

```yaml
site_name: MR Joao Bresser
docs_dir: docsmd
nav:
    - Home: index.md
    - legal: home.md
    - Projetos: nuvem.md
theme:
    name: simple-blog
    custom_dir: custom_theme/
extra_css:
    - custom.css
plugins:
    - youtube
markdown_extensions:
    - markdown.extensions.extra
    - markdown.extensions.codehilite
```

## Explicação Detalhada dos Componentes

### Expressão Regular

A expressão regular `YOUTUBE_RE` captura três grupos importantes:

- `alt`: O texto alternativo da imagem (o título do vídeo)
- `url`: A URL completa do vídeo do YouTube
- `id`: O ID do vídeo do YouTube, que é usado para criar o iframe

```python
YOUTUBE_RE = r"!\[(?P<alt>[^\]]*)\]\((?P<url>https?://www\.youtube\.com/watch\?v=(?P<id>[\w-]+)[^\)]*)\)"
```

### YouTubeEmbedProcessor

Esta classe herda de `ImageInlineProcessor` e sobrescreve o método `handleMatch` para processar links de imagem do YouTube:

1. Extrai o ID do vídeo do grupo capturado
2. Cria um elemento iframe com os atributos apropriados
3. Retorna o elemento iframe e as posições de início e fim do padrão correspondente

### YouTubeEmbedExtension

Esta classe estende a funcionalidade do Markdown:

1. Cria uma instância do `YouTubeEmbedProcessor`
2. Registra o processador com uma prioridade alta (175) para garantir que seja executado antes do processador de imagens padrão

### YouTubePlugin

Esta classe implementa o plugin do MkDocs:

1. Sobrescreve o método `on_config` para modificar a configuração do MkDocs
2. Adiciona a extensão `YouTubeEmbedExtension` à lista de extensões do Markdown

## Uso

Depois de configurar o plugin, você pode incorporar vídeos do YouTube usando a sintaxe de imagem do Markdown:

```markdown
![Título descritivo do vídeo](https://www.youtube.com/watch?v=GjZo2On_oOI)
```

O plugin detectará essa sintaxe e substituirá automaticamente pelo iframe do YouTube quando o MkDocs gerar o HTML.

## Considerações

- O plugin atualmente suporta apenas URLs no formato `https://www.youtube.com/watch?v=ID`
- Se você quiser suportar outros formatos de URL do YouTube (como URLs encurtadas), precisará ajustar a expressão regular
- Os parâmetros do iframe (largura, altura, etc.) estão definidos com valores padrão e podem ser personalizados no código conforme necessário

## Solução de Problemas

Se o plugin não funcionar como esperado:

1. Verifique se ele está listado em `mkdocs --help` na seção de plugins disponíveis
2. Verifique se o plugin está sendo carregado executando `mkdocs serve` com a opção `-v` para saída detalhada
3. Confirme se a sintaxe do markdown está correta (incluindo o protocolo `https://`)
4. Verifique a indentação no arquivo `mkdocs.yml` para garantir que a seção `plugins` esteja no nível correto
