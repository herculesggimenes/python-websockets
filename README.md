**Requisitos do Projeto**

- Servidor deve implementar dois serviços: Um que retorne números pares, e outro números ímpares;
- Cada cliente ao se conectar ao servidor deve iniciar um processo que incrementa o valor recebido do servidor em 1 a cada 500ms, enviando o novo valor ao servidor;
- Cada cliente deve, em um intervalo aleatório entre 3 e 5 segundos, requisitar ao servidor um número par ou ímpar, escolhido de forma aleatória, que será utilizado como novo valor de incremento, ao invés de 1;
- Os números devem estar sempre no range 0-99;
- Servidor deve enviar um valor ao aceitar conexão do cliente;
- Servidor deve manter o último valor enviado para cada cliente. Caso um mesmo cliente se conecte, enviar esse valor para o mesmo. Caso não haja valor registrado, enviar 0;
- Servidor deve manter um log de todas as mensagens trocadas;

**Inicialização**

1) Baixar as dependências do projeto:
```
pip install -r requirements.txt
```
2) Instanciar o Servidor
```
python3 debug_server.py ou python debug_server.py
```
3) Instanciar Clientes
```
python3 debug_client.py ou python debug_server.py
```

**Informações a respeito do Servidor**

- Tipo de Eventos
```
INCREMENT='increment'
VALUE='value'
ERROR='error'
HANDSHAKE='handshake'
SET_INITIAL_VALUE='set_initial_value'
CONNECTION_STARTED='connection_started'
CONNECTION_CLOSED='connection_closed'
```

- Modelo Mensagem do Cliente 
```
{
    'client_id': Id Único do Cliente,
    'type': Tipo de Evento,
    'value': mensagem,
}
```

- Modelo Mensagem do Servidor 
```
{
    'type': Tipo de Evento,
    'value': mensagem,
}
```

- Modelo de Evento de Log
```
Event: Tipo de Evento
Server Address: Ip do Servidor
Client Id: Id do Client
Message: Mensagem Enviada / Recebida
```
