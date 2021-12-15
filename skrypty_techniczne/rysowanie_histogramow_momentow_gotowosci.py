# Skrypt przeznaczony do zbadania wplywu rozsuwania srednich skladowych czasow przedkladania i powiekszania ich odchylen standardowych
# w celu uzyskania coraz to wiekszego wspolczynnika zmiennosci czasow przedkladania

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import math


def rysuj_histogramy_momentow_gotowosci(poziom_jednorodnosci):
    print("Rysowanie histogramow momentow gotowosci...")
    lista_nazw_instancji = os.listdir("../instancje")

    wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci + '\\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
    print(lista_nazw_inst_przedk)

    ncols = 2
    nrows = math.ceil(len(lista_nazw_inst_przedk) / ncols)
    plt.rcParams["figure.figsize"] = (ncols * 10, nrows * 7)
    plt.suptitle("Histogramy momentow gotowosci (poziom_jednorodnosci: " + str(poziom_jednorodnosci) + ")", fontsize=30, y=0.92)

    index_nazwa_inst_przedk = 1
    for nazwa_inst_przedk in lista_nazw_inst_przedk:
        print("Trwa przetwarzanie instancji: " + nazwa_inst_przedk)
        zadania = []
        f = open(file="../instancje/" + nazwa_inst_przedk, mode="r")
        for line in f:
            zadania.append(line.split(' '))
        f.close()

        momenty_gotowosci_lista = []
        for zadanie in zadania:
            momenty_gotowosci_lista.append(int(zadanie[0]))

        czasy_miedzy_przedkladaniem = []
        poprzedni_moment_gotowosci = 0
        for moment_gotowosci in momenty_gotowosci_lista:
            czasy_miedzy_przedkladaniem.append(moment_gotowosci - poprzedni_moment_gotowosci)
            poprzedni_moment_gotowosci = moment_gotowosci

        np_momenty_gotowosci = np.array(momenty_gotowosci_lista)
        np_czasy_miedzy_przedkladaniem = np.array(czasy_miedzy_przedkladaniem)

        pd_czasy_miedzy_przedkladaniem = pd.DataFrame(np_czasy_miedzy_przedkladaniem)

        print("pd_czasy_miedzy_przedkladaniem.describe():")
        print(pd_czasy_miedzy_przedkladaniem.describe())

        plt.subplot(nrows, ncols, index_nazwa_inst_przedk)
        plt.hist(np_momenty_gotowosci, bins=400)
        ax = plt.gca()
        ax.set_xlim([0, 150000000])
        ax.set_ylim([0, 600])
        plt.title(nazwa_inst_przedk)
        plt.xlabel('Czas', fontsize=8)
        plt.ylabel('Liczba wystapien', fontsize=8)

        index_nazwa_inst_przedk += 1

    plt.savefig("Histogramy momentow gotowosci.png", dpi=300)


def main():
    rysuj_histogramy_momentow_gotowosci(0.8)


if __name__ == "__main__":
    main()
