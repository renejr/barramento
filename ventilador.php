<?php
// Inclua a biblioteca para lidar com WebSocket (se necessário)

// Recebe a última mensagem do WebSocket (implemente a lógica de acordo com sua biblioteca)
$data = getLatestWebSocketData(); 

// Decodifica os dados binários (usando a mesma ordem do struct.pack em Python)
$device = unpack("a*", substr($data, 0, 2))[1]; // Lê 2 bytes como string
$respiratory_rate = unpack("f", substr($data, 2, 4))[1]; // Lê 4 bytes como float
// ... (decodifica os demais dados)

// Formata os dados para exibição
$formattedData = [
    "device" => $device,
    "respiratory_rate" => number_format($respiratory_rate, 2),
    // ... (formata os demais dados)
];

// Retorna os dados em JSON
header('Content-Type: application/json');
echo json_encode($formattedData);
?>
