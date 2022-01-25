# Skrypt przeznaczony do wygenerowania wykresow, ktore sa potrzebne dla wykonania raportu

import matplotlib.pyplot as plt
import os
import re


def wykryj_zbior_poziomow_jednorodnosci_fazy(lista_nazw_uszeregowan):
    zbior_poziomow_jednorodnosci_fazy = set()

    wzorzec_poziomu_jednorodnosci_fazy = re.compile('.*j([0-9.]*)\\.txt')
    for nazwa_uszeregowania in lista_nazw_uszeregowan:
        wynik_dopasowania = wzorzec_poziomu_jednorodnosci_fazy.match(nazwa_uszeregowania)
        if wynik_dopasowania is not None:
            zbior_poziomow_jednorodnosci_fazy.add(float(wynik_dopasowania.group(1)))
    return sorted(zbior_poziomow_jednorodnosci_fazy)


def wykryj_zbior_liczb_wezlow(lista_nazw_uszeregowan):
    zbior_liczb_wezlow = set()

    wzorzec_liczby_wezlow = re.compile('.*-n([0-9]*)-inst.*\\.txt')
    for nazwa_uszeregowania in lista_nazw_uszeregowan:
        wynik_dopasowania = wzorzec_liczby_wezlow.match(nazwa_uszeregowania)
        if wynik_dopasowania is not None:
            zbior_liczb_wezlow.add(int(wynik_dopasowania.group(1)))
    return sorted(zbior_liczb_wezlow)


def wykryj_zbior_wartosci_parametru(lista_nazw_uszeregowan):
    zbior_wartosci_parametru = set()

    wzorzec_wartosci_parametru = re.compile('.*-([0-9.]*)-j.*\\.txt')
    for nazwa_uszeregowania in lista_nazw_uszeregowan:
        wynik_dopasowania = wzorzec_wartosci_parametru.match(nazwa_uszeregowania)
        if wynik_dopasowania is not None:
            zbior_wartosci_parametru.add(float(wynik_dopasowania.group(1)))
    return sorted(zbior_wartosci_parametru)


def rysuj_wyniki_poziomu_jednorodnosci_1():
    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Wpływ poziomu jednorodności fazy $l_f$ na współczynnik zmienności $w_t$ (protokół obsługi $JSQ/PS$)")

    program_szeregujacy = "jsq"
    parametr = "przedk"
    wartosc_parametru = 0.5
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\twartosc_parametru=\"%.2f\"" % (program_szeregujacy, parametr, wartosc_parametru))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + "-%.1f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_poziomow_jednorodnosci_fazy = wykryj_zbior_poziomow_jednorodnosci_fazy(lista_wykorzystywanych_uszeregowan)
    print("Zbior poziomow jednorodnosci fazy: " + str(zbior_poziomow_jednorodnosci_fazy))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + "-%.1f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.title(r"wartość parametru $w_t$=%.1f" % wartosc_parametru)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_poziomow_jednorodnosci_fazy, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$")
    plt.xlabel(r"Wartość poziomu jednorodności fazy $l_f$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([1000, 20000000])

    program_szeregujacy = "jsq"
    parametr = "przedk"
    wartosc_parametru = 1.0
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\twartosc_parametru=\"%.2f\"" % (program_szeregujacy, parametr, wartosc_parametru))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + "-%.1f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_poziomow_jednorodnosci_fazy = wykryj_zbior_poziomow_jednorodnosci_fazy(lista_wykorzystywanych_uszeregowan)
    print("Zbior poziomow jednorodnosci fazy: " + str(zbior_poziomow_jednorodnosci_fazy))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + "-%.1f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 2)
    plt.title(r"wartość parametru $w_t$=%.1f" % wartosc_parametru)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_poziomow_jednorodnosci_fazy, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$")
    plt.xlabel(r"Wartość poziomu jednorodności fazy $l_f$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([1000, 20000000])

    plt.savefig("Raport_porownanie_poziomu_jednorodnosci_1.png", dpi=600)


def rysuj_wyniki_poziomu_jednorodnosci_2():
    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Wpływ poziomu jednorodności fazy $l_f$ na współczynnik zmienności $w_p$ (protokół obsługi $JNQ/FCFS$)")

    program_szeregujacy = "jnq"
    parametr = "rozm"
    wartosc_parametru = 1.00
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\twartosc_parametru=\"%.2f\"" % (program_szeregujacy, parametr, wartosc_parametru))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + "-%.2f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_poziomow_jednorodnosci_fazy = wykryj_zbior_poziomow_jednorodnosci_fazy(lista_wykorzystywanych_uszeregowan)
    print("Zbior poziomow jednorodnosci fazy: " + str(zbior_poziomow_jednorodnosci_fazy))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + "-%.2f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.title(r"wartość parametru $w_p$=%.1f" % wartosc_parametru)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_poziomow_jednorodnosci_fazy, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$")
    plt.xlabel(r"Wartość poziomu jednorodności fazy $l_f$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 3000000])

    program_szeregujacy = "jnq"
    parametr = "rozm"
    wartosc_parametru = 3.50
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\twartosc_parametru=\"%.2f\"" % (program_szeregujacy, parametr, wartosc_parametru))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + "-%.2f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_poziomow_jednorodnosci_fazy = wykryj_zbior_poziomow_jednorodnosci_fazy(lista_wykorzystywanych_uszeregowan)
    print("Zbior poziomow jednorodnosci fazy: " + str(zbior_poziomow_jednorodnosci_fazy))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + "-%.2f" % wartosc_parametru + "-j[0-9.]*\\.txt$"
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 2)
    plt.title(r"wartość parametru $w_p$=%.1f" % wartosc_parametru)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_poziomow_jednorodnosci_fazy, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$")
    plt.xlabel(r"Wartość poziomu jednorodności fazy $l_f$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 3000000])

    plt.savefig("Raport_porownanie_poziomu_jednorodnosci_2.png", dpi=600)


def rysuj_wyniki_wspolczynnika_zmiennosci_rozmiaru():
    parametr = "rozm"
    poziom_jednorodnosci_fazy = 0.7

    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Wpływ współczynnika zmienności rozmiarów zadań $w_p$ ($l_f=%.1f$)" % poziom_jednorodnosci_fazy)

    program_szeregujacy = "jnq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.title(r"protokół obsługi $JNQ/FCFS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="upper left")
    plt.xlabel(r"Wartość parametru współczynnika zmienności rozmiarów zadań $w_p$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 150000])

    program_szeregujacy = "jsq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 2)
    plt.title(r"protokół obsługi $JSQ/PS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="upper left")
    plt.xlabel(r"Wartość parametru współczynnika zmienności rozmiarów zadań $w_p$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 150000])

    plt.savefig("Raport_wyniki_wspolczynnika_zmiennosci_rozmiaru.png", dpi=600)


def rysuj_wyniki_obciazenia_systemu():
    parametr = "obc"
    poziom_jednorodnosci_fazy = 0.8

    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Wpływ obciażenia systemu $\rho$ ($l_f=%.1f$)" % poziom_jednorodnosci_fazy)

    program_szeregujacy = "jnq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.title(r"protokół obsługi $JNQ/FCFS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość parametru obciażenia systemu $\rho$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([1000, 4000000])

    program_szeregujacy = "jsq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 2)
    plt.title(r"protokół obsługi $JSQ/PS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość parametru obciażenia systemu $\rho$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([1000, 4000000])

    plt.savefig("Raport_wyniki_obciazenia_systemu.png", dpi=600)


def rysuj_wyniki_wspolczynnika_zmiennosci_przedkladania():
    parametr = "przedk"
    poziom_jednorodnosci_fazy = 0.8

    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Wpływ współczynnika zmienności czasów miedzy przedkładaniem zadań $w_t$ ($l_f=%.1f$)" % poziom_jednorodnosci_fazy)

    program_szeregujacy = "jnq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.title(r"protokół obsługi $JNQ/FCFS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość wspołczynnika zmienności czasów miedzy przedkładaniem zadań $w_t$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 8000000])

    program_szeregujacy = "jsq"
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 2)
    plt.title(r"protokół obsługi $JSQ/PS$")
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość współczynnika zmienności czasów miedzy przedkładaniem zadań $w_t$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.set_ylim([2000, 8000000])

    plt.savefig("Raport_wyniki_wspolczynnika_zmiennosci_czasow_miedzy_przedkladaniem.png", dpi=600)


def rysuj_wyniki_liczby_wezlow_1():
    parametr = "obc"
    poziom_jednorodnosci_fazy = 0.7
    program_szeregujacy = "jsq"

    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Porównanie liczby wezłów $N$ systemu obsługi (protokół obsługi $JSQ/PS$, $l_f=%.1f$)" % poziom_jednorodnosci_fazy)

    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość parametru obciażenia systemu $\rho$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)

    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    lista_wyskalowanych_list_czasow = []
    for index_liczba_wezlow in range(len(zbior_liczb_wezlow)):
        wyskalowana_lista_czasow = []
        index_wartosc_parametru = 0
        for czas_odpowiedzi in lista_list_czasow[index_liczba_wezlow]:
            wyskalowana_lista_czasow.append(czas_odpowiedzi / lista_list_czasow[0][index_wartosc_parametru])
            index_wartosc_parametru += 1
        lista_wyskalowanych_list_czasow.append(wyskalowana_lista_czasow)
    print(lista_wyskalowanych_list_czasow)

    plt.subplot(1, 2, 2)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_wyskalowanych_czasow_z_dana_liczba_wezlow = lista_wyskalowanych_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_wyskalowanych_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="upper right")
    plt.xlabel(r"Wartość parametru obciażenia systemu $\rho$", fontsize=10)
    plt.ylabel(r"Krotność spowolnienia czasu odpowiedzi w stosunku do superkomputera" "\n" r"(skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.yticks([1, 2, 5, 10, 20, 50, 100], [1, 2, 5, 10, 20, 50, 100])
    ax.set_ylim([0.85, 130])

    plt.savefig("Raport_wyniki_liczby_wezlow_1.png", dpi=600)


def rysuj_wyniki_liczby_wezlow_2():
    parametr = "rozm"
    poziom_jednorodnosci_fazy = 0.7
    program_szeregujacy = "jnq"

    plt.rcParams['text.usetex'] = True
    plt.rcParams["figure.figsize"] = (2 * plt.rcParams["figure.figsize"][0], plt.rcParams["figure.figsize"][1])
    plt.suptitle(r"Porównanie liczby wezłów $N$ systemu obsługi (protokół obsługi $JNQ/FCFS$, $l_f=%.1f$)" % poziom_jednorodnosci_fazy)

    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)
    print(lista_list_czasow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    plt.subplot(1, 2, 1)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="lower right")
    plt.xlabel(r"Wartość parametru współczynnika zmienności rozmiarów zadań $w_p$", fontsize=10)
    plt.ylabel(r"Czas odpowiedzi (skala logarytmiczna)", fontsize=10)

    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=\"%.1f\"" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))

    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    tekst_wzorca_wykorzystywanych_uszeregowan = '^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
    wzorzec_wykorzystywanych_uszeregowan = re.compile(tekst_wzorca_wykorzystywanych_uszeregowan)
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        tekst_wzorca_uszeregowan_z_dana_liczba_wezlow = '^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$'
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile(tekst_wzorca_uszeregowan_z_dana_liczba_wezlow)
        lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
        lista_czasow_z_dana_liczba_wezlow = []
        for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
            nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
            f = open(file=nazwa_pliku_wejsciowego, mode="r")
            [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
            lista_czasow_z_dana_liczba_wezlow.append(sredni_czas_odpowiedzi)
            f.close()
        lista_list_czasow.append(lista_czasow_z_dana_liczba_wezlow)

    mapa_kolorow = []
    for i in range(len(zbior_liczb_wezlow)):
        v = 0.8 - 0.8 * i / (len(zbior_liczb_wezlow) - 1)
        if v < 0:
            v = 0
        mapa_kolorow.append((v, v, v))

    lista_wyskalowanych_list_czasow = []
    for index_liczba_wezlow in range(len(zbior_liczb_wezlow)):
        wyskalowana_lista_czasow = []
        index_wartosc_parametru = 0
        for czas_odpowiedzi in lista_list_czasow[index_liczba_wezlow]:
            wyskalowana_lista_czasow.append(czas_odpowiedzi / lista_list_czasow[0][index_wartosc_parametru])
            index_wartosc_parametru += 1
        lista_wyskalowanych_list_czasow.append(wyskalowana_lista_czasow)
    print(lista_wyskalowanych_list_czasow)

    plt.subplot(1, 2, 2)
    plt.yscale('log')
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_wyskalowanych_czasow_z_dana_liczba_wezlow = lista_wyskalowanych_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_wyskalowanych_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=r"$%d$" % liczba_wezlow)
    plt.legend(title=r"Liczba wezłów $N$", loc="upper right")
    plt.xlabel(r"Wartość parametru współczynnika zmienności rozmiarów zadań $w_p$", fontsize=10)
    plt.ylabel(r"Krotność spowolnienia czasu odpowiedzi w stosunku do superkomputera" "\n" r"(skala logarytmiczna)", fontsize=10)
    ax = plt.gca()
    ax.grid(axis='y', linestyle='--', linewidth=0.5)
    plt.yticks([1, 2, 5, 10, 20, 50, 100], [1, 2, 5, 10, 20, 50, 100])
    ax.set_ylim([0.7, 120])

    plt.savefig("Raport_wyniki_liczby_wezlow_2.png", dpi=600)


def main():
    # rysuj_wyniki_poziomu_jednorodnosci_1()
    # rysuj_wyniki_poziomu_jednorodnosci_2()
    # rysuj_wyniki_wspolczynnika_zmiennosci_rozmiaru()
    # rysuj_wyniki_obciazenia_systemu()
    # rysuj_wyniki_wspolczynnika_zmiennosci_przedkladania()
    # rysuj_wyniki_liczby_wezlow_1()
    rysuj_wyniki_liczby_wezlow_2()


if __name__ == "__main__":
    main()
