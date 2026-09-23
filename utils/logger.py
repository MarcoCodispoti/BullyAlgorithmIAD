# In questa classe ci definisce il sistema di gestione del log dei nodi

# Importo la libreria per eseguire il loggin
import logging


# Definisco la funzione responsabile instanziare, configurare e restituire il logger personalizzato per un nodo
def setup_logger(node_id: int) -> logging.Logger:

    # Realizzo un nuovo gestore di log e gli assegno il nome del nodo a cui sarà associato
    logger = logging.getLogger(f"Node_{node_id}")

    # Imposto il livello del log su DEBUG in modo che catturi tutti i messaggi
    logger.setLevel(logging.DEBUG)

    # Se il logger non è già associato a un gestore
    if not logger.handlers:

        # Dichiaro il componente gestore che si occuperà di instradare i messaggi alla console
        console_handler = logging.StreamHandler()

        # Stabilisco la formattazione in modo che prima di ogni messaggio venga specificato l'ID del nodo che lo stampa
        formatter = logging.Formatter(f'[P{node_id}] %(message)s')

        # Applico la formattazione al componente responsabile del log sulla console
        console_handler.setFormatter(formatter)

        # Associo il componente responsabile del log sulla console al logger associato al nodo
        logger.addHandler(console_handler)

    # Ritorno il logger
    return logger