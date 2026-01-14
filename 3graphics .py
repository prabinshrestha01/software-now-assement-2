import turtle
"""
this function divides a straight line into segments to create 
an indentation that is inward and trangular.

-t(turtle.Turtle) is the object of turtle which is used for drawing
-length(float) is the length of the current segment
-depth(int) is the current level of the recursion, where depth of 0
draws a straight line

"""
def draw_recursive_edge(t, length, depth):

    if depth == 0:
        # Depth 0: It Draws a straight line
        t.forward(length)
    else:
        # 1. It Divides the edge into three equal segments
        segment_length = length / 3
        
        # It Draws the first segment
        draw_recursive_edge(t, segment_length, depth - 1)
        
        # 2. Create the inward indentation (The "V" shape)
        t.right(60)
        draw_recursive_edge(t, segment_length, depth - 1)
        
        t.left(120)
        draw_recursive_edge(t, segment_length, depth - 1)
        
        t.right(60)
        
        # It Draws the final segment
        draw_recursive_edge(t, segment_length, depth - 1)

def main():
    """
    the execution of main program.
    Here the function handles:
    -input from the user for sides length and recursion depth.
    -make sure the values are within the ranges.
    -screen setup and positioning
    -the main drawing
    """
    
    # Asks the input from the users
    try:
        sides = int(input("Enter the number of sides (3-7): "))
        if not (3 <= sides <= 7):
            print("Error: Sides must be between 3 and 7.")
            return

        length = int(input("Enter the side length in px (50-500): "))
        if not (50 <= length <= 500):
            print("Error: Length must be between 50 and 500.")
            return

        depth = int(input("Enter the recursion depth (3-9): "))
        if not (3 <= depth <= 9):
            print("Error: Depth must be between 3 and 9.")
            return
            
    except ValueError:
        print("Error: Please enter valid integers.")
        return

    # Screen Setup
    screen = turtle.Screen()
    screen.title("Recursive Indentation Pattern")
    screen.bgcolor("black")
    
    #creates pen and it tells how to draw instantly and what color.
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    t.color("cyan")
    
    # make the drawing in the centre of the screen
    t.penup()
    t.goto(-length / 2, length / 2)
    t.pendown()
    
    # it Calculates external angle for polygon
    exterior_angle = 360 / sides
    
    # Draws the Polygon
    for _ in range(sides):
        draw_recursive_edge(t, length, depth)
        t.right(exterior_angle)

        #this doesnot allow screen to exit automatically
    print("Pattern complete. Click the window to close.")
    screen.exitonclick()
if __name__ == "__main__":
    main()