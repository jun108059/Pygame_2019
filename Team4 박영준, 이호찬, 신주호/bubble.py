try:
    import sys
    import pygame
    from tilemap import *
    from sprites_BP import *
    from settings import *
    from os import path
    from pygame.locals import *
    from socket import *
    import random
    from super import *
except ImportError as err:
    print("couldn't load module. {}".format(err))
    sys.exit(2)


class bubble_fighter(Game):
    def __init__(self):
        # Superclass data
        self.sound = ["main_BGM.mp3"]

        self.result_WL = ['bubble_Win_1P.png', 'bubble_Win_2P.png', 'bubble_Lose.png']
        self.select_start = ['B_Select_start.png', 'B_Select_temp.png']
        # socket screen
        self.select_char = ['B_Select_char1.png', 'B_Select_char2.png', 'B_Select_char3.png', 'B_Select2_char1.png']
        self.start_main = ['loading_0.png', 'loading_1.png', 'loading_2.png', 'loading_Err.png']
        self.title = 'Bubble Fighter - 4 Team'
        # main
        self.main_page = ['bubble_main.png', 'bubble_main_control.png']
        # self.map_name = ["bubblemap_2.txt", 'ice.txt', "bubblemap_1.txt"]
        self.map_name = ["bubblemap_2.txt", "bubblemap_1.txt", "bubblemap_1.txt"]

        # About string
        self.enWord = 'hochan'

        # button sound
        self.button_sound = 'button-09.wav'
        self.sound = ['bubble_wait.mp3', 'bubble_main.mp3', "bubble_war_1.mp3", "bubble_war_2.mp3", "bubble_war_3.mp3"]
        self.sound_win = 'bubble_win.mp3'
        self.char_name = ["bazzi", "dao"]

        # Initialise screen
        pygame.init()

        #  라이브러리 초기화를 하지 않을 경우, 일부 기능이 정상 동작하지 않을 수 있다.
        self.screen_1 = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font_name = pygame.font.match_font('Stencil')
        pg.mixer.music.load("sound/" + self.sound[1])
        pg.mixer.music.play(1)

        # select char
        self.char_p1_1 = pygame.image.load(path.join('image', self.select_char[0])).convert()
        self.char_p1_1 = pygame.transform.scale(self.char_p1_1, (WIDTH, HEIGHT))
        self.char_p1_2 = pygame.image.load(path.join('image', self.select_char[1])).convert()
        self.char_p1_2 = pygame.transform.scale(self.char_p1_2, (WIDTH, HEIGHT))
        self.char_p1_3 = pygame.image.load(path.join('image', self.select_char[2])).convert()
        self.char_p1_3 = pygame.transform.scale(self.char_p1_3, (WIDTH, HEIGHT))
        self.char_p2_1 = pygame.image.load(path.join('image', self.select_char[3])).convert()
        self.char_p2_1 = pygame.transform.scale(self.char_p2_1, (WIDTH, HEIGHT))
        # select_start
        self.start_game = pygame.image.load(path.join('image', self.select_start[0])).convert()
        self.start_game = pygame.transform.scale(self.start_game, (WIDTH, HEIGHT))
        self.temp = pygame.image.load(path.join('image', self.select_start[1])).convert()
        self.temp = pygame.transform.scale(self.temp, (WIDTH, HEIGHT))
        # result_WL
        self.win_1p = pygame.image.load(path.join('image', self.result_WL[0])).convert()
        self.win_1p = pygame.transform.scale(self.win_1p, (WIDTH, HEIGHT))
        self.win_2p = pygame.image.load(path.join('image', self.result_WL[1])).convert()
        self.win_2p = pygame.transform.scale(self.win_2p, (WIDTH, HEIGHT))
        self.lose = pygame.image.load(path.join('image', self.result_WL[2])).convert()
        self.lose = pygame.transform.scale(self.lose, (WIDTH, HEIGHT))
        # socket 화면
        self.start_main_1 = pygame.image.load(path.join('image', self.start_main[0])).convert()
        self.start_main_1 = pygame.transform.scale(self.start_main_1, (WIDTH, HEIGHT))
        self.start_main_2 = pygame.image.load(path.join('image', self.start_main[1])).convert()
        self.start_main_2 = pygame.transform.scale(self.start_main_2, (WIDTH, HEIGHT))
        self.start_main_3 = pygame.image.load(path.join('image', self.start_main[2])).convert()
        self.start_main_3 = pygame.transform.scale(self.start_main_3, (WIDTH, HEIGHT))
        self.start_main_4 = pygame.image.load(path.join('image', self.start_main[3])).convert()
        self.start_main_4 = pygame.transform.scale(self.start_main_4, (WIDTH, HEIGHT))

        # image load 및 크기 조정
        self.start_main = pygame.image.load(path.join('image', self.main_page[0])).convert()
        self.start_main = pygame.transform.scale(self.start_main, (WIDTH, HEIGHT))
        self.start_main_control = pygame.image.load(path.join('image', self.main_page[1])).convert()
        self.start_main_control = pygame.transform.scale(self.start_main_control, (WIDTH, HEIGHT))

        Game.__init__(self)
        self.p1_bubble_status = None
        self.p2_bubble_status = None

    def show_start_screen(self):
        start = True
        pygame.display.init()
        while start:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # start 와 quit 으로 빠져나갈수 있다.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        start = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

            # click time/sec 를 맞춘다. 일정시간동안 클릭 횟수를 제한해야 클릭 1회를 특정할 수 있다.
            pygame.time.delay(self.delay_time//10)
            if self.status == 'play':
                self.screen_1.blit(self.start_main, (0, 0))
                self.button("", 110, 26, 200, 60, action="play")
                self.button("", 425, 26, 200, 60, action="controls")
                self.button("", 740, 26, 200, 60, action="quit")
                pygame.display.update()
            elif self.status == 'controls':
                self.screen_1.blit(self.start_main_control, [0, 0])
                self.button("", 93, 76, 200, 60, action="play")
                self.button("", 93, 194, 200, 60, action="main")
                self.button("", 93, 310, 200, 60, action="quit")
                pygame.display.update()
            elif self.status == 'select':
                self.data_init()
                self.screen_1.blit(self.char_p1_1, [0, 0])
                self.button2("", 78, 380, 365, 97, action="bazzi")    # P1
                self.button2("", 595, 380, 340, 97, action="dao")      # P2
                self.button4("back", 30, 30, 150, 40, action="main")
                pygame.display.update()
            elif self.status == 'select_2':
                self.screen_1.blit(self.char_p2_1, [0, 0])
                self.button3("", 78, 380, 365, 97, action="bazzi")    # P1
                self.button3("", 595, 380, 340, 97, action="dao")      # P2
                self.button4("back", 30, 30, 150, 40, action="main")
                pygame.display.update()
            elif self.status == 'quit':
                pygame.quit()
                quit()
            else:
                print('Error: status')

            pygame.display.update()

    def button(self, text, x, y, width, height, action=None, inactive_color=(0, 68, 145), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha() 투명도 코드
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (44, 42, 47), x + 75, y + 10)
            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == "quit":
                    self.status = "quit"

                if action == "controls":
                    self.status = "controls"

                if action == "play":
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[0])
                    pg.mixer.music.play(1)
                    self.status = "select"

                if action == "main":
                    self.status = "play"
        else:
            pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 75, y + 10)

    def button2(self, text, x, y, width, height, action=None, inactive_color=(236, 196, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha()
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 75, y + 5)

            if action == "bazzi":
                self.screen_1.blit(self.char_p1_2, (0, 0))
            if action == "dao":
                self.screen_1.blit(self.char_p1_3, (0, 0))

            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == "bazzi":
                    self.name = "bazzi"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                if action == "dao":
                    self.name = "dao"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                if action == "main":
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[1])
                    pg.mixer.music.play(1)
                    self.status = "play"

        else:
            # pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 75, y + 5)

    def button3(self, text, x, y, width, height, action=None, inactive_color=(236, 196, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha() 투명도 코드
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 75, y + 5)

            if action == self.char_name[0]:
                self.screen_1.blit(self.char_p1_2, (0, 0))
            if action == self.char_name[1]:
                self.screen_1.blit(self.char_p1_3, (0, 0))

            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == self.char_name[0]:     # bazzi
                    self.name_2 = self.char_name[0]
                    self.status = "play"
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[2])
                    pg.mixer.music.play(1)
                    self.screen_1.blit(self.start_game, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                    self.new()
                if action == self.char_name[1]:
                    self.name_2 = self.char_name[1]
                    self.status = "play"
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[3])
                    pg.mixer.music.play(1)
                    self.screen_1.blit(self.start_game, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                    self.new()

                if action == "main":
                    self.status = "select"

        else:
            # pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 75, y + 5)

    def button4(self, text, x, y, width, height, action=None, inactive_color=(236, 196, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha()
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 75, y + 5)

            if action == "bazzi":
                self.screen_1.blit(self.char_p1_2, (0, 0))
            if action == "dao":
                self.screen_1.blit(self.char_p1_3, (0, 0))

            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == "bazzi":
                    self.name = "bazzi"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                if action == "dao":
                    self.name = "dao"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time)
                if action == "main":
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[1])
                    pg.mixer.music.play(1)
                    self.status = "play"

        else:
            pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 75, y + 5)

    def new(self):
        """
            http://www.devshed.com/c/a/Python/PyGame-for-Game-Development-Sprite-Groups-and-Collision-Detection/
            쓰래기 공식문서보지말고 pygame.sprite.Group()은 이거보자
            https://stackoverflow.com/questions/13851051/how-to-use-sprite-groups-in-pygame group 사용법 질문이다
        :return: None
        """
        self.screen_1 = pygame.display.set_mode((WIDTH*2+120, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH*2+120, HEIGHT))
        # Create Map (basic / ice / purple)

        if self.filename == "bubblemap_1.txt":
            for row, tiles in enumerate(self.map.data):  # 맵과 두플레이어 생성
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row, 'sec_fence')
                    if tile == 'a':
                        Wall(self, col, row, 'sec_wall_2')
                    if tile == '.':
                        Grass(self, col, row, 'sec_floor')
                    if tile == 'b':
                        Wall(self, col, row, 'sec_wall_1')
                    if tile == 'c':
                        Grass(self, col, row, 'sec_wall_sha_2')
                    if tile == 'd':
                        Grass(self, col, row, 'sec_wall_sha_1')
                    if tile == 'e':
                        Wall(self, col, row, 'sec_wall_3')
                    if tile == 'f':
                        Wall(self, col, row, 'sec_wall_4')

            # 마지막에 그려야 우선순위가 다른것 보다 높아져 그위에 올라간다.
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)

        if self.filename == "bubblemap_2.txt":
            for row, tiles in enumerate(self.map.data):  # 맵과 두플레이어 생성
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row, 'sec_2_fence')
                    if tile == 'a':
                        Wall(self, col, row, 'sec_2_wall_1')
                    if tile == '.':
                        Grass(self, col, row, 'sec_2_floor')
                    if tile == 'b':
                        Wall(self, col, row, 'sec_2_wall_2')
                    if tile == 'c':
                        Grass(self, col, row, 'sec_2_wall_sha_1')
                    if tile == 'd':
                        Grass(self, col, row, 'sec_2_wall_sha_2')
                    if tile == 'e':
                        Wall(self, col, row, 'sec_2_wall_3')
                    if tile == 'f':
                        Wall(self, col, row, 'sec_2_wall_4')
                    if tile == 'g':
                        Grass(self, col, row, 'sec_2_wall_sha_3')
                    if tile == 'h':
                        Grass(self, col, row, 'sec_2_wall_5')

            # 마지막에 그려야 우선순위가 다른것 보다 높아져 그위에 올라간다.
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)

        self.camera1 = Camera1(self.map.width, self.map.height)
        self.camera2 = Camera2(self.map.width, self.map.height)

        # End of draw build
        self.run()

        # 5 kill -> player1 Win
        if self.p1_kill_ct >= 5:  # Player 1 Win
            self.p1_kill_ct = 0
            self.p2_kill_ct = 0
            self.player1_win = True
            self.GamePlay = True
            self.show_player1_win()

        elif self.p2_kill_ct >= 5:  # Player 2 Wi
            self.p1_kill_ct = 0
            self.p2_kill_ct = 0
            self.player2_win = True
            self.GamePlay = True
            self.show_player2_win()

    def draw(self):
        if self.filename == self.map_name[0]:
            self.screen_1.fill((234, 178, 119))
        elif self.filename == self.map_name[2]:
            self.screen_1.fill((93, 68, 87))
        else:
            self.screen_1.fill((35, 157, 247))
        Game.draw(self)

    def run(self):
        print(self.GamePlay)
        # game loop - set self.GamePlay = False to end the game
        while self.GamePlay:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            self.update()
            self.draw()

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
            self.p1_bubble_status = None
            self.p1_killed = False
            self.p2_kill_ct += 1
            for player in self.players:
                player.kill()
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)

        # Player2 사망 시 부활
        if self.p2_killed:
            self.p2_bubble_status = None
            self.p2_killed = False
            self.p1_kill_ct += 1
            for challenger in self.challengers:
                challenger.kill()
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)

        for player_bullet in self.player_bullets:
            wall_hits = pygame.sprite.spritecollide(player_bullet, self.walls, False)
            challenger_hits = pygame.sprite.spritecollide(player_bullet, self.challengers, False)

            for wall in wall_hits:
                self.player_bullets.remove(player_bullet)
                self.all_sprites.remove(player_bullet)

            for challenger in challenger_hits:
                challenger.health -= player_bullet.damage
                if challenger.health < 40:
                    self.p2_bubble_status = 'bubble'
                self.player_bullets.remove(player_bullet)
                self.all_sprites.remove(player_bullet)

        for challenger_bullet in self.challenger_bullets:
            wall_hits = pg.sprite.spritecollide(challenger_bullet, self.walls, False)
            player_hits = pg.sprite.spritecollide(challenger_bullet, self.players, False)

            for wall in wall_hits:
                self.challenger_bullets.remove(challenger_bullet)
                self.all_sprites.remove(challenger_bullet)


            for player in player_hits:
                player.health -= challenger_bullet.damage
                if player.health < 40:
                    self.p1_bubble_status = 'bubble'
                self.challenger_bullets.remove(challenger_bullet)
                self.all_sprites.remove(challenger_bullet)


if __name__ == '__main__':
    g = bubble_fighter()
    g.show_start_screen()

    while True:
        g.new()
