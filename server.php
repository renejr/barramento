<?php
require 'vendor/autoload.php';

use Ratchet\MessageComponentInterface;
use Ratchet\ConnectionInterface;

class MyWebSocketServer implements MessageComponentInterface {
    protected $clients;

    public function __construct() {
        $this->clients = new \SplObjectStorage;
    }

    public function onOpen(ConnectionInterface $conn) {
        // Armazena a nova conexão para que possamos enviar mensagens de volta para ela mais tarde
        $this->clients->attach($conn);
        echo "Nova conexão! ({$conn->resourceId})\n";
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        // Guarda a mensagem crua para debug, se necessário
        // echo sprintf('Conexão %d enviou mensagem: %s' . "\n", $from->resourceId, bin2hex($msg)); 

        // Decodifica a mensagem binária
        $data = unpack("a2device/fRR/fVC/fPIns/ffio2/a*alarms", $msg);

        // Manipula os dados recebidos
        $device = trim($data['device']); // Remove espaços extras
        $respiratoryRate = $data['RR'];
        $tidalVolume = $data['VC'];
        $inspiratoryPressure = $data['PIns'];
        $fio2 = $data['fio2'];
        $alarms = $data['alarms']; // Descomentado

        // Cria um array associativo com os dados
        $ventiladorData = [
            "device" => $device,
            "RR" => $respiratoryRate,
            "VC" => $tidalVolume,
            "PIns" => $inspiratoryPressure,
            "fio2" => $fio2,
            "alarms" => $alarms, // Descomentado
        ];

        //print_r($ventiladorData);
        //echo "\n";

        // Salva os dados no arquivo JSON
        $dataFile = 'ventilador_data.json';

        // Converte ventiladorData para JSON
        $ventiladorDataJson = json_encode($ventiladorData);

        // Verifica o diretório atual
        echo "Diretório atual: " . getcwd() . "\n";

        // Grava o JSON no arquivo
        $result = file_put_contents($dataFile, $ventiladorDataJson);

        if ($result !== false) {
            echo "Dados gravados com sucesso em $dataFile\n";
        } else {
            echo "Erro ao gravar os dados no arquivo $dataFile\n";
        }

        foreach ($this->clients as $client) {
            if ($from !== $client) {
                // Envia a mensagem recebida para todos os outros clientes conectados
                $client->send($msg);
            }
        }
    }

    public function onClose(ConnectionInterface $conn) {
        // Remove a conexão ao fechar
        $this->clients->detach($conn);
        echo "Conexão {$conn->resourceId} desconectada.\n";
    }

    public function onError(ConnectionInterface $conn, \Exception $e) {
        echo "Erro: {$e->getMessage()}\n";
        $conn->close();
    }
}

// Execução do servidor WebSocket
require 'vendor/autoload.php';

$server = \Ratchet\Server\IoServer::factory(
    new \Ratchet\Http\HttpServer(
        new \Ratchet\WebSocket\WsServer(
            new MyWebSocketServer()
        )
    ),
    8080
);
echo "Servidor WebSocket iniciado na porta 8080.\n";
$server->run();
