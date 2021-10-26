import random
import math


def tworz_instancje(wspolczynnik_obciazenia, nazwa_pliku_wyjsciowego):
    print("Generowanie pliku " + nazwa_pliku_wyjsciowego + "...")
    liczba_zadan = 10000

    # rozmiary zadan wygenerowane przy uzyciu rozkladu Erlanga
    # 95% zadan jest krotkich, a pozostale zadania to zadania dlugie
    rozmiary_zadan = []

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik wskazujacy ile razy wieksza ma byc srednia i odchylenie standardowe rozmiarow dlugich zadan od zadan krotkich
    w_12 = 10

    # sredni czas dla zadan krotkich
    ex_1 = ex_c / (p + w_12 * (1 - p))
    # sredni czas dla zadan dlugich
    ex_2 = w_12 * ex_1

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = 1.5

    # odchylenie standardowe dla zadan krotkich
    dx2_1 = (w_c ** 2 * ex_c ** 2 - p * (ex_1 - ex_c) ** 2 - (1 - p) * (ex_2 - ex_c) ** 2) / (p + (1 - p) * w_12 ** 2)
    dx_1 = dx2_1 ** 0.5
    # odchylenie standardowe dla zadan dlugich
    dx_2 = w_12 * dx_1

    # ustalenie wspolczynnikow ksztaltu alfa i stosunku beta rozkladu gamma
    # dla ktorych zachodza ustalone wartosci srednie i odchylenia krotkich i dlugich zadan
    alpha_1 = ex_1 ** 2 / dx_1 ** 2
    alpha_2 = ex_2 ** 2 / dx_2 ** 2

    beta_1 = dx_1 ** 2 / ex_1
    beta_2 = dx_2 ** 2 / ex_2

    dx2_c = p * (dx_1 ** 2 + (ex_1 - ex_c) ** 2) + (1 - p) * (dx_2 ** 2 + (ex_2 - ex_c) ** 2)
    dx_c = dx2_c ** 0.5
    dx_c_teoretycznie = ex_c * w_c
    print("ex_c={}\tdx_c={}\tdx_c_teoretycznie={}".format(ex_c, dx_c, dx_c_teoretycznie))

    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    for _ in range(liczba_zadan):
        if random.random() < p:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))
        else:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

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
        nazwa_pliku_wyjsciowego = "../instancje/inst-obc-01-" + str(obciazenie_procentowo) + ".txt"
        tworz_instancje(obciazenie_procentowo / 100, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
