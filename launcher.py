# In questo file verrà definito il metodo responsabile dell'apertura dei 5 terminali

# Importo la libreria necessaria per l'avvio di processi e la connessione ai loro canali di input e output
import subprocess
# Importo la libreria responsabile di fornire l'accesso a parametri e funzioni specifiche dell'interprete Python
import sys
# Importo la libreria responsabile di interagire con il sistema operativo sottostante
import os
# Importo la libreria per la gestione temporale del sistema
import time
# Importo la libreria per la generazione di numeri casuali
import random


# Definisco il metodo responsabile dell'apertura dei terminali
def launch_terminal():
    # Recupero e salvo il percorso della cartella in cui si trova lo script attuale
    current_dir = os.path.abspath(os.path.dirname(__file__))

    # Scelgo casualmente l'Id del processo che andrà ad avviare l'elezione iniziale
    starter_node_id = random.randint(1, 4)

    # Dizionario con le posizioni delle finestre su macOS (x_inizio, y_inizio, x_fine, y_fine)
    # Disposizione a griglia (3 sopra, 2 sotto) per non farle sovrapporre
    mac_positions = {
        1: "{0, 0, 450, 350}",  # P1: in alto a sinistra
        2: "{450, 0, 900, 350}",  # P2: in alto al centro
        3: "{900, 0, 1350, 350}",  # P3: in alto a destra
        4: "{0, 385, 450, 700}",  # P4: in basso a sinistra
        5: "{450, 385, 900, 700}"  # P5: in basso al centro
    }
    # Parto dal processo 5 e fino al processo 1
    for i in range(5, 0, -1):
        # Se il sistema operativo su cui si sta eseguendo lo script è macOS
        if sys.platform == "darwin":
            # Estraggo le coordinate specifiche per il nodo attuale
            bounds = mac_positions[i]

            # Definisco lo script da eseguire su macchine basate su sistema operativo macOS
            apple_script = f'''
            tell application "Terminal"
                set newTab to do script "cd '{current_dir}' && clear && python3 main.py {i} {starter_node_id} && clear"
                set bounds of front window to {bounds}
            end tell
            '''
            # Un processo esegue il comando di sistema per eseguire lo script apple responsabile di lanciare il processo del nodo da terminale
            subprocess.run(["osascript", "-e", apple_script])

        # Se il sistema operativo su cui si sta eseguendo lo script è Windows
        elif sys.platform == "win32":
            # Un processo esegue lo script windows per lanciare il processo del nodo da terminale windows
            subprocess.run(f'start cmd /k "cd /d {current_dir} && clear && python main.py {i} {starter_node_id}" ', shell=True)

        # Se il sistema operativo su cui si sta eseguendo lo script è Linux
        elif sys.platform == "linux":
            # Definisco ed eseguo lo script per i sistemi Linux
            linux_script = f'gnome-terminal -- bash -c "cd \'{current_dir}\' && clear && python3 main.py {i} {starter_node_id}; exec bash"'
            subprocess.run(linux_script)

        else:
            print("Sistema operativo non supportato per l'avvio automatico")
            return

        time.sleep(1)

    print("Processi sui terminali aperti con successo")