# barramentoSimulador de Equipamentos Médicos em Python
Este projeto consiste em um conjunto de scripts Python que simulam o comportamento de diversos equipamentos médicos, enviando dados de telemetria para um servidor WebSocket.

Objetivo:

Demonstrar a comunicação entre equipamentos médicos e um sistema central: Simular o envio de dados de telemetria de diferentes equipamentos para um servidor central, representando um sistema de monitoramento e controle.
Facilitar o desenvolvimento e teste de aplicações de saúde: Fornecer um ambiente de simulação para testar e desenvolver aplicações que interagem com dados de equipamentos médicos.
Estrutura do Projeto:

O projeto é organizado em vários arquivos Python, cada um representando um tipo de equipamento médico:

camaHospitalar.py: Simula uma cama hospitalar, enviando dados como inclinação, elevação da cabeça, peso do paciente e status de alarme.
bombaInfusora.py: Simula uma bomba infusora, enviando dados como taxa de infusão, volume total administrado e status da infusão.
estacaoTriagem.py: Simula uma estação de triagem, enviando dados como temperatura, pressão arterial, frequência cardíaca e prioridade do paciente.
equipamentosMedicosDiversos.py: Simula um equipamento médico genérico, enviando dados como status de operação, tempo de exposição, qualidade da imagem e código de alarme.
monitorMultiparametro.py: Simula um monitor multiparâmetro, enviando dados como frequência cardíaca, pressão arterial, saturação de oxigênio, temperatura corporal e frequência respiratória.
ventiladorMecanico.py: Simula um ventilador mecânico, enviando dados como frequência respiratória e volume corrente.
dash.py: Um script Flask que recebe dados do servidor WebSocket e os exibe em um dashboard HTML.
Como Executar:

Instale as dependências:

pip install websockets flask-socketio
Execute o servidor WebSocket:

Opção 1: Utilizando um servidor WebSocket externo: Configure um servidor WebSocket (como o Socket.IO) e ajuste o endereço uri nos scripts Python para apontar para o servidor.
Opção 2: Utilizando um servidor WebSocket simples em Python: Crie um servidor WebSocket simples em Python para receber os dados dos simuladores.
Execute os scripts Python:

Execute cada script Python individualmente para simular o comportamento de um equipamento médico.
Os dados serão enviados para o servidor WebSocket configurado.
Execute o dashboard:

Execute o script dash.py para iniciar o servidor Flask e exibir o dashboard.
Acesse o endereço http://localhost:5000/ no navegador para visualizar o dashboard.
Observações:

Este projeto é um exemplo de simulação de equipamentos médicos e pode ser adaptado para outros cenários.
Os dados simulados são aleatórios e não representam dados reais de equipamentos médicos.
O projeto não inclui implementação de segurança ou autenticação.
Próximos Passos:

Implementar um servidor WebSocket mais robusto para receber os dados dos simuladores.
Adicionar mais tipos de equipamentos médicos ao projeto.
Implementar funcionalidades de análise e visualização de dados.
Integrar o projeto com outras plataformas de saúde.
Contribuições:

Contribuições para este projeto são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou entrar em contato com o autor.