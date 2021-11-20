# Skrypt przeznaczony dla weryfikacji poprawności zaproponowanego uszeregowania

import re
import os


def weryfikuj_uszeregowanie_jnq(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego):
    print("Weryfikacja uszeregowania jnq: " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")

    zadania = []
    f = open(file=nazwa_pliku_wejsciowego, mode="r")
    for line in f:
        line_split = line.split(' ')
        zadania.append([int(line_split[0]), int(line_split[1])])
    f.close()

    f = open(file=nazwa_pliku_wyjsciowego, mode="r")
    [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
    wezly = []
    for line in f:
        lista_zadan = [int(indeks_zadania) for indeks_zadania in line.split()]
        lista_zadan.pop(0)
        wezly.append(lista_zadan)
    f.close()

    wzorzec_liczby_wezlow = re.compile('^\\.\\./uszeregowanie/szer-.*-n([0-9]*)-nodes-.*\\.txt$')
    liczba_wezlow = int(wzorzec_liczby_wezlow.match(nazwa_pliku_wyjsciowego).group(1))

    czas_opoznienia = []
    czas_przetwarzania = []
    czas_odpowiedzi = []

    for lista_zadan in wezly:
        czas_wezla = 0
        for indeks_zadania in lista_zadan:
            zadanie = zadania[indeks_zadania]
            moment_gotowosci = int(zadanie[0])
            rozmiar_zadania = int(zadanie[1])

            if czas_wezla > moment_gotowosci:
                czas_rozpoczecia = czas_wezla
            else:
                czas_rozpoczecia = moment_gotowosci

            czas_ukonczenia = czas_rozpoczecia + rozmiar_zadania * liczba_wezlow
            czas_wezla = czas_ukonczenia

            czas_opoznienia.append(czas_rozpoczecia - moment_gotowosci)
            czas_przetwarzania.append(czas_ukonczenia - czas_rozpoczecia)
            czas_odpowiedzi.append(czas_ukonczenia - moment_gotowosci)

    obliczony_sredni_czas_opoznienia = sum(czas_opoznienia) / len(czas_opoznienia)
    obliczony_sredni_czas_przetwarzania = sum(czas_przetwarzania) / len(czas_przetwarzania)
    obliczony_sredni_czas_odpowiedzi = sum(czas_odpowiedzi) / len(czas_odpowiedzi)

    if (sredni_czas_opoznienia == obliczony_sredni_czas_opoznienia) and (sredni_czas_przetwarzania == obliczony_sredni_czas_przetwarzania) and (sredni_czas_odpowiedzi == obliczony_sredni_czas_odpowiedzi):
        return [1]
    else:
        print("[ERROR]\tNowe obliczone srednie statystyki maja rozne wartosci od podanych przez program szeregujacy.")
        print("sredni_czas_opoznienia=\t\t\t\t" + str(sredni_czas_opoznienia) + "\tsredni_czas_przetwarzania=\t\t\t\t" + str(sredni_czas_przetwarzania) + "\tsredni_czas_odpowiedzi=\t\t\t\t" + str(sredni_czas_odpowiedzi))
        print("obliczony_sredni_czas_opoznienia=\t" + str(obliczony_sredni_czas_opoznienia) + "\tobliczony_sredni_czas_przetwarzania=\t" + str(obliczony_sredni_czas_przetwarzania) + "\tobliczony_sredni_czas_odpowiedzi=\t" + str(obliczony_sredni_czas_odpowiedzi))
        return [-1, nazwa_pliku_wyjsciowego]


def weryfikuj_uszeregowanie_jsq(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego):
    print("Weryfikacja uszeregowania jsq: " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")

    zadania = []
    f = open(file=nazwa_pliku_wejsciowego, mode="r")
    for line in f:
        line_split = line.split(' ')
        zadania.append([int(line_split[0]), int(line_split[1])])
    f.close()

    f = open(file=nazwa_pliku_wyjsciowego, mode="r")
    [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
    wezly = []
    for line in f:
        lista_zadan = [int(indeks_zadania) for indeks_zadania in line.split()]
        lista_zadan.pop(0)
        wezly.append(lista_zadan)
    f.close()

    wzorzec_liczby_wezlow = re.compile('^\\.\\./uszeregowanie/szer-.*-n([0-9]*)-nodes-.*\\.txt$')
    liczba_wezlow = int(wzorzec_liczby_wezlow.match(nazwa_pliku_wyjsciowego).group(1))

    czas_opoznienia = []
    czas_przetwarzania = []
    czas_odpowiedzi = []

    for lista_zadan in wezly:
        czas_wezla = 0
        wykonywane_zadania_wezla = []
        for indeks_zadania in lista_zadan:
            zadanie = zadania[indeks_zadania]
            moment_gotowosci = int(zadanie[0])
            rozmiar_zadania = int(zadanie[1])

            liczba_wykonywanych_zadan = len(wykonywane_zadania_wezla)
            while (liczba_wykonywanych_zadan > 0) and (czas_wezla + wykonywane_zadania_wezla[0][1] <= moment_gotowosci):
                czas_ukonczenia = czas_wezla + wykonywane_zadania_wezla[0][1]
                czas_opoznienia.append(0)
                czas_przetwarzania.append(czas_ukonczenia - wykonywane_zadania_wezla[0][0])
                czas_odpowiedzi.append(czas_przetwarzania[-1])

                uplyniety_czas = wykonywane_zadania_wezla[0][1]
                wykonywane_zadania_wezla.pop(0)
                liczba_wykonywanych_zadan -= 1
                czas_wezla = czas_ukonczenia

                j = 0
                while j < liczba_wykonywanych_zadan:
                    wykonywane_zadanie = wykonywane_zadania_wezla[j]
                    wykonywane_zadanie[1] = (wykonywane_zadanie[1] - uplyniety_czas) * liczba_wykonywanych_zadan / (liczba_wykonywanych_zadan + 1)
                    j += 1

            i = 0
            uplyniety_czas = moment_gotowosci - czas_wezla
            while i < liczba_wykonywanych_zadan:
                wykonywane_zadania_wezla[i][1] = (wykonywane_zadania_wezla[i][1] - uplyniety_czas) * (liczba_wykonywanych_zadan + 1) / liczba_wykonywanych_zadan
                i += 1

            czas_wezla = moment_gotowosci

            i = 0
            czas_trwania_nowego_zadania = rozmiar_zadania * liczba_wezlow * (liczba_wykonywanych_zadan + 1)
            while i < liczba_wykonywanych_zadan:
                if czas_trwania_nowego_zadania < wykonywane_zadania_wezla[i][1]:
                    break
                i += 1
            wykonywane_zadania_wezla.insert(i, [moment_gotowosci, czas_trwania_nowego_zadania])

        liczba_wykonywanych_zadan = len(wykonywane_zadania_wezla)
        while liczba_wykonywanych_zadan > 0:
            czas_ukonczenia = czas_wezla + wykonywane_zadania_wezla[0][1]
            czas_opoznienia.append(0)
            czas_przetwarzania.append(czas_ukonczenia - wykonywane_zadania_wezla[0][0])
            czas_odpowiedzi.append(czas_przetwarzania[-1])

            uplyniety_czas = wykonywane_zadania_wezla[0][1]
            wykonywane_zadania_wezla.pop(0)
            liczba_wykonywanych_zadan -= 1
            czas_wezla = czas_ukonczenia

            j = 0
            while j < liczba_wykonywanych_zadan:
                wykonywane_zadanie = wykonywane_zadania_wezla[j]
                wykonywane_zadanie[1] = (wykonywane_zadanie[1] - uplyniety_czas) * liczba_wykonywanych_zadan / (liczba_wykonywanych_zadan + 1)
                j += 1

    obliczony_sredni_czas_opoznienia = sum(czas_opoznienia) / len(czas_opoznienia)
    obliczony_sredni_czas_przetwarzania = sum(czas_przetwarzania) / len(czas_przetwarzania)
    obliczony_sredni_czas_odpowiedzi = sum(czas_odpowiedzi) / len(czas_odpowiedzi)

    if (sredni_czas_opoznienia == obliczony_sredni_czas_opoznienia) and (sredni_czas_przetwarzania == obliczony_sredni_czas_przetwarzania) and (sredni_czas_odpowiedzi == obliczony_sredni_czas_odpowiedzi):
        return [1]
    else:
        print("[ERROR]\tNowe obliczone srednie statystyki maja rozne wartosci od podanych przez program szeregujacy.")
        print("sredni_czas_opoznienia=\t\t\t\t" + str(sredni_czas_opoznienia) + "\tsredni_czas_przetwarzania=\t\t\t\t" + str(sredni_czas_przetwarzania) + "\tsredni_czas_odpowiedzi=\t\t\t\t" + str(sredni_czas_odpowiedzi))
        print("obliczony_sredni_czas_opoznienia=\t" + str(obliczony_sredni_czas_opoznienia) + "\tobliczony_sredni_czas_przetwarzania=\t" + str(obliczony_sredni_czas_przetwarzania) + "\tobliczony_sredni_czas_odpowiedzi=\t" + str(obliczony_sredni_czas_odpowiedzi))
        return [-1, nazwa_pliku_wyjsciowego]


def weryfikuj_uszeregowanie_test(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego):
    print("Weryfikacja uszeregowania test: " + nazwa_pliku_wyjsciowego + "\t(" + nazwa_pliku_wejsciowego + ")")

    zadania = []
    f = open(file=nazwa_pliku_wejsciowego, mode="r")
    for line in f:
        line_split = line.split(' ')
        zadania.append([int(line_split[0]), int(line_split[1])])
    f.close()

    f = open(file=nazwa_pliku_wyjsciowego, mode="r")
    [sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi] = [float(liczba) for liczba in f.readline().split(' ')]
    wezly = []
    for line in f:
        lista_zadan = [int(indeks_zadania) for indeks_zadania in line.split()]
        lista_zadan.pop(0)
        wezly.append(lista_zadan)
    f.close()

    wzorzec_liczby_wezlow = re.compile('^\\.\\./uszeregowanie/szer-.*-n([0-9]*)-nodes-.*\\.txt$')
    liczba_wezlow = int(wzorzec_liczby_wezlow.match(nazwa_pliku_wyjsciowego).group(1))

    czas_opoznienia = []
    czas_przetwarzania = []
    czas_odpowiedzi = []

    for lista_zadan in wezly:
        czas_wezla = 0
        for indeks_zadania in lista_zadan:
            zadanie = zadania[indeks_zadania]
            moment_gotowosci = int(zadanie[0])
            rozmiar_zadania = int(zadanie[1])

            if czas_wezla > moment_gotowosci:
                czas_rozpoczecia = czas_wezla
            else:
                czas_rozpoczecia = moment_gotowosci

            czas_ukonczenia = czas_rozpoczecia + rozmiar_zadania * liczba_wezlow
            czas_wezla = czas_ukonczenia

            czas_opoznienia.append(czas_rozpoczecia - moment_gotowosci)
            czas_przetwarzania.append(czas_ukonczenia - czas_rozpoczecia)
            czas_odpowiedzi.append(czas_ukonczenia - moment_gotowosci)

    obliczony_sredni_czas_opoznienia = sum(czas_opoznienia) / len(czas_opoznienia)
    obliczony_sredni_czas_przetwarzania = sum(czas_przetwarzania) / len(czas_przetwarzania)
    obliczony_sredni_czas_odpowiedzi = sum(czas_odpowiedzi) / len(czas_odpowiedzi)

    if (sredni_czas_opoznienia == obliczony_sredni_czas_opoznienia) and (sredni_czas_przetwarzania == obliczony_sredni_czas_przetwarzania) and (sredni_czas_odpowiedzi == obliczony_sredni_czas_odpowiedzi):
        return [1]
    else:
        print("[ERROR]\tNowe obliczone srednie statystyki maja rozne wartosci od podanych przez program szeregujacy.")
        print("sredni_czas_opoznienia=\t\t\t\t" + str(sredni_czas_opoznienia) + "\tsredni_czas_przetwarzania=\t\t\t\t" + str(sredni_czas_przetwarzania) + "\tsredni_czas_odpowiedzi=\t\t\t\t" + str(sredni_czas_odpowiedzi))
        print("obliczony_sredni_czas_opoznienia=\t" + str(obliczony_sredni_czas_opoznienia) + "\tobliczony_sredni_czas_przetwarzania=\t" + str(obliczony_sredni_czas_przetwarzania) + "\tobliczony_sredni_czas_odpowiedzi=\t" + str(obliczony_sredni_czas_odpowiedzi))
        return [-1, nazwa_pliku_wyjsciowego]


def weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego):
    wzorzec_szer_jnq = re.compile('^\\.\\./uszeregowanie/szer-jnq-.*\\.txt$')
    wzorzec_szer_jsq = re.compile('^\\.\\./uszeregowanie/szer-jsq-.*\\.txt$')
    wzorzec_szer_test = re.compile('^\\.\\./uszeregowanie/szer-test-.*\\.txt$')

    if wzorzec_szer_jnq.match(nazwa_pliku_wyjsciowego):
        return weryfikuj_uszeregowanie_jnq(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
    elif wzorzec_szer_jsq.match(nazwa_pliku_wyjsciowego):
        return weryfikuj_uszeregowanie_jsq(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
    elif wzorzec_szer_test.match(nazwa_pliku_wyjsciowego):
        return weryfikuj_uszeregowanie_test(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
    else:
        print("[ERROR]\tNierozpoznany algorytm szeregujacy, weryfikacja pominieta.")
        return [0, nazwa_pliku_wyjsciowego]


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


def weryfikuj_uszeregowanie_proba_01():
    wyniki_weryfikacji = WynikWeryfikacjiWszystkichUszeregowan()
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]

    for liczba_wezlow in liczby_wezlow:
        nazwa_pliku_wejsciowego = "../instancje/inst-obc-0.95-c020.txt"
        nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-test-n" + "%03d-nodes-" % liczba_wezlow + "inst-obc-0.95-c020.txt"
        wynik_weryfikacji = weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
        wyniki_weryfikacji.dodaj_wynik_weryfikacji(wynik_weryfikacji)

    wyniki_weryfikacji.wyswietl_wyniki_weryfikacji()


def weryfikuj_uszeregowanie_proba_02():
    wyniki_weryfikacji = WynikWeryfikacjiWszystkichUszeregowan()
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]

    for liczba_wezlow in liczby_wezlow:
        nazwa_pliku_wejsciowego = "../instancje/inst-rozm-1.50-c010.txt"
        nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-jnq-n" + "%03d-nodes-" % liczba_wezlow + "inst-rozm-1.50-c010.txt"
        wynik_weryfikacji = weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
        wyniki_weryfikacji.dodaj_wynik_weryfikacji(wynik_weryfikacji)

    wyniki_weryfikacji.wyswietl_wyniki_weryfikacji()


def weryfikuj_uszeregowanie_proba_03():
    wyniki_weryfikacji = WynikWeryfikacjiWszystkichUszeregowan()
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]

    for liczba_wezlow in liczby_wezlow:
        nazwa_pliku_wejsciowego = "../instancje/inst-przedk-1.75-c020.txt"
        nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-jsq-n" + "%03d-nodes-" % liczba_wezlow + "inst-przedk-1.75-c020.txt"
        wynik_weryfikacji = weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
        wyniki_weryfikacji.dodaj_wynik_weryfikacji(wynik_weryfikacji)

    wyniki_weryfikacji.wyswietl_wyniki_weryfikacji()


def weryfikuj_wszystkie_uszeregowania_wszystkich_instancji():
    zawartosc_folderu_instancje = os.listdir("../instancje")
    wzorzec_inst = re.compile('^inst.*\\.txt$')
    lista_nazw_instancji = list(filter(wzorzec_inst.match, zawartosc_folderu_instancje))

    zawartosc_folderu_uszeregowania = os.listdir("../uszeregowanie")
    wzorzec_uszer = re.compile('^szer.*-nodes-.*\\.txt$')
    lista_nazw_uszeregowan = list(filter(wzorzec_uszer.match, zawartosc_folderu_uszeregowania))

    wyniki_weryfikacji = WynikWeryfikacjiWszystkichUszeregowan()

    for nazwa_instancji in lista_nazw_instancji:
        wzorzec_uszer_danej_inst = re.compile('^szer-.*' + nazwa_instancji + '$')
        lista_nazw_uszeregowan_danej_instancji = list(filter(wzorzec_uszer_danej_inst.match, lista_nazw_uszeregowan))
        for nazwa_uszeregowania in lista_nazw_uszeregowan_danej_instancji:
            nazwa_pliku_wejsciowego = "../instancje/" + nazwa_instancji
            nazwa_pliku_wyjsciowego = "../uszeregowanie/" + nazwa_uszeregowania
            wynik_weryfikacji = weryfikuj_uszeregowanie(nazwa_pliku_wejsciowego, nazwa_pliku_wyjsciowego)
            wyniki_weryfikacji.dodaj_wynik_weryfikacji(wynik_weryfikacji)

    wyniki_weryfikacji.wyswietl_wyniki_weryfikacji()


class WynikWeryfikacjiWszystkichUszeregowan:

    def __init__(self):
        self.liczba_poprawnych_uszeregowan = 0
        self.liczba_blednych_uszeregowan = 0
        self.lista_blednych_uszeregowan = []
        self.liczba_niezweryfikowanych_uszeregowan = 0
        self.lista_niezweryfikowanych_uszeregowan = []

    def dodaj_wynik_weryfikacji(self, wynik_weryfikacji):
        if wynik_weryfikacji[0] == 1:
            self.liczba_poprawnych_uszeregowan += 1
        elif wynik_weryfikacji[0] == -1:
            self.liczba_blednych_uszeregowan += 1
            self.lista_blednych_uszeregowan.append(wynik_weryfikacji[1])
        else:
            self.liczba_niezweryfikowanych_uszeregowan += 1
            self.lista_niezweryfikowanych_uszeregowan.append(wynik_weryfikacji[1])

    def wyswietl_wyniki_weryfikacji(self):
        print("Licbza poprawnych uszeregowan:\t%d" % self.liczba_poprawnych_uszeregowan)
        print("Liczba blednych uszeregowan:\t%d" % self.liczba_blednych_uszeregowan)
        if self.liczba_blednych_uszeregowan != 0:
            print("Lista blednych uszeregowan:")
            for bledne_uszeregowanie in self.lista_blednych_uszeregowan:
                print("\t%s" % bledne_uszeregowanie)
        print("Liczba niezweryfikowanych uszeregowan:\t%d" % self.liczba_niezweryfikowanych_uszeregowan)
        if self.liczba_niezweryfikowanych_uszeregowan != 0:
            print("Lista niezweryfikowanych uszeregowan:")
            for niezweryfikowane_uszeregowanie in self.lista_niezweryfikowanych_uszeregowan:
                print("\t%s" % niezweryfikowane_uszeregowanie)


def main():
    # weryfikuj_uszeregowanie_proba_01()
    # weryfikuj_uszeregowanie_proba_02()
    # weryfikuj_uszeregowanie_proba_03()

    weryfikuj_wszystkie_uszeregowania_wszystkich_instancji()


if __name__ == "__main__":
    main()
