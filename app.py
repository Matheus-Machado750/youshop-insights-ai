from flask import Flask, render_template, request
import sqlite3
import os
from database import *
from insights_ai import *

app = Flask(__name__)
criar_tabela()

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/resultado/<int:id>")
def resultado_por_id(id):
    """
    Busca uma análise salva pelo ID e prepara sua exibição.

    Os dados básicos vem do banco, enquanto os insights são gerados novamente
    pela IA no momento em que o usuário acessa o item do histórico.
    """

    analise = buscar_por_id(id)

    if not analise:
        return "Análise não encontrada"
    
    analise_atual = preparar_analise(analise, usar_ia = True)

    historico = [
        preparar_analise(item)
        for item in buscar_todas()
    ]

    return render_template(
        "resultado.html",
        analise_atual=analise_atual,
        historico=historico
    )

@app.route("/resultado", methods=["GET", "POST"])
def resultado():
    """
    Controla a página de resultados.

    No POST, recebe os dados do formulário, salva os dados básicos do produto
    no banco e prepara a análise atual com métricas calculadas e insights da IA.
    No GET, carrega apenas o histórico de análises já cadastradas.
    """


    if request.method == "POST":

        produto = request.form["produto"]
        visitas = int(request.form["visitas"])
        vendas = int(request.form["vendas"])
        preco = float(request.form["preco"])
        origem = request.form["origem"]

        id_analise = salvar_analise(produto, visitas, vendas, preco, origem)

        metricas = gerar_metricas(visitas, vendas, preco)

        analise = buscar_por_id(id_analise)
        analise_atual = preparar_analise(analise, usar_ia=True)

        historico = [
            preparar_analise(item, usar_ia=False)
            for item in buscar_todas()
        ]

        return render_template(
            "resultado.html",
            analise_atual=analise_atual,
            historico=historico
        )
    
    historico = [
        preparar_analise(item)
        for item in buscar_todas()
    ]

    return render_template(
        "resultado.html",
        analise_atual = None,
        historico = historico
    )


if __name__ == "__main__":
    app.run(debug=True)