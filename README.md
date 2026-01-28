> 🚧 **Work in Progress**
>
> Este repositório está em evolução contínua.
> Novos projetos, melhorias e refinamentos arquiteturais
> estão sendo adicionados progressivamente.


# Projetos Avançados de Engenharia de Software

Este repositório reúne uma **série de projetos avançados de desenvolvimento de software**, focados em desafios reais de nível **sênior e especialista**, indo além de aplicações CRUD tradicionais.

Os projetos exploram problemas comuns em ambientes de produção, com ênfase em **arquitetura, domínio, escalabilidade, consistência, resiliência e trade-offs técnicos**.

---

O objetivo deste repositório **não é ensinar frameworks**, mas sim simular cenários reais enfrentados por engenheiros experientes, como:

- Decisões arquiteturais e seus impactos
- Modelagem de domínio e separação de responsabilidades
- Sistemas distribuídos e processamento assíncrono
- Observabilidade, falhas e resiliência
- Manutenção e evolução de sistemas complexos

Cada projeto foi pensado para refletir problemas que surgem **além do CRUD**.


## 📁 Estrutura

Cada pasta representa um projeto independente

## Projetos

#### 1. Load Balancer e Reverse Proxy Customizado

Entender como o tráfego flui na rede é crucial para especialistas. Ao invés de usar Nginx, construa um balanceador simples.

O Desafio: Receber tráfego HTTP e distribuí-lo entre múltiplos servidores de backend baseados em métricas.

Funcionalidades Avançadas:
Algoritmos de Balanceamento: Implementar Round-Robin, Least Connections e IP Hash.
Health Checks Ativos: O load balancer deve "pingar" os backends e remover os inativos da rota automaticamente.
TLS Termination: Lidar com o handshake SSL/TLS no proxy antes de passar para o backend.

O que destaca: Networking (TCP/HTTP), concorrência massiva, segurança e monitoramento de sistemas.
