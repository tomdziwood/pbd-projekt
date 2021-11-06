import random


def generuj_ziarno_losowosci(wspolczynnik_obciazenia, wspolczynnik_zmiennosci_przedkladania, wspolczynnik_zmiennosci_rozmiaru, liczba_cykli):
    ziarno_losowosci = wspolczynnik_obciazenia * 100
    ziarno_losowosci *= 1000
    ziarno_losowosci += wspolczynnik_zmiennosci_przedkladania * 100
    ziarno_losowosci *= 1000
    ziarno_losowosci += wspolczynnik_zmiennosci_rozmiaru * 100
    ziarno_losowosci *= 100
    ziarno_losowosci += liczba_cykli
    return round(ziarno_losowosci)


def generuj_instancje(wspolczynnik_obciazenia, wspolczynnik_zmiennosci_przedkladania, wspolczynnik_zmiennosci_rozmiaru, liczba_cykli, nazwa_pliku_wyjsciowego):
    ziarno_losowosci = generuj_ziarno_losowosci(wspolczynnik_obciazenia, wspolczynnik_zmiennosci_przedkladania, wspolczynnik_zmiennosci_rozmiaru, liczba_cykli)
    random.seed(ziarno_losowosci)
    print("\nGenerowanie pliku " + nazwa_pliku_wyjsciowego + ", ziarno_losowosci=" + str(ziarno_losowosci))

    # stala wartosc wskazujaca liczbe zadan do wykonania
    liczba_zadan = 100000

    # rozmiary zadan wygenerowane przy uzyciu rozkladu Erlanga
    # 95% zadan jest krotkich, a pozostale zadania to zadania dlugie
    rozmiary_zadan = []

    # ulamek wskazujacy jaka czesc wszystkich zadan instancji stanowia zadania krotkie
    p = 0.95

    # oczekiwany sredni rozmiar wszystkich zadan dla instancji
    ex_c = 1000

    # wspolczynnik okreslajacy stosunek wartosci odchylenia standardowego do wartosci oczekiwanej danego skladowego rozkladu rozmiaru zadan
    w_de = 1 / 3

    # wspolczynnik zmiennosci rozmiarow zadan (odchylenie standardowe / wartosc srednia; dx_c / ex_c)
    w_c = wspolczynnik_zmiennosci_rozmiaru

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

    print("Parametry rozmiarow zadan:")
    print("ex_c={}\tdx_c={}".format(ex_c, dx_c))
    print("alpha_1={}\tbeta_1={}\tex_1={}\tdx_1={}".format(alpha_1, beta_1, ex_1, dx_1))
    print("alpha_2={}\tbeta_2={}\tex_2={}\tdx_2={}".format(alpha_2, beta_2, ex_2, dx_2))

    for _ in range(liczba_zadan):
        if random.random() < p:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha_1, beta=beta_1)))
        else:
            rozmiary_zadan.append(round(random.gammavariate(alpha=alpha_2, beta=beta_2)))

    # definicja sredniej wartosci czasu przedkladania w oparciu o znany sredni rozmiar zadania i docelowe obciazenie
    ex_t = ex_c / wspolczynnik_obciazenia

    # wartosc wszpolczynnika zmiennosci czasow przedkladania zadan
    w_t = wspolczynnik_zmiennosci_przedkladania

    # odchylenie standardowe czasu przedkladania zadan
    dx_t = w_t * ex_t

    # wspolczynnik wielokrotnosci wskazujacy ile razy wieksza jest srednia dlugich czasow przedkladania od sredniej krotkich czasow przedkladania
    k_t = 2

    # srednie krotkich (1) i dlugich (2) czasow przedkladania
    ex_t1 = 2 * ex_t / (1 + k_t)
    ex_t2 = k_t * ex_t1

    # zalozenie jednakowego wspolczynnika zmiennosci zarowno dla krotkich jak i dlugich czasow przedkladania
    # wowczas wspolczynnik ten dla wczesniejszych stalych przyjmuje wartosc okreslona ponizszym wzorem
    w_t0 = ((2 * dx_t ** 2 - (ex_t1 - ex_t) ** 2 - (ex_t2 - ex_t) ** 2) / (ex_t1 ** 2 + ex_t2 ** 2)) ** 0.5

    # odchylenia krotkich i dlugich czasow przedkladania
    dx_t1 = w_t0 * ex_t1
    dx_t2 = w_t0 * ex_t2

    # ustalenie wspolczynnikow ksztaltu alfa i stosunku beta rozkladu gamma czasow przedkladania
    # dla ktorych zachodza ustalone wartosci srednie i odchylenia czasow przedkladania
    alpha_t1 = (1 / w_t0) ** 2
    alpha_t2 = (1 / w_t0) ** 2

    beta_t1 = ex_t1 / alpha_t1
    beta_t2 = ex_t2 / alpha_t2

    print("Parametry czasow przedkladania:")
    print("ex_t={}\tdx_t={}".format(ex_t, dx_t))
    print("alpha_t1={}\tbeta_t1={}\tex_t1={}\tdx_t1={}".format(alpha_t1, beta_t1, ex_t1, dx_t1))
    print("alpha_t2={}\tbeta_t2={}\tex_t2={}\tdx_t2={}".format(alpha_t2, beta_t2, ex_t2, dx_t2))
    print("dx_t? / ex_t? = w_t0 = {}".format(w_t0))

    # generowanie kolejno momentow gotowosci dla kolejnych zadan
    momenty_gotowosci = [0]
    for i in range(1, liczba_zadan):
        if (i // (liczba_zadan / (2 * liczba_cykli))) % 2 == 0:
            momenty_gotowosci.append(momenty_gotowosci[i - 1] + round(random.gammavariate(alpha=alpha_t1, beta=beta_t1)))
        else:
            momenty_gotowosci.append(momenty_gotowosci[i - 1] + round(random.gammavariate(alpha=alpha_t2, beta=beta_t2)))

    zadania = []
    for i in range(liczba_zadan):
        zadania.append([momenty_gotowosci[i], rozmiary_zadan[i]])

    f = open(file=nazwa_pliku_wyjsciowego, mode="w")
    for zadanie in zadania:
        f.write(str(zadanie[0]) + ' ' + str(zadanie[1]) + '\n')
    f.close()
