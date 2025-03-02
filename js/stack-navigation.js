// Implementação de navegação em pilha para MkDocs
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
