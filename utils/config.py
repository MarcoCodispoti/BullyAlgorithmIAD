# In questo file definisco le costanti globali del sistema

# Definisce l'IP della comunicazione impostando l'indirizzo IP locale (localhost)
HOST = "127.0.0.1"

# Dizionario che conterrà l'associazione di ciascun nodo con il relativo numero di porta
NODE_ADDRESSES = {
    1: 5001,
    2: 5002,
    3: 5003,
    4: 5004,
    5: 5005,
}

# Definisco il tempo massimo (in secondi) di attesa per ricevere un messaggio ANSWER dopo l'avvio di un'elezione
TIMEOUT_T = 6.0

# Definisce il tempo massimo di attesa per ricevere un messaggio COORDINATOR dopo avere ricevuto un ANSWER da un nodo superiore
TIMEOUT_T_PRIME = 9.0
