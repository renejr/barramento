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
        $data = unpack("a2device/fRR/fVC/fPIns/ffio2/a*resto", $msg);

        // Manipula os dados recebidos
        $device = trim($data['device']); // Remove espaços extras
        $respiratoryRate = $data['RR'];
        $tidalVolume = $data['VC'];
        $inspiratoryPressure = $data['PIns'];
        $fio2 = $data['fio2'];

        // Imprime os dados decodificados (apenas para debug)
        echo "Device: $device\n";
        echo "Frequência Respiratória: $respiratoryRate\n";
        echo "Volume Corrente: $tidalVolume\n";
        echo "Pressão Inspiratória: $inspiratoryPressure\n";
        echo "FiO2: $fio2\n";

        // TODO: Implemente a lógica para armazenar os dados (ex: banco de dados, arquivo, etc.)


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
