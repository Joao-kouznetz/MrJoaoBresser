from setuptools import setup, find_packages

setup(
    name="mkdocs-youtube-plugin",
    version="0.1.0",
    description="Plugin para embutir vídeos do YouTube em documentação MkDocs",
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "youtube = plugins.youtube:YouTubePlugin",
        ]
    },
)
