import subprocess
import time
import os
import requests
import threading
import signal

def list_vpn_configs(folder):
    return [f for f in os.listdir(folder) if f.endswith('.conf') or f.endswith('.ovpn')]

def choose_config(configs, label):
    print(f"\n🔘 Обери {label} VPN-файл:")
    for idx, name in enumerate(configs, 1):
        print(f"{idx}. {name}")
    while True:
        try:
            choice = int(input("👉 Введи номер: ")) - 1
            if 0 <= choice < len(configs):
                return configs[choice]
        except ValueError:
            pass
        print("❌ Невірний вибір. Спробуй ще раз.")

def ask_logging():
    print("\n📝 Хочеш логувати трафік VPN?")
    print("[1] Так, зберігати лог-файли")
    print("[2] Ні, не логувати")
    while True:
        choice = input("👉 Введи варіант (1 або 2): ").strip()
        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("❌ Невірний вибір. Спробуй ще раз.")

def show_ip(label=""):
    try:
        ip = requests.get('https://api.ipify.org').text
        prefix = f"🌐 IP {label}:" if label else "🌐 Поточна IP:"
        print(f"{prefix} {ip}")
    except:
        print("⚠️ Неможливо отримати IP-адресу")

def start_vpn(config_path, log_path):
    return subprocess.Popen(
        ["sudo", "openvpn", "--config", config_path],
        stdout=open(log_path, "w"),
        stderr=subprocess.STDOUT
    )

def monitor_input(vpn1, vpn2):
    while True:
        cmd = input("\n🛑 Введи 'q' для завершення VPN: ").strip().lower()
        if cmd == 'q':
            print("⏹️ Завершення VPN-з'єднань...")
            for vpn, name in [(vpn2, "Другий"), (vpn1, "Перший")]:
                if vpn.poll() is None:
                    vpn.terminate()
                    print(f"🔒 {name} VPN завершено")
            break

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vpn_folder = os.path.join(script_dir, "vpn_configs")
    configs = list_vpn_configs(vpn_folder)

    if len(configs) < 2:
        print("⚠️ У папці vpn_configs має бути щонайменше два VPN-файли (.conf або .ovpn)")
        return

    vpn1_file = choose_config(configs, "перший")
    vpn2_file = choose_config(configs, "другий")
    log_enabled = ask_logging()

    log1_path = os.path.join(script_dir, "vpn1.log") if log_enabled else os.devnull
    log2_path = os.path.join(script_dir, "vpn2.log") if log_enabled else os.devnull

    show_ip("до VPN")

    print(f"\n🚀 Підключення до першого VPN: {vpn1_file}")
    vpn1 = start_vpn(os.path.join(vpn_folder, vpn1_file), log1_path)
    time.sleep(10)
    show_ip("після першого VPN")

    print(f"\n🔁 Підключення до другого VPN: {vpn2_file}")
    vpn2 = start_vpn(os.path.join(vpn_folder, vpn2_file), log2_path)
    time.sleep(10)
    show_ip("після другого VPN")

    threading.Thread(target=monitor_input, args=(vpn1, vpn2), daemon=True).start()

    vpn1.wait()
    vpn2.wait()
    print("\n📴 Обидва VPN завершені")

    show_ip("після завершення VPN")

    if log_enabled:
        print("\n📁 Логи збережені:")
        print(f" ▸ vpn1.log")
        print(f" ▸ vpn2.log")

if __name__ == "__main__":
    main()