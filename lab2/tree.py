class ExprNode:
    def __init__(self, value, left_node=None, right_node=None):
        self.value = value
        self.left_node = left_node
        self.right_node = right_node

    def preorder_traversal(self):
        """ Предварительный обход дерева """
        nodes = [self]
        while nodes:
            node = nodes.pop()
            yield node
            if node.right_node:
                nodes.append(node.right_node)
            if node.left_node:
                nodes.append(node.left_node)

    def inorder_traversal(self):
        """ Последовательный обход дерева """
        node = self
        stack = []
        while stack or node:
            while node:
                stack.append(node)
                node = node.left_node
            node = stack.pop()
            yield node
            node = node.right_node

    def __str__(self):
        """ Печать дерева для отладки """
        def recurse(node, level):
            output = ""
            if node:
                output += recurse(node.right_node, level + 1)
                output += "|   " * level
                output += str(node.value) + "\n"
                output += recurse(node.left_node, level + 1)
            return output
        return recurse(self, 0)

def construct_expression_tree(token_list):
    node_stack = []
    for token in token_list:
        if token[1] == "TERM" or token[1] == "START-LINE" or token[1] == "END-LINE":
            node_stack.append(ExprNode(token))
        else:
            right_node = node_stack.pop() if node_stack else None
            left_node = node_stack.pop() if node_stack else None
            node_stack.append(ExprNode(token, left_node, right_node))
    return node_stack.pop() if node_stack else None
