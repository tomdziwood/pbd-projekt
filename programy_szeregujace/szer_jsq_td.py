import re
import random
import os
from datetime import datetime


def szereguj_instancje(nazwa_instancji, liczba_wezlow):
    czas = datetime.now()
    print("\n[%s] Szeregowanie instancji %s, liczba_wezlow=%d" % (czas, nazwa_instancji, liczba_wezlow))
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
    wykonana_praca_wezlow = [0] * liczba_wezlow
    zadania_wezlow = [[] for _ in range(liczba_wezlow)]
    wykonywane_zadania_wezlow = [[] for _ in range(liczba_wezlow)]

    czas_opoznienia = []
    czas_przetwarzania = []
    czas_odpowiedzi = []

    for indeks_zadania in range(len(zadania)):
        zadanie = zadania[indeks_zadania]
        moment_gotowosci = int(zadanie[0])
        rozmiar_zadania = int(zadanie[1])

        # aktualizacja stanow wezlow do chwili zakonczenia zadania ukonczonego jako ostatnie przed momentem gotowosci obecnego zadania
        for indeks_wezla in range(liczba_wezlow):
            wykonywane_zadania_wezla = wykonywane_zadania_wezlow[indeks_wezla]
            liczba_wykonywanych_zadan = len(wykonywane_zadania_wezla)
            while liczba_wykonywanych_zadan > 0:
                czas_ukonczenia = czas_wezlow[indeks_wezla] + (wykonywane_zadania_wezla[0][1] - wykonana_praca_wezlow[indeks_wezla]) * liczba_wykonywanych_zadan
                if czas_ukonczenia > moment_gotowosci:
                    break
                czas_opoznienia.append(0)
                czas_przetwarzania.append(czas_ukonczenia - wykonywane_zadania_wezla[0][0])
                czas_odpowiedzi.append(czas_przetwarzania[-1])

                wykonana_praca_wezlow[indeks_wezla] += (czas_ukonczenia - czas_wezlow[indeks_wezla]) / liczba_wykonywanych_zadan
                wykonywane_zadania_wezla.pop(0)
                liczba_wykonywanych_zadan -= 1
                czas_wezlow[indeks_wezla] = czas_ukonczenia

        # wybor wezla z najmniejsza kolejka wykonywanych zadan
        indeks_wybranego_wezla = 0
        najmniejsza_liczba_zadan_w_kolejce = len(wykonywane_zadania_wezlow[0])
        indeks_wezla = 1
        while (indeks_wezla < liczba_wezlow) and (najmniejsza_liczba_zadan_w_kolejce > 0):
            if najmniejsza_liczba_zadan_w_kolejce > len(wykonywane_zadania_wezlow[indeks_wezla]):
                najmniejsza_liczba_zadan_w_kolejce = len(wykonywane_zadania_wezlow[indeks_wezla])
                indeks_wybranego_wezla = indeks_wezla
            indeks_wezla += 1

        # aktualizacja stanu wezla do chwili momentu gotowosci obecnego zadania
        i = 0
        wykonywane_zadania_wezla = wykonywane_zadania_wezlow[indeks_wybranego_wezla]
        liczba_wykonywanych_zadan = len(wykonywane_zadania_wezla)
        uplyniety_czas = moment_gotowosci - czas_wezlow[indeks_wybranego_wezla]
        if liczba_wykonywanych_zadan > 0:
            wykonana_praca_wezlow[indeks_wybranego_wezla] += uplyniety_czas / liczba_wykonywanych_zadan
        while i < liczba_wykonywanych_zadan:
            wykonywane_zadania_wezla[i][1] -= wykonana_praca_wezlow[indeks_wybranego_wezla]
            i += 1
        czas_wezlow[indeks_wybranego_wezla] = moment_gotowosci
        wykonana_praca_wezlow[indeks_wybranego_wezla] = 0

        # wstawienie obecnego zadania do listy wykonywanych zadan wezla
        i = 0
        czas_trwania_nowego_zadania = rozmiar_zadania * liczba_wezlow
        while i < liczba_wykonywanych_zadan:
            if czas_trwania_nowego_zadania < wykonywane_zadania_wezla[i][1]:
                break
            i += 1
        wykonywane_zadania_wezla.insert(i, [moment_gotowosci, czas_trwania_nowego_zadania])
        zadania_wezlow[indeks_wybranego_wezla].append(indeks_zadania)

    # po przydzieleniu wszystkich zadan nastepuje dokonczenie zadan przebywajacych jeszcze w kolejkach wezlow
    for indeks_wezla in range(liczba_wezlow):
        wykonywane_zadania_wezla = wykonywane_zadania_wezlow[indeks_wezla]
        liczba_wykonywanych_zadan = len(wykonywane_zadania_wezla)
        while liczba_wykonywanych_zadan > 0:
            czas_ukonczenia = czas_wezlow[indeks_wezla] + (wykonywane_zadania_wezla[0][1] - wykonana_praca_wezlow[indeks_wezla]) * liczba_wykonywanych_zadan
            czas_opoznienia.append(0)
            czas_przetwarzania.append(czas_ukonczenia - wykonywane_zadania_wezla[0][0])
            czas_odpowiedzi.append(czas_przetwarzania[-1])

            wykonana_praca_wezlow[indeks_wezla] += (czas_ukonczenia - czas_wezlow[indeks_wezla]) / liczba_wykonywanych_zadan
            wykonywane_zadania_wezla.pop(0)
            liczba_wykonywanych_zadan -= 1
            czas_wezlow[indeks_wezla] = czas_ukonczenia

    sredni_czas_opoznienia = sum(czas_opoznienia) / len(czas_opoznienia)
    sredni_czas_przetwarzania = sum(czas_przetwarzania) / len(czas_przetwarzania)
    sredni_czas_odpowiedzi = sum(czas_odpowiedzi) / len(czas_odpowiedzi)
    czas = datetime.now()
    print("[%s] sredni_czas_opoznienia=%f\tsredni_czas_przetwarzania=%f\tsredni_czas_odpowiedzi=%f" % (czas, sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi))

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
