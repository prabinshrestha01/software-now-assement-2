import turtle

def draw_recursive_edge(t, length, depth):
    if depth == 0:
        # Depth 0: Draw a straight line
        t.forward(length)
    else:
        # 1. Divide the edge into three equal segments
        segment_length = length / 3
        
        # Draw the first segment
        draw_recursive_edge(t, segment_length, depth - 1)
        
        # 2. Create the inward indentation (The "V" shape)
        t.right(60)
        draw_recursive_edge(t, segment_length, depth - 1)
        
        t.left(120)
        draw_recursive_edge(t, segment_length, depth - 1)
        
        t.right(60)
        
        # Draw the final segment
        draw_recursive_edge(t, segment_length, depth - 1)

def main():
    
    
    # User Input Parameters
    try:
        sides = int(input("Enter the number of sides: "))
        length = int(input("Enter the side length: "))
        depth = int(input("Enter the recursion depth: "))
    except ValueError:
        print("Error: Please enter valid numbers.")
        return

    # Screen Setup
    screen = turtle.Screen()
    screen.title("Question 3: Recursive Indentation Pattern")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.pensize(2)
    
    # Center the drawing
    t.penup()
    t.goto(-length / 2, length / 2)
    t.pendown()
    
    # Calculate external angle for polygon
    exterior_angle = 360 / sides
    
    # Draw the Polygon
    for _ in range(sides):
        draw_recursive_edge(t, length, depth)
        t.right(exterior_angle)

if __name__ == "__main__":
    main()