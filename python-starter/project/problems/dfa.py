import argparse
from project.problem import Problem

class DFAproblem(Problem):
    
    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--check',
            type=str,
            help='Commas separated list of words to check'
        )

    def is_chosen_problem(self, args):
        """
        Akkor valasztjuk ezt a feladatot, ha a felhasznalo megadta a --check kapcsolot.
        """
        return bool(args.check)

    def run(self, args):
        """
        A DFA szimulacio futtatasa.
        """
        input_file = args.input
        output_file = args.output
        words_to_check = args.check

        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        start_state = lines[2]
        accept_states = set(lines[3].split())

        transitions = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                src, symbol, dst = parts
                transitions[(src, symbol)] = dst

        words = words_to_check.split(',')
        results = []

        for word in words:
            curr_state = start_state
            accepted = True

            for char in word:
                if (curr_state, char) in transitions:
                    curr_state = transitions[(curr_state, char)]
                else:
                    accepted = False
                    break

            if accepted and (curr_state in accept_states):
                results.append("IGEN")
            else:
                results.append("NEM")

        with open(output_file, 'w') as f:
            f.write('\n'.join(results) + '\n')

