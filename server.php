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
        echo sprintf('Conexão %d enviou mensagem: %s' . "\n", $from->resourceId, $msg);

        // Aqui você pode processar a mensagem recebida (JSON, XML, etc.)
        // Pode ser um dado de sinal vital, comando, alerta, etc.

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
