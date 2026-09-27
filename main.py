
import sys
import threading
import time


from core.node import Node
from launcher import launch_terminal


# Funzione responsabile per l'invocazione dell'elezione iniziale e dell'invocazione dell'elezione per un nodo
def delayed_startup(node, is_starter):
    # Se il nodo che esegue la funzione è il prescelto si occupa di avviare l'elezione iniziale
    if is_starter:
        time.sleep(5)
        if node.coordinator_id is None:
            node.logger.info("Sono responsabile dell'elezione iniziale")
            time.sleep(3)
            node.start_election()
    else:
        # Tutti i nodi che non sono coordinatori attendono
        time.sleep(22)
        # Se un nodo è tornato attivo nel sistema avvia un elezione per ottenere il coordinatore attuale o eventualmente proclamarsi tale


# Definisco la funzione main che i nodi andranno a eseguire
def main():
    # Se non ci sono argomenti da riga di comando lo script è stato lanciato manualmente, l'avvio dei terminali avviene tramite launcher
    if len(sys.argv) == 1:
        launch_terminal()
        return

    try:
        # Estraggo i parametri di configurazione passati dall'invocazione tramite launcher
        node_id = int(sys.argv[1])
        starter_node_id = int(sys.argv[2])

        # Istanzio e inizializzo un nuovo nodo
        node = Node(node_id)

        # Verifico se il nodo che sta eseguendo possiede l'id del nodo sorteggiato per eseguire l'elezione principale
        is_starter = (node_id == starter_node_id)

        # Avvio in maniera asincrono e non bloccante il metodo per l'elezione iniziale o l'elezione di un nodo rientrato in funzione
        threading.Thread(target=delayed_startup, args=(node, is_starter), daemon=True).start()

        # Avvio il ciclo di esecuzione della macchina a stati del nodo
        node.run()

    # Se vengono passati come parametri valori che non sono numeri interi ritorna il messaggio di errore e termina l'esecuzione
    except ValueError:
        print("Errore: I parametri devono essere numeri interi")
        sys.exit(1)

# Verifica che l'esecuzione di questo file sia stata lanciata direttamente e non utilizzato come modulo esterno
if __name__ == "__main__":
    main()

