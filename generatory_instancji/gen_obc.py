from gen_inst import generuj_instancje


def main():
    liczby_faz = [1, 2, 5, 10, 20, 50, 100]

    for obciazenie_procentowo in range(50, 100, 5):
        for liczba_faz in liczby_faz:
            nazwa_pliku_wyjsciowego = "../instancje/inst-obc-" + str(obciazenie_procentowo) + "-f" + str(liczba_faz) + ".txt"
            generuj_instancje(obciazenie_procentowo / 100, 1, 1.5, liczba_faz, nazwa_pliku_wyjsciowego)


if __name__ == "__main__":
    main()
