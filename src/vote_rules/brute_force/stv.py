# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import List

class stv:
    def __init__(self, candidates : List, votes : List[List]) -> None:
        # List of all candidates
        self.candidates = candidates
        # List of all the votes
        self.votes = votes
        self.nr_of_candidates = len(candidates)
        return
    
    def add_vote(self, vote : List[str]) -> None:
        self.votes.append(vote)
        return

    def find_worst_candidate(self) -> any:
        """
        Finds the worst candidate of all that is the candidate that is least time first, if there are more of tham than the one that is least time secodn etc.
        Output candidate
        """
        # Set first element to worst candidate
        worst_candidate = self.candidates[0]
        worst_candidate_list = [0] * self.nr_of_candidates
        for vote in self.votes:
            if worst_candidate in vote:
                index = vote.index(worst_candidate)
                worst_candidate_list[index] += 1

        # Go thru all the candidates to find the worst
        for candidate in self.candidates:
            # For every candidate make array of its occurrences
            candidate_list = [0] * self.nr_of_candidates
            # Find where the candidate is in this vote
            for vote in self.votes:
                if candidate in vote:
                    index = vote.index(candidate)
                    candidate_list[index] += 1
            for i in range(self.nr_of_candidates):
                # Compare current candidate to worst candidate
                if candidate_list[i] < worst_candidate_list[i]:
                    worst_candidate_list = candidate_list
                    worst_candidate = candidate
                    break
                if candidate_list[i] > worst_candidate_list[i]:
                    break
        return worst_candidate

    def remove_worst(self):
        # print("Hledame nejhorsiho:")
        # Find the worst candidate
        worst = self.find_worst_candidate()
        # From every vote remove the worst candidate
        for vote in self.votes:
            if worst in vote:
                index = vote.index(worst)
                vote.pop(index)
            # print(vote)
        # Remove worst from candidates also
        index = self.candidates.index(worst)
        self.candidates.pop(index)
        self.nr_of_candidates -= 1
        return worst

    def stv(self) -> int:
        result = []
        # Simply find the winner
        while self.nr_of_candidates > 1:
            x = self.remove_worst()
            result = [x] + result
            # print("Nejhorsi:" + str(x))
        # print(self.candidates[0])
        result = self.candidates + result
        # print(result)
        return result
