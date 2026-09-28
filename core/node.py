
import time
from core.states import NodeState
from network.messages import Message, MessageType
from network.connection import UdpConnection
from utils.logger import setup_logger
from utils.config import HOST, NODE_ADDRESSES, TIMEOUT_T, TIMEOUT_T_PRIME


class Node:
    # Inizializzazione dello stato del nodo e dell'interfaccia di rete
    # Il nodo parte sempre nello stato NORMAL
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.logger = setup_logger(self.node_id)

        self.port = NODE_ADDRESSES[self.node_id]
        self.connection = UdpConnection(HOST, self.port)

        self.state = NodeState.NORMAL
        self.coordinator_id = None

        # Timer per l'algoritmo del bullo: T per l'attesa di ANSWER e T' per l'attesa di COORDINATOR
        self.election_timer_start = None
        self.coord_timer_start = None

        # Variabili di supporto per il rilevamento dei guasti del coordinatore
        self.last_coordinator_msg = time.time()
        self.last_heartbeat_sent = 0.0



    # Loop di esecuzione del nodo
    def run(self):
        self.logger.info("Avvio nodo")
        try:
            while True:
                # Verifica se i timer dell'algoritmo del bullo e del meccanismo di rilevamento dei guasti del coordinatore sono scaduti
                self._check_timeouts()

                try:
                    # Lettura dei dati dal canale di comunicazione
                    packet = self.connection.receive()

                    # Se il pacchetto non è vuoto decifra il messaggio
                    if packet:
                        data, ip, port = packet

                        # UNRMARSHALLING: Converte il messaggio dalla rappresentazione esterna dei dati a quella interna
                        msg = Message.from_xml(data.decode('utf-8'))

                        # Elabora il messaggio e reagisce in base al tipo di messaggio ricevuto
                        self._process_message(msg)

                    # Rallento leggermente per non saturare la CPU
                    time.sleep(0.01)

                except Exception as e:
                    self.logger.error(f"Errore critico durante la ricezione del messagio: {e}")

        except KeyboardInterrupt:
            self.logger.info("*** Processo interrotto ***")
        finally:
            self.connection.close()



    # Definisco il metodo responsabile di avviare un elezione
    def start_election(self):
        self.state = NodeState.IN_ELECTION
        self.logger.info("Avvio elezione")

        time.sleep(1.5)

        # Prendo tutti gli identificatori dei nodi con id maggiore del nodo attuale
        higher_nodes = [nid for nid in NODE_ADDRESSES.keys() if nid > self.node_id]

        # Se non ci sono nodi con ID superiore il nodo si dichiara coordinatore
        if not higher_nodes:
            self.logger.info("Nessun nodo con ID superiore")
            self._declare_coordinator()
        else:
            # Invia un messaggio di election a tutti i nodi con ID superiore
            msg = Message(MessageType.ELECTION, self.node_id)
            payload = msg.to_xml().encode('utf-8')
            for nid in higher_nodes:
                # Invia il messaggio e lo riporta sul logger
                self.connection.send(payload, HOST, NODE_ADDRESSES[nid])
                self.logger.info(f"Inviato ELECTION: a P{nid}")
                time.sleep(1.5)

                # Innesca il Timeout T di attesa del messaggio ANSWER
                self.election_timer_start = time.time()



    # Definisco il metodo per dichiararsi coordinatore
    def _declare_coordinator(self):
        time.sleep(1.5)

        # Imposto lo stato del nodo come coordinatore
        self.state = NodeState.LEADER
        # Assegno a coordinator_id il valore dell'id del nodo stesso che sta eseguendo
        self.coordinator_id = self.node_id
        self.logger.info("Mi dichiaro COORDINATORE")

        # Azzero il contatore dei timer per l'elezione
        self.election_timer_start = None
        self.coord_timer_start = None

        # Invio un messaggio COORDINATOR a tutti i nodi con ID inferiore
        lower_nodes = [nid for nid in NODE_ADDRESSES.keys() if nid < self.node_id]
        msg = Message(MessageType.COORDINATOR, self.node_id)
        payload = msg.to_xml().encode('utf-8')
        for nid in lower_nodes:
            self.connection.send(payload, HOST, NODE_ADDRESSES[nid])



    # Definisco il metodo che gestisce il comportamento alla ricezione di un messaggio
    def _process_message(self, msg: Message):
        msg_type = msg.message_type

        # Verifico se il messaggio ricevuto è un messaggio di battito di routine del leader attuale
        is_heartbeat = (msg_type == MessageType.COORDINATOR and self.coordinator_id == msg.sender_id and self.state == NodeState.NORMAL)

        # Stampa la ricezione del messaggio se il messaggio non è di battito
        if not is_heartbeat:
            self.logger.info(f"Ricevuto {msg_type.name} da P{msg.sender_id}")


        # Definisco il comportamento che dovrà avere il nodo in base al tipo del messggio che ha ricevuto
        match msg_type:
            case MessageType.ELECTION:
                # Rispondo sempre con answer: Istanzio il nuovo messaggio ANSWER e lo invio al nodo da cui ho ricevuto il messaggio ELECTION
                answer_msg = Message(MessageType.ANSWER, self.node_id)
                self.connection.send(answer_msg.to_xml().encode('utf-8'), HOST, NODE_ADDRESSES[msg.sender_id])
                self.logger.info(f"Inviato ANSWER a P{msg.sender_id}")

                # Se il nodo è già coordinatore rispondo anche con un messaggio COORDINATOR
                if self.state == NodeState.LEADER:
                    coord_msg = Message(MessageType.COORDINATOR, self.node_id)
                    self.connection.send(coord_msg.to_xml().encode('utf-8'), HOST, NODE_ADDRESSES[msg.sender_id])
                    self.logger.info(f"Inviato COORDINATOR: a P{msg.sender_id}")

                # Se non sono LEADER e non sono in elezione ne avvio una
                elif self.state != NodeState.IN_ELECTION:
                    self.start_election()


            case MessageType.ANSWER:
                # Se durante un'elezione ricevo un messaggio ANSWER cambio stato, termino il timer di attesa di ANSWER e avvio quello del COORDINATOR
                if self.state == NodeState.IN_ELECTION:
                    self.state = NodeState.WAITING_COORD
                    self.election_timer_start = None
                    self.coord_timer_start = time.time()


            case MessageType.COORDINATOR:
                # Se ho ricevuto un messaggio COORDINATOR da un nodo con ID minore del nodo attuale ignoro il messaggio e avvio un elezione
                # Necessario nel caso in cui un nodo con ID maggiore rientri in funzione dopo un guasto
                if msg.sender_id < self.node_id:
                    self.logger.warning(f"Rifiuto COORDINATOR da un nodo con ID inferiori (P{msg.sender_id}). Avvio elezione")
                    if self.state != NodeState.IN_ELECTION:
                        self.start_election()

                # Se il nodo che ha inviato il messaggio ha un ID con valore superiore all'ID del nodo attuale quest'ultimo si sottomette
                else :
                    # Resetto i timer di attesa e faccio tornare lo stato a NORMAL
                    self.election_timer_start = None
                    self.coord_timer_start = None
                    self.state = NodeState.NORMAL

                    # Se l'id del mittente del messaggio coordinator è diverso da quello precedentemente salvato aggiorno il valore di coordinator_id
                    if self.coordinator_id != msg.sender_id:
                        self.coordinator_id = msg.sender_id
                        self.logger.info(f"Nuovo coordinatore registrato: P{self.coordinator_id}")

                    # Azzera il cronometro che controlla eventiai guasti del coordinatore
                    self.last_coordinator_msg = time.time()



    # Verifica le scadenza dei timeout
    def _check_timeouts(self):
        now = time.time()

        # Verifico la scadenza del timeout T per l'attesa del messaggio di ANSWER
        if self.election_timer_start and (now - self.election_timer_start > TIMEOUT_T):
            self.logger.info("Timeout T Scaduto: Nessuna risposa dai nodi superiori")
            self.election_timer_start = None
            self._declare_coordinator()

        # Verifico se è scaduto il timeout relativo all'attesa del messaggio coordinator
        elif self.coord_timer_start and (now - self.coord_timer_start > TIMEOUT_T_PRIME):
            self.logger.info("Timeout T' Scaduto: Il coordinatore non risponde. Riavvio elezione")
            self.coord_timer_start = None
            self.start_election()

        # Meccanismo di controllo dello stato del coordinatore: Serve per verificare se il coordinatore ha subito un guasto ed è fallito
        if self.coordinator_id is not None:

            # Se il nodo corrente è il leader annuncia la sua presenza ogni T/2 secondi
            if self.node_id == self.coordinator_id:
                # Imposto un intervallo di attesa tra un invio e l'altro di un messaggio di coordinator ai nodi con id inferiore
                # Questo segnala agli altri nodi che il nodo attuale è ancora attivo
                interval = TIMEOUT_T/2

                # Se l'intervallo di tempo tra l'orario attuale e quello in cui ho mandato l'ultimo "segno di vita" è maggiore
                # dell'intervallo di tempo stabilito invio un nuovo messaggio coordinator per segnalare il corretto funzionamento del nodo
                if now - self.last_heartbeat_sent > interval:
                    msg = Message(MessageType.COORDINATOR, self.node_id)
                    payload = msg.to_xml().encode('utf-8')

                    # Dal dizionario presente nella configuraziona estraggo gli ID di tutti i nodi e la loro porta
                    for target_id, target_addr in NODE_ADDRESSES.items():
                        # Invio il messaggio COORDINATOR a tutti i nodi tranne che al nodo stesso che sta eseguendo
                        if target_id != self.node_id:
                            self.connection.send(payload, HOST,target_addr)

                    # Aggiorno la variabile che tiene traccia dell'istante in cui è stato realizzato l'ultimo invio
                    self.last_heartbeat_sent = now

            # I nodi sotto il coordinatore considerano il leader fallito dopo il timeout T
            elif self.state == NodeState.NORMAL:
                if now - self.last_coordinator_msg > TIMEOUT_T:
                    self.logger.error(f"*** Il COORDINATORE P{self.coordinator_id} E' Caduto! ***")
                    self.coordinator_id = None
                    self.start_election()