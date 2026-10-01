
import sys
import threading
import time


from core.node import Node
from launcher import launch_terminal


# Avvia in maniera asincrona l'elezione iniziale
def delayed_startup(node, is_starter):
    # Se il nodo che esegue la funzione è il prescelto si occupa di avviare l'elezione iniziale
    if is_starter:
        # Attende che i processi si siano assestati dopo l'apertura
        time.sleep(5)

        # Se non è stato eletto nessun coordinatore nel frattempo, procede ad avviare l'elezione iniziale
        if node.coordinator_id is None:
            node.logger.info("Sono responsabile dell'elezione iniziale")
            time.sleep(3)
            node.start_election()
    else:
        # Tutti i nodi che non sono coordinatori attendono e, se il nodo prescelto non ha avviato l'elezione iniziale, procedono loro stessi ad avviarla
        time.sleep(30)
        node.start_election()


# Funzione main di esecuzione del programma
def main():
    # Se non ci sono argomenti da riga di comando lo script è stato lanciato manualmente, l'avvio dei terminali avviene tramite launcher
    if len(sys.argv) == 1:
        launch_terminal()
        return

    try:
        # Estragge i parametri di configurazione passati dall'invocazione tramite launcher
        node_id = int(sys.argv[1])
        starter_node_id = int(sys.argv[2])

        # Istanzia e inizializzo un nuovo nodo
        node = Node(node_id)

        # Verifica se il nodo che sta eseguendo possiede l'id sorteggiato per eseguire l'elezione principale
        is_starter = (node_id == starter_node_id)

        # Avvia in maniera asincrona e non bloccante il metodo per l'elezione iniziale
        threading.Thread(target=delayed_startup, args=(node, is_starter), daemon=True).start()

        # Avvia il ciclo di esecuzione della macchina a stati del nodo
        node.run()

    # Gestisce l'eccezione nel caso vengano passati come parametri valori che non sono numeri interi
    except ValueError:
        print("Errore: I parametri devono essere numeri interi")
        sys.exit(1)

# Verifica che lo script sia stato eseguito direttamente come programma e non importato come modulo
if __name__ == "__main__":
    main()

