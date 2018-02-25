class PriorityQueue:
    """Represents a custom priority queue instance. While Python has a
    PriorityQueue library available, this is more efficient because it sorts on
    dequeue, rather than enqueue."""

    def __init__(self, key, items=[]):
        """Initializes a PriorityQueue instance.

        Args:
            key: The function that will act as the sort key of our queue.
            items: Any initial queue items.
        """

        self.key = key
        self.items = items

    def enqueue(self, item):
        """Add an item to the queue.

        Args:
            item: The item that's being added.
        """

        self.items.append(item)

    def dequeue(self):
        """Sort using our key function and pop an item from the queue.

        Returns:
            The item at the top of the queue, post-sorting.
        """

        # reverse the sort as pop takes the last item from the queue
        self.items.sort(key=self.key, reverse=True)
        return self.items.pop()

    def __len__(self):
        """Overload __len__ to return length of queue.

        Returns:
            The number of items in our queue.
        """

        return len(self.items)
