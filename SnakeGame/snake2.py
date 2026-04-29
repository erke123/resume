import pygame
import random
import time
import psycopg2


conn = psycopg2.connect(
    dbname="snake",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        username VARCHAR(100) PRIMARY KEY,
        score INT
    )
""")
conn.commit()

username = input("Enter your name: ").strip()

cursor.execute("SELECT score FROM players WHERE username = %s", (username,))
result = cursor.fetchone()

if result:
    score = result[0]
    print(f"Welcome back, {username}! Your current score is {score}")
else:
    score = 0
    cursor.execute("INSERT INTO players (username, score) VALUES (%s, %s)", (username, score))
    conn.commit()
    print(f"Welcome, {username}! Let's start playing.")


pygame.init()

w, h = (720, 480)
white = (255, 255, 255)
green = (0, 190, 0)
red = (255, 0, 0)
purple = (128, 0, 128)
orang = (255, 165, 0)

screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

snakepos = [100, 50]
snakebody = [[100, 50], [90, 50], [80, 50], [70, 50]]
apple_pos = [random.randrange(1, (w // 10)) * 10, random.randrange(1, (h // 10)) * 10]
orange = None
app_spawn = True
direction = 'RIGHT'
change_to = direction
count_app = 0
snake_speed = 5

def score_show(color, font, size):
    score_font = pygame.font.Font(font, 30)
    score_surf = score_font.render(f'SCORE:{score}', True, white)
    screen.blit(score_surf, (10, 10))

def game_over():
    
    cursor.execute("UPDATE players SET score = %s WHERE username = %s", (score, username))
    conn.commit()

    my_font = pygame.font.Font(None, 50)
    over = my_font.render(f'YOUR SCORE IS:{score}', True, red)
    screen.blit(over, (w / 4, h / 4))
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    cursor.close()
    conn.close()
    exit()

apple_spawn_time = pygame.time.get_ticks()
orange_spawn_time = pygame.time.get_ticks()
orange_timeout_time = None
orange_timeout_duration = 10000
orange_spawn_duration = 30000
current_time = pygame.time.get_ticks()

while True:
    current_time = pygame.time.get_ticks()
    
    if orange is not None and current_time >= orange_timeout_time:
        orange = None
        orange_spawn_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    if direction == 'UP':
        snakepos[1] -= 10
    if direction == 'DOWN':
        snakepos[1] += 10
    if direction == 'LEFT':
        snakepos[0] -= 10
    if direction == 'RIGHT':
        snakepos[0] += 10

    snakebody.insert(0, list(snakepos))

    if snakepos == apple_pos:
        score += 10
        count_app += 1
        app_spawn = False
    elif snakepos == orange:
        score += 20
        orange = None
        orange_spawn_time = current_time
    else:
        snakebody.pop()

    if not app_spawn:
        apple_pos = [random.randrange(1, (w // 10)) * 10, random.randrange(1, (h // 10)) * 10]
    app_spawn = True

    if orange is None and current_time - orange_spawn_time >= orange_spawn_duration:
        orange = [random.randrange(1, (w // 10)) * 10, random.randrange(1, (h // 10)) * 10]
        orange_timeout_time = current_time + orange_timeout_duration

    screen.fill(green)

    for pos in snakebody:
        pygame.draw.rect(screen, purple, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))

    if orange is not None:
        pygame.draw.rect(screen, orang, pygame.Rect(orange[0], orange[1], 14, 14))

    if snakepos[0] < 0 or snakepos[0] > w - 10 or snakepos[1] < 0 or snakepos[1] > h - 10:
        game_over()

    if snakepos in snakebody[1:]:
        game_over()

    if count_app == 4:
        snake_speed += 4
        count_app = 0

    score_show(red, None, 30)
    pygame.display.update()
    clock.tick(snake_speed)
