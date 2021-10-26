# Skrypt przeznaczony do zbadania charakterystyki rozkladu rozmiarow krotkich i dlugich zadan dla zadanych parametrow.

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def sprawdz_parametry_1():
    # definicja wartosci stalych

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik wskazujacy ile razy wieksza ma byc srednia i odchylenie standardowe rozmiarow dlugich zadan od zadan krotkich
    w_12 = 20

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = 5

    # obliczanie charakterystyk rozkladow

    # sredni czas dla zadan krotkich
    ex_1 = ex_c / (p + w_12 * (1 - p))
    # sredni czas dla zadan dlugich
    ex_2 = w_12 * ex_1

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

    # odchylenie standardowe zbioru wszystkich zadan
    dx2_c = p * (dx_1 ** 2 + (ex_1 - ex_c) ** 2) + (1 - p) * (dx_2 ** 2 + (ex_2 - ex_c) ** 2)
    dx_c = dx2_c ** 0.5

    # wypisanie uzyskanych charakterystyk
    print("Charakterystyki rozkladu gamma rozmiarow krotkich zadan:")
    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))

    print("\nCharakterystyki rozkladu gamma rozmiarow dlugich zadan:")
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    print("\nCharakterystyki rozkladu mieszanego rozmiarow wszystkich zadan:")
    print("ex_c={}\tdx_c={}".format(ex_c, dx_c))

    # wizualizacja rozkladow
    liczba_zadan = 10000
    rozmiary_krotkie = []
    for _ in range(liczba_zadan):
        rozmiary_krotkie.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))

    rozmiary_dlugie = []
    for _ in range(liczba_zadan):
        rozmiary_dlugie.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

    rozmiary_mieszane = []
    for _ in range(liczba_zadan):
        if random.random() < p:
            rozmiary_mieszane.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))
        else:
            rozmiary_mieszane.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

    np_rozmiary_krotkie = np.array(rozmiary_krotkie)
    np_rozmiary_dlugie = np.array(rozmiary_dlugie)
    np_rozmiary_mieszane = np.array(rozmiary_mieszane)

    pd_rozmiary_krotkie = pd.DataFrame(np_rozmiary_krotkie)
    pd_rozmiary_dlugie = pd.DataFrame(np_rozmiary_dlugie)
    pd_rozmiary_mieszane = pd.DataFrame(np_rozmiary_mieszane)

    print("\npd_rozmiary_krotkie.describe():")
    print(pd_rozmiary_krotkie.describe())
    print("\npd_rozmiary_dlugie.describe():")
    print(pd_rozmiary_dlugie.describe())
    print("\npd_rozmiary_mieszane.describe():")
    print(pd_rozmiary_mieszane.describe())

    plt.subplot(3, 2, 1)
    plt.hist(np_rozmiary_krotkie, bins=200)
    plt.title("krotkie")

    plt.subplot(3, 2, 3)
    plt.hist(np_rozmiary_dlugie, bins=200)
    plt.title("dlugie")

    plt.subplot(3, 2, 2)
    plt.hist(np_rozmiary_krotkie, bins=200)
    plt.title("krotkie skalowane")
    plt.xlim(0, ex_2 + 3 * dx_2)

    plt.subplot(3, 2, 4)
    plt.hist(np_rozmiary_dlugie, bins=200)
    plt.title("dlugie skalowane")
    plt.xlim(0, ex_2 + 3 * dx_2)

    plt.subplot(3, 2, (5, 6))
    plt.hist(pd_rozmiary_mieszane, bins=200)
    plt.title("mieszane")

    plt.show()


def rysuj_charakterystyki_w_funkcji_wspolczynnika_zmiennosci_rozmiarow_zadan_1():
    # definicja wartosci stalych

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik wskazujacy ile razy wieksza ma byc srednia i odchylenie standardowe rozmiarow dlugich zadan od zadan krotkich
    w_12 = 10

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = np.arange(0.1, 5, 0.05)
    print(w_c)

    # obliczanie charakterystyk rozkladow

    # sredni czas dla zadan krotkich
    ex_1 = ex_c / (p + w_12 * (1 - p)) * np.ones(w_c.shape)
    # sredni czas dla zadan dlugich
    ex_2 = w_12 * ex_1

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

    # odchylenie standardowe zbioru wszystkich zadan
    dx2_c = p * (dx_1 ** 2 + (ex_1 - ex_c) ** 2) + (1 - p) * (dx_2 ** 2 + (ex_2 - ex_c) ** 2)
    dx_c = dx2_c ** 0.5

    # wypisanie uzyskanych charakterystyk
    print("Charakterystyki rozkladu gamma rozmiarow krotkich zadan:")
    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))

    print("\nCharakterystyki rozkladu gamma rozmiarow dlugich zadan:")
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    print("\nCharakterystyki rozkladu mieszanego rozmiarow wszystkich zadan:")
    print("ex_c={}\tdx_c={}".format(ex_c, dx_c))

    # wizualizacja charakterystyk
    plt.subplot(3, 2, 1)
    plt.plot(w_c, alpha_1)
    plt.title("alpha_1")

    plt.subplot(3, 2, 2)
    plt.plot(w_c, alpha_2)
    plt.title("alpha_2")

    plt.subplot(3, 2, 3)
    plt.plot(w_c, beta_1)
    plt.title("beta_1")

    plt.subplot(3, 2, 4)
    plt.plot(w_c, beta_2)
    plt.title("beta_2")

    plt.subplot(3, 2, 5)
    plt.plot(w_c, dx_1)
    plt.plot(w_c, ex_1)
    plt.title("dx_1")

    plt.subplot(3, 2, 6)
    plt.plot(w_c, dx_2)
    plt.plot(w_c, ex_2)
    plt.title("dx_2")

    plt.show()


def sprawdz_parametry_2():
    # definicja wartosci stalych

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik okreslajacy stosunek wartosci odchylenia standardowego do wartosci oczekiwanej danego skladowego rozkladu rozmiaru zadan
    w_de = 1 / 3

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = 1.5

    # obliczanie charakterystyk rozkladow

    # uklad rownan
    # p * ex_1 + (1 - p) * ex_2 = ex_c
    # dx_c ** 2 = p * (dx_1 ** 2 + (ex_1 - ex_c) ** 2) + (1 - p) * {dx_2 ** 2 + (ex_2 - ex_c) ** 2}
    # z ktorego otrzymywane jest rownanie kwadratowe z niewiadoma ex_1
    # p * (1 + w_de ** 2) * ex_1 ** 2 - 2 * p * ex_c * (1 + w_de ** 2) * ex_1 + (p + w_de ** 2 - w_c ** 2 + p * w_c ** 2) * ex_c ** 2 = 0
    ex_1 = ex_c * (1 - (((1 - p) * (w_c ** 2 - w_de ** 2)) / (p * (1 + w_de ** 2))) ** 0.5)
    ex_2 = (ex_c - p * ex_1) / (1 - p)

    dx_1 = w_de * ex_1
    dx_2 = w_de * ex_2
    dx_c = w_c * ex_c

    # ustalenie wspolczynnikow ksztaltu alfa i stosunku beta rozkladu gamma
    # dla ktorych zachodza ustalone wartosci srednie i odchylenia krotkich i dlugich zadan
    alpha_1 = (1 / w_de) ** 2
    alpha_2 = (1 / w_de) ** 2

    beta_1 = ex_1 / alpha_1
    beta_2 = ex_2 / alpha_2

    # wypisanie uzyskanych charakterystyk
    print("Charakterystyki rozkladu gamma rozmiarow krotkich zadan:")
    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))

    print("\nCharakterystyki rozkladu gamma rozmiarow dlugich zadan:")
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    print("\nCharakterystyki rozkladu mieszanego rozmiarow wszystkich zadan:")
    print("ex_c={}\tdx_c={}".format(ex_c, dx_c))

    # wizualizacja rozkladow
    liczba_zadan = 10000
    rozmiary_krotkie = []
    for _ in range(liczba_zadan):
        rozmiary_krotkie.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))

    rozmiary_dlugie = []
    for _ in range(liczba_zadan):
        rozmiary_dlugie.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

    rozmiary_mieszane = []
    for _ in range(liczba_zadan):
        if random.random() < p:
            rozmiary_mieszane.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))
        else:
            rozmiary_mieszane.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

    np_rozmiary_krotkie = np.array(rozmiary_krotkie)
    np_rozmiary_dlugie = np.array(rozmiary_dlugie)
    np_rozmiary_mieszane = np.array(rozmiary_mieszane)

    pd_rozmiary_krotkie = pd.DataFrame(np_rozmiary_krotkie)
    pd_rozmiary_dlugie = pd.DataFrame(np_rozmiary_dlugie)
    pd_rozmiary_mieszane = pd.DataFrame(np_rozmiary_mieszane)

    print("\npd_rozmiary_krotkie.describe():")
    print(pd_rozmiary_krotkie.describe())
    print("\npd_rozmiary_dlugie.describe():")
    print(pd_rozmiary_dlugie.describe())
    print("\npd_rozmiary_mieszane.describe():")
    print(pd_rozmiary_mieszane.describe())

    plt.subplot(3, 2, 1)
    plt.hist(np_rozmiary_krotkie, bins=200)
    plt.title("krotkie")

    plt.subplot(3, 2, 3)
    plt.hist(np_rozmiary_dlugie, bins=200)
    plt.title("dlugie")

    plt.subplot(3, 2, 2)
    plt.hist(np_rozmiary_krotkie, bins=200)
    plt.title("krotkie skalowane")
    plt.xlim(0, ex_2 + 3 * dx_2)

    plt.subplot(3, 2, 4)
    plt.hist(np_rozmiary_dlugie, bins=200)
    plt.title("dlugie skalowane")
    plt.xlim(0, ex_2 + 3 * dx_2)

    plt.subplot(3, 2, (5, 6))
    plt.hist(pd_rozmiary_mieszane, bins=200)
    plt.title("mieszane")

    plt.show()


def rysuj_charakterystyki_w_funkcji_wspolczynnika_zmiennosci_rozmiarow_zadan_2():
    # definicja wartosci stalych

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik okreslajacy stosunek wartosci odchylenia standardowego do wartosci oczekiwanej danego skladowego rozkladu rozmiaru zadan
    w_de = 1 / 3

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = np.arange(0.1, 5, 0.05)
    print(w_c)

    # obliczanie charakterystyk rozkladow

    # uklad rownan
    # p * ex_1 + (1 - p) * ex_2 = ex_c
    # dx_c ** 2 = p * (dx_1 ** 2 + (ex_1 - ex_c) ** 2) + (1 - p) * {dx_2 ** 2 + (ex_2 - ex_c) ** 2}
    # z ktorego otrzymywane jest rownanie kwadratowe z niewiadoma ex_1
    # p * (1 + w_de ** 2) * ex_1 ** 2 - 2 * p * ex_c * (1 + w_de ** 2) * ex_1 + (p + w_de ** 2 - w_c ** 2 + p * w_c ** 2) * ex_c ** 2 = 0
    ex_1 = ex_c * (1 - (((1 - p) * (w_c ** 2 - w_de ** 2)) / (p * (1 + w_de ** 2))) ** 0.5)
    ex_2 = (ex_c - p * ex_1) / (1 - p)

    dx_1 = w_de * ex_1
    dx_2 = w_de * ex_2
    dx_c = w_c * ex_c

    # ustalenie wspolczynnikow ksztaltu alfa i stosunku beta rozkladu gamma
    # dla ktorych zachodza ustalone wartosci srednie i odchylenia krotkich i dlugich zadan
    alpha_1 = (1 / w_de) ** 2
    alpha_2 = (1 / w_de) ** 2

    beta_1 = ex_1 / alpha_1
    beta_2 = ex_2 / alpha_2

    # wypisanie uzyskanych charakterystyk
    print("Charakterystyki rozkladu gamma rozmiarow krotkich zadan:")
    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))

    print("\nCharakterystyki rozkladu gamma rozmiarow dlugich zadan:")
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    print("\nCharakterystyki rozkladu mieszanego rozmiarow wszystkich zadan:")
    print("ex_c={}\tdx_c={}".format(ex_c, dx_c))

    # wizualizacja charakterystyk
    plt.subplot(3, 2, 1)
    plt.plot(w_c, alpha_1)
    plt.title("alpha_1")

    plt.subplot(3, 2, 2)
    plt.plot(w_c, alpha_2)
    plt.title("alpha_2")

    plt.subplot(3, 2, 3)
    plt.plot(w_c, beta_1)
    plt.title("beta_1")

    plt.subplot(3, 2, 4)
    plt.plot(w_c, beta_2)
    plt.title("beta_2")

    plt.subplot(3, 2, 5)
    plt.plot(w_c, dx_1)
    plt.plot(w_c, ex_1)
    plt.title("dx_1")

    plt.subplot(3, 2, 6)
    plt.plot(w_c, dx_2)
    plt.plot(w_c, ex_2)
    plt.title("dx_2")

    plt.show()


def main():
    # sprawdz_parametry_1()
    # rysuj_charakterystyki_w_funkcji_wspolczynnika_zmiennosci_rozmiarow_zadan_1()

    sprawdz_parametry_2()
    # rysuj_charakterystyki_w_funkcji_wspolczynnika_zmiennosci_rozmiarow_zadan_2()


if __name__ == "__main__":
    main()
