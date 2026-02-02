import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Нельзя развернуться на 180 градусов
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + (x * CELL_SIZE)) % WIDTH
        new_y = (head[1] + (y * CELL_SIZE)) % HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
            return False
            
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN if i == 0 else GRAY
            rect = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
    
    def grow(self):
        self.length += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_score(surface, score):
    font = pygame.font.SysFont('Arial', 24)
    text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(text, (5, 5))

def main():
    snake = Snake()
    food = Food()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
        
        # Движение змейки
        if not snake.move():
            # Если змейка умерла, небольшая пауза
            time.sleep(1)
        
        # Проверка поедания еды
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # Проверяем, чтобы еда не появилась на змейке
            while food.position in snake.positions:
                food.randomize_position()
        
        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, snake.score)
        pygame.display.update()
        
        # Скорость игры (чем длиннее змейка, тем быстрее)
        speed = 10 + min(snake.length // 5, 15)
        clock.tick(speed)
    
    pygame.quit()

if __name__ == "__main__":
    main()
