from gen_inst import generuj_instancje


def main():
    liczby_cykli = [1, 2, 5, 10, 20, 50, 100]

    for wo_tmp in range(50, 100, 5):
        wspolczynnik_obciazenia = wo_tmp / 100
        for liczba_cykli in liczby_cykli:
            nazwa_pliku_wyjsciowego = "../instancje/inst-obc-" + "%.2f" % (wspolczynnik_obciazenia) + "-c" + "%03d" % (liczba_cykli) + ".txt"
            generuj_instancje(wspolczynnik_obciazenia, 1, 1.5, liczba_cykli, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
