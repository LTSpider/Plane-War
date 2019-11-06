import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名
from pygame.locals import *
import time
import random
import sys

# 定义常量(定义后,不再改值)
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512

enemy_list = []
score = 0


class HeroBullet:
    """英雄子弹类"""
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.window = window

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        """向上飞"""
        self.y -= 10

    def is_hit_enemy(self, enemy):
        if pygame.Rect.colliderect(
            pygame.Rect(self.x, self.y, 20, 31),
            pygame.Rect(enemy.x, enemy.y, 100, 68)
        ):  # 判断是否交叉
            return True
        else:
            return False


class EnemyPlane:
    """敌人飞机类"""
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)  # 图片对象
        self.x = x  # 飞机坐标
        self.y = y
        self.window = window  # 飞机所在的窗口
        self.is_hited = False

    def move(self):
        self.y += 10
        # 到达窗口下边界,回到顶部
        if self.y >= WINDOW_HEIGHT:
            self.x = random.randint(0, random.randint(0, WINDOW_WIDTH - 100))
            self.y = 0

    def display(self):
        """贴图"""
        if self.is_hited:
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.y = 0
            self.is_hited = False

        self.window.blit(self.img, (self.x, self.y))


class HeroPlane:
    def __init__(self, img_path, x, y, window):
        self.img = pygame.image.load(img_path)  # 图片对象
        self.x = x  # 飞机坐标
        self.y = y
        self.window = window  # 飞机所在的窗口
        self.bullets = []  # 记录该飞机发出的所有子弹

    def display(self):
        """贴图"""
        self.window.blit(self.img, (self.x, self.y))

    def display_bullets(self):
        # 贴子弹图
        deleted_bullets = []

        for bullet in self.bullets:
            # 判断 子弹是否超出 上边界
            if bullet.y >= -31:  # 没有出边界
                bullet.display()
                bullet.move()
            else:  # 飞出边界
                deleted_bullets.append(bullet)

            for enemy in enemy_list:
                if bullet.is_hit_enemy(enemy):  # 判断是否击中敌机
                    enemy.is_hited = True
                    deleted_bullets.append(bullet)
                    global score
                    score += 10
                    break

        for out_window_bullet in deleted_bullets:
            self.bullets.remove(out_window_bullet)

    def move_left(self):
        """往左飞"""
        self.x -= 5

    def move_right(self):
        """往右飞"""
        self.x += 5

    def fire(self):
        """发射子弹"""
        # 创建子弹对象  子弹x = 飞机x + 飞机宽度的一半 - 子弹宽度的一半
        bullet = HeroBullet("res/bullet_9.png", self.x + 60 - 10, self.y - 31, self.window)
        # 显示子弹(贴子弹图)
        bullet.display()
        self.bullets.append(bullet)  # 为了避免子弹对象被释放(只有局部变量引用对象,方法一执行完就会释放)


def main():
    """主函数  一般将程序的入口"""
    pygame.init()
    # 创建窗口  set_mode((窗口尺寸))
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # 将图片加载到内存中  load(图片资源路径)
    bg_img = pygame.image.load("res/img_bg_level_1.jpg")
    # 创建对象
    hero_plane = HeroPlane("res/hero2.png", 240, 500, window)
    enemy_plane1 = EnemyPlane("res/img-plane_5.png", random.randint(0, WINDOW_WIDTH - 100), 0, window)
    enemy_plane2 = EnemyPlane("res/img-plane_5.png", random.randint(0, WINDOW_WIDTH - 100), random.randint(-150, -68), window)
    enemy_plane3 = EnemyPlane("res/img-plane_5.png", random.randint(0, WINDOW_WIDTH - 100), random.randint(-300, -140), window)
    enemy_list.append(enemy_plane1)
    enemy_list.append(enemy_plane2)
    enemy_list.append(enemy_plane3)
    # 创建文字对象
    score_font = pygame.font.Font("res/SIMHEI.TTF", 40)

    while True:
        # 贴图 把图片贴到窗口中  blit(图片对象, 相对原点的坐标)
        window.blit(bg_img, (0, 0))
        # 贴飞机图
        hero_plane.display()
        hero_plane.display_bullets()
        # 贴敌机图
        for enemy in enemy_list:
            enemy.display()
            # 让敌机移动
            enemy.move()
        # 贴得分文字
        score_text = score_font.render("得分:%d" % score, 1, (255, 255, 255))
        window.blit(score_text, (10, 10))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()
        # 获取事件，比如按键等  先显示界面,再根据获取的事件,修改界面效果
        for event in pygame.event.get():
            # 判断是否是点击了退出按钮
            if event.type == QUIT:
                sys.exit()  # 让程序终止
                pygame.quit()
            # 判断是否是按下了键
            elif event.type == KEYDOWN:
                # 检测按键是否是空格键
                if event.key == K_SPACE:
                    hero_plane.fire()
        # 获取连续按下的情况
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            hero_plane.move_left()

        if pressed_keys[pygame.K_RIGHT]:
            hero_plane.move_right()
        # 每次循环,让程序休眠一会儿
        time.sleep(0.01)

if __name__ == '__main__':  # 判断是否主动执行该文件
    main()