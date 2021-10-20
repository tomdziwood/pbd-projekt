import random
import math


def main():
    liczba_zadan = 10000
    wspolczynnik_obciazenia = 0.8

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

    f = open(file="../instancje/inst-01.txt", mode="w")
    for zadanie in zadania:
        f.write(str(zadanie[0]) + ' ' + str(zadanie[1]) + '\n')
    f.close()


if __name__ == "__main__":
    main()
