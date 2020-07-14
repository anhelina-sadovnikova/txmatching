from typing import List, Tuple, Set

from kidney_exchange.patients.donor import Donor
from kidney_exchange.patients.recipient import Recipient
from kidney_exchange.solvers.matching.transplant_cycle import TransplantCycle
from kidney_exchange.solvers.matching.transplant_round import TransplantRound
from kidney_exchange.solvers.matching.transplant_sequence import TransplantSequence


class Matching:
    """
    Set of disjoint TransplantRound's
    """

    def __init__(self, donor_recipient_list: List[Tuple[Donor, Recipient]] = None):
        # TODO list of TransplantRounds?
        self._donor_recipient_list = donor_recipient_list
        self._initialize()

    def __str__(self) -> str:
        cycles = self.get_cycles()
        sequences = self.get_cycles()

        repr = "[Matching]"

        if len(cycles) > 0:
            repr += "Cycles:\n"

            for cycle in self.get_cycles():
                repr += "\t" + str(cycle) + "\n"

        if len(sequences) > 0:
            repr = "\nSequences:\n"
            for sequence in sequences:
                repr += "\t" + str(sequence) + "\n"

        return repr

    @property
    def donor_recipient_list(self):
        return self._donor_recipient_list

    def get_cycles(self) -> Set[TransplantCycle]:
        return self._cycles

    def get_sequences(self) -> Set[TransplantSequence]:
        return self._sequences

    def get_rounds(self) -> Set[TransplantRound]:
        cycles = self.get_cycles()
        sequences = self.get_sequences()
        return set.union(cycles, sequences)

    def _initialize(self):
        recipients = [recipient for donor, recipient in self._donor_recipient_list]
        donors = [donor for donor, recipient in self._donor_recipient_list]

        # Construct graph with vertices indexed by transplants
        # Edges tell us which transplant will come next
        vertices = list(range(len(self._donor_recipient_list)))
        edges = {recipient_index: donors.index(recipient.related_donor) for recipient_index, recipient
                 in enumerate(recipients) if recipient.related_donor in donors}
        reverse_edges = {dest_vertex: source_vertex for source_vertex, dest_vertex in edges.items()}

        unprocessed_vertices = set(vertices)

        vertex_cycles = set()
        vertex_sequences = set()

        while len(unprocessed_vertices) > 0:
            start_vertex = unprocessed_vertices.pop()
            next_vertex = edges.get(start_vertex)
            vertex_round = [start_vertex]
            while next_vertex is not None and next_vertex != start_vertex:
                vertex_round.append(next_vertex)
                unprocessed_vertices.remove(next_vertex)
                next_vertex = edges.get(next_vertex)

            if next_vertex == start_vertex:
                vertex_cycles.add(tuple(vertex_round))
            elif next_vertex is None:
                previous_vertex = reverse_edges.get(start_vertex)
                while previous_vertex is not None:
                    vertex_round.insert(0, previous_vertex)
                    unprocessed_vertices.remove(previous_vertex)
                    previous_vertex = reverse_edges.get(previous_vertex)
                vertex_sequences.add(tuple(vertex_round))
            else:
                raise AssertionError("Next vertex is not None nor equal to start vertex")

        self._cycles = set(TransplantCycle([self._donor_recipient_list[i] for i in cycle])
                           for cycle in vertex_cycles)
        self._sequences = set(TransplantSequence([self._donor_recipient_list[i] for i in seq])
                              for seq in vertex_sequences)
