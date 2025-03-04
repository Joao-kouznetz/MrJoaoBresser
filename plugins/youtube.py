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

        # Cria o elemento div para responsividade
        wrapper = etree.Element("div")
        wrapper.set("class", "youtube-container")

        # Cria o elemento iframe
        iframe = etree.SubElement(wrapper, "iframe")
        iframe.set("src", f"https://www.youtube.com/embed/{video_id}")
        iframe.set("title", "YouTube video player")
        iframe.set("frameborder", "0")
        iframe.set(
            "allow",
            "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
        )
        iframe.set("allowfullscreen", "allowfullscreen")
        iframe.set("loading", "lazy")

        return wrapper, m.start(0), m.end(0)


class YouTubeEmbedExtension(Extension):
    def extendMarkdown(self, md):
        pattern = YouTubeEmbedProcessor(YOUTUBE_RE, md)
        # Aumenta a prioridade para 210 para que seja processado antes do resize_image
        md.inlinePatterns.register(pattern, "youtube_embed", 210)


class YouTubePlugin(mkdocs.plugins.BasePlugin):
    def on_config(self, config):
        # Adicione a extensão à lista de extensões markdown
        config["markdown_extensions"].append(YouTubeEmbedExtension())
        return config


# Função necessária para registro do plugin
def get_plugin_class():
    return YouTubePlugin
