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

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод отрисовки объекта. Определяется объектом самостоятельно."""
        pass


# Класс Яблока (от родительского класса GameObject).
class Apple(GameObject):
    """Класс яблока - объекта поедания."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()
        self.direction = None
        self.quantity = 0

    # Метод draw класса Apple
    def draw(self):
        """Метод отрисовки объекта яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Метод случайного положения яблока
    def randomize_position(self):
        """Метод случайного расположения яблока на игровом поле."""
        position = (
            (randrange(0, SCREEN_WIDTH, GRID_SIZE)),
            (randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        )
        while position in Snake().positions:
            position = (
                (randrange(0, SCREEN_WIDTH, GRID_SIZE)),
                (randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            )
        return position


# Класс Змейки (от родительского класса GameObject).
class Snake(GameObject):
    """Класс змейки - объекта, поедающего яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), ]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод draw класса Snake.
    def draw(self):
        """Метод отрисовки змейки на поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

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
    def update_direction(self):
        """Метод обновления направления."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод обновления позиции змейки, добавления головы
    # и удаления последнего элемента.
    def move(self):
        """Метод движения змейки и результаты пожирания яблока ею."""
        # Обновление координат каждой секции.
        self.x, self.y = self.get_head_position()
        if self.direction == RIGHT:
            self.positions.insert(0, (self.x + GRID_SIZE, self.y))
        elif self.direction == LEFT:
            self.positions.insert(0, (self.x - GRID_SIZE, self.y))
        elif self.direction == UP:
            self.positions.insert(0, (self.x, self.y - GRID_SIZE))
        elif self.direction == DOWN:
            self.positions.insert(0, (self.x, self.y + GRID_SIZE))
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
        self.update_direction()

    def reset(self):
        """Метод окончиния игры и начала следующей."""
        main()


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция обработки нажатия кнопок пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной метод игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        # handle_keys(apple)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.move()

        # Если голова змеи съела яблоко, то змея увеличилась на 1 клетку.
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            snake.length += 1
            # apple.quantity += 1

        pygame.display.update()

        # Тут опишите основную логику игры.
        # Если змея врезается в себя, то конец игры, подсчет очков.
        if snake.positions[0] in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()


if __name__ == '__main__':
    main()
