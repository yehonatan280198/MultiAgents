from functools import total_ordering

@total_ordering
class State:
    def __init__(self, CurPosition, g=0, parent=None):
        # The current location (position and direction) of the agent
        self.CurPosition = CurPosition
        # Cost to reach this state from the initial state
        self.g = g
        # Parent state for path reconstruction
        self.parent = parent

    # Define equality based on current location and cost
    def __eq__(self, other):
        return isinstance(other, State) and self.CurPosition == other.CurPosition and self.g == other.g

    # Define a hash function based on current location and cost
    def __hash__(self):
        return hash((self.CurPosition, self.g))

    # Define less-than for ordering, based on cost g
    def __lt__(self, other):
        return self.g < other.g