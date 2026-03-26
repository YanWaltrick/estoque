# Acesso ao Sistema de Estoque pela Rede

## Como Iniciar o Servidor

```bash
python app.py
```

O servidor será iniciado e ficará disponível para acesso na rede.

## Acessando de Outra Máquina na Rede

### Obter o IP da Máquina Servidor

Execute no terminal do servidor:
```bash
ipconfig
```

Procure por "IPv4 Address" em suas conexões de rede ativas (geralmente está em Ethernet ou WiFi).
Exemplo: `192.168.x.x` ou `10.0.0.x`

### Acessar o Sistema

Na máquina cliente, abra um navegador e acesse:

```
http://seu-ip-do-servidor:5000
```

**Exemplo:**
```
http://192.168.1.100:5000
```

## Dados de Login

- **Usuário:** admin
- **Senha:** admin

⚠️ **Importante:** Altere a senha padrão após o primeiro acesso!

## Requisitos na Máquina Cliente

- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Conexão ativa na mesma rede que o servidor
- Porta 5000 liberada no firewall (se necessário)

## Resolução de Problemas

### Não consigo acessar o servidor

1. Verifique se o servidor está rodando no terminal
2. Confirme o IP correto com `ipconfig`
3. Teste a conectividade com ping: `ping seu-ip-do-servidor`
4. Verifique se a porta 5000 não está bloqueada pelo firewall

### Versão para Produção

No arquivo `app.py`, na última linha (line 508), altere para:

```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

Isso desativa o modo debug, mais seguro para produção.
