from collections import deque

class TreeNode:
    @staticmethod
    def from_expression(rpn_expression):
        eval_stack = deque()
        for tok in rpn_expression:
            if type()


class BinaryOperator(TreeNode):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right


def simplify(expression):
