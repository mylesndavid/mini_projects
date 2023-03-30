import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the dimensions of the game window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Initialize the pygame library
pygame.init()

# Set the screen dimensions and create the screen object
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the title of the game window
pygame.display.set_caption("Pong")

# Create the game objects
ball = pygame.Rect(350, 250, 20, 20)
paddle_1 = pygame.Rect(50, 200, 20, 100)
paddle_2 = pygame.Rect(620, 200, 20, 100)

# Define the initial direction of the ball (1 = right, -1 = left)
direction = 1

# Define the game loop
done = False
while not done:
    # Check for user input
    for event in pygame.event.get():
        # If the user closes the game window, end the game loop
        if event.type == pygame.QUIT:
            done = True

    # Move the paddles based on user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle_2.y = paddle_2.y - 5
    if keys[pygame.K_DOWN]:
        paddle_2.x = paddle_2.x +5


    # Move the ball
    ball.x += direction
    ball.y += direction

    # Check if the ball has collided with a wall or a paddle
    if ball.y < 0 or ball.y > SCREEN_HEIGHT - 20:
        direction = -direction
    if ball.colliderect(paddle_1) or ball.colliderect(paddle_2):
        direction = -direction

    # Clear the screen and draw the game objects
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, paddle_1)
    pygame.draw.rect(screen, WHITE, paddle_2)

    # Update the screen
    pygame.display.flip()

# Close the game window
pygame.quit()