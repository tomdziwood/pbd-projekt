import random
import math


def tworz_instancje(wspolczynnik_obciazenia, nazwa_pliku_wyjsciowego):
    print("Generowanie pliku " + nazwa_pliku_wyjsciowego + "...")
    liczba_zadan = 10000

    # rozmiary zadan wygenerowane przy uzyciu rozkladu Erlanga
    # 95% zadan jest krotkich, a pozostale zadania to zadania dlugie
    rozmiary_zadan = []

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    czesc_krotkich_zadan = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    sredni_rozmiar_zadania = 1000

    # wspolczynnik wskazujacy ile razy wieksza ma byc srednia i odchylenie standardowe rozmiarow dlugich zadan od zadan krotkich
    w = 10

    # srednie czasy dla zadan krotkich i zadan dlugich
    sredni_rozmiar_zadania_krotkiego = sredni_rozmiar_zadania / (czesc_krotkich_zadan + w * (1 - czesc_krotkich_zadan))
    sredni_rozmiar_zadania_dlugiego = w * sredni_rozmiar_zadania_krotkiego

    # wspolczynnik ksztaltu alfa rozkladu Erlanga o wybranej wartosci, jednakowy dla krotkich i dlugich zadan
    # wybrana wartosc zapewnia rozdzielnosc miedzy rozkladem rozmiarow krotkich a dlugich zadan
    alpha = 8

    # wspolczynniki stosunku beta rozkladu Erlanga dostosowane wedlug wspolczynnika alpha i oczekiwanej sredniej
    beta_zadania_krotkiego = sredni_rozmiar_zadania_krotkiego / alpha
    beta_zadania_dlugiego = sredni_rozmiar_zadania_dlugiego / alpha

    for _ in range(liczba_zadan):
        if random.random() < czesc_krotkich_zadan:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha, beta=beta_zadania_krotkiego)))
        else:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha, beta=beta_zadania_dlugiego)))

    suma_rozmiarow_zadan = sum(rozmiary_zadan)
    max_czas_zakonczenia = math.ceil(suma_rozmiarow_zadan / wspolczynnik_obciazenia)

    momenty_gotowosci = []
    for i in range(liczba_zadan):
        while True:
            moment_gotowosci = random.randrange(max_czas_zakonczenia)
            if moment_gotowosci + rozmiary_zadan[i] <= max_czas_zakonczenia:
                momenty_gotowosci.append(moment_gotowosci)
                break

    zadania = []
    for i in range(liczba_zadan):
        zadania.append([momenty_gotowosci[i], rozmiary_zadan[i]])

    zadania.sort(key=lambda x: x[0])

    f = open(file=nazwa_pliku_wyjsciowego, mode="w")
    for zadanie in zadania:
        f.write(str(zadanie[0]) + ' ' + str(zadanie[1]) + '\n')
    f.close()


def main():
    for obciazenie_procentowo in range(50, 100, 5):
        nazwa_pliku_wyjsciowego = "../instancje/inst-obc-" + str(obciazenie_procentowo) + ".txt"
        tworz_instancje(obciazenie_procentowo / 100, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
