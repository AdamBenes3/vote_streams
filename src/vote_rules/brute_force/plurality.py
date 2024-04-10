from vector import Vector

class Plurality:
    def __init__(self) -> None:
        self.result = Vector([1, 3, 4])
        return
    def ticket_update(self, new_ticket : Vector) -> None:
        self.result += new_ticket
        return

PL = Plurality()

PL.ticket_update(Vector([1, 4]))

PL.ticket_update(Vector([1, 4]))

print(PL.result)
