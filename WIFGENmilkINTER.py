import subprocess
import datetime
import time

def print_logo():
    logo = """
====================================================================================
  WIF KEY GENERATOR V.02 INTERVAL use ./bx - libbitcoin

  Ten skrypt generuje klucze WIF (Wallet Import Format) dla Bitcoinów, p2wpkh-p2sh:
  wykorzystując określony zakres dat i czasów, od północy 2 maja 2009 do 23:59 tego samego dnia.
  Używa narzędzia bx oraz symulacji czasu za pomocą faketime,
  Dodano interwał czasowy.
====================================================================================
"""
    print(logo)

def parse_time_interval():
    time_units = {
        's': 1,
        'm': 60,
        'h': 3600
    }
    while True:
        interval_input = input("Podaj interwał czasowy (np. 10s, 5m, 1h): ")
        if interval_input.isdigit() and int(interval_input) == 0:
            return 1  # Co sekundę, jeśli podano 0
        unit = interval_input[-1]
        if unit in time_units and interval_input[:-1].isdigit():
            return int(interval_input[:-1]) * time_units[unit]
        print("Nieprawidłowy format. Użyj 's' dla sekund, 'm' dla minut, 'h' dla godzin.")

def generate_keys():
    start_time = datetime.datetime(2011, 1, 1, 0, 0, 0)
    end_time = datetime.datetime(2011, 1, 19, 23, 59, 59)
    interval = parse_time_interval()

    total_seconds = int((end_time - start_time).total_seconds())
    steps = total_seconds // interval + 1

    file = open('keyWIF.txt', 'w')
    current_time = start_time
    progress = 0

    print("Rozpoczynanie generacji kluczy:")
    while current_time <= end_time:
        faketime = current_time.strftime('%Y-%m-%d %H:%M:%S')
        command = f"faketime '{faketime}' ./bx seed | ./bx ec-new | ./bx ec-to-wif"
        try:
            wif_key = subprocess.check_output(command, shell=True).decode().strip()
            file.write(f"p2wpkh-p2sh:{wif_key}\n")
        except subprocess.CalledProcessError as e:
            print("Błąd podczas generowania klucza: ", e)

        # Aktualizacja paska postępu
        progress_percentage = (progress / steps) * 100
        progress_bar_length = int(50 * progress_percentage / 100)
        progress_bar = '#' * progress_bar_length + '-' * (50 - progress_bar_length)
        print(f"\r[{progress_bar}] {progress_percentage:.2f}%", end='', flush=True)

        current_time += datetime.timedelta(seconds=interval)
        progress += 1

    file.close()
    print("\nGenerowanie kluczy zakończone.")

if __name__ == "__main__":
    print_logo()
    generate_keys()
