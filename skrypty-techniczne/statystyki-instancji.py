import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    liczba_zadan = 10000
    zadania = []
    f = open(file="../instancje/inst-test.txt", mode="r")
    for _ in range(liczba_zadan):
        zadania.append(f.readline().split(' '))
    f.close()

    momenty_gotowosci_lista = []
    czasy_trwania_lista = []
    for zadanie in zadania:
        momenty_gotowosci_lista.append(int(zadanie[0]))
        czasy_trwania_lista.append(int(zadanie[1]))

    czasy_miedzy_przedkladaniem = []
    poprzedni_moment_gotowosci = 0
    for moment_gotowosci in momenty_gotowosci_lista:
        czasy_miedzy_przedkladaniem.append(moment_gotowosci - poprzedni_moment_gotowosci)
        poprzedni_moment_gotowosci = moment_gotowosci

    np_momenty_gotowosci = np.array(momenty_gotowosci_lista)
    np_czasy_trwania = np.array(czasy_trwania_lista)
    np_czasy_miedzy_przedkladaniem = np.array(czasy_miedzy_przedkladaniem)

    pd_momenty_gotowosci = pd.DataFrame(np_momenty_gotowosci)
    pd_czasy_trwania = pd.DataFrame(np_czasy_trwania)
    pd_czasy_miedzy_przedkladaniem = pd.DataFrame(np_czasy_miedzy_przedkladaniem)

    print("pd_momenty_gotowosci.describe():")
    print(pd_momenty_gotowosci.describe())
    print("pd_czasy_trwania.describe():")
    print(pd_czasy_trwania.describe())
    print("pd_czasy_miedzy_przedkladaniem.describe():")
    print(pd_czasy_miedzy_przedkladaniem.describe())

    plt.subplot(2, 2, 1)
    plt.hist(np_momenty_gotowosci, bins=200)

    plt.subplot(2, 2, 2)
    plt.hist(np_czasy_trwania, bins=200)

    plt.subplot(2, 2, 3)
    plt.hist(np_czasy_miedzy_przedkladaniem, bins=200)

    plt.show()


if __name__ == "__main__":
    main()
