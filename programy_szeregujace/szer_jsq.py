import re
import random
import os
from processor_sharing import Task, Node, least_busy


def szereguj_instancje(nazwa_instancji, liczba_wezlow):
    print("\nSzeregowanie instancji " + nazwa_instancji + ", liczba_wezlow=" + str(liczba_wezlow))
    random.seed(0)

    loaded_tasks: list[Task] = []
    nodes: list[Node] = [Node() for _ in range( liczba_wezlow)]
    cycle_counter: int = 0

    nazwa_pliku_wejsciowego = "../instancje/" + nazwa_instancji

    with open(file=nazwa_pliku_wejsciowego, mode="r") as file:
        for idx, line in enumerate(file):
            start, duration = line.split(' ')
            loaded_tasks.append(Task(idx, int(start), int(duration)))

    nazwa_pliku_wyjsciowego = "../uszeregowanie/szer-jsq-n" + "%03d-" % liczba_wezlow + nazwa_instancji
    nazwa_pliku_wyjsciowego_nodes = "../uszeregowanie/szer-jsq-n" + "%03d-nodes-" % liczba_wezlow + nazwa_instancji

    # compute
    while sum(node.active_tasks for node in nodes) + len(loaded_tasks) > 0:
        while loaded_tasks and loaded_tasks[0].start <= cycle_counter:  # assume sorted
            least_busy(nodes).add_task(loaded_tasks.pop(0))

        for node in nodes:
            if node.active_tasks == 0:
                continue
            time_in_cycle = 1
            compute_time = time_in_cycle / node.active_tasks
            [task.add_compute_time(compute_time, cycle_counter) for task in
             node.tasks]  # parts of time wasted
            node.mark_completed()
        cycle_counter += 1

    # results
    all_tasks = []
    for node in nodes:
        all_tasks.extend(node.completed_tasks)

    sredni_czas_opoznienia = 0
    sredni_czas_przetwarzania = sum(task.real_duration for task in all_tasks) / len(all_tasks)
    sredni_czas_odpowiedzi = sredni_czas_przetwarzania
    print("sredni_czas_opoznienia=" + str(sredni_czas_opoznienia) + "\tsredni_czas_przetwarzania=" + str(sredni_czas_przetwarzania) + "\tsredni_czas_odpowiedzi=" + str(sredni_czas_odpowiedzi))

    f = open(file=nazwa_pliku_wyjsciowego, mode="w")
    f.write("%.5f %.5f %.5f" % (sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi))
    f.close()

    f = open(file=nazwa_pliku_wyjsciowego_nodes, mode="w")
    f.write("%.5f %.5f %.5f" % (sredni_czas_opoznienia, sredni_czas_przetwarzania, sredni_czas_odpowiedzi))
    for node in nodes:
        f.write("\n%d" % len(node.completed_tasks))
        for task in node.completed_tasks:
            f.write(" %d" % task.id)
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
