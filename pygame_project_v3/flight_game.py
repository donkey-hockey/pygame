import pygame
import os
import random
#############################################################################################


pygame.init()


# 화면 크기 설정
screen_width = 480
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Shooting Game")

# fps
clock = pygame.time.Clock()
#############################################################################################


# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

# image path
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# info
info = pygame.image.load(os.path.join(image_path, "info.png"))
info_size = info.get_rect().size
info_width = info_size[0]
info_height = info_size[1]

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height

character_speed = 20
character_to_x = 0
character_to_y = 0


# weapon
weapon = pygame.image.load(os.path.join(image_path, "bullet.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapon_speed = 15

weapons = []

weapon_num = 30

# enemy
enemy_images = [
    pygame.image.load(os.path.join(image_path, "enemy_1.png")),
    pygame.image.load(os.path.join(image_path, "enemy_2.png")),
    pygame.image.load(os.path.join(image_path, "enemy_3.png"))
]

enemy_speed = [-18, -15, -12]

enemys = []

# first enemy
enemys.append({
    "pos_x": 70,
    "pos_y": 80,
    "img_idx": 0,
    "to_x": -4,
    "to_y": 8,
    "init_spd_y": enemy_speed[0]
})
enemys.append({
    "pos_x": 300,
    "pos_y": 80,
    "img_idx": 0,
    "to_x": 3,
    "to_y": -5,
    "init_spd_y": enemy_speed[0]
})

# enemy_weapon
enemy_weapon = pygame.image.load(os.path.join(image_path, "enemy_bullet.png"))
enemy_weapon_size = enemy_weapon.get_rect().size
enemy_weapon_width = enemy_weapon_size[0]
enemy_weapon_height = enemy_weapon_size[1]

enemy_weapon_speed = 30

enemy_weapons = []

# game font
game_font = pygame.font.Font(None, 40)
game_result = "Mission Failed"
no_bullet = "No Bullet"

# time
total_time = 100
start_ticks = pygame.time.get_ticks()
time_num = 0

# collision
weapon_to_remove = -1
enemy_to_remove = -1

character_life = 3

# item
item = pygame.image.load(os.path.join(image_path, "item.png"))
item_size = item.get_rect().size
item_width = item_size[0]
item_height = item_size[1]

item_speed = 5

items = []


# 이벤트 루프
running = True
while running:
    dt = clock.tick(30)
    time_num += 1

    # print("fps : " + str(clock.get_fps())) # 프레임 확인

    # 2. 이벤트 처리 ( 키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_UP:
                character_to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                character_to_y += character_speed
            elif event.key == pygame.K_SPACE:
                if weapon_num > 0:
                    weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos, weapon_y_pos])
                    weapon_num -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                character_to_y = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    character_y_pos += character_to_y

    # in box
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if character_y_pos < info_height:
        character_y_pos = info_height
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height

    # weapon up
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # auto del
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # enemy bullet
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(
        int(total_time - elapsed_time)), True, (0, 0, 255))

    # enemy position
    for enemy_index, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_size = enemy_images[enemy_img_idx].get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]

        if enemy_pos_x < 0 or enemy_pos_x > screen_width - enemy_width:
            enemy_val["to_x"] = enemy_val["to_x"] * -1

        if enemy_pos_y < info_height or enemy_pos_y > screen_height - info_height*6:
            enemy_val["to_y"] = enemy_val["to_y"] * -1

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]

        if time_num % 30 == 0:

            enemy_weapon_x_pos = enemy_pos_x + enemy_width/2 - enemy_weapon_width/2
            enemy_weapon_y_pos = enemy_pos_y + enemy_height + enemy_weapon_height
            enemy_weapons.append([enemy_weapon_x_pos, enemy_weapon_y_pos])

    # enemy weapon down
    enemy_weapons = [[w[0], w[1] + enemy_weapon_speed] for w in enemy_weapons]

    # auto del
    enemy_weapons = [[w[0], w[1]]
                     for w in enemy_weapons if w[1] < screen_height]

    # 4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for enemy_index, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_rect = enemy_images[enemy_img_idx].get_rect()
        enemy_rect.left = enemy_pos_x
        enemy_rect.top = enemy_pos_y

        if character_rect.colliderect(enemy_rect):
            running = False
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(enemy_rect):
                weapon_to_remove = weapon_idx
                enemy_to_remove = enemy_index

                if random.randrange(1, 3) % 2 == 1:
                    item_x_pos = enemy_pos_x + enemy_width/2 - item_width/2
                    item_y_pos = enemy_pos_y + enemy_height
                    items.append([item_x_pos, item_y_pos])

                if enemy_img_idx < 2:
                    enemy_width = enemy_rect.size[0]
                    enemy_height = enemy_rect.size[1]

                    small_enemy_rect = enemy_images[enemy_img_idx + 1].get_rect()
                    small_enemy_width = small_enemy_rect.size[0]
                    small_enemy_height = small_enemy_rect.size[1]

                    enemys.append({
                        "pos_x": enemy_pos_x + enemy_width/2 - small_enemy_width/2,
                        "pos_y": enemy_pos_y + enemy_height/2 - small_enemy_height/2,
                        "img_idx": enemy_img_idx + 1,
                        "to_x": -4,
                        "to_y": 7,
                        "init_spd_y": enemy_speed[enemy_img_idx + 1]
                    })
                    enemys.append({
                        "pos_x": enemy_pos_x + enemy_width/2 - small_enemy_width/2,
                        "pos_y": enemy_pos_y + enemy_height/2 - small_enemy_height/2,
                        "img_idx": enemy_img_idx + 1,
                        "to_x": +4,
                        "to_y": -6,
                        "init_spd_y": enemy_speed[enemy_img_idx + 1]
                    })

                break

        else:
            continue
        break

    for enemy_weapon_idx, enemy_weapon_val in enumerate(enemy_weapons):
        enemy_weapon_pos_x = enemy_weapon_val[0]
        enemy_weapon_pos_y = enemy_weapon_val[1]

        enemy_weapon_rect = enemy_weapon.get_rect()
        enemy_weapon_rect.left = enemy_weapon_pos_x
        enemy_weapon_rect.top = enemy_weapon_pos_y

        if enemy_weapon_rect.colliderect(character_rect):
            del enemy_weapons[enemy_weapon_idx]
            character_life -= 1
            if character_life == 0:
                running = False

    for item_idx, item_val in enumerate(items):
        item_pos_x = item_val[0]
        item_pos_y = item_val[1]

        item_rect = item.get_rect()
        item_rect.left = item_pos_x
        item_rect.top = item_pos_y

        if item_rect.colliderect(character_rect):
            del items[item_idx]
            character_life += 1
            weapon_num += 10

    if enemy_to_remove > -1:
        del enemys[enemy_to_remove]
        enemy_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    items = [[i[0], i[1]+item_speed] for i in items]

    items = [[i[0], i[1]] for i in items if i[1] < screen_height]

    if len(enemys) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(enemys):
        enemy_pos_x = val["pos_x"]
        enemy_pos_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx], (enemy_pos_x, enemy_pos_y))

    for enemy_weapon_x_pos, enemy_weapon_y_pos in enemy_weapons:
        screen.blit(enemy_weapon, (enemy_weapon_x_pos, enemy_weapon_y_pos))

    for item_x_pos, item_y_pos in items:
        screen.blit(item, (item_x_pos, item_y_pos))

    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False

    if weapon_num == 0:
        bullet_msg = game_font.render(no_bullet, True, (255, 255, 0))
        bullet_msg_rect = bullet_msg.get_rect(
            center=(int(screen_width/2), int(screen_height/2)))
        screen.blit(bullet_msg, bullet_msg_rect)

    screen.blit(info, (0, 0))

    screen.blit(character, (character_x_pos, character_y_pos))

    weapon_number = game_font.render(
        "Bullet:{}".format(weapon_num), True, (0, 0, 255))
    screen.blit(weapon_number, (350, 10))
    life_times = game_font.render("Life : {}".format(
        character_life), True, (0, 0, 255))
    screen.blit(life_times, (200, 10))
    screen.blit(timer, (10, 10))

    pygame.display.update()  # 화면을 한 프레임마다 다시 그린다.


msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
