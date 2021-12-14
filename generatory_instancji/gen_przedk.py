from gen_inst import generuj_instancje


def main():
    poziomy_jednorodnosci_fazy = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for wzp_tmp in range(2, 13, 1):
        wspolczynnik_zmiennosci_przedkladania = wzp_tmp / 10
        for poziom_jednorodnosci_fazy in poziomy_jednorodnosci_fazy:
            nazwa_pliku_wyjsciowego = "../instancje/inst-przedk-" + "%.1f" % (wspolczynnik_zmiennosci_przedkladania) + "-j" + "%.1f" % (poziom_jednorodnosci_fazy) + ".txt"
            generuj_instancje(0.75, wspolczynnik_zmiennosci_przedkladania, 1.5, poziom_jednorodnosci_fazy, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
