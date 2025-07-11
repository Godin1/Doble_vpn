# 🔐 Doble VPN

Програма на **Python 3**, яка дозволяє створити каскадне VPN-підключення за допомогою двох `.ovpn` файлів через OpenVPN. Підходить для підвищення приватності та обходу мережевих обмежень.

---

## ⚙️ Що потрібно для роботи

### 🧩 Залежності

- Python **3.6+**
- Встановлений OpenVPN  
  👉 `sudo apt install openvpn`
- Модуль `requests`  
  👉 Встановлення: `pip install requests`
- Папка `vpn_configs/` з `.ovpn` файлами  
  🔗 Джерело безкоштовних VPN: [vpngate.net](https://www.vpngate.net/en/)

---

## 🗂 Структура проєкту
/папка_з_проєктом/ │ 
- ├── doble_vpn.py     ← скрипт програми 
- ├── vpn_configs/     ← папка з VPN-файлами (.ovpn або .conf) 
- │ ├── first_vpn.ovpn 
- │ └── second_vpn.ovpn
---

## 🚀 Як користуватись програмою

1️⃣ **Запуск**
```bash
python3 doble_vpn.py
2️⃣ Вибір VPN-файлів
Програма виведе список файлів з vpn_configs/
Обери два VPN — один буде першим, другий накладатиметься поверх
3️⃣ Логування трафіку
Вибери: [1] Так або [2] Ні
Якщо увімкнено — створюються файли vpn1.log і vpn2.log
4️⃣ Перевірка IP-адреси
До підключення: показ поточної IP
Після кожного VPN: оновлена IP
5️⃣ Керування підключенням
Програма запускатиме OpenVPN по черзі для обраних файлів
Для завершення роботи — введи q у терміналі
6️⃣ Завершення
Після завершення VPN-з'єднання IP знову перевіряється
Логи зберігаються у папці де знаходится програма, створюються два файла .log для кожного VPN,
якщо обрано логування. 
✅ Результат
🔒 Працюєш через два VPN, які каскадно накладаються одне на одного. Це дає:
Додаткову анонімність
Краще шифрування трафіку
Обхід геоблоків та цензури
