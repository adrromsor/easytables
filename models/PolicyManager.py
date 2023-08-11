import subprocess

class PolicyManager:

    def update_policies(self):
        policies = []
        result = subprocess.run(['sudo', 'iptables', '-S'], capture_output=True, text=True).stdout

        input_policy = result.splitlines()[0]
        output_policy = result.splitlines()[2]

        splitted_input_policy = input_policy.split()
        splitted_output_policy = output_policy.split()

        defined_input_policy = splitted_input_policy[2]
        defined_output_policy = splitted_output_policy[2]

        policies = [defined_input_policy, defined_output_policy]

        return policies

    def set_policy(self, chain, target):
        subprocess.call("sudo iptables -P " + chain + " " + target, shell=True)
