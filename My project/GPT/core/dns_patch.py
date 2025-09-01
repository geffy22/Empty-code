import subprocess

# Резервный DNS (Google и Cloudflare)
NEW_DNS = ["8.8.8.8", "1.1.1.1"]
INTERFACE = "Wi-Fi"  ## Измени на свой, если нужно (Ethernet и т.д.)

def set_dns():
    try:
        for dns in NEW_DNS:
            subprocess.run(
                ["netsh", "interface", "ip", "add", "dns", INTERFACE, dns],
                capture_output=True, text=True
            )
        print(f"[+] DNS изменён на {', '.join(NEW_DNS)}")
    except Exception as e:
        print(f"[!] Ошибка при установке DNS: {e}")

def restore_dns():
    try:
        subprocess.run(
            ["netsh", "interface", "ip", "set", "dns", INTERFACE, "dhcp"],
            capture_output=True, text=True
        )
        print("[*] DNS восстановлен (DHCP)")
    except Exception as e:
        print(f"[!] Ошибка при восстановлении DNS: {e}")
