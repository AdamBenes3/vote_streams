class stv:
    def __init__(self, candidates, votes, nr_of_candidates):
        # List of all candidates
        self.candidates = candidates
        # List of all the votes
        self.votes = votes
        self.nr_of_candidates = nr_of_candidates

    def find_worst_candidate(self):
        # First element to worst candidate
        worst_candidate = self.candidates[0]
        worst_candidate_list = [0] * self.nr_of_candidates
        for vote in votes:
            index = vote.index(worst_candidate)
            worst_candidate_list[index] += 1

        for candidate in candidates:
            candidate_list = [0] * self.nr_of_candidates
            for vote in votes:
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

    def remove_worst(self):
        worst = self.find_worst_candidate()
        for vote in self.votes:
            index = vote.index(worst)
            vote.pop(index)
        index = self.candidates.index(worst)
        self.candidates.pop(index)
        self.nr_of_candidates -= 1

    def stv(self):
        while self.nr_of_candidates > 1:
            self.remove_worst()
        return self.candidates[0]


candidates = [1, 2, 3, 4, 5]
votes = [[4, 2, 3, 1, 5], [3, 1, 2, 4, 5], [4, 1, 3, 5, 2], [5, 1, 3, 2, 4]]

print("Votes: ")

for vote in votes:
    print(vote)

S = stv(candidates, votes, len(candidates))

print("Winner: " + str(S.stv()))



