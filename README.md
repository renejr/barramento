Simulador de Equipamentos Médicos em Python com Dashboard Interativo
Este projeto simula o comportamento de diversos equipamentos médicos, enviando dados de telemetria em tempo real para um dashboard interativo, construído com Flask e Socket.IO.

Objetivo
O projeto visa:

Demonstrar a comunicação em tempo real: Simula o envio de dados de telemetria de diferentes equipamentos para um dashboard central, representando um sistema de monitoramento e controle em tempo real.
Auxiliar no desenvolvimento e teste de aplicações de saúde: Fornece um ambiente de simulação para testar e desenvolver aplicações que interagem com dados de equipamentos médicos em tempo real.
Visualizar dados de forma clara e intuitiva: Apresenta os dados simulados em um dashboard interativo, facilitando a análise e acompanhamento das informações.
Estrutura do Projeto
O projeto é composto por:

Simuladores de Equipamentos Médicos: Scripts Python que simulam o comportamento de diferentes equipamentos, enviando dados específicos via WebSocket:
camaHospitalar.py: Simula uma cama hospitalar.
bombaInfusora.py: Simula uma bomba infusora.
estacaoTriagem.py: Simula uma estação de triagem.
equipamentosMedicosDiversos.py: Simula um equipamento médico genérico.
monitorMultiparametro.py: Simula um monitor multiparâmetro.
ventiladorMecanico.py: Simula um ventilador mecânico.
Servidor WebSocket: Utiliza Flask-SocketIO para gerenciar a comunicação bidirecional em tempo real entre os simuladores e o dashboard.
Dashboard Interativo: Interface web construída com Flask que exibe os dados recebidos dos simuladores em tempo real, utilizando gráficos e elementos visuais para melhor acompanhamento.

Como Executar

Instalação de Dependências:
pip install websockets flask flask-socketio

Inicialização do Servidor WebSocket:
python app.py 

Execução dos Simuladores:

python camaHospitalar.py
python bombaInfusora.py
# ... outros simuladores
Acesso ao Dashboard: Abra um navegador web e acesse http://localhost:5000/ para visualizar o dashboard.

Próximos Passos
Implementar persistência de dados para análise histórica.
Adicionar mais tipos de equipamentos médicos e dados simulados.
Implementar funcionalidades de controle e interação com os simuladores a partir do dashboard.
Integrar com frameworks de front-end como React, Vue.js ou Angular para um dashboard mais dinâmico.
Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou entrar em contato com os autores.
