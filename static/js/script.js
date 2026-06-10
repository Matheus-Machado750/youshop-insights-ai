const formulario = document.querySelector(".form_insights");
const botao = document.querySelector(".botao_gerar_insights");

if (formulario && botao) {
    formulario.addEventListener("submit", () => {
        botao.textContent = "Gerando...";
        botao.disabled = true;
    });
};