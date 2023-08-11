from tkinter import *
from models.PolicyManager import PolicyManager
from models.RuleManager import RuleManager
from models.TableManager import TableManager
from views.AddRuleWindow import AddRuleWindow
from views.RuleTableWindow import RuleTableWindow

class Application(Tk):

    def __init__(self):
        super().__init__()

        self.title("EasyTables - iptables made easy")

        # Designate Height and Width of the app
        app_width = 1500
        app_height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2 ) - (app_height / 2)

        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.mainframe = Frame(self)

        self.policy_manager_model = PolicyManager()
        policies = self.policy_manager_model.update_policies()

        self.rule_manager_model = RuleManager()
        rules = self.rule_manager_model.update_rules()
        self.rule_table_view = RuleTableWindow(self.mainframe, self)
        self.update_policies(policies)
        rules_table = self.rule_table_view.tree
        self.table_manager_model = TableManager(rules_table, rules)

        self.rule_table_view.grid(column=0, row=0)

    def update_policies(self, policies):
        self.rule_table_view.input_policy_combo.set(policies[0])
        self.rule_table_view.output_policy_combo.set(policies[1])

    def open_add_rule_window_action(self, event):
        self.add_rule_view = AddRuleWindow(self)

    def add_rule_action(self, event):
        rule = self.create_rule_action()

        if rule != None:
            position = self.add_rule_view.position_combo.get()

            self.rule_manager_model.append_rule(rule, position)
            self.table_manager_model.add_row(rule, position)

    def open_edit_rule_window_action(self, event):
        selected_rule_values = self.table_manager_model.get_row_values()

        if selected_rule_values != None:
            if ":" in selected_rule_values[1]:
                source_socket = selected_rule_values[1].split(':')
                source_ip = source_socket[0]
                source_port = source_socket[1]

            else:
                source_ip = selected_rule_values[1]
                source_port = ''

            if ":" in selected_rule_values[2]:
                destination_socket = selected_rule_values[2].split(':')
                destination_ip = destination_socket[0]
                destination_port = destination_socket[1]

            else:
                destination_ip = selected_rule_values[2]
                destination_port = ''

            protocol = selected_rule_values[3]
            target = selected_rule_values[5]
            states = selected_rule_values[6]
            comment = selected_rule_values[7]

            if len(states) > 0:
                states_array = states.split(',')
            else:
                states_array = None

            self.add_rule_view = AddRuleWindow(self, 1)

            self.add_rule_view.src_ip_entry.insert(0, source_ip)
            self.add_rule_view.src_port_entry.insert(0, source_port)
            self.add_rule_view.dst_ip_entry.insert(0, destination_ip)
            self.add_rule_view.dst_port_entry.insert(0, destination_port)
            self.add_rule_view.protocol_combo.set(protocol)
            self.add_rule_view.target_combo.set(target)
            self.add_rule_view.comment_entry.insert(0, comment)

            if states_array != None:
                for state in states_array:

                    if state == 'INVALID':
                        self.add_rule_view.invalid_state.set(1)

                    elif state == 'NEW':
                        self.add_rule_view.new_state.set(1)

                    elif state == 'RELATED':
                        self.add_rule_view.related_state.set(1)

                    else:
                        self.add_rule_view.established_state.set(1)

    def edit_rule_action(self, event):
        rule = self.create_rule_action(1)

        if rule != None:
            rule_id = str(self.table_manager_model.get_row_id())

            self.rule_manager_model.replace_rule(rule, rule_id)
            self.table_manager_model.edit_row(rule)

            self.add_rule_view.display_error_label()

    def delete_rule_action(self, event):
        selected_rule_id = self.table_manager_model.get_row_id()
        selected_rule_chain = self.table_manager_model.get_row_chain()

        if selected_rule_id != None:
            self.rule_manager_model.delete_rule(selected_rule_id, selected_rule_chain)
            self.table_manager_model.delete_row()

    def flush_rules_action(self, event):
        self.rule_manager_model.flush_rules()
        self.table_manager_model.delete_all_rows()

    def create_rule_action(self, edit_mode = 0):
        source_ip = self.add_rule_view.src_ip_entry.get()
        source_port = self.add_rule_view.src_port_entry.get()
        destination_ip = self.add_rule_view.dst_ip_entry.get()
        destination_port = self.add_rule_view.dst_port_entry.get()
        protocol = self.add_rule_view.protocol_combo.get()
        target = self.add_rule_view.target_combo.get()
        comment = self.add_rule_view.comment_entry.get()

        if edit_mode == 1:
            chain = self.table_manager_model.get_row_chain()

        else:
            chain = self.add_rule_view.chain_combo.get()

        states_dictionary = dict()
        states_dictionary['invalid'] = self.add_rule_view.invalid_state.get()
        states_dictionary['new'] = self.add_rule_view.new_state.get()
        states_dictionary['related'] = self.add_rule_view.related_state.get()
        states_dictionary['established'] = self.add_rule_view.established_state.get()

        states = []
        for i in states_dictionary:
            if states_dictionary[i] == 1:
                states.append(str(i.upper()))

        validation_result = self.table_manager_model.validate_user_input(source_ip, source_port, destination_ip, destination_port, protocol)

        if validation_result == True:
            rule = self.rule_manager_model.get_rule(source_ip, source_port, destination_ip, destination_port, chain, protocol, target, states, comment)

            self.add_rule_view.display_error_label()

            return rule

        else:
            self.add_rule_view.display_error_label("Error: " + validation_result)

            return None

    def set_input_policy_action(self, event):
        target = self.rule_table_view.input_policy_combo.get()
        self.policy_manager_model.set_policy("INPUT", target)

    def set_output_policy_action(self, event):
        target = self.rule_table_view.output_policy_combo.get()
        self.policy_manager_model.set_policy("OUTPUT", target)
