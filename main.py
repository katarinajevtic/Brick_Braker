import pygame
import sys


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 20
PADDLE_SPEED = 12
BALL_SPEED_X, BALL_SPEED_Y = 8, 8

# Colors
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Background
background_image = pygame.image.load('assets/background.jpg')
background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# Bricks
bricks = []
for row in range(5):
    for col in range(WIDTH // BRICK_WIDTH):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
playing = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if playing:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Ball movement
        ball.move_ip(ball_speed[0], ball_speed[1])

        # Ball collisions
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # Paddle collision
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Brick collisions
        for brick in bricks:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed[1] = -ball_speed[1]
                score += 5

        # Checking if all bricks are destroyed
        if not bricks:
            playing = False

        # Draw everything
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, PURPLE, paddle)
        pygame.draw.circle(screen, ORANGE, ball.center, BALL_RADIUS)

        for brick in bricks:
            brick_image = pygame.image.load('assets/brick.png')
            brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))
            screen.blit(brick_image, brick)

        # Display score
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Checking if ball is below the screen
        if ball.y >= HEIGHT - 10:
            playing = False

    else:
        # Game over message
        game_over_text = font.render("Game Over! Press SPACE to play again.", True, ORANGE)
        screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

        # Reset variables on space press
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            playing = True
            ball.x = WIDTH // 2 - BALL_RADIUS
            ball.y = HEIGHT // 2 - BALL_RADIUS
            score = 0
            bricks = []
            for row in range(5):
                for col in range(WIDTH // BRICK_WIDTH):
                    brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
                    bricks.append(brick)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
