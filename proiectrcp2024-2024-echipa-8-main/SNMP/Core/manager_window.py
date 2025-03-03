import threading
import time
from tkinter import *
from Requests.ReceiveTrap import ReceiveTrap
from Requests.GetRequest import GetRequest, SendRequest
from Requests.SetRequest import SetRequest
from Utils.mib_utils import MIB

agent_ips = ['127.0.0.1', '127.0.0.2', '127.0.0.3']

def updateOIDs(output_text, selected_agent_ip):
    oids = {
        "1.1": "Temperatura",
        "1.2": "Nume",
        "1.3": "RAM Usage (%)",
        "1.4": "RAM Usage (GB)",
        "1.5": "CPU Usage (%)"
    }

    def fetch_data():
        while True:
            output_text.delete(1.0, END)
            output_text.insert(END, f"Agent selectat: {selected_agent_ip.get()}\n\n")

            for oid, description in oids.items():
                try:
                    value = SendRequest(oid, selected_agent_ip.get())
                    output_text.insert(END, f"  {description}: {value}\n")
                except Exception as e:
                    output_text.insert(END, f"  {description}: Eroare - {e}\n")
            output_text.insert(END, "\n")
            time.sleep(2)

    threading.Thread(target=fetch_data, daemon=True).start()

def startWindow():
    # Configurare fereastră principală
    window = Tk()
    window.title("Interfață Manager SNMP")
    window.geometry("700x550")
    window.configure(bg='#fff2e6')

    # Variabilă pentru agentul selectat
    selected_agent_ip = StringVar(window)
    selected_agent_ip.set(agent_ips[0])

    title_label = Label(
        window,
        text="Manager SNMP",
        font=('Comic Sans MS', 24, 'bold'),
        bg='#fff2e6',
        fg='#ff6600'
    )
    title_label.pack(pady=10)

    # Cadru pentru butoane
    button_frame = Frame(window, bg='#ffe6cc', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=10, padx=10)

    Label(button_frame, text="Selectează Agentul:", font=('Helvetica', 12), bg='#ffe6cc').grid(row=0, column=0, padx=5)
    agent_menu = OptionMenu(button_frame, selected_agent_ip, *agent_ips)
    agent_menu.grid(row=0, column=1, padx=5)

    Button(
        button_frame, text="Get Request", command=lambda: GetRequest(),
        bg="#ff9933", fg="white", font=('Helvetica', 14), width=20, height=2
    ).grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    Button(
        button_frame, text="Set Request", command=lambda: SetRequest(selected_agent_ip.get()),
        bg="#ff6600", fg="white", font=('Helvetica', 14), width=20, height=2
    ).grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    separator = Frame(window, height=2, bd=1, relief=SUNKEN, bg="#ff6600")
    separator.pack(fill="x", padx=20, pady=5)

    output_frame = Frame(window, bg='#ffe6cc', relief=RIDGE, borderwidth=3)
    output_frame.pack(pady=10, padx=20)

    output_label = Label(output_frame, text="Valori OID-uri în timp real", bg='#ffe6cc', font=('Helvetica', 14, 'bold'))
    output_label.pack(pady=5)

    output_text = Text(output_frame, height=8, width=60, bg="white", fg="black", font=('Helvetica', 12), wrap=WORD)
    output_text.pack(padx=10, pady=10)
    output_text.tag_configure("center", justify="center")
    output_text.tag_add("center", "1.0", "end")

    footer_label = Label(
        window,
        text="SNMP Manager - Interfață Grafică",
        bg='#fff2e6',
        fg='#cc4400',
        font=('Helvetica', 12, 'italic')
    )
    footer_label.pack(side=BOTTOM, pady=10)

    threading.Thread(target=lambda: ReceiveTrap(), daemon=True).start()
    updateOIDs(output_text, selected_agent_ip)

    window.mainloop()
