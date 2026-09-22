
# Importo la libreria per l'enumerazione
from enum import Enum

# Importo la libreria per la rappresentazione xml
from xml.etree import ElementTree as ElemTree


class MessageType(Enum):
    # Definisco gli Enum dei tipi di messaggi che si andranno a utilizzare
    ANSWER = "ANSWER"
    COORDINATOR = "COORDINATOR"
    ELECTION = "ELECTION"
    PING = "PING"



class Message:

    # Costruttore della classe Message
    def __init__(self, message_type: MessageType, sender_id: int):
        self.message_type = message_type
        self.sender_id = sender_id


    # MARSHALLING: Metodo per convertire il messaggio in una rappresentazione esterna dei dati
    def to_xml(self) -> str:
        # Creo il nodo principale del messaggio xml e lo chiamo Message
        xml_root = ElemTree.Element("message")

        # Creo due sottonodi collegati al nodo xml principale chiamandoli rispettivamente Type e SenderId
        xml_type_elem = ElemTree.SubElement(xml_root, "Type")
        xml_sender_id_elem = ElemTree.SubElement(xml_root, "SenderId")

        # Assegno al valore testuale degli elementi/sottonodi di root i rispettivi valori delle variabili message_type e sender_id
        xml_type_elem.text = self.message_type.value
        xml_sender_id_elem.text = str(self.sender_id)

        # serializzo la struttura xml in una stringa di testo codificata in unicode e ritorno il suo valore
        return ElemTree.tostring(xml_root, encoding="unicode")


    # UNMARSHALLING: Metodo per riconvertire il messaggio dalla rappresentazione dei dati esterna in un oggetto della classe Message
    @staticmethod
    def from_xml(xml_string: str):
        # Trasformo la stringa codificata in un una struttura xml
        xml_root = ElemTree.fromstring(xml_string)

        # Estraggo dalla struttura xml i valori dei suoi campi/sottonodi Type e SenderId
        msg_type_str = xml_root.find("Type").text
        sender_id_str = int(xml_root.find("SenderId").text)

        # Ritorno un oggetto della classe Message appena istanziato tramite invocazione del metodo costruttore
        return Message(MessageType(msg_type_str), sender_id_str)