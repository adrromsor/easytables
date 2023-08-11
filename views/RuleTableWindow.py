from tkinter import *
from tkinter import ttk

class RuleTableWindow(ttk.Frame):

    def __init__(self, container, controller):
        super().__init__()

        self.create_policies(controller)
        self.create_treeview()
        self.create_buttons(controller)

    def create_policies(self, controller):
        policies = ["ACCEPT", "DROP"]

        self.input_policy = StringVar()
        self.input_policy_label = ttk.Label(self, text="    INPUT POLICY")
        self.input_policy_label.grid(column=0, row=0, sticky=(W), columnspan = 2)
        self.input_policy_combo = ttk.Combobox(self, textvariable=self.input_policy, state="readonly", values=policies)
        self.input_policy_combo.current(0)
        self.input_policy_combo.grid(column=1, row=0, pady=10)
        self.input_policy_combo.bind("<<ComboboxSelected>>", controller.set_input_policy_action)

        self.output_policy = StringVar()
        self.output_policy_label = ttk.Label(self, text="    OUTPUT POLICY")
        self.output_policy_label.grid(column=0, row=1, sticky=(W), columnspan = 2)
        self.output_policy_combo = ttk.Combobox(self, textvariable=self.output_policy, state="readonly", values=policies)
        self.output_policy_combo.current(0)
        self.output_policy_combo.grid(column=1, row=1, pady=20)
        self.output_policy_combo.bind("<<ComboboxSelected>>", controller.set_output_policy_action)

    def create_treeview(self):
        self.tree = ttk.Treeview(self, selectmode="browse", height=15)

        self.tree.tag_configure('input', background="white")
        self.tree.tag_configure('output', background="lightblue")

        self.tree['columns'] = ("ID", "Source", "Destination", "Protocol", "Chain", "Target", "States", "Comment")

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID", anchor=W, width=30)
        self.tree.column("Source", anchor=W, width=130)
        self.tree.column("Destination", anchor=W, width=130)
        self.tree.column("Protocol", anchor=W, width=60)
        self.tree.column("Chain", anchor=W, width=60)
        self.tree.column("Target", anchor=W, width=60)
        self.tree.column("States", anchor=W, width=230)
        self.tree.column("Comment", anchor=W, width=800)

        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("ID", text="ID", anchor=W)
        self.tree.heading("Source", text="Source", anchor=W)
        self.tree.heading("Destination", text="Destination", anchor=W)
        self.tree.heading("Protocol", text="Protocol", anchor=W)
        self.tree.heading("Chain", text="Chain", anchor=W)
        self.tree.heading("Target", text="Target", anchor=W)
        self.tree.heading("States", text="States", anchor=W)
        self.tree.heading("Comment", text="Comment", anchor=W)

        self.tree.grid(column=1, row=2, columnspan = 4)

    def create_buttons(self, controller):
        self.add_rule_button = ttk.Button(self, text = "Add rule")
        self.add_rule_button.grid(column=1, row=3, padx=10, pady=20, sticky=(W,E))
        self.add_rule_button.bind("<Button>", controller.open_add_rule_window_action)

        self.edit_rule_button = ttk.Button(self, text = "Edit rule")
        self.edit_rule_button.grid(column=2, row=3, padx=10, pady=20, sticky=(W,E))
        self.edit_rule_button.bind("<Button>", controller.open_edit_rule_window_action)

        self.delete_rule_button = ttk.Button(self, text = "Delete rule")
        self.delete_rule_button.grid(column=3, row=3, padx=10, pady=20, sticky=(W,E))
        self.delete_rule_button.bind("<Button>", controller.delete_rule_action)

        self.flush_rules_button = ttk.Button(self, text = "Flush all rules")
        self.flush_rules_button.grid(column=4, row=3, padx=10, pady=20, sticky=(W,E))
        self.flush_rules_button.bind("<Button>", controller.flush_rules_action)
