
# Importa la libreria per la gestione di socket e connessioni
import socket


class UdpConnection:
    # Inizializza l'interfaccia di comunicazione di rete
    def __init__(self, host, port):
        # Crea il socket di rete e lo salva nella variabile di istanza, specificando l'uso di datagrammi UDP e l'uso di indirizzi IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Esegue il binding del socket appena creato all'indirizzo IP e alla porta specificati da host e port
        self.sock.bind((host, port))

        # Imposta un timeout in cui se il socket non legge dati dal canale di comunicazione interrompe l'attesa per non bloccare il processo fino a una ricezione
        self.sock.settimeout(0.1)


    # Definisce il metodo per inviare datagrammi UDP verso uno specifico destinatario sul canale di comunicazione
    def send(self, data: bytes, host: str, port: int):
        try:
            # Invia il pacchetto contenente le informazioni al nodo di destinazione richiesto (tupla host, port)
            self.sock.sendto(data, (host, port))
        except ConnectionResetError:
            # Su windows ignora l'errore generato quando si tenta di inviare a un nodo caduto
            pass
        except Exception as e:
            # Se si solleva un'eccezione stampa l'errore
            print(f"Errore di invio UDP verso la porta: {port}: {e}")


    # Dichiara il metodo per ricevere i pacchetti dal canale di comunicazione
    def receive(self):
        try:
            # Legge dal buffer di rete (massimo 4096 byte).
            # Restituisce i dati grezzi e una tupla contenente l'indirizzo IP e la porta del mittente
            data, addr = self.sock.recvfrom(4096)

            # Restituisce i dati grezzi, l'IP del mittente (addr[0]) e la porta usata dal mittente (addr[1]) come elementi separati
            return data, addr[0], addr[1]

        # Se il socket non trova nessun dato in arrivo e va in timeout o viene sollevata un'eccezione non ritorna nulla
        except (socket.timeout, BlockingIOError, ConnectionResetError):
            return None
        except Exception as e:
            print(f"Errore di ricezione UDP: {e}")
            return None


    # Definisce il metodo per chiudere il canale di comunicazione
    def close(self):
        # Chiude il socket e rilascia le risorse di rete (libera la porta utilizzata)
        self.sock.close()
