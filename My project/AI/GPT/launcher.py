import os
import ctypes
import sys
from core.dpi_bypass import start_bypass, stop_bypass
from core.dns_patch import set_dns, restore_dns


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    print("\n=== GPTUnblocker: Обход блокировки ChatGPT в РФ ===")

    if not is_admin():
        print("[!] Пожалуйста, запустите скрипт от имени администратора.")
        sys.exit(1)

    try:
        set_dns()
        start_bypass()

        print("[*] Обход включён. Можете пользоваться ChatGPT.\n[*] Нажмите Enter для отключения и восстановления DNS...")
        input()

    finally:
        stop_bypass()
        restore_dns()
        print("[*] Обход отключён. DNS восстановлен. До связи!")


if __name__ == "__main__":
    main()
