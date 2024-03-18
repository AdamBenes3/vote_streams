from vector import Vector

class Plurality:
    def __init__(self):
        self.result = Vector([1, 3, 4])
    def ticket_update(self, new_ticket):
        self.result += new_ticket

PL = Plurality()

PL.ticket_update(Vector([1, 4]))

PL.ticket_update(Vector([1, 4]))

print(PL.result)