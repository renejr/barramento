$(document).ready(function() {
    // Dados para o gráfico (declaradas apenas UMA VEZ)
    var graphData = {
        labels: [], 
        rrValues: [] 
    };

    // Máximo de pontos no gráfico (declarada apenas UMA VEZ)
    const maxDataPoints = 50;

    // Criação do gráfico Chart.js (APENAS UMA VEZ)
    // console.log(' graphData.rrValues = '+graphData.rrValues);

    var ctx = document.getElementById('graph-rr').getContext('2d');
    var myChart = new Chart(ctx, { // Agora 'Chart' deve ser encontrado
        type: 'line',
        data: {
            labels: graphData.labels, // Usa a variável global
            datasets: [{
                label: 'Frequência Respiratória',
                data: graphData.rrValues, // Usa a variável global
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            elements: {
                line: {
                    tension: 1, // Ajuste o valor para controlar a curvatura (0 = sem curva, 1 = curva máxima)
                    backgroundColor: 'rgba(54, 162, 235, 0.2)', // Cor de fundo (opcional)
                    borderColor: 'rgba(54, 162, 235, 1)', // Cor da linha (azul)
                    borderWidth: 2
                }
            },
        }
    });
    
    // Função para atualizar o gráfico com novos dados
    function updateChart(chart, newData) {
        // console.log(' updateChart() newData = '+newData);
        chart.data.labels.push(newData.label); 
        chart.data.datasets[0].data.push(newData.value); 

        // Usa a constante global maxDataPoints
        if (chart.data.labels.length > maxDataPoints) { 
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        chart.update(); 
    }

    function updateData() {
        $.ajax({
            url: "ventilador.php",
            dataType: "json",
            success: function(data) {
                // ... (atualiza os elementos de texto) ...
                $("#device").html(data.device);

            // Itere sobre as propriedades do objeto 'data'
            for (let chave in data) {
                console.log(chave + ": " + data[chave]);
                console.log(typeof data[chave]);
            }

            // ... dentro da função success do AJAX ...
                // Atualiza o gráfico apenas se o valor for um número válido
                updateChart(myChart, {
                    label: new Date().toLocaleTimeString(), 
                    value: data.respiratory_rate
                });
            },
            error: function() {
                console.error("Erro ao buscar dados do ventilador.");
            }
        });
    }

    // ... (lógica para os botões) ...

    // Atualiza os dados a cada segundo
    setInterval(updateData, 1000); 
});