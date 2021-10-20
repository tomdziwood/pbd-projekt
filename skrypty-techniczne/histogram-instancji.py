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

    np_momenty_gotowosci = np.array(momenty_gotowosci_lista)
    np_czasy_trwania = np.array(czasy_trwania_lista)

    pd_momenty_gotowosci = pd.DataFrame(np_momenty_gotowosci)
    pd_czasy_trwania = pd.DataFrame(np_czasy_trwania)

    print("pd_momenty_gotowosci.describe():")
    print(pd_momenty_gotowosci.describe())
    print("pd_czasy_trwania.describe():")
    print(pd_czasy_trwania.describe())

    plt.hist(pd_momenty_gotowosci, bins=200)
    plt.show()

    plt.hist(np_czasy_trwania, bins=200)
    plt.show()


if __name__ == "__main__":
    main()
