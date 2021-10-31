from gen_inst import generuj_instancje


def main():
    liczby_faz = [1, 2, 5, 10, 20, 50, 100]

    for wzr_tmp in range(50, 401, 50):
        wspolczynnik_zmiennosci_rozmiaru = wzr_tmp / 100
        for liczba_faz in liczby_faz:
            nazwa_pliku_wyjsciowego = "../instancje/inst-rozm-" + str(wspolczynnik_zmiennosci_rozmiaru) + "-f" + str(liczba_faz) + ".txt"
            generuj_instancje(0.75, 1, wspolczynnik_zmiennosci_rozmiaru, liczba_faz, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
