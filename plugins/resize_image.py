import re
from markdown.inlinepatterns import ImageInlineProcessor
from markdown.extensions import Extension
from xml.etree import ElementTree as etree
import mkdocs.plugins

# Expressão regular para detectar ![texto|tamanho](image.png)
RESIZED_IMAGE_RE = r"!\[(?P<alt>[^\]\|]*)(?:\|(?P<size>\d+%?))?\]\((?P<url>[^)]+)\)"


class ResizedImageProcessor(ImageInlineProcessor):
    def handleMatch(self, m, data):
        # Extrai o texto alternativo, URL da imagem e tamanho (se fornecido)
        alt_text = m.group("alt") or ""
        image_url = m.group("url")
        size = m.group("size")

        # Cria o elemento img
        img = etree.Element("img")
        img.set("src", image_url)
        img.set("alt", alt_text)

        # Aplica o tamanho se especificado
        if size:
            # Adiciona % se não estiver presente
            if not size.endswith("%"):
                size = f"{size}%"
            img.set("width", size)
            img.set("style", f"max-width: {size}; height: auto;")

        return img, m.start(0), m.end(0)


class ResizedImageExtension(Extension):
    def extendMarkdown(self, md):
        # Substitui o processador de imagem padrão
        md.inlinePatterns.register(
            ResizedImageProcessor(RESIZED_IMAGE_RE, md), "resized_image", 200
        )  # Prioridade mais alta que a padrão


class ResizedImagePlugin(mkdocs.plugins.BasePlugin):
    def on_config(self, config):
        # Adiciona a extensão à lista de extensões markdown
        config["markdown_extensions"].append(ResizedImageExtension())
        return config


# Função necessária para registro do plugin
def get_plugin_class():
    return ResizedImagePlugin
