# Script per controllare un proiettore tramite interfaccia grafica
# Pacchetti da installare con pip (se non già presenti):
# pip install pypjlink
# pip install ttkbootstrap

import tkinter as tk
from pypjlink import Projector
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Simulazione del proiettore
projector = Projector.from_address('indirizzo_ip') # Indirizzo IP del proiettore
projector.authenticate('admin') # Password di accesso al proiettore

# Stato iniziale dell'audio/video
audio_video_on = False

# Funzione per determinare lo stato del proiettore (acceso o spento)
def stato_proiettore():
    stato = projector.get_power()
    if stato == 'on':
        return True
    else:
        return False

# Funzione per accendere o spegnere il proiettore
def accendi_o_spegni():
    global proiettore_acceso
    if proiettore_acceso:
        mostra_conferma_spegnimento()
    else:
        projector.set_power('on')
        stato_label.config(text="Stato proiettore: ON", bootstyle="success")
        pulsante_on.config(state="disabled", bootstyle="success")  # Disabilita il pulsante ON
        pulsante_off.config(state="normal", bootstyle="danger")  # Abilita il pulsante OFF
        pulsante_audio_video.config(state="normal", bootstyle="success")  # Abilita il pulsante audio/video
        proiettore_acceso = True
        toggle_audio_video()  # Attiva l'audio/video appena acceso il proiettore

# Finestra di conferma per spegnere il proiettore
def mostra_conferma_spegnimento():
    conferma_finestra = tk.Toplevel(root)
    conferma_finestra.title("Conferma Spegnimento Proiettore")
    conferma_finestra.geometry("300x100")
    conferma_finestra.grab_set()

    label = ttk.Label(conferma_finestra, text="Spegnere il proiettore?", font=("Arial", 12))
    label.pack(pady=10)

    btn_si = ttk.Button(conferma_finestra, text="Sì", command=lambda: spegni(conferma_finestra))
    btn_si.pack(side="left", padx=30, pady=10)
    btn_no = ttk.Button(conferma_finestra, text="No", command=conferma_finestra.destroy)
    btn_no.pack(side="right", padx=30, pady=10)

# Spegne il proiettore e aggiorna la GUI
def spegni(conferma_finestra):
    projector.set_power('off')
    conferma_finestra.destroy()
    stato_label.config(text="Stato proiettore: OFF", bootstyle="danger")
    pulsante_on.config(state="normal", bootstyle="success")  # Abilita il pulsante ON
    pulsante_off.config(state="disabled", bootstyle="danger")  # Disabilita il pulsante OFF
    pulsante_audio_video.config(state="disabled", bootstyle="light")  # Disabilita il pulsante audio/video
    pulsante_audio_video.config(text="Audio/Video")  # Reset del testo del pulsante
    global proiettore_acceso, audio_video_on
    proiettore_acceso = False
    audio_video_on = False  # Resetta lo stato dell'audio/video quando il proiettore è spento

# Funzione per accendere o spegnere audio e video
def toggle_audio_video():
    global audio_video_on
    if audio_video_on:
        # Spegnere audio e video
        projector.send_command("AVMT", "31")
        pulsante_audio_video.config(bootstyle="success", text="Audio/Video")
    else:
        # Accendere audio e video
        projector.send_command("AVMT", "30")
        pulsante_audio_video.config(bootstyle="light", text="Audio/Video")

    audio_video_on = not audio_video_on

# Stato iniziale del proiettore (verifica se è acceso o spento)
proiettore_acceso = stato_proiettore()

# Creazione della finestra principale
root = ttk.Window(themename="flatly")
root.title("Controllo Dispositivo")
root.geometry("750x250")

# Creazione della casella di testo per lo stato del proiettore
stato_label = ttk.Label(
    root,
    text="Stato proiettore: " + ("ON" if proiettore_acceso else "OFF"),
    font=("Arial", 14),
    bootstyle="success" if proiettore_acceso else "danger"
)
stato_label.pack(pady=20)

# Creazione dei pulsanti ON e OFF
frame_pulsanti = ttk.Frame(root, padding=10)
frame_pulsanti.pack(pady=20)

pulsante_on = ttk.Button(
    frame_pulsanti,
    text="ON",
    command=accendi_o_spegni,
    width=15,
    bootstyle="success" if not proiettore_acceso else "light",
    state="normal" if not proiettore_acceso else "disabled"
)
pulsante_on.pack(side="left", padx=5)

pulsante_off = ttk.Button(
    frame_pulsanti,
    text="OFF",
    command=mostra_conferma_spegnimento,
    width=15,
    bootstyle="danger" if proiettore_acceso else "light",
    state="disabled" if not proiettore_acceso else "normal"
)
pulsante_off.pack(side="left", padx=5)

# Creazione del pulsante per audio/video
pulsante_audio_video = ttk.Button(
    frame_pulsanti,
    text="Audio/Video",
    command=toggle_audio_video,
    width=20,
    bootstyle="light",  # Inizialmente il pulsante è spento
    state="disabled" if not proiettore_acceso else "normal"  # Il pulsante è disabilitato se il proiettore è spento
)
pulsante_audio_video.pack(side="left", padx=5)

# Avvio del loop della GUI
root.mainloop()
