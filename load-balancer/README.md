# Load Balancer (Python / Sockets)

Implementacao simples de um load balancer TCP (round-robin) que repassa mensagens de clientes para 1..N backends.

**Formato da mensagem**

Os servidores esperam receber strings no formato:

```text
endpoint;payload
```

Exemplo:

```text
/hello;ola mundo
```

## Requisitos

- Python 3

## Estrutura

- `server-backend.py`: servidor backend TCP (recebe e imprime as mensagens).
- `server-lb.py`: load balancer TCP (aceita conexoes de clientes e repassa para os backends).
- `client.py`: cliente interativo (le do stdin e envia para o LB).
- `Data.py`: parser do formato `endpoint;payload`.
- `config-backend.mj` / `config-backend2.mj`: configs (JSON) dos backends.
- `config-lb.mj`: config (JSON) do load balancer (porta + lista de backends).

## Como subir (ordem correta)

Abra terminais separados.

### 1) Suba o(s) backend(s)

Terminal 1:

```bash
python3 server-backend.py --conf config-backend.mj
```

Opcional (segundo backend), Terminal 2:

```bash
python3 server-backend.py --conf config-backend2.mj
```

### 2) Ajuste o config do LB (se tiver mais de 1 backend)

O `config-lb.mj` define a porta do LB e para quais backends ele vai conectar. Para 2 backends (8085 e 8086), deixe assim:

```json
{
  "server": { "port": 8084, "max_connections": 10 },
  "backends": [
    { "port": 8085, "ip": "127.0.0.1" },
    { "port": 8086, "ip": "127.0.0.1" }
  ]
}
```

### 3) Suba o load balancer

Terminal 3:

```bash
python3 server-lb.py --conf config-lb.mj
```

### 4) Rode o cliente e envie mensagens

Terminal 4:

```bash
python3 client.py
```

Digite mensagens no formato `endpoint;payload` (uma por linha). Exemplo:

```text
/ping;1
/ping;2
/users;listar
```

Com mais de um backend configurado no `config-lb.mj`, o LB deve alternar (round-robin) o backend destino a cada mensagem recebida.

## Portas (padrao)

- LB: `8084` (ver `config-lb.mj`)
- Backends: `8085` e `8086` (ver `config-backend.mj` / `config-backend2.mj`)

