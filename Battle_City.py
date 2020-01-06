import pygame
from pygame.sprite import Sprite
import random


# 信息栏类
class MessageBox:
    def __init__(self):
        # 信息栏背景图片信息
        self.image = pygame.image.load('tank_img/inifbox.png')
        self.rect = self.image.get_rect()
        self.rect.left = 780
        self.rect.top = 0
        # 存放信息栏的敌方坦克数量的列表
        self.enemy_tanks_list = []
        # 用下标控制信息栏敌方坦克的数量
        self.index1 = 12

    # 将信息栏显示到窗口上
    def display_inifbox(self):
        MainGame.window.blit(self.image, self.rect)

    # 信息栏的敌方坦克图片
    def display_enemy_tanks(self):
        image = pygame.image.load('tank_img/display_enemy_tanks.png')
        rect1 = image.get_rect()
        rect1.left = 840
        rect1.top = 50
        self.enemy_tanks_list.append(rect1)
        rect2 = image.get_rect()
        rect2.left = 890
        rect2.top = 50
        self.enemy_tanks_list.append(rect2)
        rect3 = image.get_rect()
        rect3.left = 840
        rect3.top = 90
        self.enemy_tanks_list.append(rect3)
        rect4 = image.get_rect()
        rect4.left = 890
        rect4.top = 90
        self.enemy_tanks_list.append(rect4)
        rect5 = image.get_rect()
        rect5.left = 840
        rect5.top = 130
        self.enemy_tanks_list.append(rect5)
        rect6 = image.get_rect()
        rect6.left = 890
        rect6.top = 130
        self.enemy_tanks_list.append(rect6)
        rect7 = image.get_rect()
        rect7.left = 840
        rect7.top = 170
        self.enemy_tanks_list.append(rect7)
        rect8 = image.get_rect()
        rect8.left = 890
        rect8.top = 170
        self.enemy_tanks_list.append(rect8)
        rect9 = image.get_rect()
        rect9.left = 840
        rect9.top = 210
        self.enemy_tanks_list.append(rect9)
        rect10 = image.get_rect()
        rect10.left = 890
        rect10.top = 210
        self.enemy_tanks_list.append(rect10)
        rect11 = image.get_rect()
        rect11.left = 840
        rect11.top = 250
        self.enemy_tanks_list.append(rect11)
        rect12 = image.get_rect()
        rect12.left = 890
        rect12.top = 250
        self.enemy_tanks_list.append(rect12)
        # 控制信息栏显示敌方坦克数量
        for item in self.enemy_tanks_list[0:self.index1]:
            MainGame.window.blit(image, item)

    # 修改下标控制信息栏显示敌方坦克数量
    def pop_index1(self):
        self.index1 -= 1

    # 玩家命数图片
    def player_lives(self):
        image = pygame.image.load('tank_img/player_lives.png')
        rect = image.get_rect()
        rect.left = 840
        rect.top = 450
        MainGame.window.blit(image, rect)

    # 关卡图片
    def checkpoint(self):
        image = pygame.image.load('tank_img/checkpoint.png')
        rect = image.get_rect()
        rect.left = 850
        rect.top = 600
        MainGame.window.blit(image, rect)

    # 开始图片
    def interface(self):
        image = pygame.image.load('tank_img/interface.png')
        rect = image.get_rect()
        rect.left = 0
        rect.top = 0
        MainGame.window.blit(image, rect)


# 精灵类，继承精灵
class BaseItem(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


# 坦克父类，继承精灵类
class BaseTank(BaseItem):
    # 定义类属性，所有坦克对象高和宽都是一样
    width = 60
    height = 60

    def __init__(self, left, top):
        # 坦克的方向默认向上
        self.direction = 'U'
        # 存放玩家坦克图片的字典
        self.images = {
            'U': pygame.image.load('tank_img/p1tankU.gif'),
            'D': pygame.image.load('tank_img/p1tankD.gif'),
            'L': pygame.image.load('tank_img/p1tankL.gif'),
            'R': pygame.image.load('tank_img/p1tankR.gif')
        }
        # 坦克的图片由方向决定
        self.image = self.images[self.direction]
        # 坦克的速度
        self.speed = 10
        self.rect = self.image.get_rect()
        # 设置放置的位置
        self.rect.left = left
        self.rect.top = top
        # 坦克是否停止
        self.stop = True
        # 决定坦克是否消灭了
        self.live = True
        # 保持原来的位置
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 射击方法
    def shot(self):
        return Bullet(self)

    # 坦克的移动
    def move(self):
        # 保存原位置
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的移动方向
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 780:
                self.rect.top += self.speed
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < 780:
                self.rect.left += self.speed

    # 显示坦克
    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)

    # 撞墙处理
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                # 碰到后保持当前位置不变
                self.stay()

    # 处理位置不变
    def stay(self):
        # 位置等于原位置
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop


# 玩家坦克类
class HeroTank(BaseTank):
    def __init__(self, left, top):
        super().__init__(left, top)

    # 玩家坦克不能与敌方坦克重叠
    def myTank_hit_enemyTank(self):
        for enemyTank in MainGame.EnemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                # 碰到后保持当前位置不变
                self.stay()

    # 玩家不能与老家重合
    def myTank_home(self):
        if pygame.sprite.collide_rect(MainGame.home, self):
            # 碰到后保持当前位置不变
            self.stay()


# 敌方坦克类
class EnemyTank(BaseTank):
    # 初始化坦克生成的坐标（x，y）
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)
        # 存放敌方坦克图片的字典
        self.images = {
            'U': pygame.image.load('tank_img/enemy1U.gif'),
            'D': pygame.image.load('tank_img/enemy1D.gif'),
            'L': pygame.image.load('tank_img/enemy1L.gif'),
            'R': pygame.image.load('tank_img/enemy1R.gif')
        }
        # 坦克的方向等于随机方向
        self.direction = self.RandomDirection()
        # 坦克的图片由方向决定
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        # 固定游戏界面左中右三个点随机一个位置显示坦克
        self.rect.left = left
        self.rect.top = top
        # 坦克速度随机1~4
        self.speed = speed
        # 固定移动60步后更改方向
        self.step = 60

    # 坦克出生随机方向
    def RandomDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        else:
            return 'R'

    # 坦克随机移动
    def randomMove(self):
        # 如果移动60步后，重新随机方向，再给60步
        if self.step < 0:
            self.direction = self.RandomDirection()
            self.step = 60
        # 每次移动步数减1
        else:
            self.move()
            self.step -= 1

    # 坦克射击
    def shot(self):
        # 坦克发射子弹几率30/1
        num = random.randint(1, 30)
        if num == 1:
            return Bullet(self)

    # 敌方坦克碰撞玩家坦克
    def enemyTank_hit_MyTank(self):
        for enemy in MainGame.EnemyTankList:
            if MainGame.my_tank and MainGame.my_tank.live:
                if pygame.sprite.collide_rect(MainGame.my_tank, enemy):
                    # 碰到后保持当前位置不变
                    self.stay()

    # 敌方坦克不能与老家重合
    def enemyTank_home(self):
        if pygame.sprite.collide_rect(MainGame.home, self):
            # 碰到后保持当前位置不变
            self.stay()


# 子弹类
class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('tank_img/tankmissile.gif')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        # 根据坦克方向，生成子弹位置
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.width / 2

        # 子弹的速度
        self.speed = 15

        # 子弹状态
        self.live = True

    # 显示子弹
    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    # 子弹的移动
    def move(self):
        # 如果走到界面边界就消失
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < 780:
                self.rect.left += self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < 780:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False

    # 玩家子弹击中敌方坦克
    def myBullet_hit_enemy(self):
        for enemytank in MainGame.EnemyTankList:
            if pygame.sprite.collide_rect(enemytank, self):
                enemytank.live = False
                self.live = False
                # 坦克爆炸音效
                nusic = Music('tank_img/bomb.wav')
                nusic.play()
                # 创建爆炸对象
                explode = Explode(enemytank)
                # 把被击中的坦克添加到爆炸列表里
                MainGame.explodeList.append(explode)

    # 敌方子弹击中玩家坦克
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 玩家每被击中一次，命就减少一次
                MainGame.myTank_life -= 1
                if MainGame.myTank_life == 0:
                    # 如果玩家坦克死了三次，更改玩家坦克状态
                    MainGame.my_tank.live = False
                    # 打中玩家坦克的子弹为False，不再进行显示
                    self.live = False

                # 坦克爆炸音效
                nusic = Music('tank_img/bomb.wav')
                nusic.play()
                # 创建爆炸对象
                explode = Explode(MainGame.my_tank)
                # 把被击中的坦克添加到爆炸列表里
                MainGame.explodeList.append(explode)
                # 如果玩家坦克命不小于0
                if MainGame.myTank_life > 0:
                    # 创建玩家坦克
                    game.createMyTank()

    # 玩家子弹击中敌方子弹
    def myBullet_hitBullet(self):
        for item in MainGame.EnemyBulletList:
            if pygame.sprite.collide_rect(self, item):
                # 更改玩家坦克子弹状态
                self.live = False
                # 更改敌方坦克状态
                item.live = False

    # 子弹击中老家
    def home_bullrt(self):
        # 如果老家每死亡，才判断子弹击中老家
        if MainGame.home.live:
            if pygame.sprite.collide_rect(MainGame.home, self):
                # 老家爆炸音效
                nusic = Music('tank_img/bomb.wav')
                nusic.play()
                # 创建老家爆炸对象
                explode = Explode(MainGame.home)
                # 先把被击中的老家先添加到爆炸列表里，爆炸位置在老家位置
                MainGame.explodeList.append(explode)
                # 再老家图片移出游戏界面外
                MainGame.home.rect.left = 1500
                MainGame.home.rect.top = 1500

    # 射击墙壁
    def wall_bullet(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(wall, self):
                # 更改子弹的状态
                self.live = False
                # 更改墙的状态
                wall.live = False


# 老家类
class Home:
    def __init__(self):
        self.image = pygame.image.load('tank_img/home.jpg')
        self.rect = self.image.get_rect()
        self.rect.left = 360
        self.rect.top = 720
        self.live = True

    def displayhome(self):
        # 如果老家活着，贴老家图片
        if self.live:
            MainGame.window.blit(self.image, self.rect)
        else:
            # 如果老家被击中，且爆炸图片显示完，更改了老家的状态为False，那么就显示被破坏的老家图片
            self.image = pygame.image.load('tank_img/destory.gif')
            self.rect = self.image.get_rect()
            self.rect.left = 360
            self.rect.top = 730
            MainGame.window.blit(self.image, self.rect)


# 墙壁类
class Wall:
    def __init__(self, left, top):
        self.image = pygame.image.load('tank_img/walls.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True

    # 如果墙壁没被击中，状态为True就显示，
    def display_wall(self):
        if self.live:
            MainGame.window.blit(self.image, self.rect)


# 爆炸类
class Explode:
    def __init__(self, tank):
        # 爆炸的位置由坦克决定，获取坦克的x，y坐标。
        x, y, e, r = tank.rect
        # 矫正爆炸位置
        self.rect = x - 40, y - 20, e, r
        # 爆炸图片
        self.images = [
            pygame.image.load('tank_img/blast0.gif'),
            pygame.image.load('tank_img/blast1.gif'),
            pygame.image.load('tank_img/blast2.gif'),
            pygame.image.load('tank_img/blast3.gif'),
            pygame.image.load('tank_img/blast4.gif'),
            pygame.image.load('tank_img/blast5.gif'),
            pygame.image.load('tank_img/blast6.gif'),
            pygame.image.load('tank_img/blast7.gif')
        ]
        # 图片索引
        self.step = 1
        # 按照图片索引加载图片
        self.image = self.images[self.step]
        # 爆炸状态是否结束
        self.live = True

    # 加载爆炸类
    def displayExplode(self):
        # 如果当前显示的爆炸图片小于爆炸图片列表的长度，就接着显示，
        if self.step < len(self.images):
            self.image = self.images[self.step]
            # 图片索引加1
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            # 如果爆炸图片显示完了，更改爆炸图片状态
            self.live = False


# 音效类 所有音效继承它
class Music:
    # 接收传入的音效地址
    def __init__(self, filename):
        self.filename = filename
        # 初始化音乐
        pygame.mixer.init()
        # 加载音效地址
        pygame.mixer.music.load(filename)

    # 播放音效
    def play(self):
        pygame.mixer.music.play()


# 游戏类
class MainGame:
    # 游戏窗口宽度
    WINDOW_WIDTH = 980
    # 游戏窗口高度
    WINDOW_HEIGHT = 780
    # 游戏背景颜色 黑色
    COLOR_GREEN = pygame.color.Color('#000000')
    # 游戏窗口 创建方法: create_window
    window = None
    # 玩家坦克 创建方法: createMyTank
    my_tank = None
    # 玩家坦克一共三条命
    myTank_life = 3
    # 信息栏对象
    message_box = MessageBox()
    # 每有一個坦克创建就添加到此列表，如果此列表长度等于12后，就不在生成坦克，或者生成空
    EnemyTank_mostList = []
    # 敌方坦克游戏界面初始列表，默认为5辆
    EnemyTankList = []
    # 开局五个敌方坦克
    EnemyTankCount = 5
    # 存储玩家子弹列表
    myBulletList = []
    # 存储敌方子弹的列表
    EnemyBulletList = []
    # 被击中的坦克或老家的对象列表
    explodeList = []
    # 存放墙壁列表
    wallList = []
    # 创建老家类
    home = Home()
    # 当前关数
    checkpoint_num = 1

    # 文字显示类
    def draw_text(self, text, x, y, textHeight=30, fontColor=(255, 255, 255), backgroudColor=None):
        # 通过字体文件获得字体对象  参数1 字体文件 参数2 字体大小
        font_obj = pygame.font.Font('./tank_img/baddf.ttf', textHeight)
        # 1文字  2是否抗锯齿 3文字颜色 4背景颜色
        text_obj = font_obj.render(text, True, fontColor, backgroudColor)
        # 获得要显示的对象的矩形区域
        text_rect = self.message_box.image.get_rect()
        # 设置显示对象的坐标
        text_rect.topleft = x, y
        # 绘制字 到指定区域  参1是文字对象 参2 矩形区域对象
        MainGame.window.blit(text_obj, text_rect)

    # 游戏开始方法
    def start_game(self):
        # 初始化游戏模块
        pygame.init()
        # 初始化展示模块
        pygame.display.init()
        # 调用创建窗口的方法
        self.create_window()
        # 设置游戏窗口标题
        pygame.display.set_caption('坦克大战')
        # 初始化玩家坦克
        self.createMyTank()
        # 初始化敌方坦克
        self.creatEnemyTank()
        # 初始化墙壁
        self.createWall()
        # 创建时钟对象 控制循环次数
        clock = pygame.time.Clock()
        # 初始界面判断
        self.interface_live = True
        # 控制输赢游戏不更新
        self.winning_osing = True
        # 程序持续进行
        while True:
            # 每秒循环速度
            clock.tick(20)
            # 更改背景颜色
            MainGame.window.fill(MainGame.COLOR_GREEN)
            #  开始界面
            if self.interface_live:
                # 贴开始图片
                self.message_box.interface()
                # 获取事件列表
                event_list01 = pygame.event.get()
                # 循环事件
                for event in event_list01:
                    # 如果空格键，就开始游戏
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # 改变开始图片的状态
                            self.interface_live = False
                    # 点击窗口的叉号实现游戏结束
                    if event.type == pygame.QUIT:
                        # pygame退出
                        pygame.quit()
                        # 程序退出
                        exit()
                # 持续更新窗口
                pygame.display.update()

            # 开始游戏
            else:
                # 获取事件
                self.getEvent()
                # 如果玩家坦克创建了且坦克没被打中
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 显示玩家坦克
                    MainGame.my_tank.displayTank()
                    # 如果坦克没有遇到障碍物，说明可以移动，持续更新坦克位置
                    if not MainGame.my_tank.stop:
                        # 调用坦克的移动
                        MainGame.my_tank.move()
                        # 坦克撞墙处理
                        MainGame.my_tank.hitWall()
                        # 玩家坦克与敌方坦碰撞
                        MainGame.my_tank.myTank_hit_enemyTank()
                        # 玩家坦克与老家碰撞
                        MainGame.my_tank.myTank_home()
                else:
                    # 如果坦克被击中了，从游戏类中删除玩家坦克类
                    del MainGame.my_tank
                    # 重置为None
                    MainGame.my_tank = None
                # 加载玩家子弹
                self.biltMyBullet()
                # 显示敌方坦克
                self.biltEnemyTank()
                # 显示敌方子弹
                self.biltEnemyBullet()
                # 显示爆炸效果
                self.blitExplode()
                # 显示墙壁
                self.blitWall()
                # 重复添加坦克判断
                self.put_more_enemytank()
                # 显示信息栏背景图片
                self.message_box.display_inifbox()
                # 显示信息栏敌方坦克图片
                self.message_box.display_enemy_tanks()
                # 显示信息栏玩家命数图片
                self.message_box.player_lives()
                # 显示信息栏当前关数图片
                self.message_box.checkpoint()
                # 显示老家图片
                self.home.displayhome()
                # 显示信息界面文字
                self.draw_text('敌方:%s' % MainGame.message_box.index1, 830, 13)  # 敌方坦克剩余数
                self.draw_text('玩家', 830, 415)  # 显示“玩家”文字
                self.draw_text('%s' % MainGame.myTank_life, 890, 455)  # 显示玩家命数数字
                self.draw_text('关数', 830, 560)  # 显示“关数”文字
                self.draw_text('%s' % MainGame.checkpoint_num, 890, 615)  # 显示关数数字
                # 玩家输了，游戏结束,显示文字，修改输赢状态控制玩家能不能移动
                if MainGame.myTank_life == 0 or not MainGame.home.live:
                    self.draw_text('Game Over', 245, 350, textHeight=60)
                    self.winning_osing = False
                # 玩家赢了，显示文字，修改输赢状态控制玩家能不能移动
                if MainGame.message_box.index1 <= 0:
                    self.draw_text('You Win', 270, 350, textHeight=60)
                    self.winning_osing = False
                # 窗口持续刷新
                pygame.display.update()

    # 重复添加敌方坦克的添加判断
    def put_more_enemytank(self):
        # 如果敌方坦克总数低于12就添加
        if len(MainGame.EnemyTank_mostList) < 12:
            # 如果游戏界面的坦克低于5辆就添加
            while len(MainGame.EnemyTankList) < 5:
                # 调用方法创建后续坦克对象
                self.more()

    # 创建游戏窗口方法：
    def create_window(self):
        # 如果没有游戏窗口就创建
        if not MainGame.window:
            # 创建窗口
            MainGame.window = pygame.display.set_mode((MainGame.WINDOW_WIDTH, MainGame.WINDOW_HEIGHT))
        # 如果窗口存在，就返回已存在的窗口
        return MainGame.window

    # 创建玩家坦克
    def createMyTank(self):
        MainGame.my_tank = HeroTank((780 - HeroTank.width) / 2 - 120, 780 - HeroTank.height)
        # 第一次创建玩家坦克时才放开场音乐
        if MainGame.myTank_life == 3:
            # 加载音乐
            music = Music('tank_img/start.wav')
            # 播放音乐
            music.play()

    # 创建墙壁
    def createWall(self):
        # 所有墙的左上角坐标
        a = [0, 60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660, 720]
        b = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600, 660]
        # 存放随机墙坐标，判断位置重复的列表，
        c1 = []
        i = 0
        # 随机墙数量
        while i < 60:  # 墙出现位置随机不重复，范围0~140,超过游戏运行不了
            x = random.randint(0, len(a) - 1)
            y = random.randint(0, len(b) - 1)
            c = [a[x], b[y]]
            # 老家旁边不能有墙，如果生成再老家旁边就跳过次循环，循环次数不变
            if b[y] == 660 and (a[x] == 300 or a[x] == 360 or a[x] == 420):
                continue
            # 如果新随机墙的位置不在列表里，说明重复，循环次数加1，创建四个小墙模块
            if c not in c1:
                # 每次新随机墙位置添加到列表里
                c1.append(c)
                i += 1
                # 创建四个墙对象
                top = b[y]
                left = a[x]
                wall = Wall(left, top)
                MainGame.wallList.append(wall)
                top = b[y]
                left = a[x] + 30
                wall1 = Wall(left, top)
                MainGame.wallList.append(wall1)
                top = b[y] + 30
                left = a[x]
                wall2 = Wall(left, top)
                MainGame.wallList.append(wall2)
                top = b[y] + 30
                left = a[x] + 30
                wall3 = Wall(left, top)
                MainGame.wallList.append(wall3)
        # 老家周围墙壁
        home_wall1 = Wall(330, 750)
        home_wall2 = Wall(330, 720)
        home_wall3 = Wall(330, 690)
        home_wall4 = Wall(360, 690)
        home_wall5 = Wall(390, 690)
        home_wall6 = Wall(420, 690)
        home_wall7 = Wall(420, 690)
        home_wall8 = Wall(420, 720)
        home_wall9 = Wall(420, 750)
        s = [home_wall1, home_wall2, home_wall3, home_wall4, home_wall5, home_wall6, home_wall7, home_wall8, home_wall9]
        for item in s:
            MainGame.wallList.append(item)

    # 显示墙壁
    def blitWall(self):
        # 遍历所有墙
        for wall in MainGame.wallList:
            # 判断墙的状态是否存在
            if wall.live:
                wall.display_wall()
            else:
                # 如果不存在就从列表里删除
                MainGame.wallList.remove(wall)

    # 加载玩家子弹
    def biltMyBullet(self):
        # 遍历玩家子弹列表
        for bullet in MainGame.myBulletList:
            # 如果子弹存在
            if bullet.live:
                # 显示子弹
                bullet.displayBullet()
                # 子弹移动
                bullet.move()
                # 玩家子弹击中敌方坦克
                bullet.myBullet_hit_enemy()
                # 射击墙壁
                bullet.wall_bullet()
                # 子弹击中老家
                bullet.home_bullrt()
                # 玩家子弹击中敌方子弹
                bullet.myBullet_hitBullet()
            else:
                # 如果子弹碰撞到了，不存在，将子弹从列表里删除
                MainGame.myBulletList.remove(bullet)

    # 创建初始敌方坦克
    def creatEnemyTank(self):
        # 在游戏界面最顶端添加坦克
        top = 0
        # 开局默认添加五辆坦克
        for i in range(MainGame.EnemyTankCount):
            # x坐标左中右随机一个
            left = random.choice([0, 360, 720])
            # 速度随机3~6
            speed = random.randint(3, 6)
            # 创建敌方坦克对象
            enemy = EnemyTank(left, top, speed)
            # 添加到敌方初始的列表里
            MainGame.EnemyTankList.append(enemy)
            # 添加到敌方总坦克列表里
            MainGame.EnemyTank_mostList.append(enemy)

    # 后续坦克的添加
    def more(self):
        # 获取玩家坦克位置，保证新添加的敌方坦克不与玩家坦克重叠
        y, x, q, w = game.my_tank.rect
        top = 0
        # 判断游戏界面坦克是否少于5
        for i in range(5 - len(MainGame.EnemyTankList)):
            # 如果玩家坦克在游戏界面最上一排的左边，那么敌方坦克随机生成的位置为中或者右
            if x <= 70 and y <= 70:
                left = random.choice([360, 720])
                # 速度随机1~4
                speed = random.randint(1, 4)
                # 创建坦克对象
                enemy = EnemyTank(left, top, speed)
                # 添加到敌方初始的列表里
                MainGame.EnemyTankList.append(enemy)
                # 添加到敌方总坦克列表里
                MainGame.EnemyTank_mostList.append(enemy)
            elif x <= 70 and y >= 290 and y <= 430:
                left = random.choice([0, 720])
                speed = random.randint(1, 4)
                enemy = EnemyTank(left, top, speed)
                MainGame.EnemyTankList.append(enemy)
                MainGame.EnemyTank_mostList.append(enemy)
            elif x <= 70 and y >= 650:
                left = random.choice([0, 360])
                speed = random.randint(1, 4)
                enemy = EnemyTank(left, top, speed)
                MainGame.EnemyTankList.append(enemy)
                MainGame.EnemyTank_mostList.append(enemy)
            # 如果玩家坦克不在游戏界面的最上一排，那么敌方坦克左中右随机生成一辆
            else:
                left = random.choice([0, 360, 720])
                speed = random.randint(1, 4)
                enemy = EnemyTank(left, top, speed)
                MainGame.EnemyTankList.append(enemy)
                MainGame.EnemyTank_mostList.append(enemy)

    # 加载敌方坦克
    def biltEnemyTank(self):
        # 遍历敌方坦克列表
        for enemytank in MainGame.EnemyTankList:
            # 如果敌方坦克存在
            if enemytank.live:
                # 显示敌方坦克
                enemytank.displayTank()
                # 敌方子弹调用射击方法
                EnemyBullet = enemytank.shot()
                # 敌方坦克随机移动
                enemytank.randomMove()
                # 敌方坦克碰墙处理
                enemytank.hitWall()
                # 敌方坦克碰撞玩家坦克
                enemytank.enemyTank_hit_MyTank()
                # 敌方不能与老家重合
                enemytank.enemyTank_home()
                # 如果敌方子弹存在
                if EnemyBullet:
                    # 将敌方子弹添加到敌方子弹列表里
                    MainGame.EnemyBulletList.append(EnemyBullet)
            else:
                # 如果坦克不存在，将坦克咧白里的坦克减少一辆
                MainGame.EnemyTankList.remove(enemytank)
                # 初始敌方坦克列表数量少了，说明后续就可以再添加一辆坦克
                MainGame.EnemyTankCount -= 1
                # 调用方法减少一个下标，信息栏的敌方坦克就少显示一辆，
                MainGame.message_box.pop_index1()

    # 加载敌方子弹
    def biltEnemyBullet(self):
        # 遍历敌方坦克列表
        for bullet in MainGame.EnemyBulletList:
            # 如果子弹存在
            if bullet.live:
                # 显示子弹
                bullet.displayBullet()
                # 移动子弹
                bullet.move()
                # 敌方子弹击中玩家坦克
                bullet.enemyBullet_hit_myTank()
                # 击中墙壁
                bullet.wall_bullet()
                # 子弹击中老家
                bullet.home_bullrt()
            else:
                # 如果子弹不存在，就从子弹列表里删除
                MainGame.EnemyBulletList.remove(bullet)

    # 加载爆炸效果
    def blitExplode(self):
        # 遍历要爆炸的对象列表
        for explode in MainGame.explodeList:
            # 获取爆炸位置
            x, y, q, w = explode.rect
            # 如果还没爆炸
            if explode.live:
                # 显示爆炸图片
                explode.displayExplode()
            else:
                # 如果爆炸位置是320*700 说明爆炸的是老家，更改老家的状态
                if x == 320 and y == 700:
                    MainGame.home.live = False
                # 如果爆炸完了，从爆炸对象列表中删除爆炸完了的对象
                MainGame.explodeList.remove(explode)

    # 获取游戏中的所有事件
    def getEvent(self):
        # 获取游戏中的事件列表
        event_list = pygame.event.get()
        for e in event_list:
            # 点击窗口的叉号实现游戏结束
            if e.type == pygame.QUIT:
                # pygame退出
                pygame.quit()
                # 程序退出
                exit()
            # 如果玩家或老家没死，玩家可以移动
            if self.winning_osing:
                # 通过上下左右键控制坦克的移动
                if e.type == pygame.KEYDOWN:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                            MainGame.my_tank.direction = 'D'
                            MainGame.my_tank.stop = False
                            print("按下向下的键，向下移动")
                        elif e.key == pygame.K_UP or e.key == pygame.K_w:
                            MainGame.my_tank.direction = 'U'
                            MainGame.my_tank.stop = False
                            print("按下向上的键，向上移动")
                        elif e.key == pygame.K_LEFT or e.key == pygame.K_a:
                            MainGame.my_tank.direction = 'L'
                            MainGame.my_tank.stop = False
                            print("按下向左的键，向左移动")
                        elif e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                            MainGame.my_tank.direction = 'R'
                            MainGame.my_tank.stop = False
                            print("按下向右的键，向右移动")
                        # 空格发射子弹
                        elif e.key == pygame.K_SPACE:
                            print('发射子弹')
                            # 创建玩家子弹，每次最多发射五颗子弹
                            if len(MainGame.myBulletList) < 5:
                                # 创建子弹对象到玩家坦克
                                mybullet = Bullet(MainGame.my_tank)
                                # 将子弹对象添加玩家子弹列表
                                MainGame.myBulletList.append(mybullet)
                                # 加载射击音效
                                Shot_music = Music('tank_img/fire.wav')
                                # 播放射击音效
                                Shot_music.play()

                elif e.type == pygame.KEYUP:
                    # 键盘按键弹起就停止移动
                    if e.key == pygame.K_UP or e.key == pygame.K_DOWN or e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT \
                            or e.key == pygame.K_w or e.key == pygame.K_s or e.key == pygame.K_a or e.key == pygame.K_d:
                        # 如果游戏类坦克存在，且坦克没被子弹击中
                        if MainGame.my_tank and MainGame.my_tank.live:
                            # 允许玩家坦克移动
                            MainGame.my_tank.stop = True


# 只能在本程序上运行，被作为模块调用
if __name__ == '__main__':
    # 创建游戏类对象
    game = MainGame()
    # 游戏类对象调用游戏开始方法
    game.start_game()
