import modules.validation_module as validation_module

class TableManager:

    def __init__(self, table, rows):
        self.table = table
        self.input_index = 1
        self.output_index = 1

        for row in rows:
            self.add_row(row)

    def validate_user_input(self, source_ip, source_port, destination_ip, destination_port, protocol):
        validation_result = validation_module.validate_user_input(source_ip, source_port, destination_ip, destination_port, protocol)

        return validation_result

    def add_row(self, row, position = 'Bottom'):
        new_row_values = self.new_row(row)

        chain = new_row_values[3]

        if chain == 'INPUT':
            if position == 'Top':
                self.table.insert(parent='', index=0, values=(1, new_row_values[0], new_row_values[1], new_row_values[2], new_row_values[3], new_row_values[4], new_row_values[5], new_row_values[6]), tags='input')
                return self.regenerate_indexes()

            else:
                self.table.insert(parent='', index='end', values=(self.input_index, new_row_values[0], new_row_values[1], new_row_values[2], new_row_values[3], new_row_values[4], new_row_values[5], new_row_values[6]), tags='input')

            self.input_index += 1

        else:
            if position == 'Top':
                self.table.insert(parent='', index=0, values=(1, new_row_values[0], new_row_values[1], new_row_values[2], new_row_values[3], new_row_values[4], new_row_values[5], new_row_values[6]), tags='output')
                return self.regenerate_indexes()

            else:
                self.table.insert(parent='', index='end', values=(self.output_index, new_row_values[0], new_row_values[1], new_row_values[2], new_row_values[3], new_row_values[4], new_row_values[5], new_row_values[6]), tags='output')

            self.output_index += 1

    def regenerate_indexes(self):
        self.input_index = 1
        self.output_index = 1

        for row in self.table.get_children():
            chain = self.table.set(row, column='Chain')

            if chain == 'INPUT':
                self.table.set(row, column='ID', value=self.input_index)
                self.table.item(row, tags='input')

                self.input_index += 1

            else:
                self.table.set(row, column='ID', value=self.output_index)
                self.table.item(row, tags='output')

                self.output_index += 1

    def get_row_id(self):
        selected_row = self.table.focus()

        if selected_row != "":
            selected_row_id = self.table.set(selected_row, column='ID')

            return selected_row_id

        else:
            return None

    def get_row_chain(self):
        selected_row = self.table.focus()

        if selected_row != "":
            selected_row_chain = self.table.set(selected_row, column='Chain')

            return selected_row_chain

        else:
            return None

    def get_row_values(self):
        selected_row = self.table.focus()

        if selected_row != "":
            row_values = self.table.item(selected_row, 'values')

            return row_values

        else:
            return None

    def edit_row(self, row):
        new_row_values = self.new_row(row)

        selected_row = self.table.focus()
        id = str(self.table.item(selected_row, 'values')[0])

        self.table.item(selected_row, values=(id, new_row_values[0], new_row_values[1], new_row_values[2], new_row_values[3], new_row_values[4], new_row_values[5], new_row_values[6]))

    def delete_row(self):
        selected_row = self.table.focus()
        self.table.delete(selected_row)

        self.regenerate_indexes()

    def delete_all_rows(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.input_index = 1
        self.output_index = 1

    def new_row(self, row):
        source_ip = getattr(row, "source_ip")
        source_port = getattr(row, "source_port")
        destination_ip = getattr(row, "destination_ip")
        destination_port = getattr(row, "destination_port")
        protocol = getattr(row, "protocol").upper()
        chain = getattr(row, "chain")
        target = getattr(row, "target")
        states = getattr(row, "states")
        comment = getattr(row, "comment")

        if source_port:
            source_ip = source_ip + ':' + source_port

        if destination_port:
            destination_ip = destination_ip + ':' + destination_port

        states = getattr(row, "states")
        if len(states) > 0:
            states_string = ','.join(states)
        else:
            states_string = ''

        values = [source_ip, destination_ip, protocol, chain, target, states_string, comment]

        return values
