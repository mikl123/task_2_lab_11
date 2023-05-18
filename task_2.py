"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log, inf
import random
import sys
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

sys.setrecursionlimit(3000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of source_collection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """
        Inorder traversal
        """
        current = self._root
        stack = []
        lyst = list()
        while True:
            if current is not None:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                lyst.append(current.data)
                current = current.right
            else:
                break
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        counter = 0
        if not self.isEmpty():
            current_pos = self._root
            while True:
                counter += 1
                if current_pos.data == item:
                    return (item, counter)
                if item <= current_pos.data:
                    if current_pos.left is None:
                        break
                    current_pos = current_pos.left
                if item > current_pos.data:
                    if current_pos.right is None:
                        break
                    current_pos = current_pos.right
        return None

    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            current_node = self._root
            while True:
                if item <= current_node.data:
                    if current_node.left is None:
                        current_node.left = BSTNode(item)
                        break
                    else:
                        current_node = current_node.left
                if item > current_node.data:
                    if current_node.right is None:
                        current_node.right = BSTNode(item)
                        break
                    else:
                        current_node = current_node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        if self.isEmpty():
            return None
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right
        if item_removed is None:
            return None
        if not current_node.left is None and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:
            if current_node.left is None:
                new_child = current_node.right
            else:
                new_child = current_node.left
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            height_left = 0
            height_right = 0
            if top.left is not None:
                height_left = 1 + height1(top.left)
            if top.right is not None:
                height_right = 1 + height1(top.right)
            return max(height_left, height_right)

        if self._root is not None:
            return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        if self.height() < 2 * log(len(self) + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        buf = []
        for elem in self.inorder():
            if low <= elem <= high:
                buf.append(elem)
        return buf

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        buffer = sorted(self.inorder())

        def build_sub_tree(list_buf, left=0, right=0):
            if len(list_buf[left:right]) == 0:
                return None
            mid_index = (left + right) // 2
            mid = BSTNode(list_buf[mid_index])
            mid.left = build_sub_tree(list_buf, left, mid_index)
            mid.right = build_sub_tree(list_buf, mid_index + 1, right)
            return mid

        if len(buffer) != 0:
            self._root = build_sub_tree(buffer, 0, len(buffer))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        smallest_bigger = inf
        for i in self.inorder():
            if item < i:
                if i < smallest_bigger:
                    smallest_bigger = i
        if smallest_bigger == inf:
            return None
        return smallest_bigger

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        bigger_smaller = -1
        for i in self.inorder():
            if i < item:
                if i > bigger_smaller:
                    bigger_smaller = i
        if bigger_smaller == -1:
            return None
        return bigger_smaller

    @staticmethod
    def get_random_elements(list_to_get, number):
        """
        Get random value from list
        """
        result = []
        counter = 0
        while counter != number:
            elem = random.choice(list_to_get)
            if elem in result:
                continue
            else:
                result.append(elem)
                counter += 1
        return result

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # Initialize veriables
        results = []
        results_1 = []
        tree_1 = LinkedBST()
        tree_2 = LinkedBST()
        list_buf = []
        # Getting data from file
        with open(path, "r", encoding="utf-8") as file:
            while True:
                word = file.readline().strip()
                if not word:
                    break
                list_buf.append(word)
        # Shuffling data
        list_buf_shaffle = list_buf[:]
        random.shuffle(list_buf_shaffle)
        # Adding data to the trees
        for index, _ in enumerate(list_buf):
            tree_2.add(list_buf_shaffle[index])
            tree_1.add(list_buf[index])
        # Getting random data to find
        find_test_list = LinkedBST.get_random_elements(list_buf_shaffle, 100)
        # Measuring time for tree based on data in alphabetic order
        iterations = 0
        start = time.time()
        for i in find_test_list:
            finded = tree_1.find(i)
            if i == finded[0]:
                iterations += finded[1]
                continue
        end = time.time()
        results_1.append(end - start)
        results.append(iterations)
        # Measuring rime for tree based on data in random order
        iterations = 0
        start = time.time()
        for i in find_test_list:
            finded = tree_2.find(i)
            if i == finded[0]:
                iterations += finded[1]
                continue
        end = time.time()
        results_1.append(end - start)
        results.append(iterations)
        # Balancing the tree
        tree_1.rebalance()
        # Measuring time in balanced tree
        iterations = 0
        start = time.time()
        for i in find_test_list:
            finded = tree_1.find(i)
            if i == finded[0]:
                iterations += finded[1]
                continue
        end = time.time()
        results_1.append(end - start)
        results.append(iterations)
        # Finding elements throught list
        iterations = 0
        start = time.time()
        for elem in find_test_list:
            for i in list_buf:
                iterations += 1
                if i == elem:
                    break
        end = time.time()
        results_1.append(end - start)
        results.append(iterations)
        # Printing results
        print(
            "Повний перебір списку: "
            + str(results[3])
            + " ітерацій, "
            + str(results_1[3])
            + " секунд\n"
            "Бінарне дерево на основі списку в алфавітному порядку: "
            + str(results[0])
            + " ітерацій, "
            + str(results_1[0])
            + " секунд\n"
            + "Бінарне дерево на основі списку в рандомному порядку: "
            + str(results[1])
            + " ітерацій, "
            + str(results_1[1])
            + " секунд\n"
            + "Збалансоване бінарне дерево на основі списку: "
            + str(results[2])
            + " ітерацій, "
            + str(results_1[2])
            + " секунд"
        )

