# -*- encoding:utf-8 -*-
from leeco._representations import TreeNodeParser


def drawtree(root):
    def height(_node):
        return 1 + max(height(_node.left), height(_node.right)) if _node else -1

    def jumpto(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()

    def _draw_lines(parent_pos, lc_pos, rc_pos):
        if rc_pos:
            jumpto(*parent_pos)
            t.goto(rc_pos[0], rc_pos[1] + 20)
        if lc_pos:
            jumpto(*parent_pos)
            t.goto(lc_pos[0], lc_pos[1] + 20)

    def draw_l2r(node, start_x: int, y: int) -> (int, (int, int)):
        if node is None:
            return start_x, None
        x = start_x
        # draw left subtree
        x, lc_pos = draw_l2r(node.left, x, y - 60)
        x += 20
        # draw self
        self_node_pos = (x, y - 20)
        jumpto(*self_node_pos)
        t.write(node.val, align='center', font=('Arial', 12, 'normal'))
        # draw right subtree
        x += 20
        x, rc_pos = draw_l2r(node.right, x, y - 60)
        # draw lines
        _draw_lines(self_node_pos, lc_pos, rc_pos)
        return x, self_node_pos

    def draw_r2l(node, start_x: int, y: int) -> (int, (int, int)):
        if node is None:
            return start_x, None
        x = start_x
        # draw right subtree
        x, rc_pos = draw_r2l(node.right, x, y - 60)
        x -= 20
        # draw self
        self_node_pos = (x, y - 20)
        jumpto(*self_node_pos)
        t.write(node.val, align='center', font=('Arial', 12, 'normal'))
        # draw left subtree
        x -= 20
        x, lc_pos = draw_r2l(node.left, x, y - 60)
        # draw lines
        _draw_lines(self_node_pos, lc_pos, rc_pos)
        return x, self_node_pos

    def draw_root(root, x, y):
        if root:
            root_pos = (x, y - 20)
            jumpto(*root_pos)
            t.write(root.val, align='center', font=('Arial', 12, 'normal'))
            _, lc_pos = draw_r2l(root.left, x - 20, y - 60)
            jumpto(x, y - 20)
            _, rc_pos = draw_l2r(root.right, x + 20, y - 60)
            _draw_lines(root_pos, lc_pos, rc_pos)

    import turtle
    t = turtle.Turtle()
    t.speed(0)
    turtle.delay(0)
    h = height(root)
    jumpto(0, 30 * h)
    draw_root(root, 0, 30 * h)
    t.hideturtle()
    turtle.title('LeetCode TreeNode Visualizer')
    turtle.mainloop()


def visualize_tree(tree_repr: str):
    drawtree(TreeNodeParser.parse(tree_repr))


if __name__ == '__main__':
    visualize_tree('[1,2,3,4,null,null,7,8,9,null,14]')
    # t = '[1,2,10,12,13,4,6]'
    # drawtree(TreeNodeParser.parse(t))
