from tkinter import *
import socket
from Protocol.packet_utils import *
from Utils.mib_utils import MIB

def SetRequest(selected_agent_ip):
    def introdusNume(inputtxt):
        nume = inputtxt.get("1.0", "end-1c")

        UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        encoded_message = encode_snmp_message(
            version=1,
            community="public",
            pdu_type=0xA3,  # Set Request
            request_id=1,
            error_status=0,
            error_index=0,
            variable_bindings=[("2.1", nume)]
        )
        UDPclient.sendto(encoded_message, (selected_agent_ip, 161))

        data = UDPclient.recvfrom(1024)[0]
        decoded_message = decode_snmp_message(data)
        response = decoded_message['variable_bindings'][0][1]
        print("Numele a fost schimbat în", response)

    def changeTemperature(temp):
        UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        encoded_message = encode_snmp_message(
            version=1,
            community="public",
            pdu_type=0xA3,  # Set Request
            request_id=1,
            error_status=0,
            error_index=0,
            variable_bindings=[("2.2", temp)]
        )
        UDPclient.sendto(encoded_message, (selected_agent_ip, 161))

        data = UDPclient.recvfrom(1024)[0]
        decoded_message = decode_snmp_message(data)
        response = decoded_message['variable_bindings'][0][1]
        print("Temperatura a fost schimbată în", response)

    def changeRamThreshold(value):

        UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        encoded_message = encode_snmp_message(
            version=1,
            community="public",
            pdu_type=0xA3,  # Set Request
            request_id=1,
            error_status=0,
            error_index=0,
            variable_bindings=[("2.3", float(value))]
        )
        UDPclient.sendto(encoded_message, (selected_agent_ip, 161))

        data = UDPclient.recvfrom(1024)[0]
        decoded_message = decode_snmp_message(data)
        response = decoded_message['variable_bindings'][0][1]
        print("Pragul RAM a fost setat la", response)

    def changeCpuThreshold(value):

        UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        encoded_message = encode_snmp_message(
            version=1,
            community="public",
            pdu_type=0xA3,  # Set Request
            request_id=1,
            error_status=0,
            error_index=0,
            variable_bindings=[("2.4", float(value))]
        )
        UDPclient.sendto(encoded_message, (selected_agent_ip, 161))

        data = UDPclient.recvfrom(1024)[0]
        decoded_message = decode_snmp_message(data)
        response = decoded_message['variable_bindings'][0][1]
        print("Pragul CPU a fost setat la", response)

    def setRequestName():

        name_window = Tk()
        name_window.title("Introduceți Numele")
        name_window.geometry("700x400")
        name_window.configure(bg='#ccffcc')

        Label(
            name_window, text="Introduceți Numele Agentului SNMP",
            bg='#ccffcc', fg='#006600', font=('Comic Sans MS', 18, 'bold')
        ).pack(pady=20)

        inputtxt = Text(name_window, height=1, width=40, bg="white", font=('Helvetica', 14))
        inputtxt.pack(pady=10)

        Button(
            name_window, text="Setează Nume", command=lambda: introdusNume(inputtxt),
            bg="#33cc33", fg="white", font=('Helvetica', 14), width=15
        ).pack(pady=20)

        Button(
            name_window, text="Înapoi", command=name_window.destroy,
            bg="#006400", fg="white", font=('Helvetica', 14), width=15
        ).pack(pady=20)

        name_window.mainloop()

    def setRequestTemperature():

        temp_window = Tk()
        temp_window.title("Setare Temperatură")
        temp_window.geometry("700x400")
        temp_window.configure(bg='#e6f2ff')

        Label(
            temp_window, text="Alegeți Unitatea de Temperatură",
            bg='#e6f2ff', fg='#004080', font=('Comic Sans MS', 18, 'bold')
        ).pack(pady=20)

        button_style = {"bg": "#3385ff", "fg": "white", "font": ('Helvetica', 14), "width": 20, "height": 2}

        Button(temp_window, text="Celsius", command=lambda: changeTemperature("Celsius"), **button_style).pack(pady=10)
        Button(temp_window, text="Fahrenheit", command=lambda: changeTemperature("Fahrenheit"), **button_style).pack(pady=10)
        Button(temp_window, text="Kelvin", command=lambda: changeTemperature("Kelvin"), **button_style).pack(pady=10)

        Button(
            temp_window, text="Înapoi", command=temp_window.destroy,
            bg="#004080", fg="white", font=('Helvetica', 14, 'bold'), width=15
        ).pack(pady=20)

        temp_window.mainloop()

    def setRequestSliders():

        slider_window = Tk()
        slider_window.title("Setare Praguri RAM și CPU")
        slider_window.geometry("700x400")
        slider_window.configure(bg='#f9f9f9')

        Label(
            slider_window, text="Setați Pragurile RAM și CPU",
            bg='#f9f9f9', fg='#333333', font=('Comic Sans MS', 18, 'bold')
        ).pack(pady=20)

        ram_label = Label(slider_window, text="Prag RAM (%)", bg='#f9f9f9', font=('Helvetica', 14))
        ram_label.pack(pady=10)
        ram_slider = Scale(
            slider_window, from_=30, to=100, orient=HORIZONTAL, length=400, command=lambda value: changeRamThreshold(value)
        )
        ram_slider.set(MIB.get_check_ram())
        ram_slider.pack()

        cpu_label = Label(slider_window, text="Prag CPU (%)", bg='#f9f9f9', font=('Helvetica', 14))
        cpu_label.pack(pady=10)
        cpu_slider = Scale(
            slider_window, from_=30, to=100, orient=HORIZONTAL, length=400, command=lambda value: changeCpuThreshold(value)
        )
        cpu_slider.set(MIB.get_check_cpu())
        cpu_slider.pack()

        Button(
            slider_window, text="Înapoi", command=slider_window.destroy,
            bg="#333333", fg="white", font=('Helvetica', 14), width=15
        ).pack(pady=20)

        slider_window.mainloop()

    main_window = Tk()
    main_window.title("Setare Informații SNMP")
    main_window.geometry("700x400")
    main_window.configure(bg='#ffe5e5')

    Label(
        main_window,
        text="Setează Parametrii SNMP",
        font=('Comic Sans MS', 20, 'bold'),
        bg='#ffe5e5',
        fg='#ff3333'
    ).pack(pady=20)

    button_frame = Frame(main_window, bg='#ffcccc', relief=RAISED, borderwidth=3)
    button_frame.pack(pady=20, padx=20)

    Button(
        button_frame, text="Setează Nume", command=setRequestName,
        bg="#ff66b2", fg="white", font=('Arial', 14), width=20, height=2
    ).grid(row=0, column=0, padx=15, pady=10)

    Button(
        button_frame, text="Setează Temperatură", command=setRequestTemperature,
        bg="#ff66b2", fg="white", font=('Arial', 14), width=20, height=2
    ).grid(row=0, column=1, padx=15, pady=10)

    Button(
        button_frame, text="Setează RAM și CPU Usage", command=setRequestSliders,
        bg="#ff66b2", fg="white", font=('Arial', 14), width=20, height=2
    ).grid(row=1, column=0, columnspan=2, pady=10)

    Button(
        main_window, text="Înapoi", command=main_window.destroy,
        bg="#ff3333", fg="white", font=('Helvetica', 14, 'bold'), width=15, height=2
    ).pack(pady=20)

    main_window.mainloop()
