import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = 30
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, int(self.y)), self.size // 2)

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, 400)
        self.passed = False
    
    def move(self):
        self.x -= PIPE_SPEED
    
    def draw(self):
        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, 
                        (self.x, self.height, 50, SCREEN_HEIGHT - self.height))
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, 
                        (self.x, 0, 50, self.height - PIPE_GAP))

def main():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Create new pipes
        if current_time - last_pipe > PIPE_FREQUENCY:
            pipes.append(Pipe())
            last_pipe = current_time

        # Update game state
        bird.move()
        
        # Move and remove pipes
        for pipe in pipes[:]:
            pipe.move()
            if pipe.x < -50:
                pipes.remove(pipe)
            # Score counting
            if not pipe.passed and pipe.x < bird.x:
                score += 1
                pipe.passed = True

        # Collision detection
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        for pipe in pipes:
            # Check collision with bottom pipe
            if (bird.x + bird.size//2 > pipe.x and 
                bird.x - bird.size//2 < pipe.x + 50):
                if (bird.y + bird.size//2 > pipe.height or 
                    bird.y - bird.size//2 < pipe.height - PIPE_GAP):
                    running = False

        # Draw everything
        screen.fill(SKY_BLUE)
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Game Over screen
    screen.fill(SKY_BLUE)
    game_over_text = font.render(f'Game Over! Score: {score}', True, WHITE)
    restart_text = font.render('Press R to restart', True, WHITE)
    screen.blit(game_over_text, 
                (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                 SCREEN_HEIGHT//2 - 50))
    screen.blit(restart_text, 
                (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                 SCREEN_HEIGHT//2 + 50))
    pygame.display.flip()

    # Wait for restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()

if __name__ == "__main__":
    main()