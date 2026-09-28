# In questo file si definisce il sistema di gestione del log dei nodi

# Importa la libreria per eseguire il logging
import logging


# Definisce la funzione responsabile di instanziare, configurare e restituire il logger personalizzato per un nodo
def setup_logger(node_id: int) -> logging.Logger:

    # Realizza un nuovo gestore di log e gli assegna il nome del nodo a cui sarà associato
    logger = logging.getLogger(f"Node_{node_id}")

    # Imposta il livello del log su DEBUG in modo che catturi tutti i messaggi
    logger.setLevel(logging.DEBUG)

    # Se il logger non è già associato a un gestore
    if not logger.handlers:

        # Dichiara il componente gestore che si occuperà di instradare i messaggi alla console
        console_handler = logging.StreamHandler()

        # Stabilisce la formattazione in modo che prima di ogni messaggio venga specificato l'ID del nodo che lo stampa
        formatter = logging.Formatter(f'[P{node_id}] %(message)s')

        # Applica la formattazione al componente responsabile del log sulla console
        console_handler.setFormatter(formatter)

        # Associa il componente responsabile del log sulla console al logger associato al nodo
        logger.addHandler(console_handler)

    # Ritorna il logger
    return logger