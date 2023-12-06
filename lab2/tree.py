class TreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def build_tree(lexemes):
    stack = []
    for lexeme in lexemes:
        if lexeme[1] != "TERM":
            node = TreeNode(lexeme)
            if lexeme[1] == "UNARY":
                node.left = stack.pop()
            else:
                node.right = stack.pop()
                node.left = stack.pop()
            stack.append(node)
        else:
            stack.append(TreeNode(lexeme))
    return stack[-1] if stack else None

def analyze_tree(node, context=None):
    if node is None:
        return True

    if context is None:
        context = {'has_iteration': False, 'depth': 0}

    if node.data[1] == "UNARY":
        context['has_iteration'] = True
        return analyze_tree(node.left, context)

    if node.data[1] in ["BINARY", "CONCAT"]:
        left_analysis = analyze_tree(node.left, context)
        right_analysis = analyze_tree(node.right, context)
        return left_analysis and right_analysis

    context['depth'] += 1
    return node.data[1] == "TERM"

def extract_prefix_suffix(node, is_prefix=True):
    if node is None:
        return ""

    if node.data[1] == "TERM":
        return node.data[0] if is_prefix else ""

    if node.data[1] == "UNARY":
        return extract_prefix_suffix(node.left, is_prefix)

    if node.data[1] in ["BINARY", "CONCAT"]:
        left_part = extract_prefix_suffix(node.left, is_prefix)
        right_part = extract_prefix_suffix(node.right, is_prefix)
        return left_part + right_part if is_prefix else right_part

    return ""

def print_tree(node, indent="", position="root"):
    if node is not None:
        print(indent + position + ": " + str(node.data))
        indent += "    "
        print_tree(node.left, indent, "L")
        print_tree(node.right, indent, "R")
