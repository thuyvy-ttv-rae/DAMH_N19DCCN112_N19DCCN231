import pygame
import random

def new():
    background_x, background_y = 0, 0
    dinosaur_x, dinosaur_y = 100, 360
    obj_x, obj_y = 1000, 320
    x_velocity, y_velocity = 6, 6
    score = 0
    pausing = False
    bool_s2 = True
    return bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y, x_velocity, y_velocity, score, pausing

def write(x, y, text, font):
    a = font.render(text, True, RED)
    screen.blit(a,(x,y))

def velocity_background(background_x):
    screen.blit(background,(background_x,background_y))
    screen.blit(background, (background_x+1000, background_y))
    background_x -= x_velocity
    if background_x + 1000 <= 0:
        background_x = 0
    return background_x

def velocity_obj(obj_x, i):
    # obj = [pygame.image.load('tree1.png'), pygame.image.load('tree2.png'), pygame.image.load('tree3.png'),
    #        pygame.image.load('cloud1.png'), pygame.image.load('cloud2.png'), pygame.image.load('cloud3.png')]
    # nó tương tự velocity_tree lúc trước nhưng giờ ghi object để dùng chung cho đám mây
    ojb_rect = screen.blit(obj[i], (obj_x, obj_y))
    obj_x -= x_velocity
    if obj_x <= -100: # -100 là tọa độ biến mất của object, nếu để nó lớn hơn nhiều quá thì nó sẽ giống như biến mất chứ
                    # không phải chạy qua
        ojb_x = 1100 # 1000 là tọa độ xuất hiện của object, nếu để nó nhỏ hơn nhiều quá thì nó sẽ giống như bổng nhiên
                    # xuất hiện không phải chạy ra (xuất hiện bên phải ngoài màn hình background)
        return ojb_rect, ojb_x, True # true/ false là để cho step
    return ojb_rect, obj_x, False

def velocity_dinosaur(dinosaur_y, jump, up):
    up += 1
    if up <= 10 or jump: # nếu vòng while đã chạy 11 lần hoặc con khủng long đang nhảy thì tọa độ xuất hiện của con khủng long sẽ bình thường
        dinosaur_rect = screen.blit(dinosaur, (dinosaur_x, dinosaur_y))
    else: # nếu nó không nhảy mà chạy thì cứ 10 lượt vòng while nó sẽ nhảy lên trên 20 cm
        dinosaur_rect = screen.blit(dinosaur, (dinosaur_x, dinosaur_y-20))
        if up == 20: # sau 10 lượt vòng while nữa nó sẽ trở lại mặt đất up sẽ reset về 0
            up = 0
    if 360 >= dinosaur_y >= 100 and jump: # nhảy lên
        dinosaur_y -= y_velocity
    else:
        jump = False
    if dinosaur_y < 360 and jump == False: # nhảy xuống
        dinosaur_y += y_velocity
        up = 0 # vì lúc này còn nhảy nhưng jump đã về false nên phải set up về 0 để nó k bị nhảy tưng tưng trên không
    return dinosaur_rect, dinosaur_y, jump, up

def gameOver(pausing, x_velocity, y_velocity):
    if dinosaur_rect.colliderect(obj_rect):
        pausing = True
        write(360, 200, "GAME OVER", font1)
        x_velocity = 0
        y_velocity = 0
    return pausing, x_velocity, y_velocity

def random_obj(x_velocity, score):
    rand_obj = random.randint(0, 5) # random object
    score += 1
    write(5, 5, "Score: " + str(score), font)
    if score % 3 == 0 and score < 30:
        x_velocity += 1
    # Mỗi lần obj đạt mốc x*3 thì tốc độ tăng 1 nhưng tới 100đ tốc độ không tăng nữa
    # Vì tới 100đ là tốc độ tăng gấp 10 lần rồi rất nhanh rồi
    return rand_obj, x_velocity, score
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 500)) #Độ dài, rộng của màn hình
    pygame.display.set_caption('DAMH_N19DCCN112_N19DCCN231') #Tên của cửa sổ
    bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y, x_velocity, y_velocity, score, pausing = new()
    # bool_s2: s2 là sound2_ âm kết thúc, = true là chưa kêu lần nào. kêu 1 lần nó sẽ về false

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    step, rand_obj, rand2 = 0, 1, 1
    # step là bước chuyển của object hiện tại đang là 1200 (là một bước) = 1000 chiều ngang của backround (X)
    # + 200 (là rìa xuất hiện và biến mất đã nói ở hàm velocity_obj

    font = pygame.font.SysFont('Times New Roman', 20)
    font1 = pygame.font.SysFont('Times New Roman', 40)

    background = pygame.image.load('asset/images/background.png')
    write(100,100,str(background),font)
    dinosaur = pygame.image.load('asset/images/dinosaur.png')
    obj = [pygame.image.load('asset/images/tree1.png'), pygame.image.load('asset/images/tree2.png'), pygame.image.load(
        'asset/images/tree3.png'),
           pygame.image.load('asset/images/Cloud1.png'), pygame.image.load('asset/images/Cloud2.png'), pygame.image.load(
            'asset/images/cloud3.png')]
    sound1 = pygame.mixer.Sound('asset/audio/tick.mp3')
    sound2 = pygame.mixer.Sound('asset/audio/te.mp3')
    clock = pygame.time.Clock()

    jump = False # Nhảy cao
    running = True
    up = 0 # Nhảy tưng tưng (chạy)
    # k để kiểu bool vì 1 vòng while đã nhảy thì rất nhanh rối mất, nên cho nó đếm mỗi vòng while
    # Nếu nó đặt mốc 10 sẽ nhảy lên 1 lần.

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        background_x = velocity_background(background_x)
        write(5, 5, "Score: " + str(score), font)
        # if x_velocity > 0:
        #     write(5, 25, "Speed: " + str(x_velocity-5), font)

        if step:
            rand_obj, x_velocity, score = random_obj(x_velocity, score)
            # random hình xuất hiện. nếu k có if step nó sẽ xuất hiện lung tung
            # xóa if để xem thử sẽ biết
        if rand_obj < 3:
            obj_y = 320
            # Nhỏ hơn 3 là cây tung độ xuất hiện của nó sẽ là 320
        else:
            if 1100 >= obj_x >= 1000:
                obj_y = random.randint(150, 320)
            # từ 3-5 sẽ là mây mây sẽ được random tọa độ
            # if 1000 tới 1100 vì ở đây object sẽ chưa xuất hiện có random cũng không làm hình xuất hiện lung tung
            # khoảng này có thể nhỏ hơn 1050-1100 hay 1000- 1050 nói chung trong khoảng object chưa xuất hiên
        obj_rect, obj_x, step = velocity_obj(obj_x, rand_obj)

        dinosaur_rect, dinosaur_y, jump, up = velocity_dinosaur(dinosaur_y, jump, up)
        pausing, x_velocity, y_velocity = gameOver(pausing, x_velocity, y_velocity)
        # write(100, 100, str(dinosaur_rect), font)

        if pausing and bool_s2:
            pygame.mixer.Sound.play(sound2)
            bool_s2 = False
            # Khúc này để âm thanh chỉ xuất hiện 1 lần

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dinosaur_y == 360:
                        pygame.mixer.Sound.play(sound1)
                        jump = True
                    if pausing:
                        bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y , x_velocity, y_velocity, score, pausing = new()
        pygame.display.flip()
    pygame.quit()