import re
import random
import os


def szereguj_instancje(nazwa_instancji, liczba_wezlow):
    print("\nSzeregowanie instancji " + nazwa_instancji + ", liczba_wezlow=" + str(liczba_wezlow))
    random.seed(0)

    zadania = []
    nazwa_pliku_wejsciowego = "../instancje/" + nazwa_instancji
    f = open(file=nazwa_pliku_wejsciowego, mode="r")
    for line in f:
        zadania.append(line.split(' '))
    f.close()

    nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-jsq-n" + "%03d-" % liczba_wezlow + nazwa_instancji
    nazwa_pliku_wyjsciowego_nodes = "../uszeregowanie/szer-jsq-n" + "%03d-nodes-" % liczba_wezlow + nazwa_instancji

    czas_wezlow = [0] * liczba_wezlow
    zadania_wezlow = [[] for _ in range(liczba_wezlow)]

    czas_opoznienia = []
    czas_przetwarzania = []
    czas_odpowiedzi = []

    # TODO: Trzeba zrobic tutaj szeregowanie drugim sposobem tym z Processor Sharing
    #  Ponizszy zakomentowany kod to jest przekopiowany z "szer_jnq.py"
    #  (Ten wyzej kod tez jest przekopiowany, z drobna roznica przy nazwie plikow wyjsciowych.)
    #  Schemat przechodzenia petla po kolejnym przychodzacym zadaniu zostaje pewnie ten sam,
    #  ale no trzeba jakos odpowiednio zmienic obliczanie przydzielenia wezla i czasow zakonczenia.
    #  Jakies dodatkowe listy do pamietania biezacych zadan na danym wezlie sie przydadza, itp, itd...

    """
    for indeks_zadania in range(len(zadania)):
        zadanie = zadania[indeks_zadania]
        moment_gotowosci = int(zadanie[0])
        rozmiar_zadania = int(zadanie[1])

        indeks_przydzielonego_wezla = czas_wezlow.index(min(czas_wezlow))
        zadania_wezlow[indeks_przydzielonego_wezla].append(indeks_zadania)

        if czas_wezlow[indeks_przydzielonego_wezla] > moment_gotowosci:
            czas_rozpoczecia = czas_wezlow[indeks_przydzielonego_wezla]
        else:
            czas_rozpoczecia = moment_gotowosci

        czas_ukonczenia = czas_rozpoczecia + rozmiar_zadania * liczba_wezlow
        czas_wezlow[indeks_przydzielonego_wezla] = czas_ukonczenia

        czas_opoznienia.append(czas_rozpoczecia - moment_gotowosci)
        czas_przetwarzania.append(czas_ukonczenia - czas_rozpoczecia)
        czas_odpowiedzi.append(czas_opoznienia[-1] + czas_przetwarzania[-1])

    sredni_czas_opoznienia = sum(czas_opoznienia) / len(czas_opoznienia)
    sredni_czas_przetwarzania = sum(czas_przetwarzania) / len(czas_przetwarzania)
    sredni_czas_odpowiedzi = sum(czas_odpowiedzi) / len(czas_odpowiedzi)
    print("sredni_czas_opoznienia=" + str(sredni_czas_opoznienia) + "\tsredni_czas_przetwarzania=" + str(sredni_czas_przetwarzania) + "\tsredni_czas_odpowiedzi=" + str(sredni_czas_odpowiedzi))

    f = open(file=nazwa_pliku_wyjsciowego, mode="w")
    f.write("%.5f %.5f %.5f" % (sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi))
    f.close()

    f = open(file=nazwa_pliku_wyjsciowego_nodes, mode="w")
    f.write("%.5f %.5f %.5f" % (sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi))
    for zadania_wezla in zadania_wezlow:
        f.write("\n%d" % len(zadania_wezla))
        for zadanie_wezla in zadania_wezla:
            f.write(" %d" % zadanie_wezla)
    f.close()
    """


def main():
    liczby_wezlow = [1, 2, 5, 10, 20, 50, 100]

    zawartosc_folderu_instance = os.listdir("../instancje")
    wzorzec_inst = re.compile('^inst.*\\.txt$')
    lista_nazw_instancji = list(filter(wzorzec_inst.match, zawartosc_folderu_instance))

    for nazwa_instancji in lista_nazw_instancji:
        for liczba_wezlow in liczby_wezlow:
            szereguj_instancje(nazwa_instancji, liczba_wezlow)


if __name__ == "__main__":
    main()
