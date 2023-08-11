class RuleDTO:

    def __init__(self, source_ip, source_port, destination_ip, destination_port, chain, protocol, target, states, comment):
        self.source_ip = source_ip
        self.source_port = source_port
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.chain = chain
        self.protocol = protocol
        self.target = target
        self.states = states
        self.comment = comment
