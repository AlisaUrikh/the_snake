from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (132, 195, 190)

# Цвет по умолчанию
DEFAULT_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_quit(event):
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                     and event.key == pygame.K_ESCAPE):
        pygame.quit()
        raise SystemExit


def handle_keys(game_object):
    for event in pygame.event.get():
        handle_quit(event)
        # if event.type == pygame.QUIT:
        #     pygame.quit()
        #     raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position=(0, 0), body_color=DEFAULT_COLOR):
        self.position = position
        self.body_color = body_color

    # Абстрактный переопределяемый класс
    """Нарисовать объект ЦЕЛИКОМ"""
    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        return (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
            )

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        current_head = self.get_head_position()
        new_head = ((current_head[0] + self.direction[0] * GRID_SIZE)
                    % SCREEN_WIDTH, (current_head[1] + self.direction[1]
                    * GRID_SIZE) % SCREEN_HEIGHT)
        if new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = list(self.positions)
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.next_direction = None

    def draw(self):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
