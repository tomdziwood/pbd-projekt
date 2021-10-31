from gen_inst import generuj_instancje


def main():
    liczby_faz = [1, 2, 5, 10, 20, 50, 100]

    for wzp_tmp in range(50, 301, 25):
        wspolczynnik_zmiennosci_przedkladania = wzp_tmp / 100
        for liczba_faz in liczby_faz:
            nazwa_pliku_wyjsciowego = "../instancje/inst-przedk-" + str(wspolczynnik_zmiennosci_przedkladania) + "-f" + str(liczba_faz) + ".txt"
            generuj_instancje(0.75, wspolczynnik_zmiennosci_przedkladania, 1.5, liczba_faz, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
