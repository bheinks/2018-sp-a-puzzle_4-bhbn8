from collections import deque
from pprint import pprint

# local imports
from node import Node
from priorityqueue import PriorityQueue


class Tree:
    """Represents a tree instance. This is where the magic happens."""

    def __init__(self, top):
        """Initializes a tree instance.

        Args:
            top: A puzzle instance that represents the root of our tree

        Returns:
            A fully initialized tree object.
        """

        # our root node is also initially considered the node with max score
        self.root = self.max_node = Node(top)

        # immediately remove any matches that our board may have started with
        self.root.state.remove_matches(self.root.state.get_all_matches())

    # breadth-first tree search algorithm for traversing tree
    def bfts(self):
        """Generate, traverse and evaluate tree nodes based on a breadth-first
        approach.

        Returns:
            The swaps performed by our goal node as displayed by show_swaps().
            If no solution found, return swaps performed by node with highest
            score.
        """

        # initialize our frontier as a FIFO queue with the root node on top
        frontier = deque([self.root])

        # while we still have nodes to evaluate
        while len(frontier) > 0:
            node = frontier.pop()

            # keep track of node with highest score
            if node.state.score > self.max_node.state.score:
                self.max_node = node

            # if we reach max swaps, pursue branch no further
            if node.cost >= node.state.max_swaps:
                continue

            # if we reach our score quota, game over
            if node.state.score >= node.state.quota:
                break
            
            # for every valid swap
            for dev1, dev2 in node.state.get_valid_moves():
                # create a new node as a copy of the current
                new_node = Node(node.state, (dev1, dev2), node, node.cost)

                # swap dev1 and dev2
                new_node.perform_action()

                # remove any matches
                new_node.state.remove_matches(new_node.state.get_matches(dev1, dev2))

                # append new node to the end of our queue

                frontier.appendleft(new_node)
        # if this happens, we ran out of nodes without reaching our score quota
        else:
            # return node with highest score instead
            node = self.max_node

        return self.show_swaps(node)

    def show_swaps(self, node):
        """Display swaps performed by node in an output-friendly format.

        Args:
            node: The node to display.

        Returns:
            A multi-line string representing swaps made by the node.
        """

        return '\n'.join(["{},{}".format(dev1, dev2) for dev1, dev2 in node.state.swaps])

    def id_dfts(self):
        """Generate, traverse and evaluate tree nodes based on an iterative-
        deepening depth-first approach.

        Returns:
            The swaps performed by our goal node as displayed by show_swaps().
            If no solution found, return swaps performed by node with highest
            score.
        """

        # for depth from 0 to the maximum branch depth (inclusive)
        for depth in range(self.root.state.max_swaps+1):
            node = self._dls(self.root, depth)
            
            # if node isn't None, it's a goal node
            if node:
                return self.show_swaps(node)

        # if no solution found, return node with highest score
        return self.show_swaps(self.max_node)

    def _dls(self, node, depth):
        """Traverse child nodes using a depth-limited depth first search (DLS).

        Args:
            node: The base node to traverse.
            depth: The depth at which to traverse nodes. If 0, we've reached
                our depth limit.

        Returns:
            If depth is 0 and quota is reached (base case), return the goal node.
            If depth is > 0, recursively call this function on child nodes.
            Otherwise, return None.
        """

        # if depth is 0 and quota reached (aka goal found), return goal node
        if depth == 0 and node.state.score >= node.state.quota:
            return node

        if depth > 0:
            # keep track of node with highest score
            if node.state.score >= self.max_node.state.score:
                self.max_node = node

            # for every valid swap
            for dev1, dev2 in node.state.get_valid_moves():
                # create a new node as a copy of the current
                new_node = Node(node.state, (dev1, dev2), node, node.cost)
                
                # swap dev1 and dev2
                new_node.perform_action()

                # remove any matches
                new_node.state.remove_matches(new_node.state.get_matches(dev1, dev2))

                # recurse on new node
                found = self._dls(new_node, depth-1)

                # if goal node found, return it
                if found:
                    return found

        # no goal found
        return None

    def grbefgs(self):
        """Generate, traverse and evaluate tree nodes based on a greedy best-
        first approach using a custom heuristic.

        Returns:
            The swaps performed by our goal node as displayed by show_swaps().
            If no solution found, return swaps performed by node with highest
            score.
        """

        # create a priority queue for our heuristic, which is quota - score
        frontier = PriorityQueue(lambda node: node.state.quota-node.state.score, [self.root])

        # graph search, so explored set
        explored = []

        # while we still have nodes to evaluate
        while len(frontier) > 0:
            node = frontier.dequeue()

            # if we've seen the node before, skip it
            if new_node in explored:
                continue
            else:
                explored.append(new_node)

            # keep track of node with highest score
            if node.state.score > self.max_node.state.score:
                self.max_node = node

            # if we reach max swaps, pursue branch no further
            if node.cost >= node.state.max_swaps:
                continue

            # if we reach our score quota, game over
            if node.state.score >= node.state.quota:
                break
            
            # for every valid swap
            for dev1, dev2 in node.state.get_valid_moves():
                # create a new node as a copy of the current
                new_node = Node(node.state, (dev1, dev2), node, node.cost)

                # swap dev1 and dev2
                new_node.perform_action()

                # remove any matches
                new_node.state.remove_matches(new_node.state.get_matches(dev1, dev2))

                # append new node to our queue
                frontier.enqueue(new_node)
        # if this happens, we ran out of nodes without reaching our score quota
        else:
            # return node with highest score instead
            node = self.max_node

        return self.show_swaps(node)

    def astargs(self):
        """Generate, traverse and evaluate tree nodes based on an A* approach
        using a custom heuristic.

        Returns:
            The swaps performed by our goal node as displayed by show_swaps().
            If no solution found, return swaps performed by node with highest
            score.
        """

        # create a priority queue for our heuristic, which is abs(quota - score) * cost
        frontier = PriorityQueue(lambda node: abs(node.state.quota-node.state.score)*node.cost, [self.root])

        # graph search, so explored set
        explored = []

        # while we still have nodes to evaluate
        while len(frontier) > 0:
            node = frontier.dequeue()

            # if we've seen the node before, skip it
            if node in explored:
                continue
            else:
                explored.append(node)

            # keep track of node with highest score
            if node.state.score > self.max_node.state.score:
                self.max_node = node

            # if we reach our score quota, game over
            if node.state.score >= node.state.quota:
                break

            # if we reach max swaps, pursue branch no further
            if node.cost >= node.state.max_swaps:
                continue
            
            # for every valid swap
            for dev1, dev2 in node.state.get_valid_moves():
                # create a new node as a copy of the current
                new_node = Node(node.state, (dev1, dev2), node, node.cost)

                # swap dev1 and dev2
                new_node.perform_action()

                # remove any matches
                new_node.state.remove_matches(new_node.state.get_matches(dev1, dev2))

                # append new node to our queue
                frontier.enqueue(new_node)

        # if this happens, we ran out of nodes without reaching our score quota
        else:
            # return node with highest score instead
            node = self.max_node

        return self.show_swaps(node)
