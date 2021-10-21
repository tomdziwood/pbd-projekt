import random
import math


def tworz_instancje(wspolczynnik_obciazenia, nazwa_pliku_wyjsciowego):
    print("Generowanie pliku " + nazwa_pliku_wyjsciowego + "...")
    liczba_zadan = 10000

    rozmiary_zadan = []
    for _ in range(liczba_zadan):
        if random.random() < 0.95:
            rozmiary_zadan.append(round(random.gammavariate(alpha=8, beta=125)))
        else:
            rozmiary_zadan.append(round(random.gammavariate(alpha=8, beta=1250)))

    sum_rozmiary_zadan = sum(rozmiary_zadan)
    max_czas_zakonczenia = math.ceil(sum_rozmiary_zadan / wspolczynnik_obciazenia)

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
