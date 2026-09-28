
# Importo la libreria Enum per permettere l'enumerazione
from enum import Enum

# Definisce le costanti enumerative che rappresentano i possibili stati di un nodo
# Sono utilizzate dalle istanze della classe Node per tracciare il proprio stato e implementare la logica della macchina a stati
class NodeState(Enum):
    # Tipi di stati dei nodi definiti come stringhe costanti

    # Definisce lo stato passivo e di stabilità di un nodo appena avviato o sotto il controllo di un coordinatore
    NORMAL = "NORMAL"

    # Fase di elezione
    IN_ELECTION = "IN_ELECTION"

    # Fase in cui si attende un messaggio COORDINATOR dopo aver ricevuto un messaggio di ANSWER
    WAITING_COORD = "WAITING_COORD"

    # Stato di coordinatore in cui entra un nodo dopo aver vinto l'elezione
    LEADER = "LEADER"

