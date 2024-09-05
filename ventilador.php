<?php
// Define o caminho para o arquivo onde os dados do WebSocket serão armazenados
$dataFile = 'ventilador_data.json';

// Função para ler os dados do arquivo
function getVentiladorData() {
    global $dataFile;
    if (file_exists($dataFile)) {
        $data = json_decode(file_get_contents($dataFile), true);
        return $data;
    } else {
        return []; // Retorna um array vazio se o arquivo não existir
    }
}

// Obtém os dados do arquivo
$ventiladorData = getVentiladorData();

// Formata os dados para exibição
$formattedData = [
    "device" => isset($ventiladorData['device']) ? $ventiladorData['device'] : 'N/A',
    "respiratory_rate" => isset($ventiladorData['RR']) ? number_format($ventiladorData['RR'], 2) : 'N/A',
    "tidal_volume" => isset($ventiladorData['VC']) ? number_format($ventiladorData['VC'], 2) : 'N/A',
    "inspiratory_pressure" => isset($ventiladorData['PIns']) ? number_format($ventiladorData['PIns'], 2) : 'N/A',
    "fio2" => isset($ventiladorData['fio2']) ? number_format($ventiladorData['fio2'], 2) : 'N/A',
    //"alarms" => isset($ventiladorData['alarms']) ? $ventiladorData['alarms'] : 'N/A',
    // ... (formata os demais dados)
];


//(var_dump($formattedData));

// Retorna os dados em JSON
header('Content-Type: application/json');
echo json_encode($formattedData);
?>
