from tkinter import *
import socket
from Protocol.packet_utils import *
from Utils.mib_utils import *

agentIp = '127.0.0.1'
conn = agentIp
bufferSize = 1024

def update_textbox(message):
    output_text.delete(1.0, END)
    textbox_height = int(output_text['height'])
    lines_required = (textbox_height - 1) // 2
    for _ in range(lines_required):
        output_text.insert(END, "\n")
    output_text.insert(END, message)
    output_text.tag_add("center", 1.0, "end")

def GetRequest():
    window = Tk()
    window.title("Cereri SNMP")
    window.geometry("800x500")
    window.configure(bg='#f0f0ff')
    title_label = Label(
        window,
        text="Selectați informația dorită",
        font=('Comic Sans MS', 20, 'bold'),
        bg='#f0f0ff',
        fg='#6633ff'
    )
    title_label.pack(pady=10)
    button_frame = Frame(window, bg='#e6e6ff', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=10, padx=10)
    button_commands = [
        ("Nume", GetRequestName),
        ("Temperatura", GetRequestTemperatura),
        ("Ram % Usage", GetRequestRamPercent),
        ("Ram Gb Usage", GetRequestRamGB),
        ("Cpu Usage", GetRequestCpuUsage)
    ]
    for i, (text, command) in enumerate(button_commands):
        Button(
            button_frame,
            text=text,
            command=command,
            bg="#6699ff", fg="white", font=('Arial', 14),
            width=20, height=2
        ).grid(row=i // 2, column=i % 2, padx=15, pady=5)
    separator = Frame(window, height=2, bd=1, relief=SUNKEN, bg="#6633ff")
    separator.pack(fill="x", padx=20, pady=10)
    global output_text
    output_text = Text(
        window,
        height=6,
        width=40,
        bg="#ffffff",
        fg="#333333",
        font=('Arial', 14),
        wrap=WORD,
        relief=RIDGE,
        bd=2
    )
    output_text.tag_configure("center", justify="center")
    output_text.pack(padx=20, pady=5)
    back_button_frame = Frame(window, bg='#f0f0ff')
    back_button_frame.pack(side=BOTTOM, pady=10)
    Button(
        back_button_frame, text="Înapoi", command=window.destroy,
        bg="#cc33ff", fg="white", font=('Helvetica', 14, 'bold'), width=15, height=2
    ).pack()
    window.mainloop()

def SendRequest(oid, agent_ip):
    message = encode_snmp_message(
        version=1,
        community="public",
        pdu_type=GET_REQUEST,
        request_id=1,
        error_status=0,
        error_index=0,
        variable_bindings=[(oid, None)]
    )
    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPclient.sendto(message, (agent_ip, 161))
    data = UDPclient.recvfrom(bufferSize)[0]
    decoded = decode_snmp_message(data)
    return decoded['variable_bindings'][0][1]

def GetRequestTemperatura():
    value = SendRequest("1.1", agent_ip=agentIp)
    temperature = float(value)

    if temperature > 273:
        unit = "°K"
    elif temperature > 100:
        unit = "°F"
    else:
        unit = "°C"
    update_textbox(f"Temperatura: {temperature:.2f} {unit}")

def GetRequestName():
    value = SendRequest("1.2", agent_ip=agentIp)
    update_textbox(f"Numele agentului: {value}")

def GetRequestRamPercent():
    value = SendRequest("1.3", agent_ip=agentIp)
    update_textbox(f"RAM Usage: {float(value):.2f}%")

def GetRequestRamGB():
    value = SendRequest("1.4", agent_ip=agentIp)
    update_textbox(f"RAM Usage: {float(value):.2f} GB")

def GetRequestCpuUsage():
    value = SendRequest("1.5", agent_ip=agentIp)
    update_textbox(f"CPU usage: {float(value):.2f}%")








