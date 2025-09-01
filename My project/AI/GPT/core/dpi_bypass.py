import pydivert
import threading

bypass_thread = None
bypass_active = False

def _dpi_bypass_worker():
    global bypass_active
    with pydivert.WinDivert("outbound or inbound") as w:
        for packet in w:
            if not bypass_active:
                break
            try:
                # UDP 443 
                if packet.is_udp and packet.dst_port == 443:
                    continue 

                if packet.is_tcp and packet.tcp_rst:
                    continue 

                w.send(packet)
            except Exception:
                continue

def start_bypass():
    global bypass_thread, bypass_active
    if bypass_active:
        print("[*] DPI обход уже активен.")
        return
    bypass_active = True
    bypass_thread = threading.Thread(target=_dpi_bypass_worker, daemon=True)
    bypass_thread.start()
    print("[+] DPI обход запущен")

def stop_bypass():
    global bypass_active
    if not bypass_active:
        return
    bypass_active = False
    print("[-] DPI обход остановлен")
