import subprocess
import datetime
from tqdm import tqdm


def print_logo():
    logo = """
███╗   ███╗██╗██╗     ██╗  ██╗    ██╗    ██╗██╗███████╗    ██╗  ██╗███████╗██╗   ██╗
████╗ ████║██║██║     ██║ ██╔╝    ██║    ██║██║██╔════╝    ██║ ██╔╝██╔════╝╚██╗ ██╔╝
██╔████╔██║██║██║     █████╔╝     ██║ █╗ ██║██║█████╗      █████╔╝ █████╗   ╚████╔╝
██║╚██╔╝██║██║██║     ██╔═██╗     ██║███╗██║██║██╔══╝      ██╔═██╗ ██╔══╝    ╚██╔╝
██║ ╚═╝ ██║██║███████╗██║  ██╗    ╚███╔███╔╝██║██║         ██║  ██╗███████╗   ██║
╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝╚═╝         ╚═╝  ╚═╝╚══════╝   ╚═╝

 ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
====================================================================================
  WIF KEY GENERATOR V.O1 use ./bx - libbitcoin


  Ten skrypt generuje klucze WIF (Wallet Import Format) dla Bitcoinów,
  wykorzystując określony zakres dat i czasów, od północy 2 maja 2009 do 23:59 tego samego dnia.
  Używa narzędzia bx oraz symulacji czasu za pomocą faketime,
  iterując przez każdą sekundę określonego zakresu,
  z wynikami zapisywanymi do pliku keyWIF.txt .

  usage: python3 MILKWIFGEN.py

====================================================================================
    """
    print(logo)

if __name__ == '__main__':
    print_logo()



# Funkcja do wykonywania komendy z ustawionym środowiskiem czasowym
def generate_wif_key(date, hour, minute, second):
    # Ustawienie zmiennych środowiskowych
    env = {
        "LD_PRELOAD": "/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1",
        "FAKETIME": f"{date} {hour:02d}:{minute:02d}:{second:02d}",
        "FAKETIME_FMT": "%Y-%m-%d %H:%M:%S"
    }

    # Polecenie generujące klucz WIF
    command = "./bx seed | ./bx ec-new | ./bx ec-to-wif"

    # Wykonanie polecenia
    result = subprocess.run(command, shell=True, capture_output=True, env=env, text=True)

    # Zwrócenie wyniku
    return result.stdout.strip()

# Ustawienie startowej i końcowej daty oraz czasu
start_date_time = datetime.datetime(2009, 5, 1, 0, 0, 0)
end_date_time = datetime.datetime(2009, 5, 1, 1, 1, 56)

# Otwarcie pliku do zapisu wyników
with open('keyWIF.txt', 'w') as file:
    # Obliczenie całkowitej liczby iteracji dla paska postępu
    total_seconds = int((end_date_time - start_date_time).total_seconds())

    with tqdm(total=total_seconds, desc="Generating WIF keys") as pbar:
        current_time = start_date_time
        while current_time <= end_date_time:
            # Wygenerowanie klucza WIF dla danej daty i czasu
            wif_key = generate_wif_key(current_time.date(), current_time.hour, current_time.minute, current_time.second)
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            # Zapis do pliku
            file.write(f"{wif_key}\n")
            # Aktualizacja paska postępu z informacją o dacie i czasie
            pbar.set_description(f"Generating WIF keys for {timestamp}")
            pbar.refresh()  # to update the description on the bar
            pbar.update(1)
            # Przejście do następnej sekundy
            current_time += datetime.timedelta(seconds=1)

print("WIF keys generated and saved to keyWIF.txt.")
