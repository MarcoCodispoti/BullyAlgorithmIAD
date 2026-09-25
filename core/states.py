
# Importo la libreria Enum per permettere l'enumerazione
from enum import Enum

# Definisco la classe che andrà a enumerare i tipi di messaggi che i nodi si scambieranno
class NodeState(Enum):
    # Tipi di messaggi defini come stringhe costanti
    NORMALE = "NORMAL"
    ANSWER = "ANSWER"
    COORDINATOR = "COORDINATOR"
    ELECTION = "ELECTION"

