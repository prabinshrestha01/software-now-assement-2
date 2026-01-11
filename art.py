import turtle
def draw_recursive_edge(t, length, depth):

    
    if depth == 0:
        # Base case: Draw a straight line
        t.forward(length)