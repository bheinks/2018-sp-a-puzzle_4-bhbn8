class Node:
    """A container object for our state, action, parent and path cost. This
    represents an individual node of our tree."""

    def __init__(self, state, action=None, parent=None, cost=0):
        """Initializes a node instance.

        Args:
            state: A puzzle instance representing the current state.
            action: The coordinates of the devices to be swapped.
            parent: The parent node.
            cost: The path cost (number of swaps) thus far.

        Returns:
            A fully initialized node object.
        """

        # perform an deep copy of the puzzle instance
        self.state = state.copy()
        self.action = action
        self.parent = parent
        self.cost = cost

    def perform_action(self):
        """Perform a swap based on the value of self.action. Also append to
        list of swaps and add to path cost."""

        self.state.swap(self.action[0], self.action[1])
        self.state.swaps.append((self.action[0], self.action[1]))
        self.cost += 1

    def __eq__(self, other):
        return self.state == other.state
