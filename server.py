from flask import Flask, request, send_file, render_template_string
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Isso permite que o frontend se comunique com o servidor

# CSS como string
CSS = '''
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f0f2f5;
}

.tela {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    max-width: 500px;
    width: 100%;
    text-align: center;
}

h1 {
    color: #1a73e8;
    margin-bottom: 20px;
}

select, button {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

button {
    background-color: #1a73e8;
    color: white;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #1557b0;
}

.botoes {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

.botoes button {
    flex: 1;
}

#descricaoCaso {
    font-size: 16px;
    line-height: 1.6;
    margin: 20px 0;
    text-align: left;
}

#descricaoCaso strong {
    color: #1a73e8;
    display: block;
    margin-bottom: 15px;
    font-size: 20px;
}

#descricaoCaso br + br {
    margin-bottom: 15px;
}

.disclaimer-content {
    text-align: left;
    margin: 20px 0;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 5px;
}

.disclaimer-content h3 {
    color: #1a73e8;
    margin-top: 20px;
    margin-bottom: 15px;
    font-size: 18px;
}

.disclaimer-content p {
    margin: 15px 0;
    line-height: 1.6;
    font-size: 16px;
}

.disclaimer-content ol {
    margin: 15px 0;
    padding-left: 25px;
    list-style-type: decimal;
}

.disclaimer-content ol li {
    margin: 10px 0;
    line-height: 1.5;
    font-size: 15px;
}

.disclaimer-content strong {
    color: #202124;
}

.disclaimer-content li strong + span {
    color: #5f6368;
    font-size: 14px;
    margin-left: 5px;
}

.caso-sumario {
    color: #1a73e8;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    border-left: 4px solid #1a73e8;
}

.caso-steps {
    background-color: white;
    padding: 15px;
    border-radius: 5px;
}

.caso-steps-titulo {
    color: #202124;
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 16px;
}

.caso-steps-lista {
    margin: 0;
    padding-left: 20px;
}

.caso-steps-lista li {
    margin-bottom: 8px;
    line-height: 1.5;
}

h2 {
    color: #202124;
    margin-bottom: 25px;
    font-size: 24px;
}

.classificacao-container {
    margin-top: 30px;
}

.classificacao-grupo {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.classificacao-grupo h3 {
    color: #202124;
    font-size: 16px;
    margin-bottom: 15px;
    text-align: center;
}

.classificacao-grupo .botoes {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.classificacao-grupo .botoes button {
    flex: 1;
    padding: 10px;
    font-size: 14px;
}

.classificacao-grupo .botoes button:first-child {
    background-color: #34A853;
}

.classificacao-grupo .botoes button:first-child:hover {
    background-color: #2d8e47;
}

.classificacao-grupo .botoes button:last-child {
    background-color: #EA4335;
}

.classificacao-grupo .botoes button:last-child:hover {
    background-color: #d33828;
}
'''

# JavaScript como string
JAVASCRIPT = '''
// Casos de teste por usuário
const casosPorUsuario = {
    Tiago: [
        {
            summary: "Check permission manager under Privacy settings",
            steps: "1. Go to \"Security & Privacy\" on Settings\\n2. Go to \"Permission manager\"\\n3. Tap on one permission\\n4. Tap on one app under permission selected\\n5. Tap on allow/deny options\\n6. Verify all app permission"
        },
        // ... outros casos ...
    ],
    // ... outros usuários ...
};

let respostas = {
    nome: '',
    classificacoes: []
};

let casoAtual = 0;
let casos = [];
let classificacaoAtual = {
    individual: null,
    conjunto: null
};

function iniciarTeste() {
    const nome = document.getElementById('selecionarNome').value;
    if (!nome) {
        alert('Por favor, selecione um nome');
        return;
    }
    
    respostas.nome = nome;
    casos = casosPorUsuario[nome];
    
    if (!casos || casos.length === 0) {
        alert('Erro: Casos não encontrados para este usuário.');
        return;
    }
    
    document.getElementById('telaSelecaoNome').style.display = 'none';
    document.getElementById('telaDisclaimer').style.display = 'block';
}

function mostrarExplicacao() {
    document.getElementById('telaDisclaimer').style.display = 'none';
    document.getElementById('telaExplicacao').style.display = 'block';
    
    const numeroCasos = casos.length;
    document.getElementById('numeroCasos').textContent = 
        `São ${numeroCasos} casos no total. Escolha com atenção!`;
}

function iniciarCasos() {
    document.getElementById('telaExplicacao').style.display = 'none';
    document.getElementById('telaCasos').style.display = 'block';
    document.getElementById('totalCasos').textContent = casos.length;
    mostrarCasoAtual();
}

function mostrarCasoAtual() {
    document.getElementById('numeroCaso').textContent = casoAtual + 1;
    const caso = casos[casoAtual];
    
    const passos = caso.steps.split('\\n').map(passo => {
        const passoSemNumero = passo.replace(/^\\d+\\.\\s*/, '');
        return `<li>${passoSemNumero}</li>`;
    }).join('');
    
    document.getElementById('descricaoCaso').innerHTML = `
        <div class="caso-sumario">${caso.summary}</div>
        <div class="caso-steps">
            <div class="caso-steps-titulo">Passos:</div>
            <ol class="caso-steps-lista">
                ${passos}
            </ol>
        </div>
    `;
}

function responderIndividual(valor) {
    classificacaoAtual.individual = valor;
    verificarEAvancar();
}

function responderConjunto(valor) {
    classificacaoAtual.conjunto = valor;
    verificarEAvancar();
}

function verificarEAvancar() {
    if (classificacaoAtual.individual !== null && classificacaoAtual.conjunto !== null) {
        respostas.classificacoes.push({
            caso: casoAtual + 1,
            descricao: casos[casoAtual].summary,
            passos: casos[casoAtual].steps,
            classificacao_individual: classificacaoAtual.individual ? 'Sim' : 'Não',
            classificacao_conjunto: classificacaoAtual.conjunto ? 'Sim' : 'Não'
        });

        casoAtual++;
        classificacaoAtual = { individual: null, conjunto: null };

        if (casoAtual < casos.length) {
            mostrarCasoAtual();
        } else {
            finalizarTeste();
        }
    }
}

function finalizarTeste() {
    document.getElementById('telaCasos').style.display = 'none';
    
    const resultadosJSON = JSON.stringify(respostas, null, 2);
    const blob = new Blob([resultadosJSON], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `resultados_${respostas.nome}.json`;
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    alert('Teste finalizado! Os resultados foram baixados automaticamente.');
    
    location.reload();
}
'''

# HTML template com CSS e JavaScript incorporados
HTML_TEMPLATE = f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste de Casos</title>
    <style>
        {CSS}
    </style>
</head>
<body>
    <!-- Tela de Seleção de Nome -->
    <div id="telaSelecaoNome" class="tela">
        <h1>Selecione seu Nome</h1>
        <select id="selecionarNome">
            <option value="">Escolha seu nome</option>
            <option value="Tiago">Thiago</option>
            <option value="Alexandre">Alexandre</option>
            <option value="Rebeca">Rebeca</option>
            <option value="Marcos">Marcos</option>
            <option value="Igor">Igor</option>
            <option value="Vinicius">Vinicius</option>
            <option value="Ronaldo">Ronaldo</option>
            <option value="Andres">Andres</option>
            <option value="Maikon">Maikon</option>
            <option value="Giulia">Giulia</option>
            <option value="Gabriel">Gabriel</option>
            <option value="Andre">Andre</option>
            <option value="Eulanda">Eulanda</option>
            <option value="Yan">Yan</option>
        </select>
        <button onclick="iniciarTeste()">Iniciar</button>
    </div>

    <!-- Tela de Disclaimer -->
    <div id="telaDisclaimer" class="tela" style="display: none;">
        <h1>Importante: Entenda o Conceito</h1>
        <div class="disclaimer-content">
            <p>Um caso de teste com fluxo lógico entre passos deve garantir que cada ação ou verificação no teste tenha uma relação direta e sequencial com a anterior, ou seja, o resultado de um passo deve influenciar ou condicionar o próximo.</p>
            
            <h3>Exemplo com fluxo lógico correto:</h3>
            <ol>
                <li><strong>Inserir nome de usuário</strong> (passo inicial)</li>
                <li><strong>Inserir senha</strong> (passo dependente da inserção do nome de usuário)</li>
                <li><strong>Clicar em "Entrar"</strong> (passo que depende das entradas anteriores)</li>
                <li><strong>Verificar se a página de início foi carregada</strong> (passo que depende do clique anterior)</li>
            </ol>

            <h3>Exemplo sem fluxo lógico:</h3>
            <ol>
                <li><strong>Inserir nome de usuário</strong></li>
                <li><strong>Verificar a cor da página inicial</strong> (não faz sentido antes de tentar login)</li>
                <li><strong>Clicar em "Entrar"</strong></li>
                <li><strong>Inserir senha</strong> (a senha deveria ser inserida antes do clique)</li>
            </ol>

            <p>No segundo exemplo, a ordem dos passos não segue uma sequência lógica que permitiria a execução bem-sucedida do teste.</p>
        </div>
        <button onclick="mostrarExplicacao()">Entendi, Continuar</button>
    </div>

    <!-- Tela de Explicação -->
    <div id="telaExplicacao" class="tela" style="display: none;">
        <h1>Bem-vindo ao Teste</h1>
        <p>Neste teste, você vai analisar diferentes casos e classificá-los como lógicos ou não lógicos.</p>
        <p id="numeroCasos"></p>
        <button onclick="iniciarCasos()">Continuar</button>
    </div>

    <!-- Tela de Casos -->
    <div id="telaCasos" class="tela" style="display: none;">
        <h2>Caso <span id="numeroCaso">1</span>/<span id="totalCasos"></span></h2>
        <p id="descricaoCaso"></p>
        
        <div class="classificacao-container">
            <div class="classificacao-grupo">
                <h3>Os passos fazem sentido individualmente?</h3>
                <div class="botoes">
                    <button onclick="responderIndividual(true)">Sim</button>
                    <button onclick="responderIndividual(false)">Não</button>
                </div>
            </div>
            
            <div class="classificacao-grupo">
                <h3>Os passos fazem sentido em conjunto?</h3>
                <div class="botoes">
                    <button onclick="responderConjunto(true)">Sim</button>
                    <button onclick="responderConjunto(false)">Não</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        {JAVASCRIPT}
    </script>
</body>
</html>
'''

# Garantir que o diretório de resultados existe
RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/salvar_resultado', methods=['POST'])
def salvar_resultado():
    dados = request.json
    
    # Criar nome do arquivo com timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = os.path.join(RESULTS_DIR, f"resultado_{dados['nome']}_{timestamp}.json")
    
    # Salvar resultados em um arquivo
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    return "Resultados salvos com sucesso!"

@app.route('/resultados')
def ver_resultados():
    # Lista todos os arquivos de resultado
    resultados = []
    for arquivo in os.listdir(RESULTS_DIR):
        if arquivo.endswith('.json'):
            with open(os.path.join(RESULTS_DIR, arquivo), 'r', encoding='utf-8') as f:
                resultados.append(json.load(f))
    
    # Ordenar resultados por data (mais recentes primeiro)
    resultados.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    # Criar uma tabela HTML com os resultados
    html = '''
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #1a73e8; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .respostas { max-width: 400px; }
        .classificacao { font-weight: bold; }
        .sim { color: #34A853; }
        .nao { color: #EA4335; }
    </style>
    <h1>Resultados dos Testes</h1>
    <table>
        <tr>
            <th>Nome</th>
            <th>Data/Hora</th>
            <th>Respostas</th>
        </tr>
    '''
    
    for r in resultados:
        respostas_html = '<br>'.join([
            f"Caso {c['caso']}:<br>"
            f"Individual: <span class='classificacao {"sim" if c["classificacao_individual"] == "Sim" else "nao"}'>"
            f"{c['classificacao_individual']}</span><br>"
            f"Conjunto: <span class='classificacao {"sim" if c["classificacao_conjunto"] == "Sim" else "nao"}'>"
            f"{c['classificacao_conjunto']}</span>"
            for c in r['classificacoes']
        ])
        
        html += f'''
        <tr>
            <td>{r['nome']}</td>
            <td>{r.get('timestamp', 'N/A')}</td>
            <td class="respostas">{respostas_html}</td>
        </tr>
        '''
    
    html += '</table>'
    return html

if __name__ == '__main__':
    app.run(debug=True)

application = app 