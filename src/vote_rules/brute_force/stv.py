from typing import List

class stv:
    def __init__(self, candidates : List[int], votes : List[List[int]], nr_of_candidates : int) -> None:
        # List of all candidates
        self.candidates = candidates
        # List of all the votes
        self.votes = votes
        self.nr_of_candidates = nr_of_candidates
        return

    def find_worst_candidate(self) -> candidate:
        """
        Finds the worst candidate of all that is the candidate that is least time first, if there are more of tham than the one that is least time secodn etc.
        Output candidate
        """
        # Set first element to worst candidate
        worst_candidate = self.candidates[0]
        worst_candidate_list = [0] * self.nr_of_candidates
        for vote in self.votes:
            index = vote.index(worst_candidate)
            worst_candidate_list[index] += 1

        # Go thru all the candidates to find the worst
        for candidate in self.candidates:
            candidate_list = [0] * self.nr_of_candidates
            for vote in self.votes:
                index = vote.index(candidate)
                candidate_list[index] += 1
            for i in range(self.nr_of_candidates):
                if candidate_list[i] < worst_candidate_list[i]:
                    worst_candidate_list = candidate_list
                    worst_candidate = candidate
                    break
                if candidate_list[i] > worst_candidate_list[i]:
                    break
        return worst_candidate

    def remove_worst(self) -> None:
        worst = self.find_worst_candidate()
        for vote in self.votes:
            index = vote.index(worst)
            vote.pop(index)
        index = self.candidates.index(worst)
        self.candidates.pop(index)
        self.nr_of_candidates -= 1
        return

    def stv(self) -> int:
        while self.nr_of_candidates > 1:
            self.remove_worst()
        return self.candidates[0]
