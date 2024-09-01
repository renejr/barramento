<?php
// Define o caminho para o arquivo onde os dados do WebSocket ser�o armazenados
$dataFile = 'ventilador_data.json';

// Fun��o para ler os dados do arquivo
function getVentiladorData() {
    global $dataFile;
    if (file_exists($dataFile)) {
        $data = json_decode(file_get_contents($dataFile), true);
        return $data;
    } else {
        return []; // Retorna um array vazio se o arquivo n�o existir
    }
}

// Obt�m os dados do arquivo
$ventiladorData = getVentiladorData();

// Formata os dados para exibi��o
$formattedData = [
    "device" => isset($ventiladorData['device']) ? $ventiladorData['device'] : 'N/A',
    "respiratory_rate" => isset($ventiladorData['RR']) ? number_format($ventiladorData['RR'], 2) : 'N/A',
    "tidal_volume" => isset($ventiladorData['VC']) ? number_format($ventiladorData['VC'], 2) : 'N/A',
    "inspiratory_pressure" => isset($ventiladorData['PIns']) ? number_format($ventiladorData['PIns'], 2) : 'N/A',
    "fio2" => isset($ventiladorData['fio2']) ? number_format($ventiladorData['fio2'], 2) : 'N/A'
    // ... (formata os demais dados)
];

// Retorna os dados em JSON
header('Content-Type: application/json');
echo json_encode($formattedData);
?>
