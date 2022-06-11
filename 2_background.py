from encodings import utf_8
import pygame

# 뼈대 만글기

pygame.init()
# 초기화. pygame import시 반드시 호출해준다.

# 화면 크기 설정
screen_width = 480  # 가로 크기
screen_height = 640  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 배경화면
background = pygame.image.load(
    "/Users/jeongju/Desktop/coding/python/proj/pygame_basic/background.png")


# 화면 타이틀 설정
pygame.display.set_caption("Nado Game")

# 프로그램 종료되지 않도록 대기
# 이벤트 루프
running = True  # 게임이 진행중인지 확인하는 변수
while running:
    for event in pygame.event.get():  # 어떤 이벤트가 발생 하였는가?
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생 하였는가?
            running = False  # 게임이 진행중이 아니게됨

    # screen.blit(background, (0, 0))  # 사진와 좌표 설정, 배경 그리기
    screen.fill((0, 0, 255))  # 색을 설정
    pygame.display.update()  # 화면을 한 프레임마다 다시 그린다.

# pygame 종료
pygame.quit()
