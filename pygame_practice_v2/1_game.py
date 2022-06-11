
import pygame
import os
#############################################################################################
# 기본 초기화(반드시 해야하는 것들)


pygame.init()


# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Balloon Game")

# fps
clock = pygame.time.Clock()
#############################################################################################


# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
# path
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_width = stage_size[0]
stage_height = stage_size[1]

# character
character_front = pygame.image.load(
    os.path.join(image_path, "character_front.png"))
character_size = character_front.get_size()
character_width = character_size[0]
character_height = character_size[1]

character_left = pygame.image.load(
    os.path.join(image_path, "character_left.png"))
character_right = pygame.image.load(
    os.path.join(image_path, "character_right.png"))
character = character_front

character_x_pos = screen_width / 2 - character_width/2
character_y_pos = screen_height - stage_height - character_height

# character move direction
character_to_x = 0
# character move speed
character_speed = 10

# weapon system
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 20

# ball system
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon_1.png")),
    pygame.image.load(os.path.join(image_path, "balloon_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon_3.png")),
    pygame.image.load(os.path.join(image_path, "balloon_4.png"))
]

ball_speed_y = [-18, -15, -12, -9]

balls = []
balls.append(
    {
        "pos_x": 50,
        "pos_y": 50,
        "img_idx": 0,
        "to_x": 3,
        "to_y": -6,
        "init_spd_y": ball_speed_y[0]
    }
)

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

game_font = pygame.font.Font(None, 40)

game_result = "Game Over"

total_time = 100
start_ticks = pygame.time.get_ticks()


# 이벤트 루프
running = True
while running:
    dt = clock.tick(30)
    # print("fps : " + str(clock.get_fps())) # 프레임 확인

    # 2. 이벤트 처리 ( 키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character = character_left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character = character_right
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
                character = character_front

    character_x_pos += character_to_x

    # border line
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapon position control
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # ball position
    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_index, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_index

                if ball_img_idx < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect[1]

                    balls.append(
                        {
                            "pos_x": ball_pos_x + ball_width/2 - small_ball_width/2,
                            "pos_y": ball_pos_y + ball_height/2 - small_ball_height/2,
                            "img_idx": ball_img_idx + 1,
                            "to_x": -3,
                            "to_y": -6,
                            "init_spd_y": ball_speed_y[ball_img_idx + 1]
                        }
                    )
                    balls.append({
                        "pos_x": ball_pos_x + ball_width/2 - small_ball_width/2,  # 공의 x좌표
                        "pos_y": ball_pos_y + ball_height/2 - small_ball_height/2,  # 공의 y좌표
                        "img_idx": ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x": 3,  # 공의 x축 이동 방향 -3이면 왼쪽, 3이면 오른쪽
                        "to_y": -6,  # 공의 y축 이동 방향
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]  # y 최초 속도
                    })

                break
        else:
            continue
        break

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(
        int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()  # 화면을 한 프레임마다 다시 그린다.

msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
