document.addEventListener("DOMContentLoaded", function () {
	// Encontra todos os blocos de código
	const codeBlocks = document.querySelectorAll("pre");

	codeBlocks.forEach(function (codeBlock) {
		// Cria o botão de copiar
		const copyButton = document.createElement("button");
		copyButton.className = "copy-code-button";
		copyButton.type = "button";
		copyButton.innerHTML =
			'<svg class="copy-icon" viewBox="0 0 24 24" width="18" height="18"><path d="M16 1H4C2.9 1 2 1.9 2 3V17H4V3H16V1ZM19 5H8C6.9 5 6 5.9 6 7V21C6 22.1 6.9 23 8 23H19C20.1 23 21 22.1 21 21V7C21 5.9 20.1 5 19 5ZM19 21H8V7H19V21Z"></path></svg><svg class="check-icon" viewBox="0 0 24 24" width="18" height="18"><path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z"></path></svg>';

		// Adiciona o botão ao bloco de código
		codeBlock.style.position = "relative";
		codeBlock.appendChild(copyButton);

		// Adiciona o evento de clique
		copyButton.addEventListener("click", function () {
			const code = codeBlock.querySelector("code")
				? codeBlock.querySelector("code").innerText
				: codeBlock.innerText;

			navigator.clipboard
				.writeText(code)
				.then(function () {
					// Muda temporariamente para o ícone de confirmação
					copyButton.classList.add("copied");
					setTimeout(function () {
						console.log(
							"Timeout function executada - removendo 'copied' class"
						); // ADICIONE ESTA LINHA
						copyButton.classList.remove("copied");
					}, 2000);
					// setTimeout(function () {
					// 	copyButton.classList.remove("copied");
					// }, 2000);
				})
				.catch(function (error) {
					console.error("Erro ao copiar: ", error);
				});
		});
	});
});
