try:
    import sys
    import pygame
    from tilemap import *
    # from sprites import *
    from sprites_BP import *
    from settings import *
    from os import path
    from pygame.locals import *
    from socket import *
    import random
except ImportError as err:
    print("couldn't load module. {}".format(err))
    sys.exit(2)

# https://m.blog.naver.com/moya021/221294544608 유튜브 음원 추출 사이트


class Game:
    def __init__(self):
        # sprites setting
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.challengers = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.challenger_bullets = pygame.sprite.Group()
        self.player_explosions = pg.sprite.Group()
        self.challenger_explosions = pg.sprite.Group()
        self.ex_lasting_t = 0.04

        # Game init setting
        self.dt = 0
        self.status = 'play'
        self.GamePlay = True
        self.delay_time = 1000
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)

        # init player
        self.player = None
        self.challenger = None

        # init View
        self.camera1 = None
        self.camera2 = None

        # About map
        self.num = 0
        self.p1_hit = 0
        self.p2_hit = 0
        self.p1_kill_ct = 0      # player1 킬수
        self.p2_kill_ct = 0      # player2 킬수

        self.p1_killed = False
        self.p1_suicide = False
        self.p2_killed = False
        self.p2_suicide = False
        self.player1_win = False
        self.player2_win = False
        self.map = None
        self.name = None
        self.name_2 = None
        self.bullet1 = None
        self.filename = None
        self.p_last_ex = 0
        self.c_last_ex = 0
        self.pKillText = None
        self.cKillText = None
        pygame.font.init()

        # map random select
        self.num = random.randrange(1, 4)
        if self.num == 1:
            self.filename = self.map_name[0]
        elif self.num == 2:
            self.filename = self.map_name[1]
        elif self.num == 3:
            self.filename = self.map_name[2]
        self.load_data()

    def data_init(self):
        # sprites setting
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.grounds = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.challengers = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.challenger_bullets = pygame.sprite.Group()
        self.player_explosions = pygame.sprite.Group()
        self.challenger_explosions = pygame.sprite.Group()
        self.ex_lasting_t = 0.04

        # init player
        self.player = None
        self.challenger = None

        # init View
        self.camera1 = None
        self.camera2 = None

        # About map
        self.num = 0
        self.p1_hit = 0
        self.p2_hit = 0
        self.p1_kill_ct = 0      # player1 킬수
        self.p2_kill_ct = 0      # player2 킬수

        self.p1_killed = False
        self.p1_suicide = False
        self.p2_killed = False
        self.p2_suicide = False
        self.player1_win = False
        self.player2_win = False
        self.map = None
        self.name = None
        self.name_2 = None
        self.bullet1 = None
        self.filename = None
        self.p_last_ex = 0
        self.c_last_ex = 0
        self.pKillText = None
        self.cKillText = None
        pygame.font.init()

        # map random select
        self.num = random.randrange(1, 4)
        if self.num == 1:
            self.filename = self.map_name[0]
        elif self.num == 2:
            self.filename = self.map_name[1]
        elif self.num == 3:
            self.filename = self.map_name[2]
        self.load_data()

    def load_data(self):
        '''
            Loading map function
            example : path.dirname(__file__)
            C: / Users / 이호찬 / Desktop / pygame_broll / pygame_test
        :return: None
        '''
        self.map = Map(path.join(path.dirname(__file__), self.filename))

    def show_start_screen(self):
        pass

    def button(self, text, x, y, width, height, action=None, inactive_color=(0, 0, 0), active_color=(255, 255, 0)):
        pass

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen_1.blit(text_surface, text_rect)

    def new(self):
        pass

    def run(self):
        print(self.GamePlay)
        # game loop - set self.GamePlay = False to end the game
        while self.GamePlay:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def update(self):
        '''
            Update portion of the game loop
        :return: None
        '''
        p_kill = pygame.font.SysFont('Comic Sans MS', 18)
        c_kill = pygame.font.SysFont('Comic Sans MS', 18)
        self.pKillText = p_kill.render("Kills: " + str(self.p1_kill_ct) + "  Weapon: " + str(self.player.weapon), False,
                                      (0, 0, 0))
        self.cKillText = c_kill.render("Kills: " + str(self.p2_kill_ct) + "  Weapon: " + str(self.challenger.weapon), False,
                                      (0, 0, 0))

        self.all_sprites.update()
        self.camera1.update(self.player)
        self.camera2.update(self.challenger)

        # over 5 Kill -> Statement change
        if self.p1_kill_ct >= 5:
            self.p2_killed = False
            self.GamePlay = False
        elif self.p2_kill_ct >= 5:
            self.p1_killed = False
            self.GamePlay = False

    def draw(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                sprite.draw_health()
            if isinstance(sprite, Challenger):
                sprite.draw_health()

        for sprite in self.all_sprites:
            self.screen_1.blit(sprite.image, self.camera1.apply(sprite))
            self.screen_2.blit(sprite.image, self.camera2.apply(sprite))

        self.screen_1.blit(self.pKillText, (46, 10))
        self.screen_1.blit(self.cKillText, (558, 10))
        self.screen_1.blit(self.pKillText, (1086, 10))
        self.screen_1.blit(self.cKillText, (1598, 10))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # 윈도우의 닫기 버튼이 눌렸을 때, 프로그램을 종료하도록 처리
            if event.type == pygame.QUIT:
                self.quit()
                if self.GamePlay:
                    self.GamePlay = False
            # ESC 눌렀을 때 종료
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

        # Player1 사망 시 부활
        if self.p1_killed:
            self.p1_killed = False
            if self.p1_suicide is False:
                self.p2_kill_ct += 1
            else:
                self.p1_suicide = False
            for player in self.players:
                player.kill()                                              # ??
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)
            self.p1_killed = False

        # Player2 사망 시 부활
        if self.p2_killed:
            self.p2_killed = False
            if self.p2_suicide is False:
                self.p1_kill_ct += 1
            else:
                self.p2_suicide = False
            for challenger in self.challengers:
                challenger.kill()                               # ??
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)
            self.p2_killed = False

        if time.time() - self.p_last_ex > self.ex_lasting_t:
            for explosion in self.player_explosions:
                self.player_explosions.remove(explosion)
                self.all_sprites.remove(explosion)

        if time.time() - self.c_last_ex > self.ex_lasting_t:
            for explosion in self.challenger_explosions:
                self.challenger_explosions.remove(explosion)
                self.all_sprites.remove(explosion)

    def show_player1_win(self):
        self.player1_win = False
        self.screen_1 = pygame.display.set_mode((WIDTH * 2, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH * 2, HEIGHT))
        self.screen_1.blit(self.win_1p, [0, 0])
        self.screen_1.blit(self.lose, [1024, 0])
        print('p1 win')
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/" + self.sound_win)
        pygame.mixer.music.play(1)
        self.status = "play"
        pygame.display.update()

        pygame.time.delay(self.delay_time * 10)
        self.screen_1 = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/" + self.sound[1])
        pygame.mixer.music.play(1)
        pygame.display.init()

    def show_player2_win(self):
        self.player2_win = False
        self.screen_1 = pygame.display.set_mode((WIDTH * 2, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH * 2, HEIGHT))
        self.screen_1.blit(self.lose, [0, 0])
        self.screen_1.blit(self.win_2p, [1024, 0])
        print('p2 win')
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/" + self.sound_win)
        pygame.mixer.music.play(1)
        self.status = "play"
        pygame.display.update()

        pygame.time.delay(self.delay_time * 10)
        self.screen_1 = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sound/" + self.sound[1])
        pygame.mixer.music.play(1)
        pygame.display.init()
