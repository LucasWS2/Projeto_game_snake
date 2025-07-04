import pygame
import sys
import random

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicializa tela e relógio
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Fonte para pontuação
font = pygame.font.SysFont(None, 36)

def draw_text(text, pos):
    img = font.render(text, True, WHITE)
    screen.blit(img, pos)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Começa indo para cima
        self.grow = False

    def turn(self, dir):
        # Evita que a cobra vire 180 graus
        opposite = (-self.direction[0], -self.direction[1])
        if dir != opposite:
            self.direction = dir

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        if new_head in self.positions[1:]:
            return False  # bateu no corpo, fim de jogo

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def eat(self):
        self.grow = True

    def draw(self, surface):
        for pos in self.positions:
            r = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, r)

class Food:
    def __init__(self):
        self.position = (0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def draw(self, surface):
        r = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, r)

def main():
    snake = Snake()
    food = Food()
    score = 0

    while True:
        clock.tick(10)  # FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.turn((1, 0))

        if not snake.move():
            # Game over
            break

        if snake.positions[0] == food.position:
            snake.eat()
            score += 1
            food.randomize()

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_text(f'Score: {score}', (10, 10))
        pygame.display.flip()

    # Tela de game over
    screen.fill(BLACK)
    draw_text('Game Over!', (WIDTH//2 - 80, HEIGHT//2 - 20))
    draw_text(f'Score final: {score}', (WIDTH//2 - 100, HEIGHT//2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == '__main__':
    main()
