
# Importa la libreria necessaria per l'enumerazione
from enum import Enum

# Importa la libreria per la rappresentazione e la manipolazione xml
from xml.etree import ElementTree as ElemTree


class MessageType(Enum):
    # Costanti enumerative che definiscono i tre tipi di messaggi utilizzati
    ANSWER = "ANSWER"
    COORDINATOR = "COORDINATOR"
    ELECTION = "ELECTION"



class Message:
    # Inizializza un nuovo messaggio specificando il tipo di messaggio e l'ID del nodo mittente
    def __init__(self, message_type: MessageType, sender_id: int):
        self.message_type = message_type
        self.sender_id = sender_id


    # MARSHALLING: Serializza il messaggio in una rappresentazione esterna dei dati
    def to_xml(self) -> str:
        # Crea il nodo principale dell'elemento xml e lo chiama message
        xml_root = ElemTree.Element("message")

        # Crea due sottonodi collegati al nodo xml principale per inserire i valori di Type e SenderId
        xml_type_elem = ElemTree.SubElement(xml_root, "Type")
        xml_sender_id_elem = ElemTree.SubElement(xml_root, "SenderId")

        # Assegna al valore testuale degli elementi/sottonodi di root i rispettivi valori delle variabili message_type e sender_id
        xml_type_elem.text = self.message_type.value
        xml_sender_id_elem.text = str(self.sender_id)

        # serializza la struttura xml in una stringa di testo codificata in unicode e ritorna il suo valore
        return ElemTree.tostring(xml_root, encoding="unicode")


    # UNMARSHALLING: Deserializza una stringa di testo unicode ricevuta dalla rete e ricostruisce l'oggetto Message originale
    @staticmethod
    def from_xml(xml_string: str):
        # Trasforma la stringa codificata in una struttura xml
        xml_root = ElemTree.fromstring(xml_string)

        # Estrae dalla struttura xml i valori dei suoi campi/sottonodi Type e SenderId
        msg_type_str = xml_root.find("Type").text
        sender_id_str = int(xml_root.find("SenderId").text)

        # Istanzia un nuovo oggetto message utilizzando i dati estratti dalla struttura e poi restituisce l'oggetto
        return Message(MessageType(msg_type_str), sender_id_str)