# Skrypt przeznaczony do rysowania zaleznosci miedzy wynikami czasow uszeregowania uzyskanymi dzieki wskazanemu programowi szeregujacemu

import os
import re
import matplotlib.pyplot as plt


def porownaj_liczbe_wezlow():
    print("Porownuje liczbe wezlow...")


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


def rysuj_wykres_porownania_liczby_wezlow(program_szeregujacy, parametr, poziom_jednorodnosci_fazy):
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tpoziom_jednorodnosci_fazy=%s" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))
    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    wzorzec_wykorzystywanych_uszeregowan = re.compile('^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile('^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
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

    plt.title("program_szeregujacy=\"%s\" parametr=\"%s\" poziom_jednorodnosci_fazy=%s" % (program_szeregujacy, parametr, poziom_jednorodnosci_fazy))
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
    plt.legend(title="Liczba wezlow")
    plt.show()


def rysuj_wykresy_porownania_liczby_wezlow(program_szeregujacy, parametr):
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"" % (program_szeregujacy, parametr))
    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    wzorzec_wykorzystywanych_uszeregowan = re.compile('^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-j[0-9.]*\\.txt$')
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_poziomow_jednorodnosci_fazy = wykryj_zbior_poziomow_jednorodnosci_fazy(lista_wykorzystywanych_uszeregowan)
    print("Zbior poziomow jednorodnosci fazy: " + str(zbior_poziomow_jednorodnosci_fazy))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    index_poziom_jednorodnosci_fazy = 1
    ncols = len(zbior_poziomow_jednorodnosci_fazy)
    nrows = 3
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("program_szeregujacy=\"%s\" | parametr=\"%s\"" % (program_szeregujacy, parametr), fontsize=30, y=0.95)
    for poziom_jednorodnosci_fazy in zbior_poziomow_jednorodnosci_fazy:
        lista_list_czasow = []
        for liczba_wezlow in zbior_liczb_wezlow:
            wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile('^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
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

        plt.subplot(nrows, ncols, index_poziom_jednorodnosci_fazy)
        plt.title("poziom_jednorodnosci_fazy=%s" % poziom_jednorodnosci_fazy)
        for indeks in range(len(zbior_liczb_wezlow)):
            liczba_wezlow = zbior_liczb_wezlow[indeks]
            lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
            plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
        plt.legend(title="Liczba wezlow")
        plt.xlabel("Wartosc parametru", fontsize=8)
        plt.ylabel("Czas odpowiedzi", fontsize=8)

        plt.subplot(nrows, ncols, ncols + index_poziom_jednorodnosci_fazy)
        plt.title("poziom_jednorodnosci_fazy=%s" % poziom_jednorodnosci_fazy)
        plt.yscale('log')
        for indeks in range(len(zbior_liczb_wezlow)):
            liczba_wezlow = zbior_liczb_wezlow[indeks]
            lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
            plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
        plt.legend(title="Liczba wezlow")
        plt.xlabel("Wartosc parametru", fontsize=8)
        plt.ylabel("Czas odpowiedzi (skala logarytmiczna)", fontsize=8)

        maksymalny_czas_odpowiedzi_dla_danej_wartosci_parametru = []
        for i in range(len(zbior_wartosci_parametru)):
            maksymalny_czas_odpowiedzi_dla_danej_wartosci_parametru.append(0)

        for lista_czasow in lista_list_czasow:
            for i in range(len(zbior_wartosci_parametru)):
                if maksymalny_czas_odpowiedzi_dla_danej_wartosci_parametru[i] < lista_czasow[i]:
                    maksymalny_czas_odpowiedzi_dla_danej_wartosci_parametru[i] = lista_czasow[i]

        lista_wyskalowanych_list_czasow = []
        for index_liczba_wezlow in range(len(zbior_liczb_wezlow)):
            wyskalowana_lista_czasow = []
            index_wartosc_parametru = 0
            for czas_odpowiedzi in lista_list_czasow[index_liczba_wezlow]:
                wyskalowana_lista_czasow.append(czas_odpowiedzi / maksymalny_czas_odpowiedzi_dla_danej_wartosci_parametru[index_wartosc_parametru])
                index_wartosc_parametru += 1
            lista_wyskalowanych_list_czasow.append(wyskalowana_lista_czasow)

        plt.subplot(nrows, ncols, 2 * ncols + index_poziom_jednorodnosci_fazy)
        plt.title("poziom_jednorodnosci_fazy=%s" % poziom_jednorodnosci_fazy)
        for indeks in range(len(zbior_liczb_wezlow)):
            liczba_wezlow = zbior_liczb_wezlow[indeks]
            lista_wyskalowanych_czasow_z_dana_liczba_wezlow = lista_wyskalowanych_list_czasow[indeks]
            plt.plot(zbior_wartosci_parametru, lista_wyskalowanych_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
        plt.legend(title="Liczba wezlow")
        plt.xlabel("Wartosc parametru", fontsize=8)
        plt.ylabel("Stosunek czasu odpowiedzi do maksymalnego czasu odpowiedzi dla danej wartosci parametru", fontsize=8)


        index_poziom_jednorodnosci_fazy += 1

    plt.savefig("Porownanie liczby wezlow (%s, %s).png" % (program_szeregujacy, parametr), dpi=300)


def main():
    # rysuj_wykres_porownania_liczby_wezlow("jnq", "obc", 1)
    # rysuj_wykresy_porownania_liczby_wezlow("jnq", "obc")
    # rysuj_wykresy_porownania_liczby_wezlow("jnq", "rozm")
    # rysuj_wykresy_porownania_liczby_wezlow("jnq", "przedk")
    # rysuj_wykresy_porownania_liczby_wezlow("jsq", "obc")
    # rysuj_wykresy_porownania_liczby_wezlow("jsq", "rozm")
    rysuj_wykresy_porownania_liczby_wezlow("jsq", "przedk")


if __name__ == "__main__":
    main()
