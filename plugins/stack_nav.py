import os
import mkdocs.plugins
from mkdocs.config import config_options
import mkdocs.structure.files
import shutil


class StackNavigationPlugin(mkdocs.plugins.BasePlugin):
    config_scheme = (("enable", config_options.Type(bool, default=True)),)

    def on_config(self, config):
        # Armazenar as páginas definidas no menu de navegação
        self.nav_pages = self._extract_nav_pages(config.get("nav", []))

        # Adicionar script ao extra_javascript
        if not hasattr(config, "extra_javascript"):
            config["extra_javascript"] = []

        # Caminho relativo ao site publicado
        config["extra_javascript"].append("js/stack-navigation.js")
        return config

    def _extract_nav_pages(self, nav_items):
        """Extrai todas as páginas definidas no menu de navegação"""
        pages = []
        for item in nav_items:
            if isinstance(item, dict):
                for _, value in item.items():
                    if isinstance(value, str):
                        pages.append(value)
                    elif isinstance(value, list):
                        pages.extend(self._extract_nav_pages(value))
            elif isinstance(item, str):
                pages.append(item)
        return pages

    def on_page_context(self, context, page, config, nav):
        """Adiciona informação se a página está no menu de navegação"""
        # Verifica se a página atual está no menu de navegação
        is_in_nav = page.file.src_path in self.nav_pages

        # Adiciona essa informação ao contexto para o template
        context["is_in_nav_menu"] = is_in_nav
        return context

    def on_post_build(self, config):
        # Criar diretório js no site final se não existir
        js_dir = os.path.join(config["site_dir"], "js")
        if not os.path.exists(js_dir):
            os.makedirs(js_dir)

        # Copiar o arquivo JavaScript do diretório docsmd/js para o diretório de build
        source_js_path = os.path.join(config["docs_dir"], "js", "stack-navigation.js")

        # Se o arquivo não existir, criá-lo
        if not os.path.exists(source_js_path):
            # Certificar que o diretório js existe
            source_js_dir = os.path.dirname(source_js_path)
            if not os.path.exists(source_js_dir):
                os.makedirs(source_js_dir)

            # Criar o arquivo stack-navigation.js com o conteúdo
            with open(source_js_path, "w") as f:
                f.write(self._get_js_content())

        # Copiar para o diretório de build
        shutil.copy2(source_js_path, os.path.join(js_dir, "stack-navigation.js"))

    def _get_js_content(self):
        """Retorna o conteúdo do arquivo JavaScript"""
        return """// Implementação de navegação em pilha para MkDocs
(function() {
    // Inicializa o histórico no armazenamento da sessão
    if (!sessionStorage.getItem('pageStack')) {
        sessionStorage.setItem('pageStack', JSON.stringify([]));
    }
    
    // Função para adicionar a página atual à pilha
    function addToStack(url) {
        const stack = JSON.parse(sessionStorage.getItem('pageStack'));
        
        // Verifica se a página já está no topo da pilha (evitar duplicatas)
        if (stack.length === 0 || stack[stack.length - 1] !== url) {
            stack.push(url);
            sessionStorage.setItem('pageStack', JSON.stringify(stack));
        }
    }
    
    // Função para obter a página anterior na pilha
    function getPreviousPage() {
        const stack = JSON.parse(sessionStorage.getItem('pageStack'));
        
        // Remove a página atual da pilha (que está no topo)
        if (stack.length > 0) {
            stack.pop();
            sessionStorage.setItem('pageStack', JSON.stringify(stack));
            
            // Retorna a nova página do topo (se houver)
            return stack.length > 0 ? stack[stack.length - 1] : null;
        }
        return null;
    }
    
    // Função para criar botão de navegação personalizado
    function createStackNavButton() {
        // Verifica se já existe um botão de navegação na página
        if (document.querySelector('.stack-nav-container')) {
            return; // Evita duplicação do botão
        }
        
        // Verifica se a página está no menu de navegação
        const isInNavMenu = document.body.getAttribute('data-is-in-nav') === 'true';
        
        // Só adiciona o botão para páginas que não estão no menu de navegação
        if (isInNavMenu) {
            return;
        }
        
        const stack = JSON.parse(sessionStorage.getItem('pageStack'));
        
        // Não mostrar o botão se não houver página anterior na pilha
        if (stack.length <= 1) {
            return;
        }
        
        // Cria o botão de "Voltar" na navegação
        const navContainer = document.createElement('div');
        navContainer.className = 'stack-nav-container';
        navContainer.style.margin = '20px 0';
        
        const prevLink = document.createElement('a');
        prevLink.className = 'nav-link';
        prevLink.href = '#';
        prevLink.style.display = 'inline-flex';
        prevLink.style.alignItems = 'center';
        prevLink.style.textDecoration = 'none';
        prevLink.style.color = 'var(--md-primary-fg-color, #2094f3)';
        
        const icon = document.createElement('i');
        icon.className = 'fa fa-arrow-left';
        icon.style.marginRight = '5px';
        
        const text = document.createTextNode('Voltar');
        
        prevLink.appendChild(icon);
        prevLink.appendChild(text);
        navContainer.appendChild(prevLink);
        
        // Adiciona o manipulador de eventos
        prevLink.addEventListener('click', function(e) {
            e.preventDefault();
            const prevPage = getPreviousPage();
            if (prevPage) {
                window.location.href = prevPage;
            }
        });
        
        // Adiciona o botão à página
        const content = document.querySelector('.md-content__inner, main, article');
        if (content) {
            content.insertBefore(navContainer, content.firstChild);
        }
    }
    
    // Processa os links internos para adicionar ao histórico da pilha
    function processInternalLinks() {
        // Encontra todos os links que não começam com http/https (links internos)
        const internalLinks = document.querySelectorAll('a:not([href^="http"]):not([href^="#"]):not([href^="mailto:"])');
        
        internalLinks.forEach(link => {
            // Armazena o URL original
            const originalUrl = link.getAttribute('href');
            
            // Adiciona um manipulador de eventos para salvar a página atual na pilha
            link.addEventListener('click', function(e) {
                // Adiciona a página de destino à pilha
                const destinationUrl = new URL(originalUrl, window.location.href).href;
                addToStack(destinationUrl);
            });
        });
    }
    
    // Função principal executada quando o DOM é carregado
    document.addEventListener('DOMContentLoaded', function() {
        // Registra a página atual na pilha ao carregar
        addToStack(window.location.href);
        
        // Processa os links internos
        processInternalLinks();
        
        // Cria botão de navegação se necessário
        createStackNavButton();
    });
})();
"""
