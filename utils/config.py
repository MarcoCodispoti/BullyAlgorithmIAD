# In questa classe definisco le costanti globali del sistema

# Definisco l'IP della comunicazione impostando l'indirizzo IP locale (localhost)
HOST = "123.0.0.1"

# Definisco il dizionario che conterrà l'associazione di ciascun nodo con il relativo numero di porta
NODE_ADDRESSES = {
    1: 5001,
    2: 5002,
    3: 5003,
    4: 5004,
    5: 5005,
}

# Definisco il tempo massimo (in secondi) di attesa per ricevere un messaggio ANSWER dopo aver inviato un ELECTION
TIMEOUT_T = 6.0

# Definisco il tempo massimo di attesa per ricevere un messaggio COORDINATOR dopo avere ricevuto un ANSWER
TIMEOUT_T_PRIME = 9.0

# Definisco ogni quanti secondi invio un messaggio al coordinator per verificare se è ancora attivo
PING_INTERVAL = 12.0

# Definisco il tempo massimo di attesa del messaggio di risposta al ping del leader
TIMEOUT_PING = 3.0