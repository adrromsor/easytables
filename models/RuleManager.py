import subprocess
import re
from models.RuleDTO import RuleDTO

class RuleManager:

    def update_rules(self):
        rules = []
        result = subprocess.run(['sudo', 'iptables', '-S'], capture_output=True, text=True).stdout

        for line in result.splitlines()[3:]:
            chain = self.get_chain_from_line(line)
            if chain != None:
                source_ip = self.get_source_ip_from_line(line)
                destination_ip = self.get_destination_ip_from_line(line)
                protocol = self.get_protocol_from_line(line)
                source_port = self.get_source_port_from_line(line)
                destination_port = self.get_destination_port_from_line(line)
                states = self.get_states_from_line(line)
                comment = self.get_comment_from_line(line)
                target = self.get_target_from_line(line)

                rule_dto = RuleDTO(source_ip, source_port, destination_ip, destination_port, chain, protocol, target, states, comment)
                rules.append(rule_dto)

        return rules

    def get_rule(self, source_ip, source_port, destination_ip, destination_port, chain, protocol, target, states, comment):
        rule_dto = RuleDTO(source_ip, source_port, destination_ip, destination_port, chain, protocol, target, states, comment)

        return rule_dto

    def create_rule(self, rule):
        chain = getattr(rule, "chain")
        protocol = getattr(rule, "protocol").lower()
        source_ip = getattr(rule, "source_ip").replace(" ", "")
        destination_ip = getattr(rule, "destination_ip").replace(" ", "")
        source_port = getattr(rule, "source_port")
        destination_port = getattr(rule, "destination_port")
        target = getattr(rule, "target")
        states = getattr(rule, "states")
        comment = getattr(rule, "comment").replace("\"", " ")

        new_rule = chain + " -p " + protocol + " -j " + target

        if source_ip:
            new_rule += " -s " + source_ip

        if destination_ip:
            new_rule += " -d " + destination_ip

        if source_port:
            new_rule += " --sport " + source_port

        if destination_port:
            new_rule += " --dport " + destination_port

        if len(states) > 0:
            states_string = ','.join(states)
            new_rule =  new_rule + " -m conntrack --ctstate " + states_string

        if comment:
            new_rule =  new_rule + " -m comment --comment \"" + comment + "\""

        return new_rule

    def append_rule(self, rule, position):
        new_rule = self.create_rule(rule)

        if position == 'Top':
            chain = getattr(rule, "chain")

            if chain == 'INPUT':
                new_rule = new_rule[:6] + "1 " + new_rule[6:]
            else:
                new_rule = new_rule[:7] + "1 " + new_rule[7:]

            subprocess.call("sudo iptables -I " + new_rule, shell=True)

        else:
            subprocess.call("sudo iptables -A " + new_rule, shell=True)

    def replace_rule(self, rule, rule_id):
        new_rule = self.create_rule(rule)

        if getattr(rule, "chain") == 'INPUT':
            new_rule = new_rule[:6] + rule_id + " " + new_rule[6:]
            subprocess.call("sudo iptables -R " + new_rule, shell=True)

        else:
            new_rule = new_rule[:7] + rule_id + " " + new_rule[7:]
            subprocess.call("sudo iptables -R " + new_rule, shell=True)

    def delete_rule(self, rule_id, chain):
        subprocess.call("sudo iptables -D " + chain + " " + str(rule_id), shell=True)

    def flush_rules(self):
        subprocess.call("sudo iptables -F", shell=True)

    def get_chain_from_line(self, line):
        try:
            chain = re.search('INPUT|OUTPUT', line).group()

        except AttributeError:
            chain = None

        return chain

    def get_source_ip_from_line(self, line):
        try:
            source_ip = re.search('-s ([^\/]+)', line).group(1)

        except AttributeError:
            source_ip = ''

        return source_ip

    def get_destination_ip_from_line(self, line):
        try:
            destination_ip = re.search('-d ([^\/]+)', line).group(1)

        except AttributeError:
            destination_ip = ''

        return destination_ip

    def get_source_port_from_line(self, line):
        try:
            source_port = re.search('--sport (\d+)', line).group(1)

        except AttributeError:
            source_port = ''

        return source_port

    def get_destination_port_from_line(self, line):
        try:
            destination_port = re.search('--dport (\d+)', line).group(1)

        except AttributeError:
            destination_port = ''

        return destination_port

    def get_protocol_from_line(self, line):
        try:
            protocol = re.search('all|tcp|udp', line).group()

        except AttributeError:
            protocol = 'all'

        return protocol

    def get_states_from_line(self, line):
        try:
            states = re.findall('INVALID|NEW|RELATED|ESTABLISHED', line)

        except AttributeError:
            states = []

        return states

    def get_comment_from_line(self, line):
        try:
            comment = re.search('"(.+)"', line).group(1)

        except AttributeError:
            try:
                comment = re.search('--comment ([^\s]+)', line).group(1)

            except AttributeError:
                comment = ''

        return comment

    def get_target_from_line(self, line):
        try:
            target = re.search('ACCEPT|DROP', line).group()

        except AttributeError:
            target = 'ACCEPT'

        return target
