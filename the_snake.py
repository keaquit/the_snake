from random import randrange
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Цвет фона - черный.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)
# Цвет яблока.
APPLE_COLOR = (255, 0, 0)
# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки.
SPEED = 20
# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
# Родительский класс.
class GameObject:
    """Родительский класс для создания объектов."""

    def __init__(
            self,
            position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
            color=None):
        self.position = position
        self.body_color = color

    def draw(self):
        """Метод отрисовки объекта. Определяется объектом самостоятельно."""
        raise NotImplementedError(
            f'Определите метод draw в классе {self.__class__.__name__}.'
        )

    def rect(self):
        """Метод Rect"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Класс Яблока (от родительского класса GameObject).
class Apple(GameObject):
    """Класс яблока - объекта поедания."""

    def __init__(
            self,
            position=None,
            stop_position=tuple(),
            apple_color=APPLE_COLOR):
        self.body_color = apple_color
        self.position = position
        self.stop_position = stop_position
        position = self.randomize_position(stop_position)

    # Метод draw класса Apple
    def draw(self):
        """Метод отрисовки объекта яблоко."""
        super().rect()

    # Метод случайного положения яблока
    def randomize_position(self, stop_position=tuple()):
        """Метод случайного расположения яблока на игровом поле."""
        self.position = (
            (randrange(0, SCREEN_WIDTH, GRID_SIZE)),
            (randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        )
        while self.position in stop_position:
            self.position = (
                (randrange(0, SCREEN_WIDTH, GRID_SIZE)),
                (randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            )


# Класс Змейки (от родительского класса GameObject).
class Snake(GameObject):
    """Класс змейки - объекта, поедающего яблоко."""

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), ]
        self.length = 1
        self.direction = RIGHT
        self.last = None
        self.position = None

    # Метод draw класса Snake.
    def draw(self):
        """Метод отрисовки змейки на поле."""
        for self.position in self.positions[:-1]:
            super().rect()

    # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Метод возвращения позиции головы змейки (первого элемента).
    def get_head_position(self):
        """Метод получения координат головы змейки."""
        self.head_position = self.positions[0]
        return self.head_position

    # Метод обновления направления после нажатия на кнопку.
    def update_direction(self, position):
        """Метод обновления направления."""
        self.direction = position
        position = None

    # Метод обновления позиции змейки, добавления головы
    # и удаления последнего элемента.
    def move(self):
        """Метод движения змейки и резульаты пожирания яблока ею."""
        # Обновление координат каждой секции.
        self.x, self.y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (self.x + (GRID_SIZE * direction_x)) % SCREEN_WIDTH
        new_y = (self.y + (GRID_SIZE * direction_y)) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        # Продолжение движения змейки при выходе с игрового поля.
        if self.x == SCREEN_WIDTH - GRID_SIZE and self.direction == RIGHT:
            self.positions[0] = 0, self.y
        elif self.x == 0 and self.direction == LEFT:
            self.positions[0] = SCREEN_WIDTH - GRID_SIZE, self.y
        elif self.y == SCREEN_HEIGHT - GRID_SIZE and self.direction == DOWN:
            self.positions[0] = self.x, 0
        elif self.y == 0 and self.direction == UP:
            self.positions[0] = self.x, SCREEN_HEIGHT - GRID_SIZE
        # Утверждение последнего элемента для затирания в методе Draw.
        self.last = self.positions[len(self.positions) - 1]
        # Удаление последнего элемента в змейке.
        if len(self.positions) > self.length:
            self.positions.pop()
        # self.update_direction(position=self.positions[0])

    def reset(self):
        """Метод окончиния игры и начала следующей."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), ]
        self.direction = (randrange(0, 2), randrange(0, 2))


# Функция обработки действий пользователя
def handle_keys(snake):
    """Функция обработки нажатия кнопок пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.update_direction(RIGHT)


def main():
    """Основной метод игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    stop_position = snake.positions
    apple = Apple(stop_position)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        snake.move()

        # Если голова змеи съела яблоко, то змея увеличилась на 1 клетку.
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1

        pygame.display.update()

        # Тут опишите основную логику игры.
        # Если змея врезается в себя, то конец игры, подсчет очков.
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()


if __name__ == '__main__':
    main()
