from gen_inst import generuj_instancje


def main():
    poziomy_jednorodnosci_fazy = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for wzr_tmp in range(50, 401, 50):
        wspolczynnik_zmiennosci_rozmiaru = wzr_tmp / 100
        for poziom_jednorodnosci_fazy in poziomy_jednorodnosci_fazy:
            nazwa_pliku_wyjsciowego = "../instancje/inst-rozm-" + "%.2f" % (wspolczynnik_zmiennosci_rozmiaru) + "-j" + "%.1f" % (poziom_jednorodnosci_fazy) + ".txt"
            generuj_instancje(0.75, 0.5, wspolczynnik_zmiennosci_rozmiaru, poziom_jednorodnosci_fazy, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
