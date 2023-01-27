import traceback
import os
import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window size and caption
width = 500
height = 500
pygame.display.set_caption("My Snake Game")

# Create the window
screen = pygame.display.set_mode((width, height))


class Snake:
    def __init__(self):
        self.x = 250
        self.y = 250
        self.size = 10
        self.body = [(self.x, self.y, self.size)]
        self.direction = "mid"

    def move_up(self):
        self.y -= 10
        self.body.insert(0, (self.x, self.y, self.size))
        self.body.pop()

    def move_down(self):
        self.y += 10
        self.body.insert(0, (self.x, self.y, self.size))
        self.body.pop()

    def move_left(self):
        self.x -= 10
        self.body.insert(0, (self.x, self.y, self.size))
        self.body.pop()

    def move_right(self):
        self.x += 10
        self.body.insert(0, (self.x, self.y, self.size))
        self.body.pop()

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0),
                             (segment[0], segment[1], segment[2], segment[2]))


class Food:
    def __init__(self):
        self.size = 10
        self.x = random.randint(0, width - self.size)
        self.y = random.randint(0, height - self.size)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x, self.y, self.size, self.size))


def save_high_score(high_score):
    try:
        if not os.path.exists("high_score.txt"):
            open("high_score.txt", "w").close()
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))
    except Exception as e:
        print(f"An error occurred: {e}")


def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            file_contents = f.read()
            if file_contents:
                return int(file_contents)
            else:
                return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0


# Loop until the user clicks the close button.
running = True

# Creating snake
snake = Snake()

# Creating food
food = Food()

# Create a clock object
clock = pygame.time.Clock()

# Initialize the font
font = pygame.font.Font(None, 20)

# Initialize the high score and current score
high_score = load_high_score()
current_score = 0

# Define the reserved area coordinates
# reserved_area = [(x1, y1), (x2, y2), (x3, y3), ...]


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_a and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_s and snake.direction != "up":
                snake.direction = "down"
            elif event.key == pygame.K_d and snake.direction != "left":
                snake.direction = "right"

    # Clear the screen
    screen.fill((0, 0, 0))

    # Move the snake
    if snake.direction == "up":
        snake.move_up()
    elif snake.direction == "left":
        snake.move_left()
    elif snake.direction == "down":
        snake.move_down()
    elif snake.direction == "right":
        snake.move_right()

    # Draw the snake on the screen
    snake.draw()

    # Draw the food on the screen
    food.draw()

    # Check for collision with the food
    if snake.x <= food.x + food.size and snake.x + snake.size >= food.x and snake.y <= food.y + food.size and snake.y + snake.size >= food.y:
        food.x = random.randint(0, width - food.size)
        food.y = random.randint(0, height - food.size)
        current_score += 1
        snake.body.append((snake.x, snake.y, snake.size))
        if current_score > high_score:
            high_score = current_score
            save_high_score(high_score)
    else:
        # check for collision with own body
        head_x, head_y = snake.body[0][:2]
        for segment in snake.body[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                print("Game Over! Collided with own body")
                running = False

    # Check for collision with the edges
    if snake.x < 0 or snake.x > width - snake.size or snake.y < 0 or snake.y > height - snake.size:
        print("Game Over!")
        running = False
        current_score = 0

    # Set the frame rate
    clock.tick(10)

    # Render the high score, current score and snake length on the screen
    high_score_text = font.render(
        "High Score: " + str(high_score), True, (255, 255, 255))
    current_score_text = font.render(
        "Current Score: " + str(current_score), True, (255, 255, 255))
    snake_length_text = font.render(
        "Snake Length: " + str(len(snake.body)), True, (255, 255, 255))
    screen.blit(high_score_text, (width - 150, 0))
    screen.blit(current_score_text, (width - 150, 20))
    screen.blit(snake_length_text, (width - 150, 40))

    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()
