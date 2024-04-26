from random import choice, randrange

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
BORDER_COLOR = (0, 0, 0)

APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (248, 24, 148)

# Цвет по умолчанию
DEFAULT_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Выход из игры
def handle_quit(event):
    """Прекращение игры при закрытии окна или нажатии клавиши 'escape'"""
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                     and event.key == pygame.K_ESCAPE):
        pygame.quit()
        raise SystemExit


def handle_keys(game_object):
    """Обработка действий пользователя"""
    for event in pygame.event.get():
        handle_quit(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс общих атрибутов игровых объектов"""

    def __init__(self, position=(0, 0), body_color=DEFAULT_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный переопределяемый метод: отрисовка объектов целиком"""
        pass


class Apple(GameObject):
    """Унаследованный от GameObject класс: описание яблока и действий с ним"""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Определение рандомных координат для отрисовки яблока"""
        first_stop = (GRID_WIDTH - 1) * GRID_SIZE
        second_stop = (GRID_HEIGHT - 1) * GRID_SIZE
        return (
            randrange(0, first_stop, GRID_SIZE),
            randrange(0, second_stop, GRID_SIZE)
        )

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Унаследованный от GameObject класс: описание змейки и ее поведения"""

    def __init__(self):
        super().__init__(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновления направления змейки после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Позиция головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки после столкновения с собой"""
        self.__init__()  # Решила просто унаследовать атрибуты другого метода
        self.direction = choice([UP, DOWN, RIGHT, LEFT])

    def move(self):
        """Обновление движения змейки"""
        current_head = self.get_head_position()
        new_head = ((current_head[0] + self.direction[0] * GRID_SIZE)
                    % SCREEN_WIDTH, (current_head[1] + self.direction[1]
                    * GRID_SIZE) % SCREEN_HEIGHT)
        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        """Затирание хвоста змейки"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """Основной игровой цикл"""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.move()
        snake.update_direction()

        """Съедание яблока змейкой"""
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
