# Skrypt przeznaczony do rysowania wykresow ukazujacych dlaczego zachodzi zmiana danego wspolczynnika

import matplotlib.pyplot as plt
import numpy as np
import os
import re
import math


def rysuj_przyczyne_zmiennosci_czasow_przedkladania(liczba_cykli):
    print("Rysowanie histogramow wartosci czasow przedkladania...")
    lista_nazw_instancji = os.listdir("../instancje")

    wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9\.]*-c' + "%03d" % (liczba_cykli) + '\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))

    ncols = 2
    nrows = 2 * math.ceil(len(lista_nazw_inst_przedk) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Histogramy wartosci czasow przedkladania (liczba cykli: " + str(liczba_cykli) + ")", fontsize=30, y=0.92)
    colors = ["blue", "red", "orange", "green"]

    index_nazwa_inst_przedk = 1
    for nazwa_inst_przedk in lista_nazw_inst_przedk:
        print("Trwa przetwarzanie instancji: " + nazwa_inst_przedk)
        zadania = []
        f = open(file="../instancje/" + nazwa_inst_przedk, mode="r")
        for line in f:
            zadania.append(line.split(' '))
        f.close()

        lista_momentow_gotowosci = []
        for zadanie in zadania:
            lista_momentow_gotowosci.append(int(zadanie[0]))

        liczba_zadan = len(lista_momentow_gotowosci)
        lista_krotkich_czasow_przedkladania = []
        lista_dlugich_czasow_przedkladania = []
        poprzedni_moment_gotowosci = 0
        for i in range(liczba_zadan):
            moment_gotowosci = lista_momentow_gotowosci[i]
            if (i // (liczba_zadan / (2 * liczba_cykli))) % 2 == 0:
                lista_krotkich_czasow_przedkladania.append(moment_gotowosci - poprzedni_moment_gotowosci)
            else:
                lista_dlugich_czasow_przedkladania.append(moment_gotowosci - poprzedni_moment_gotowosci)
            poprzedni_moment_gotowosci = moment_gotowosci

        np_krotkie_czasy_przedkladania = np.array(lista_krotkich_czasow_przedkladania)
        np_dlugie_czasy_przedkladania = np.array(lista_dlugich_czasow_przedkladania)
        graniczny_precentyl = 90
        xlim_max = max(np.percentile(np_krotkie_czasy_przedkladania, graniczny_precentyl), np.percentile(np_dlugie_czasy_przedkladania, graniczny_precentyl))

        np_krotkie_czasy_przedkladania = np_krotkie_czasy_przedkladania[np_krotkie_czasy_przedkladania <= xlim_max]
        np_dlugie_czasy_przedkladania = np_dlugie_czasy_przedkladania[np_dlugie_czasy_przedkladania <= xlim_max]

        plt.subplot(nrows, ncols, index_nazwa_inst_przedk * 2 + index_nazwa_inst_przedk % 2 - 2)
        plt.hist(np_krotkie_czasy_przedkladania, bins=200, color=colors[(index_nazwa_inst_przedk - 1) % 4])
        plt.title(nazwa_inst_przedk + " (krotkie czasy przedkladania)")
        plt.xlabel('Czas przedkładania', fontsize=8)
        plt.ylabel('Liczba wystapien', fontsize=8)
        ax = plt.gca()
        ax.set_xlim([0, xlim_max])
        [y1_bottom, y1_top] = ax.get_ylim()

        plt.subplot(nrows, ncols, index_nazwa_inst_przedk * 2 + index_nazwa_inst_przedk % 2)
        plt.hist(np_dlugie_czasy_przedkladania, bins=200, color=colors[(index_nazwa_inst_przedk - 1) % 4])
        plt.title(nazwa_inst_przedk + " (dlugie czasy przedkladania)")
        plt.xlabel('Czas przedkładania', fontsize=8)
        plt.ylabel('Liczba wystapien', fontsize=8)
        ax = plt.gca()
        ax.set_xlim([0, xlim_max])
        [y2_bottom, y2_top] = ax.get_ylim()

        if y1_top > y2_top:
            ax.set_ylim([y2_bottom, y1_top])
        elif y1_top < y2_top:
            plt.subplot(nrows, ncols, index_nazwa_inst_przedk * 2 + index_nazwa_inst_przedk % 2 - 2)
            ax.set_ylim([y1_bottom, y2_top])

        index_nazwa_inst_przedk += 1

    plt.savefig("Przyczyna zmiennosci czasow przedkladania.png", dpi=300)


def rysuj_przyczyne_zmiennosci_rozmiarow(liczba_cykli):
    print("Rysowanie histogramow wartosci rozmiarow...")
    lista_nazw_instancji = os.listdir("../instancje")

    wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9\.]*-c' + "%03d" % (liczba_cykli) + '\.txt$')
    lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))

    ncols = 2
    nrows = math.ceil(len(lista_nazw_inst_rozm) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Histogramy wartosci rozmiarow (liczba cykli: " + str(liczba_cykli) + ")", fontsize=30, y=0.92)

    index_nazwa_inst_rozm = 1
    for nazwa_inst_rozm in lista_nazw_inst_rozm:
        print("Trwa przetwarzanie instancji: " + nazwa_inst_rozm)
        zadania = []
        f = open(file="../instancje/" + nazwa_inst_rozm, mode="r")
        for line in f:
            zadania.append(line.split(' '))
        f.close()

        lista_czasow_trwania = []
        for zadanie in zadania:
            lista_czasow_trwania.append(int(zadanie[1]))

        plt.subplot(nrows, ncols, index_nazwa_inst_rozm)
        plt.hist(lista_czasow_trwania, bins=200)

        ax = plt.gca()
        ax.set_xlim([0, 25000])
        ax.set_ylim([0, 2000])
        plt.title(nazwa_inst_rozm, fontsize=12)
        plt.xlabel('Rozmiar zadania', fontsize=8)
        plt.ylabel('Liczba wystapien', fontsize=8)

        index_nazwa_inst_rozm += 1

    plt.savefig("Przyczyna zmiennosci rozmiarow.png", dpi=300)


def main():
    # rysuj_przyczyne_zmiennosci_czasow_przedkladania(1)
    rysuj_przyczyne_zmiennosci_rozmiarow(1)


if __name__ == "__main__":
    main()
