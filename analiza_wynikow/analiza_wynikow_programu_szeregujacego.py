# Skrypt przeznaczony do rysowania zaleznosci miedzy wynikami czasow uszeregowania uzyskanymi dzieki wskazanemu programowi szeregujacemu

import os
import re
import matplotlib.pyplot as plt


def porownaj_liczbe_wezlow():
    print("Porownuje liczbe wezlow...")


def wykryj_zbior_liczb_cykli(lista_nazw_uszeregowan):
    zbior_liczb_cykli = set()

    wzorzec_liczby_cykli = re.compile('.*c([0-9]*)\.txt')
    for nazwa_uszeregowania in lista_nazw_uszeregowan:
        wynik_dopasowania = wzorzec_liczby_cykli.match(nazwa_uszeregowania)
        if wynik_dopasowania is not None:
            zbior_liczb_cykli.add(int(wynik_dopasowania.group(1)))
    return sorted(zbior_liczb_cykli)


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

    wzorzec_wartosci_parametru = re.compile('.*-([0-9.]*)-c.*\\.txt')
    for nazwa_uszeregowania in lista_nazw_uszeregowan:
        wynik_dopasowania = wzorzec_wartosci_parametru.match(nazwa_uszeregowania)
        if wynik_dopasowania is not None:
            zbior_wartosci_parametru.add(float(wynik_dopasowania.group(1)))
    return sorted(zbior_wartosci_parametru)


def rysuj_wykres(program_szeregujacy, parametr, liczba_cykli):
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"\tliczba_cykli=%s" % (program_szeregujacy, parametr, liczba_cykli))
    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    wzorzec_wykorzystywanych_uszeregowan = re.compile('^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-c' + "%03d" % liczba_cykli + '\\.txt$')
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    lista_list_czasow = []
    for liczba_wezlow in zbior_liczb_wezlow:
        wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile('^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-c' + "%03d" % liczba_cykli + '\\.txt$')
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

    plt.title("program_szeregujacy=\"%s\" parametr=\"%s\" liczba_cykli=%s" % (program_szeregujacy, parametr, liczba_cykli))
    for indeks in range(len(zbior_liczb_wezlow)):
        liczba_wezlow = zbior_liczb_wezlow[indeks]
        lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
        plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
    plt.legend(title="Liczba wezlow")
    plt.show()


def rysuj_wykresy(program_szeregujacy, parametr):
    print("Rysuje wykres:\tprogram_szeregujacy=\"%s\"\tparametr=\"%s\"" % (program_szeregujacy, parametr))
    lista_nazw_uszeregowan = os.listdir("../uszeregowanie")
    wzorzec_wykorzystywanych_uszeregowan = re.compile('^szer-' + program_szeregujacy + '-n[0-9]*-inst-' + parametr + '-[0-9.]*-c[0-9]*\\.txt$')
    lista_wykorzystywanych_uszeregowan = list(filter(wzorzec_wykorzystywanych_uszeregowan.match, lista_nazw_uszeregowan))

    zbior_liczb_cykli = wykryj_zbior_liczb_cykli(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb cykli: " + str(zbior_liczb_cykli))

    zbior_liczb_wezlow = wykryj_zbior_liczb_wezlow(lista_wykorzystywanych_uszeregowan)
    print("Zbior liczb wezlow: " + str(zbior_liczb_wezlow))

    zbior_wartosci_parametru = wykryj_zbior_wartosci_parametru(lista_wykorzystywanych_uszeregowan)
    print("Zbior wartosci parametru: " + str(zbior_wartosci_parametru))

    index_liczba_cykli = 1
    ncols = len(zbior_liczb_cykli)
    nrows = 1
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("program_szeregujacy=\"%s\" | parametr=\"%s\"" % (program_szeregujacy, parametr), fontsize=30, y=0.92)
    for liczba_cykli in zbior_liczb_cykli:
        lista_list_czasow = []
        for liczba_wezlow in zbior_liczb_wezlow:
            wzorzec_uszeregowan_z_dana_liczba_wezlow = re.compile('^szer-' + program_szeregujacy + '-n' + "%03d" % liczba_wezlow + '-inst-' + parametr + '-[0-9.]*-c' + "%03d" % liczba_cykli + '\\.txt$')
            lista_uszeregowan_z_dana_liczba_wezlow = list(filter(wzorzec_uszeregowan_z_dana_liczba_wezlow.match, lista_wykorzystywanych_uszeregowan))
            lista_czasow_z_dana_liczba_wezlow = []
            for uszeregowanie in lista_uszeregowan_z_dana_liczba_wezlow:
                nazwa_pliku_wejsciowego = '../uszeregowanie/' + uszeregowanie
                print(str(liczba_wezlow) + ":\t" + str(nazwa_pliku_wejsciowego))
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

        plt.subplot(nrows, ncols, index_liczba_cykli)
        plt.title("liczba_cykli=%s" % liczba_cykli)
        for indeks in range(len(zbior_liczb_wezlow)):
            liczba_wezlow = zbior_liczb_wezlow[indeks]
            lista_czasow_z_dana_liczba_wezlow = lista_list_czasow[indeks]
            plt.plot(zbior_wartosci_parametru, lista_czasow_z_dana_liczba_wezlow, color=mapa_kolorow[indeks], label=str(liczba_wezlow))
        plt.legend(title="Liczba wezlow")

        index_liczba_cykli += 1

    plt.savefig("Porownanie liczby wezlow (%s, %s).png" % (program_szeregujacy, parametr), dpi=300)


def main():
    # rysuj_wykres("jnq", "obc", 1)
    rysuj_wykresy("jnq", "obc")


if __name__ == "__main__":
    main()
