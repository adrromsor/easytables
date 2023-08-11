from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont

class AddRuleWindow(Toplevel):

    def __init__(self, controller, edit_mode = 0):
        super().__init__()

        if edit_mode == 1:
            self.title("Edit rule")

        else:
            self.title("Add rule")

        self.create_widgets(controller, edit_mode)

    def create_widgets(self, controller, edit_mode):
        self.source_widgets()
        self.destination_widgets()
        self.protocol_widgets()
        self.target_widgets()
        self.state_widgets()
        self.comment_widgets()

        if edit_mode == 1:
            self.edit_buttons_widgets(controller)

        else:
            self.chain_widgets()
            self.position_widgets()
            self.buttons_widgets(controller)

        self.error_widgets()

    def source_widgets(self):
        self.src_ip = StringVar()
        self.src_ip_label = ttk.Label(self, text="Source")
        self.src_ip_label.grid(column=0, row=0)
        self.src_ip_entry = ttk.Entry(self, width=20, textvariable=self.src_ip)
        self.src_ip_entry.grid(column=1, row=0, padx=10, pady=10, sticky=(W,E), columnspan=2)

        self.src_port = StringVar()
        self.src_port_label = ttk.Label(self, text="Port")
        self.src_port_label.grid(column=3, row=0)
        self.src_port_entry = ttk.Entry(self, width=5, textvariable=self.src_port)
        self.src_port_entry.grid(column=4, row=0, padx=10, pady=10, sticky=(W,E))

    def destination_widgets(self):
        self.dst_ip = StringVar()
        self.dst_ip_label = ttk.Label(self, text="Destination")
        self.dst_ip_label.grid(column=0, row=1)
        self.dst_ip_entry = ttk.Entry(self, width=20, textvariable=self.dst_ip)
        self.dst_ip_entry.grid(column=1, row=1, padx=10, pady=10, sticky=(W,E), columnspan=2)

        self.dst_port = StringVar()
        self.dst_port_label = ttk.Label(self, text="Port")
        self.dst_port_label.grid(column=3, row=1)
        self.dst_port_entry = ttk.Entry(self, width=5, textvariable=self.dst_port)
        self.dst_port_entry.grid(column=4, row=1, padx=10, pady=10, sticky=(W,E))

    def chain_widgets(self):
        self.chain = StringVar(value="INPUT")
        chains = ["INPUT", "OUTPUT"]
        self.chain_label = ttk.Label(self, text="Chain")
        self.chain_label.grid(column=0, row=2)
        self.chain_combo = ttk.Combobox(self, textvariable=self.chain, state="readonly", values=chains)
        self.chain_combo.current(0)
        self.chain_combo.grid(column=1, row=2, padx=10, pady=10, sticky=(W,E), columnspan=4)

    def protocol_widgets(self):
        self.protocol = StringVar()
        protocols = ["ALL", "TCP", "UDP"]
        self.protocol_label = ttk.Label(self, text="Protocol")
        self.protocol_label.grid(column=0, row=3)
        self.protocol_combo = ttk.Combobox(self, textvariable=self.protocol, state="readonly", values=protocols)
        self.protocol_combo.current(0)
        self.protocol_combo.grid(column=1, row=3, padx=10, pady=10, sticky=(W,E), columnspan=4)

    def target_widgets(self):
        self.target = StringVar()
        targets = ["ACCEPT", "DROP"]
        self.target_label = ttk.Label(self, text="Action")
        self.target_label.grid(column=0, row=4)
        self.target_combo = ttk.Combobox(self, textvariable=self.target, state="readonly", values=targets)
        self.target_combo.current(0)
        self.target_combo.grid(column=1, row=4, padx=10, pady=10, sticky=(W,E), columnspan=4)

    def state_widgets(self):
        self.invalid_state = IntVar()
        self.new_state = IntVar()
        self.related_state = IntVar()
        self.established_state = IntVar()
        self.state_label = ttk.Label(self, text="State")
        self.state_label.grid(column=0, row=5)
        self.invalid_state_checkbutton = ttk.Checkbutton(self, text="INVALID", variable=self.invalid_state)
        self.invalid_state_checkbutton.grid(column=1, row=5, padx=10, pady=10)
        self.new_state_checkbutton = ttk.Checkbutton(self, text="NEW", variable=self.new_state)
        self.new_state_checkbutton.grid(column=2, row=5, padx=10, pady=10)
        self.related_state_checkbutton = ttk.Checkbutton(self, text="RELATED", variable=self.related_state)
        self.related_state_checkbutton.grid(column=3, row=5, padx=10, pady=10)
        self.established_state_checkbutton = ttk.Checkbutton(self, text="ESTABLISHED", variable=self.established_state)
        self.established_state_checkbutton.grid(column=4, row=5, padx=10, pady=10)

    def comment_widgets(self):
        self.comment = StringVar()
        self.comment_label = ttk.Label(self, text="Comment")
        self.comment_label.grid(column=0, row=6)
        self.comment_entry = ttk.Entry(self, width=20, textvariable=self.comment)
        self.comment_entry.grid(column=1, row=6, padx=10, pady=10, sticky=(W,E), columnspan=4)

    def position_widgets(self):
        self.position = StringVar()
        positions = ["Bottom", "Top"]
        self.position_label = ttk.Label(self, text="Position")
        self.position_label.grid(column=0, row=7)
        self.position_combo = ttk.Combobox(self, textvariable=self.position, state="readonly", values=positions)
        self.position_combo.current(0)
        self.position_combo.grid(column=1, row=7, padx=10, pady=10, sticky=(W,E), columnspan=4)

    def buttons_widgets(self, controller):
        close_btn = ttk.Button(self, text = "Close", command=self.destroy)
        close_btn.grid(column=3, row=8, padx=10, pady=20, sticky=(W,E))
        self.save_btn = ttk.Button(self, text = "Save")
        self.save_btn.grid(column=4, row=8, padx=10, pady=20, sticky=(W,E))
        self.save_btn.bind("<Button>", controller.add_rule_action)

    def edit_buttons_widgets(self, controller):
        self.close_btn = ttk.Button(self, text = "Close", command=self.destroy)
        self.close_btn.grid(column=3, row=8, padx=10, pady=20, sticky=(W,E))
        self.save_btn = ttk.Button(self, text = "Save")
        self.save_btn.grid(column=4, row=8, padx=10, pady=20, sticky=(W,E))
        self.save_btn.bind("<Button>", controller.edit_rule_action)

    def error_widgets(self):
        style = ttk.Style()
        style.configure("E.TLabel", foreground="red")

        error_font = tkFont.Font(family="Verdana", size=16, weight="bold", slant="roman")

        self.error_label = ttk.Label(self, text="", style="E.TLabel", font="error_font")
        self.error_label.grid(column=0, row=9, columnspan=8)

    def display_error_label(self, msg=""):
        self.error_label.config(text=msg)
