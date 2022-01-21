# Skrypt przeznaczony do wygenerowania wykresow, ktore sa potrzebne dla wykonania raportu

import matplotlib.pyplot as plt
import numpy as np
import os
import re


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


def rysuj_wykres_obciazenia():
    print("Rysowanie wykresu obciazenia systemu...")
    plt.rcParams['text.usetex'] = True
    lista_nazw_instancji = os.listdir("../instancje")

    poziom_jednorodnosci_fazy = 0.7

    wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
    wspolczynniki_obciazenia_inst_rozm = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_rozm]
    print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_obciazenia_inst_rozm))

    wzorzec_inst_obc = re.compile('^inst-obc-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
    wspolczynniki_obciazenia_inst_obc = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_obc]
    print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_obciazenia_inst_obc))

    wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
    wspolczynniki_obciazenia_inst_przedk = [oblicz_wspolczynnik_obciazenia_instancji(x) for x in lista_nazw_inst_przedk]
    print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_obciazenia_inst_przedk))

    plt.title(r"$\rho$ - obciażenie systemu")

    ax1 = plt.gca()
    line_rozm, = ax1.plot(wspolczynniki_obciazenia_inst_rozm, color='lightgreen', label=r'$w_p$', marker='.')
    ax1.axes.xaxis.set_ticks([])
    ax1.grid(axis='y', linestyle='--', linewidth=0.5)
    ax1.set_yticks(np.arange(0.5, 0.96, 0.05))
    ax1.set_xlabel(r"Kolejne instancje w danej grupie")
    ax1.set_ylabel(r"Wartość współczynnika $\rho$")

    ax2 = ax1.twiny()
    line_obc, = ax2.plot(wspolczynniki_obciazenia_inst_obc, color='blue', label=r'$\rho$', marker='.')
    ax2.axes.xaxis.set_ticks([])

    ax3 = ax2.twiny()
    line_przedk, = ax3.plot(wspolczynniki_obciazenia_inst_przedk, color='red', label=r'$w_t$', marker='.')
    ax3.axes.xaxis.set_ticks([])

    leg = plt.legend(handles=[line_rozm, line_obc, line_przedk], loc="upper left", title=r"Grupa instancji o zmiennej wartości parametru:")
    leg._legend_box.align = "left"

    plt.savefig("Raport_obciazenie_systemu.png", dpi=600)


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


def rysuj_wykres_wspolczynnika_zmiennosci_czasow_przedkladania():
    print("Rysowanie wykresu wspolczynnika zmiennosci czasow przedkladania...")
    plt.rcParams['text.usetex'] = True
    lista_nazw_instancji = os.listdir("../instancje")

    poziom_jednorodnosci_fazy = 1.0

    wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_rozm]
    print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm))

    wzorzec_inst_obc = re.compile('^inst-obc-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_obc]
    print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc))

    wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9.]*-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk = [oblicz_wspolczynnik_zmiennosci_czasow_przedkladania(x) for x in lista_nazw_inst_przedk]
    print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk))

    plt.title(r"$w_t$ - współczynnik zmienności czasów miedzy przedkładaniem zadań")

    ax1 = plt.gca()
    line_rozm, = ax1.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_rozm, color='lightgreen', label=r'$w_p$', marker='.')
    ax1.axes.xaxis.set_ticks([])
    ax1.grid(axis='y', linestyle='--', linewidth=0.5)
    ax1.set_yticks(np.arange(0.2, 1.21, 0.1))
    ax1.set_xlabel(r"Kolejne instancje w danej grupie")
    ax1.set_ylabel(r"Wartość współczynnika $w_t$")

    ax2 = ax1.twiny()
    line_obc, = ax2.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_obc, color='blue', label=r'$\rho$', marker='.')
    ax2.axes.xaxis.set_ticks([])

    ax3 = ax2.twiny()
    line_przedk, = ax3.plot(wspolczynniki_zmiennosci_czasow_przedkladania_inst_przedk, color='red', label=r'$w_t$', marker='.')
    ax3.axes.xaxis.set_ticks([])

    leg = plt.legend(handles=[line_rozm, line_obc, line_przedk], loc="upper left", title=r"Grupa instancji o zmiennej wartości parametru:")
    leg._legend_box.align = "left"

    plt.savefig("Raport_wspolczynnik_zmiennosci_czasow_miedzy_przedkladaniem.png", dpi=600)


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


def rysuj_wykres_wspolczynnika_zmiennosci_rozmiarow():
    print("Rysowanie wykresu wspolczynnika zmiennosci rozmiarow...")
    plt.rcParams['text.usetex'] = True
    lista_nazw_instancji = os.listdir("../instancje")

    poziom_jednorodnosci_fazy = 0.5

    wzorzec_inst_rozm = re.compile('^inst-rozm-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
    lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_rozmiarow_inst_rozm = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_rozm]
    print(wzorzec_inst_rozm.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_rozm))

    wzorzec_inst_obc = re.compile('^inst-obc-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
    lista_nazw_inst_obc = list(filter(wzorzec_inst_obc.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_rozmiarow_inst_obc = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_obc]
    print(wzorzec_inst_obc.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_obc))

    wzorzec_inst_przedk = re.compile('^inst-przedk-[0-9.]*-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
    wspolczynniki_zmiennosci_rozmiarow_inst_przedk = [oblicz_wspolczynnik_zmiennosci_rozmiarow(x) for x in lista_nazw_inst_przedk]
    print(wzorzec_inst_przedk.pattern + "\t" + str(wspolczynniki_zmiennosci_rozmiarow_inst_przedk))

    plt.title(r"$w_p$ - współczynnik zmienności rozmiarów zadań")

    ax1 = plt.gca()
    line_rozm, = ax1.plot(wspolczynniki_zmiennosci_rozmiarow_inst_rozm, color='lightgreen', label=r'$w_p$', marker='.')
    ax1.axes.xaxis.set_ticks([])
    ax1.grid(axis='y', linestyle='--', linewidth=0.5)
    ax1.set_yticks(np.arange(0.5, 4.01, 0.5))
    ax1.set_xlabel(r"Kolejne instancje w danej grupie")
    ax1.set_ylabel(r"Wartość współczynnika $w_p$")

    ax2 = ax1.twiny()
    line_obc, = ax2.plot(wspolczynniki_zmiennosci_rozmiarow_inst_obc, color='blue', label=r'$\rho$', marker='.')
    ax2.axes.xaxis.set_ticks([])

    ax3 = ax2.twiny()
    line_przedk, = ax3.plot(wspolczynniki_zmiennosci_rozmiarow_inst_przedk, color='red', label=r'$w_t$', marker='.')
    ax3.axes.xaxis.set_ticks([])

    leg = plt.legend(handles=[line_rozm, line_obc, line_przedk], loc="upper left", title=r"Grupa instancji o zmiennej wartości parametru:")
    leg._legend_box.align = "left"

    plt.savefig("Raport_wspolczynnik_zmiennosci_rozmiarow.png", dpi=600)


def rysuj_przyczyne_zmiennosci_rozmiarow():
    print("Rysowanie histogramow wartosci rozmiarow...")
    lista_nazw_instancji = os.listdir("../instancje")
    plt.rcParams['text.usetex'] = True

    poziom_jednorodnosci_fazy = 0.6

    wzorzec_inst_rozm = re.compile('^inst-rozm-([0-9.]*)-j' + "%.1f" % (poziom_jednorodnosci_fazy) + '\\.txt$')
    lista_nazw_inst_rozm = list(filter(wzorzec_inst_rozm.match, lista_nazw_instancji))
    lista_nazw_inst_rozm = [lista_nazw_inst_rozm[1], lista_nazw_inst_rozm[3], lista_nazw_inst_rozm[5]]

    plt.title(r"Histogram rozmiarów zadań dla danej instancji")

    plt.xlabel('Rozmiar zadania', fontsize=10)
    plt.ylabel('Liczba wystapień', fontsize=10)

    xlim_max = 20000

    ax = plt.gca()
    ax.set_xlim([0, xlim_max])
    ax.set_ylim([0, 1000])

    colors = np.linspace(1.0, 0.5, num=len(lista_nazw_inst_rozm))

    for idx in range(len(lista_nazw_inst_rozm)):
        nazwa_inst_rozm = lista_nazw_inst_rozm[idx]
        print("Trwa przetwarzanie instancji: " + nazwa_inst_rozm)
        zadania = []
        f = open(file="../instancje/" + nazwa_inst_rozm, mode="r")
        for line in f:
            zadania.append(line.split(' '))
        f.close()

        lista_czasow_trwania = []
        for zadanie in zadania:
            lista_czasow_trwania.append(int(zadanie[1]))

        np_czasy_trwania = np.array(lista_czasow_trwania)
        np_czasy_trwania = np_czasy_trwania[np_czasy_trwania <= xlim_max]

        wynik_dopasowania = wzorzec_inst_rozm.match(nazwa_inst_rozm)
        wspolczynnik_zmiennosci_rozmiarow = float(wynik_dopasowania.group(1))
        plt.hist(np_czasy_trwania, bins=200, color=(0.0, colors[idx], 0.0), alpha=0.7, label=r"$w_p = %.1f$" % wspolczynnik_zmiennosci_rozmiarow)

    leg = plt.legend(loc="upper right", title=r"Instancja z wartościa parametru:")
    leg._legend_box.align = "right"

    plt.savefig("Raport_uzyskanie_okreslonego_wspolczynnika_zmiennosc_rozmiarow_zadan.png", dpi=600)


def rysuj_przyczyne_zmiennosci_czasow_miedzy_przedkladaniem():
    print("Rysowanie histogramow wartosci czasow miedzy przedkladaniem...")
    lista_nazw_instancji = os.listdir("../instancje")
    plt.rcParams['text.usetex'] = True

    poziom_jednorodnosci_fazy = 1.0

    wzorzec_inst_przedk = re.compile('^inst-przedk-([0-9.]*)-j' + "%.1f" % poziom_jednorodnosci_fazy + '\\.txt$')
    lista_nazw_inst_przedk = list(filter(wzorzec_inst_przedk.match, lista_nazw_instancji))
    lista_nazw_inst_przedk = [lista_nazw_inst_przedk[1], lista_nazw_inst_przedk[4], lista_nazw_inst_przedk[7]]

    plt.title(r"Histogram czasów miedzy przedkładaniem zadań dla danej instancji")

    plt.xlabel('Czas miedzy przedkładaniem zadań', fontsize=10)
    plt.ylabel('Liczba wystapień', fontsize=10)

    xlim_max = 3000

    ax = plt.gca()
    ax.set_xlim([0, xlim_max])
    ax.set_ylim([0, 2000])

    colors = np.linspace(1.0, 0.5, num=len(lista_nazw_inst_przedk))

    for idx in range(len(lista_nazw_inst_przedk)):
        nazwa_inst_przedk = lista_nazw_inst_przedk[idx]
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
        lista_czasow_przedkladania = []
        poprzedni_moment_gotowosci = 0
        for i in range(liczba_zadan):
            moment_gotowosci = lista_momentow_gotowosci[i]
            lista_czasow_przedkladania.append(moment_gotowosci - poprzedni_moment_gotowosci)
            poprzedni_moment_gotowosci = moment_gotowosci

        np_czasy_przedkladania = np.array(lista_czasow_przedkladania)
        np_czasy_przedkladania = np_czasy_przedkladania[np_czasy_przedkladania <= xlim_max]

        wynik_dopasowania = wzorzec_inst_przedk.match(nazwa_inst_przedk)
        wspolczynnik_zmiennosci_czasow_miedzy_przedkladanie = float(wynik_dopasowania.group(1))
        plt.hist(np_czasy_przedkladania, bins=200, color=(colors[idx], 0.0, 0.0), alpha=0.6, label=r"$w_t = %.1f$" % wspolczynnik_zmiennosci_czasow_miedzy_przedkladanie)

    leg = plt.legend(loc="upper right", title=r"Instancja z wartościa parametru:")
    leg._legend_box.align = "right"

    plt.savefig("Raport_uzyskanie_okreslonego_wspolczynnika_zmiennosci_czasow_miedzy_przedkladaniem.png", dpi=600)


def rysuj_skutek_poziomu_jednorodnosci_fazy():
    print("Rysowanie histogramow momentow gotowosci...")
    lista_nazw_instancji = os.listdir("../instancje")
    plt.rcParams['text.usetex'] = True

    wzorzec_inst_jedn = re.compile('^inst-obc-0.75-j([0-9.]*)\\.txt$')
    lista_nazw_inst_jedn = list(filter(wzorzec_inst_jedn.match, lista_nazw_instancji))
    print(lista_nazw_inst_jedn)
    lista_nazw_inst_jedn = [lista_nazw_inst_jedn[0], lista_nazw_inst_jedn[2], lista_nazw_inst_jedn[5]]

    plt.title(r"Histogram momentów gotowości zadań dla danej instancji")

    plt.xlabel('Czas', fontsize=10)
    plt.ylabel('Liczba wystapień', fontsize=10)

    colors = np.linspace(1.0, 0.0, num=len(lista_nazw_inst_jedn))

    for idx in range(len(lista_nazw_inst_jedn)):
        nazwa_inst_jedn = lista_nazw_inst_jedn[idx]
        print("Trwa przetwarzanie instancji: " + nazwa_inst_jedn)
        zadania = []
        f = open(file="../instancje/" + nazwa_inst_jedn, mode="r")
        for line in f:
            zadania.append(line.split(' '))
        f.close()

        lista_momentow_gotowosci = []
        for zadanie in zadania:
            lista_momentow_gotowosci.append(int(zadanie[0]))

        np_momenty_gotowosci = np.array(lista_momentow_gotowosci)

        wynik_dopasowania = wzorzec_inst_jedn.match(nazwa_inst_jedn)
        poziom_jednorodnosci = float(wynik_dopasowania.group(1))
        plt.hist(np_momenty_gotowosci, bins=400, color=(0.0, 0.0, colors[idx]), alpha=0.5, label=r"$l_f = %.1f$" % poziom_jednorodnosci)

    leg = plt.legend(loc="upper right", title=r"Instancja z wartościa parametru:")
    leg._legend_box.align = "right"

    plt.savefig("Raport_skutek_poziomu_jednorodnosci.png", dpi=600)


def main():
    # rysuj_wykres_wspolczynnika_zmiennosci_rozmiarow()
    # rysuj_wykres_obciazenia()
    # rysuj_wykres_wspolczynnika_zmiennosci_czasow_przedkladania()
    # rysuj_przyczyne_zmiennosci_rozmiarow()
    # rysuj_przyczyne_zmiennosci_czasow_miedzy_przedkladaniem()
    rysuj_skutek_poziomu_jednorodnosci_fazy()

if __name__ == "__main__":
    main()
