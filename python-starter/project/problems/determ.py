import argparse
from collections import deque
from project.problem import Problem

class DeterminizeProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '--det',
            action='store_true',
            help='Determinize the given finite automaton'
        ) #hozzaadjuk a --det kapcsolot

    def is_chosen_problem(self, args):
        return bool(args.det)

    def run(self, args):
        input_file = args.input
        output_file = args.output

        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        raw_states = lines[0].split()
        alphabet = lines[1].split()
        start_states_raw = lines[2].split()
        accept_states_raw = set(lines[3].split())

        valid_states = set(raw_states)
        valid_alphabet = set(alphabet)

        for s in start_states_raw:
            if s not in valid_states:
                raise ValueError(f"Incorrect starting state: {s}")

        for s in accept_states_raw:
            if s not in valid_states:
                raise ValueError(f"Incorrect end state: {s}")

        nfa_transitions = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(f"Wrong temp line: {line}")
            src, sym, dst = parts

            if src not in valid_states:
                raise ValueError(f"Unknown source state: {src}")
            if sym not in valid_alphabet:
                raise ValueError(f"Unknown input signal: {sym}")
            if dst not in valid_states:
                raise ValueError(f"Unknown destination state: {dst}")

            nfa_transitions.setdefault((src, sym), set()).add(dst)


        initial_subset = frozenset(start_states_raw)
        state_mapping = {initial_subset: "s0"}
        queue = deque([initial_subset])
        ordered_subsets = [initial_subset]
        counter = 1

        dfa_transitions = []

        while queue:
            curr_subset = queue.popleft()
            curr_name = state_mapping[curr_subset]

            for sym in alphabet:
                next_subset = set()
                for q in curr_subset:
                    if (q, sym) in nfa_transitions:
                        next_subset.update(nfa_transitions[(q, sym)])

                if next_subset:
                    frozen_next = frozenset(next_subset)
                    if frozen_next not in state_mapping:
                        new_name = f"s{counter}"
                        counter += 1
                        state_mapping[frozen_next] = new_name
                        ordered_subsets.append(frozen_next)
                        queue.append(frozen_next)

                    target_name = state_mapping[frozen_next]
                    dfa_transitions.append((curr_name, sym, target_name))

        dfa_states = [f"s{i}" for i in range(len(ordered_subsets))]

        dfa_alphabet = alphabet

        dfa_start = "s0"

        dfa_accept = []
        for subset in ordered_subsets:
            if any(q in accept_states_raw for q in subset):
                dfa_accept.append(state_mapping[subset])
        dfa_accept.sort(key=lambda name: int(name[1:]))

        dfa_transitions.sort(key=lambda t: (int(t[0][1:]), t[1], int(t[2][1:])))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(" ".join(dfa_states) + "\n")
            f.write(" ".join(dfa_alphabet) + "\n")
            f.write(dfa_start + "\n")
            f.write(" ".join(dfa_accept) + "\n")
            for src, sym, dst in dfa_transitions:
                f.write(f"{src} {sym} {dst}\n")
