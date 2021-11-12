# Skrypt przeznaczony dla weryfikacji poprawności zaproponowanego uszeregowania

def weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego):
    print("Weryfikacja uszeregowania " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")


def weryfikuj_uszeregowanie_obc(program_szeregujacy):
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]
    liczby_cykli = [1, 2, 5, 10, 20, 50, 100]

    for wo_tmp in range(50, 100, 5):
        wspolczynnik_obciazenia = wo_tmp / 100
        for liczba_cykli in liczby_cykli:
            for liczba_wezlow in liczby_wezlow:
                nazwa_pliku_wejsciowego = "../instancje/inst-obc-" + "%.2f" % wspolczynnik_obciazenia + "-c" + "%03d" % liczba_cykli + ".txt"
                nazwa_pliku_wyjsciowego = "../uszeregowanie/%s-n" % program_szeregujacy + "%03d-nodes-" % liczba_wezlow + "inst-obc-" + "%.2f" % wspolczynnik_obciazenia + "-c" + "%03d" % liczba_cykli + ".txt"
                # print("Weryfikuje uszeregowanie " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")
                weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)


def weryfikuj_uszeregowanie_przedk(program_szeregujacy):
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]
    liczby_cykli = [1, 2, 5, 10, 20, 50, 100]

    for wzp_tmp in range(50, 301, 25):
        wspolczynnik_zmiennosci_przedkladania = wzp_tmp / 100
        for liczba_cykli in liczby_cykli:
            for liczba_wezlow in liczby_wezlow:
                nazwa_pliku_wejsciowego = "../instancje/inst-przedk-" + "%.2f" % wspolczynnik_zmiennosci_przedkladania + "-c" + "%03d" % liczba_cykli + ".txt"
                nazwa_pliku_wyjsciowego = "../uszeregowanie/%s-n" % program_szeregujacy + "%03d-nodes-" % liczba_wezlow + "inst-przedk-" + "%.2f" % wspolczynnik_zmiennosci_przedkladania + "-c" + "%03d" % liczba_cykli + ".txt"
                # print("Weryfikuje uszeregowanie " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")
                weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)


def weryfikuj_uszeregowanie_rozm(program_szeregujacy):
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]
    liczby_cykli = [1, 2, 5, 10, 20, 50, 100]

    for wzr_tmp in range(50, 401, 50):
        wspolczynnik_zmiennosci_rozmiaru = wzr_tmp / 100
        for liczba_cykli in liczby_cykli:
            for liczba_wezlow in liczby_wezlow:
                nazwa_pliku_wejsciowego = "../instancje/inst-rozm-" + "%.2f" % wspolczynnik_zmiennosci_rozmiaru + "-c" + "%03d" % liczba_cykli + ".txt"
                nazwa_pliku_wyjsciowego = "../uszeregowanie/%s-n" % program_szeregujacy + "%03d-nodes-" % liczba_wezlow + "inst-rozm-" + "%.2f" % wspolczynnik_zmiennosci_rozmiaru + "-c" + "%03d" % liczba_cykli + ".txt"
                # print("Weryfikuje uszeregowanie " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")
                weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)


def weryfikuj_uszeregowanie_szer_test():
    weryfikuj_uszeregowanie_obc("szer-test")
    weryfikuj_uszeregowanie_przedk("szer-test")
    weryfikuj_uszeregowanie_rozm("szer-test")


def weryfikuj_uszeregowanie_proba():
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]

    for liczba_wezlow in liczby_wezlow:
        nazwa_pliku_wejsciowego = "../instancje/inst-obc-0.95-c020.txt"
        nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-test-n" + "%03d-nodes-" % liczba_wezlow + "inst-obc-0.95-c020.txt"
        weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)


def main():
    weryfikuj_uszeregowanie_szer_test()

    # weryfikuj_uszeregowanie_proba()


if __name__ == "__main__":
    main()
