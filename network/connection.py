
# Importo la libreria per la gestione di socket e connessione
import socket


class UdpConnection:
    # Definisco il costruttore della classe UdpConnection
    def __init__(self, host, port):
        # Creo il socket di rete e lo salvo nella variabile di istanza, specificando l'uso di datagrammi UDP e l'uso di indirizzi IPv4
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Faccio il binding del socket appena creato all'indirizzo IP e alla porta specificati da host e port
        self.sock.bind((host, port))

        # Rallento il proesso per non saturare il processore
        self.sock.settimeout(0.1)


    # Definisco il metodo per inviare pacchetti sul canale di comunicazione
    def send(self, data: bytes, host: str, port: int):
        try:
            # Invio il pacchetto contenente le informazioni, la funzione sendto richiede necessariamente una tupla (host, port)
            self.sock.sendto(data, (host, port))
        except Exception as e:
            # Se si solleva un'eccezione stampo l'errore
            print(f"Errore di invio UDP verso la porta: {port}: {e}")


    # Dichiaro il metodo per riceve i pacchetti dal canale di comunicazione
    def receive(self):
        try:
            # Salvo il contenuto del messaggio (max 4096 bytes) nella variabile data e le coordinate del mittente nela tupla addr ('IP', porta)
            data, addr = self.sock.recvfrom(4096)

            # Restituisco i dati grezzi, l'IP del mittente (addr[0]) e la porta usata dal mittente (addr[1]) come elementi separati
            return data, addr[0], addr[1]

        # Se il socket non trova nessun dato in arrivo o viene sollevata un eccezione non ritorna nulla
        except (socket.timeout, BlockingIOError):
            return None
        except Exception as e:
            print(f"Errore di ricezione UDP: {e}")
            return None


    # Definisco il metodo per chiudere la connessione
    def close(self):
        # Chiudo il socket e rilasciano le risorse di rete (libera la porta utilizzata)
        self.sock.close()
