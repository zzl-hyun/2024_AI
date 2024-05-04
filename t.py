import pygame
import pygame_gui

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Radio Buttons")

# Pygame_gui 관리자 설정
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# 색깔
WHITE = (255, 255, 255)

# 라디오 버튼 생성
radio_button_1 = pygame_gui.elements.UIRadioButton(relative_rect=pygame.Rect((100, 100), (200, 50)),
                                                    text='Option 1',
                                                    manager=manager)
radio_button_2 = pygame_gui.elements.UIRadioButton(relative_rect=pygame.Rect((100, 150), (200, 50)),
                                                    text='Option 2',
                                                    manager=manager)
radio_button_3 = pygame_gui.elements.UIRadioButton(relative_rect=pygame.Rect((100, 200), (200, 50)),
                                                    text='Option 3',
                                                    manager=manager)

# 메인 루프
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

    manager.update(time_delta)

    WIN.fill(WHITE)
    manager.draw_ui(WIN)

    pygame.display.flip()

pygame.quit()
