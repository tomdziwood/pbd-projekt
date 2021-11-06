# Skrypt przeznaczony do zbadania charakterystyki rozmiarow i czasow przedkladania zadan dla podanej instancji.
# Mozliwe rowniez badanie charakterystyk danych zbiorow instancji

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import math


def rysuj_charakterystyki_danej_instancji():
    liczba_zadan = 10000
    zadania = []
    f = open(file="../instancje/inst-obc-80-f2.txt", mode="r")
    for _ in range(liczba_zadan):
        zadania.append(f.readline().split(' '))
    f.close()

    momenty_gotowosci_lista = []
    czasy_trwania_lista = []
    for zadanie in zadania:
        momenty_gotowosci_lista.append(int(zadanie[0]))
        czasy_trwania_lista.append(int(zadanie[1]))

    czasy_miedzy_przedkladaniem = []
    poprzedni_moment_gotowosci = 0
    for moment_gotowosci in momenty_gotowosci_lista:
        czasy_miedzy_przedkladaniem.append(moment_gotowosci - poprzedni_moment_gotowosci)
        poprzedni_moment_gotowosci = moment_gotowosci

    np_momenty_gotowosci = np.array(momenty_gotowosci_lista)
    np_czasy_trwania = np.array(czasy_trwania_lista)
    np_czasy_miedzy_przedkladaniem = np.array(czasy_miedzy_przedkladaniem)

    pd_momenty_gotowosci = pd.DataFrame(np_momenty_gotowosci)
    pd_czasy_trwania = pd.DataFrame(np_czasy_trwania)
    pd_czasy_miedzy_przedkladaniem = pd.DataFrame(np_czasy_miedzy_przedkladaniem)

    print("pd_momenty_gotowosci.describe():")
    print(pd_momenty_gotowosci.describe())
    print("pd_czasy_trwania.describe():")
    print(pd_czasy_trwania.describe())
    print("pd_czasy_miedzy_przedkladaniem.describe():")
    print(pd_czasy_miedzy_przedkladaniem.describe())

    plt.subplot(2, 2, 1)
    plt.hist(np_momenty_gotowosci, bins=200)
    plt.title("momenty gotowosci")

    plt.subplot(2, 2, 2)
    plt.hist(np_czasy_trwania, bins=200)
    plt.title("czasy trwania")

    plt.subplot(2, 2, 3)
    plt.hist(np_czasy_miedzy_przedkladaniem, bins=200)
    plt.title("czas do przedlozenia kolejnego zadania")

    plt.show()


def wykryj_zbior_liczb_faz():
    zbior_liczb_faz = set()

    lista_nazw_instancji = os.listdir("../instancje")
    wzorzec_liczby_faz = re.compile('.*f([0-9]*)\.txt')
    for nazwa_instancji in lista_nazw_instancji:
        wynik_dopasowania = wzorzec_liczby_faz.match(nazwa_instancji)
        if wynik_dopasowania is not None:
            zbior_liczb_faz.add(int(wynik_dopasowania.group(1)))
    return sorted(zbior_liczb_faz)


def oblicz_wspolczynnik_obciazenia_instancji(nazwa_instancji):
    zadania = []
    f = open(file="../instancje/" + nazwa_instancji, mode="r")
    for line in f:
        zadania.append(line.split(' '))
    f.close()

    lista_momentow_gotowosci = []
    lista_czasow_trwania = []
    for zadanie in zadania:
        lista_momentow_gotowosci.append(int(zadanie[0]))
        lista_czasow_trwania.append(int(zadanie[1]))

    lista_czasow_przedkladania = []
    poprzedni_moment_gotowosci = 0
    for moment_gotowosci in lista_momentow_gotowosci:
        lista_czasow_przedkladania.append(moment_gotowosci - poprzedni_moment_gotowosci)
        poprzedni_moment_gotowosci = moment_gotowosci

    return np.mean(lista_czasow_trwania) / np.mean(lista_czasow_przedkladania)


def rysuj_wykresy_wspolczynnika_obciazenia_systemu():
    print("Rysowanie wykresow wspolczynnika obciazenia systemu...")
    zbior_liczb_faz = wykryj_zbior_liczb_faz()
    lista_nazw_instancji = os.listdir("../instancje")
    index_liczba_faz = 1
    ncols = 2
    nrows = math.ceil(len(zbior_liczb_faz) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Wspolczynnik obciazenia systemu", fontsize=30, y=0.92)
    for liczba_faz in zbior_liczb_faz:
        wzorzec_inst_obc = re.compile('^inst-obc-[0-9]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
        wspolczynniki_obciazenia_inst_obc = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_obc]
        print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_obciazenia_inst_obc))

        wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
        wspolczynniki_obciazenia_inst_przedk = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_przedk]
        print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_obciazenia_inst_przedk))

        wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
        wspolczynniki_obciazenia_inst_rozm = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_rozm]
        print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_obciazenia_inst_rozm))

        plt.subplot(nrows, ncols, index_liczba_faz)
        plt.title("Liczba faz: " + str(liczba_faz))

        ax1 = plt.gca()
        line_obc, = ax1.plot(wspolczynniki_obciazenia_inst_obc, color='blue', label='obc', marker='.')
        ax1.axes.xaxis.set_ticks([])
        ax1.grid(axis='y', linestyle='--', linewidth=0.5)
        ax1.set_yticks(np.arange(0.5, 0.96, 0.05))

        ax2 = ax1.twiny()
        line_przedk, = ax2.plot(wspolczynniki_obciazenia_inst_przedk, color='red', label='przedk', marker='.')
        ax2.axes.xaxis.set_ticks([])

        ax3 = ax2.twiny()
        line_rozm, = ax3.plot(wspolczynniki_obciazenia_inst_rozm, color='lightgreen', label='rozm', marker='.')
        ax3.axes.xaxis.set_ticks([])

        plt.legend(handles=[line_obc, line_przedk, line_rozm], loc="upper left")

        index_liczba_faz += 1

    plt.savefig("Wspolczynnik obciazenia systemu.png", dpi=300)


def oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(nazwa_instancji):
    zadania = []
    f = open(file="../instancje/" + nazwa_instancji, mode="r")
    for line in f:
        zadania.append(line.split(' '))
    f.close()

    lista_momentow_gotowosci = []
    for zadanie in zadania:
        lista_momentow_gotowosci.append(int(zadanie[0]))

    lista_czasow_przedkladania = []
    poprzedni_moment_gotowosci = 0
    for moment_gotowosci in lista_momentow_gotowosci:
        lista_czasow_przedkladania.append(moment_gotowosci - poprzedni_moment_gotowosci)
        poprzedni_moment_gotowosci = moment_gotowosci

    return np.std(lista_czasow_przedkladania) / np.mean(lista_czasow_przedkladania)


def rysuj_wykresy_wspolczynnika_zmiennosci_czasow_przedkladania():
    print("Rysowanie wykresow wspolczynnika zmiennosci czasow przedkladania...")
    zbior_liczb_faz = wykryj_zbior_liczb_faz()
    lista_nazw_instancji = os.listdir("../instancje")
    index_liczba_faz = 1
    ncols = 2
    nrows = math.ceil(len(zbior_liczb_faz) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Wspolczynnik zmiennosci czasow przedkladania", fontsize=30, y=0.92)
    for liczba_faz in zbior_liczb_faz:
        wzorzec_inst_obc = re.compile('^inst-obc-[0-9]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_obc]
        print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc))

        wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_przedk]
        print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk))

        wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_rozm]
        print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm))

        plt.subplot(nrows, ncols, index_liczba_faz)
        plt.title("Liczba faz: " + str(liczba_faz))

        ax1 = plt.gca()
        line_obc, = ax1.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc, color='blue', label='obc', marker='.')
        ax1.axes.xaxis.set_ticks([])
        ax1.grid(axis='y', linestyle='--', linewidth=0.5)
        ax1.set_yticks(np.arange(0.5, 3.01, 0.25))

        ax2 = ax1.twiny()
        line_przedk, = ax2.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk, color='red', label='przedk', marker='.')
        ax2.axes.xaxis.set_ticks([])

        ax3 = ax2.twiny()
        line_rozm, = ax3.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm, color='lightgreen', label='rozm', marker='.')
        ax3.axes.xaxis.set_ticks([])

        plt.legend(handles=[line_obc, line_przedk, line_rozm], loc="upper left")

        index_liczba_faz += 1

    plt.savefig("Wspolczynnik zmiennosci czasow przedkladania.png", dpi=300)


def oblicz_wspolczynnik_zmiennosci_rozmiarow(nazwa_instancji):
    zadania = []
    f = open(file="../instancje/" + nazwa_instancji, mode="r")
    for line in f:
        zadania.append(line.split(' '))
    f.close()

    lista_czasow_trwania = []
    for zadanie in zadania:
        lista_czasow_trwania.append(int(zadanie[1]))

    return np.std(lista_czasow_trwania) / np.mean(lista_czasow_trwania)


def rysuj_wykresy_wspolczynnika_zmiennosci_rozmiarow():
    print("Rysowanie wykresow wspolczynnika zmiennosci czasow przedkladania...")
    zbior_liczb_faz = wykryj_zbior_liczb_faz()
    lista_nazw_instancji = os.listdir("../instancje")
    index_liczba_faz = 1
    ncols = 2
    nrows = math.ceil(len(zbior_liczb_faz) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Wspolczynnik zmiennosci rozmiarow", fontsize=30, y=0.92)
    for liczba_faz in zbior_liczb_faz:
        wzorzec_inst_obc = re.compile('^inst-obc-[0-9]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_rozmiarow_inst_obc = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_obc]
        print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_obc))

        wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_rozmiarow_inst_przedk = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_przedk]
        print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_przedk))

        wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9\.]*-f' + str(liczba_faz) + '\.txt$')
        lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
        wspolczynniki_zmiennosci_rozmiarow_inst_rozm = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_rozm]
        print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_rozm))

        plt.subplot(nrows, ncols, index_liczba_faz)
        plt.title("Liczba faz: " + str(liczba_faz))

        ax1 = plt.gca()
        line_obc, = ax1.plot(wspolczynniki_zmiennosci_rozmiarow_inst_obc, color='blue', label='obc', marker='.')
        ax1.axes.xaxis.set_ticks([])
        ax1.grid(axis='y', linestyle='--', linewidth=0.5)
        ax1.set_yticks(np.arange(0.5, 4.01, 0.5))

        ax2 = ax1.twiny()
        line_przedk, = ax2.plot(wspolczynniki_zmiennosci_rozmiarow_inst_przedk, color='red', label='przedk', marker='.')
        ax2.axes.xaxis.set_ticks([])

        ax3 = ax2.twiny()
        line_rozm, = ax3.plot(wspolczynniki_zmiennosci_rozmiarow_inst_rozm, color='lightgreen', label='rozm', marker='.')
        ax3.axes.xaxis.set_ticks([])

        plt.legend(handles=[line_obc, line_przedk, line_rozm], loc="upper left")

        index_liczba_faz += 1

    plt.savefig("Wspolczynnik zmiennosci rozmiarow.png", dpi=300)


def main():
    # rysuj_charakterystyki_danej_instancji()
    # rysuj_wykresy_wspolczynnika_obciazenia_systemu()
    # rysuj_wykresy_wspolczynnika_zmiennosci_czasow_przedkladania()
    rysuj_wykresy_wspolczynnika_zmiennosci_rozmiarow()


if __name__ == "__main__":
    main()
