import sys
import random
import time
import json
import pygame
import pygame_gui

with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)

WIDTH = settings["screen"]["width"]
HEIGHT = settings["screen"]["height"]

LILYPAD_COUNT = settings["lilypad"]["count"]
LILYPAD_RADIUS = settings["lilypad"]["radius"]
WEIGHT_RATIO = tuple(settings["lilypad"]["weight_ratio"])

FROG_JUMP_DISTANCE = settings["frog"]["jump_distance"]
FROG_WEIGHT = WEIGHT_RATIO[1] - (WEIGHT_RATIO[1] - WEIGHT_RATIO[0]) * settings["frog"]["fall_prob"]

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Second Lab")

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

slider_config = {
    "width": 300,
    "height": 30,
    "spacing": 80
}

speed_label = pygame_gui.elements.ui_label.UILabel(
    relative_rect=pygame.Rect((10, 10), (slider_config["width"], slider_config["height"])),
    text="River Speed:",
    manager=manager
)
speed_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10 + slider_config["height"] + 5),
                              (slider_config["width"], slider_config["height"])),
    start_value=settings["move_speed"],
    value_range=(0.1, 10.0),
    manager=manager
)

frequency_label = pygame_gui.elements.ui_label.UILabel(
    relative_rect=pygame.Rect((10, 10 + slider_config["spacing"]), (slider_config["width"], slider_config["height"])),
    text="Lilypad Frequency:",
    manager=manager
)
frequency_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10 + slider_config["spacing"] + slider_config["height"] + 5),
                              (slider_config["width"], slider_config["height"])),
    start_value=settings["lilypad"]["count"],
    value_range=(5, 20),
    manager=manager
)

frog_weight_label = pygame_gui.elements.ui_label.UILabel(
    relative_rect=pygame.Rect((10, 10 + 2 * slider_config["spacing"]),
                              (slider_config["width"], slider_config["height"])),
    text="Frog Weight:",
    manager=manager
)
frog_weight_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10 + 2 * slider_config["spacing"] + slider_config["height"] + 5),
                              (slider_config["width"], slider_config["height"])),
    start_value=FROG_WEIGHT,
    value_range=WEIGHT_RATIO,
    manager=manager
)

frog_jump_label = pygame_gui.elements.ui_label.UILabel(
    relative_rect=pygame.Rect((10, 10 + 3 * slider_config["spacing"]),
                              (slider_config["width"], slider_config["height"])),
    text="Frog Jump Distance:",
    manager=manager
)
frog_jump_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((10, 10 + 3 * slider_config["spacing"] + slider_config["height"] + 5),
                              (slider_config["width"], slider_config["height"])),
    start_value=FROG_JUMP_DISTANCE,
    value_range=(50, 200),
    manager=manager
)

pause_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 120, 10), (100, 40)),
    text="Pause",
    manager=manager
)

stats_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH - 120, 60), (100, 40)),
    text="Stats",
    manager=manager
)

stats_window = None

is_paused = False

COLORS = {key: tuple(settings["colors"][key]) for key in settings["colors"]}
FPS = settings["fps"]
MOVE_SPEED = settings["move_speed"]

clock = pygame.time.Clock()

frog_stats = []


class Frog:
    def __init__(self, x, y, weight, jump_distance):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.weight = weight
        self.jump_distance = jump_distance
        self.jump_line = None
        self.total_distance = 0
        self.lilypad_sunk = 0
        self.crossings = 0

    def jump(self, x, y):
        self.jump_line = [(self.rect.centerx, self.rect.centery), (x + 10, y + 10)]
        jump_dist = ((self.rect.centerx - x) ** 2 + (self.rect.centery - y) ** 2) ** 0.5
        self.total_distance += jump_dist
        self.rect.topleft = (x, y)

        if self.rect.centerx <= 0 or self.rect.centerx >= WIDTH:
            self.crossings += 1

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS["frog_color"], self.rect)
        if self.jump_line:
            pygame.draw.line(screen, COLORS["line_color"], self.jump_line[0], self.jump_line[1], 1)


class LilyPad:
    def __init__(self, x, y, strength):
        self.x = x
        self.y = y
        self.radius = LILYPAD_RADIUS
        self.strength = strength
        self.show_circle_until = None

    def canSupport(self, weight):
        return self.strength >= weight

    def move_down(self, speed):
        self.y += speed

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS["lily_color"], (self.x, self.y), self.radius)
        if self.show_circle_until and time.time() < self.show_circle_until:
            pygame.draw.circle(screen, COLORS["hit_color"], (self.x, self.y), self.radius / 1.2)

    def show_temp_circle(self):
        self.show_circle_until = time.time() + 0.1


def createLilypads():
    return [LilyPad(
        random.randint(100 + LILYPAD_RADIUS, WIDTH - 100 - LILYPAD_RADIUS),
        random.randint(-HEIGHT, 0),
        random.randint(*WEIGHT_RATIO)
    ) for _ in range(LILYPAD_COUNT)]


def moveFrog(frog, lilypads):
    nxt = random.choice(lilypads + [[0, frog.rect.y], [WIDTH, frog.rect.y]])
    if isinstance(nxt, list):
        frog.jump(nxt[0], nxt[1])
    else:
        frog.jump(nxt.x - frog.rect.width // 2, nxt.y - frog.rect.height // 2)
        if not nxt.canSupport(frog.weight):
            lilypads.remove(nxt)
            frog.lilypad_sunk += 1
        nxt.show_temp_circle()


def create_stats_table(frogs):
    global stats_window
    if stats_window is not None:
        stats_window.kill()

    stats_window = pygame_gui.elements.ui_window.UIWindow(
        rect=pygame.Rect((WIDTH // 4, HEIGHT // 4), (WIDTH // 2, HEIGHT // 2)),
        manager=manager,
        window_display_title="Frog Statistics",
        object_id="#stats_window"
    )

    headers = ["FROG_ID", "Distance", "Lilypads Sunk", "Crossings", "Avg Jump"]

    cell_width = (WIDTH // 2 - 40) // len(headers)
    cell_height = 30
    y_offset = 10

    for col, header in enumerate(headers):
        pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((10 + col * cell_width, y_offset), (cell_width, cell_height)),
            text=header,
            manager=manager,
            container=stats_window,
            object_id="#table_header"
        )
    y_offset += cell_height + 5

    for i, frog in enumerate(frogs):
        avg_jump = frog.total_distance / max(1, frog.crossings)
        row_data = [
            str(i + 1),
            f"{frog.total_distance:.2f}",
            str(frog.lilypad_sunk),
            str(frog.crossings),
            f"{avg_jump:.2f}"
        ]
        for col, data in enumerate(row_data):
            pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((10 + col * cell_width, y_offset), (cell_width, cell_height)),
                text=data,
                manager=manager,
                container=stats_window,
                object_id="#table_cell"
            )
        y_offset += cell_height + 5


def main():
    frogs = [Frog(50, HEIGHT // 2, weight=FROG_WEIGHT, jump_distance=FROG_JUMP_DISTANCE)]
    lilypads = createLilypads()
    global MOVE_SPEED, LILYPAD_COUNT, is_paused

    while True:
        time_delta = clock.tick(FPS) / 1000.0
        screen.fill(COLORS["water_color"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if not (
                        stats_window and stats_window.get_container().relative_rect.collidepoint(
                    x - stats_window.rect.x, y - stats_window.rect.y)
                        or speed_slider.get_relative_rect().collidepoint(x, y)
                        or frequency_slider.get_relative_rect().collidepoint(x, y)
                        or frog_weight_slider.get_relative_rect().collidepoint(x, y)
                        or frog_jump_slider.get_relative_rect().collidepoint(x, y)
                        or pause_button.get_relative_rect().collidepoint(x, y)
                        or stats_button.get_relative_rect().collidepoint(x, y)
                ):
                    if event.button == 1:
                        weight = frog_weight_slider.get_current_value()
                        jump_distance = frog_jump_slider.get_current_value()
                        frogs.append(Frog(x, y, weight, jump_distance))
                    elif event.button == 3 and len(frogs) > 0:
                        frogs.pop()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == pause_button:
                    is_paused = not is_paused
                    pause_button.set_text("Continue" if is_paused else "Pause")
                elif event.ui_element == stats_button:
                    create_stats_table(frogs)

            manager.process_events(event)

        if stats_window is not None and stats_window.is_blocking:
            manager.update(time_delta)

        if not is_paused:
            MOVE_SPEED = speed_slider.get_current_value()
            LILYPAD_COUNT = int(frequency_slider.get_current_value())

            for lilypad in lilypads:
                lilypad.move_down(MOVE_SPEED)

            lilypads = [lilypad for lilypad in lilypads if lilypad.y < HEIGHT]

            while len(lilypads) < LILYPAD_COUNT:
                x = random.randint(100 + LILYPAD_RADIUS, WIDTH - 100 - LILYPAD_RADIUS)
                y = random.randint(-LILYPAD_RADIUS, 0)
                strength = random.randint(*WEIGHT_RATIO)
                lilypads.append(LilyPad(x, y, strength))

            for frog in frogs:
                if pygame.time.get_ticks() % 100 < 30:
                    moveFrog(frog, lilypads)

        for lilypad in lilypads:
            lilypad.draw(screen)

        for frog in frogs:
            frog.draw(screen)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
