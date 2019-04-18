try:
    import sys
    import pygame
    from tilemap import *
    from sprites import *
    from settings import *
    from os import path
    from pygame.locals import *
    from socket import *
    import random
    from super import *
except ImportError as err:
    print("couldn't load module. {}".format(err))
    sys.exit(2)


class broll_stars(Game):
    def __init__(self):
        # Superclass data
        self.sound = ["main_BGM.mp3"]
        self.select_char = ['Select_char1.png', 'Select_char2.png', 'Select_char3.png', 'Select_char4.png',
                            'Select2_char1.png', 'Select2_char2.png', 'Select2_char3.png', 'Select2_char4.png',
                            ]
        self.result_WL = ['Win_1P.png', 'Win_2P.png', 'Lose.png']
        self.select_start = ['Select_start.png', 'Select_temp.png']
        # socket screen
        self.start_main = ['start_main_1.png', 'start_main_2.png', 'start_main_3.png', 'start_main_4.png']
        self.title = 'BrawlStars'
        # main
        self.main_page = ['start_main.png', 'start_main_control.png']
        self.map_name = ['basic.txt', 'ice.txt', 'purple.txt']
        # About string
        self.enWord = 'hochan'
        # button sound
        self.button_sound = 'button-09.wav'
        self.sound = ['wait.mp3', 'main_BGM.mp3', "war_1.mp3", "war_2.mp3", "war_3.mp3"]
        self.sound_exploding = 'Exploding.wav'
        self.sound_win = 'win.mp3'
        self.char_name = ["brock", "colt", "shelly"]

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
        self.char_p1_4 = pygame.image.load(path.join('image', self.select_char[3])).convert()
        self.char_p1_4 = pygame.transform.scale(self.char_p1_4, (WIDTH, HEIGHT))
        self.char_p2_1 = pygame.image.load(path.join('image', self.select_char[4])).convert()
        self.char_p2_1 = pygame.transform.scale(self.char_p2_1, (WIDTH, HEIGHT))
        self.char_p2_2 = pygame.image.load(path.join('image', self.select_char[5])).convert()
        self.char_p2_2 = pygame.transform.scale(self.char_p2_2, (WIDTH, HEIGHT))
        self.char_p2_3 = pygame.image.load(path.join('image', self.select_char[6])).convert()
        self.char_p2_3 = pygame.transform.scale(self.char_p2_3, (WIDTH, HEIGHT))
        self.char_p2_4 = pygame.image.load(path.join('image', self.select_char[7])).convert()
        self.char_p2_4 = pygame.transform.scale(self.char_p2_4, (WIDTH, HEIGHT))
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

    def loading(self):
        pygame.display.init()

        self.screen_1.blit(self.start_main_1, (0, 0))
        pygame.display.update()

        pygame.time.delay(self.delay_time)

        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('127.0.0.1', 8081))

        self.screen_1.blit(self.start_main_2, (0, 0))
        pygame.display.update()
        print('연결 확인 됐습니다.')

        clientSock.send(self.enWord.encode('utf-8'))
        print('메시지를 전송했습니다.')

        data = clientSock.recv(1024)
        pygame.time.delay(self.delay_time)

        if data:
            self.screen_1.blit(self.start_main_3, (0, 0))
            pygame.display.update()

            if data.decode('utf-8') == 'success':
                print(data.decode('utf-8'))
                pygame.time.delay(self.delay_time)
                self.show_start_screen()
            else:
                self.screen_1.blit(self.start_main_4, (0, 0))
                pygame.display.update()
                print(data.decode('utf-8'))
                pygame.time.delay(self.delay_time*2)

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
                self.button("Play", 50, 40, 220, 40, action="play")
                self.button("How To", 50, 110, 220, 40, action="controls")
                self.button("Quit", 50, 180, 220, 40, action="quit")
                pygame.display.update()
            elif self.status == 'controls':
                self.screen_1.blit(self.start_main_control, [0, 0])
                self.button("Play", 50, 40, 220, 40, action="play")
                self.button("Main", 50, 110, 220, 40, action="main")
                self.button("Quit", 50, 180, 220, 40, action="quit")
                pygame.display.update()
            elif self.status == 'select':
                self.data_init()
                self.screen_1.blit(self.char_p1_1, [0, 0])
                self.button2("", 120, 420, 120, 35, action="brock")
                self.button2("", 465, 420, 120, 35, action="colt")
                self.button2("", 800, 420, 120, 35, action="shelly")
                self.button2("back", 20, 10, 220, 40, action="main")
                pygame.display.update()
            elif self.status == 'select_2':
                self.screen_1.blit(self.char_p2_1, [0, 0])
                self.button3("", 120, 420, 120, 35, action="brock")
                self.button3("", 465, 420, 120, 35, action="colt")
                self.button3("", 800, 420, 120, 35, action="shelly")
                self.button3("back", 20, 10, 220, 40, action="main")
                pygame.display.update()
            elif self.status == 'quit':
                pygame.quit()
                quit()
            else:
                print('Error: status')

            pygame.display.update()

    def button(self, text, x, y, width, height, action=None, inactive_color=(0, 0, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha() 투명도 코드
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 110, y + 10)
            # click event
            if click[0] == 1 and action != None:
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
            self.draw_text(text, 28, (0, 0, 0), x + 110, y + 10)

    def button2(self, text, x, y, width, height, action=None, inactive_color=(236, 196, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha()
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 110, y + 5)

            if action == "brock":
                self.screen_1.blit(self.char_p1_2, (0, 0))
            if action == "colt":
                self.screen_1.blit(self.char_p1_3, (0, 0))
            if action == "shelly":
                self.screen_1.blit(self.char_p1_4, (0, 0))

            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == "brock":
                    self.name = "brock"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)
                if action == "colt":
                    self.name = "colt"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)
                if action == "shelly":
                    self.name = "shelly"
                    self.status = "select_2"
                    self.screen_1.blit(self.temp, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)

                if action == "main":
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[1])
                    pg.mixer.music.play(1)
                    self.status = "play"

        else:
            pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 110, y + 5)

    def button3(self, text, x, y, width, height, action=None, inactive_color=(236, 196, 0), active_color=(255, 255, 0)):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            # self.box_active = self.screen_1.convert_alpha() 투명도 코드
            pygame.draw.rect(self.screen_1, active_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (255, 255, 255), x + 110, y + 5)

            if action == self.char_name[0]:
                self.screen_1.blit(self.char_p2_2, (0, 0))
            if action == self.char_name[1]:
                self.screen_1.blit(self.char_p2_3, (0, 0))
            if action == self.char_name[2]:
                self.screen_1.blit(self.char_p2_4, (0, 0))

            # click event
            if click[0] == 1 and action is not None:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.button_sound))
                if action == self.char_name[0]:
                    self.name_2 = self.char_name[0]
                    self.status = "play"
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[2])
                    pg.mixer.music.play(1)
                    self.screen_1.blit(self.start_game, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)
                    self.new()
                if action == self.char_name[1]:
                    self.name_2 = self.char_name[1]
                    self.status = "play"
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[3])
                    pg.mixer.music.play(1)
                    self.screen_1.blit(self.start_game, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)
                    self.new()

                if action == self.char_name[2]:
                    self.name_2 = self.char_name[2]
                    self.status = "play"
                    pg.mixer.music.stop()
                    pg.mixer.music.load("sound/" + self.sound[4])
                    pg.mixer.music.play(1)
                    self.screen_1.blit(self.start_game, (0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.delay_time * 2)
                    self.new()

                if action == "main":
                    self.status = "select"

        else:
            pygame.draw.rect(self.screen_1, inactive_color, (x, y, width, height), 3)
            self.draw_text(text, 28, (0, 0, 0), x + 110, y + 5)

    def new(self):
        """
            http://www.devshed.com/c/a/Python/PyGame-for-Game-Development-Sprite-Groups-and-Collision-Detection/
            쓰레기 공식문서보지말고 pygame.sprite.Group()은 이거보자
            https://stackoverflow.com/questions/13851051/how-to-use-sprite-groups-in-pygame group 사용법 질문이다
        :return: None
        """
        self.screen_1 = pygame.display.set_mode((WIDTH*2+120, HEIGHT))
        self.screen_2 = pygame.display.set_mode((WIDTH*2+120, HEIGHT))
        # Create Map (basic / ice / purple)
        if self.filename == self.map_name[0]:
            for row, tiles in enumerate(self.map.data):  # 맵과 두플레이어 생성
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row, 'wall_1')
                    if tile == 'i':
                        Grass(self, col, row, 'ground_1')
                    if tile == '.':
                        Grass(self, col, row, 'ground_2')
                    if tile == 'u':
                        Grass(self, col, row, 'ground_3')
                    if tile == 'f':
                        Grass(self, col, row, 'ground_4')
                    if tile == 'q':
                        Wall(self, col, row, 'wall')
                    if tile == 'w':
                        Wall(self, col, row, 'wall_2')
                    if tile == 'p':
                        Wall(self, col, row, 'wall_3')
                    if tile == 'o':
                        Wall(self, col, row, 'wall_4')
                    if tile == 'a':
                        Wall(self, col, row, 'wall_5')
                    if tile == 'x':
                        Grass(self, col, row, 'shadow')
                    if tile == 's':
                        Grass(self, col, row, 'shadow_1')
                    if tile == 'g':
                        Grass(self, col, row, 'grass')
                    if tile == 'y':
                        Grass(self, col, row, 'grass_1')
                    if tile == 't':
                        Grass(self, col, row, 'grass_2')
                    if tile == 'r':
                        Grass(self, col, row, 'grass_3')
                    if tile == 'l':
                        Grass(self, col, row, 'grass_4')
                    if tile == 'k':
                        Grass(self, col, row, 'grass_5')
                    if tile == 'h':
                        Grass(self, col, row, 'grass_6')
                    if tile == 'j':
                        Grass(self, col, row, 'grass_7')
                    if tile == 'z':
                        Grass(self, col, row, 'grass_8')
                    if tile == 'e':
                        Grass(self, col, row, 'cactus')
            # 마지막에 그려야 우선순위가 다른것 보다 높아져 그위에 올라간다.
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)

        if self.filename == self.map_name[1]:
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row, '2_fence')
                    if tile == '.':
                        Grass(self, col, row, '2_floor_1')
                    if tile == 'a':
                        Wall(self, col, row, '2_grass')
                    if tile == 'c':
                        Grass(self, col, row, '2_shadow_1')
                    if tile == 'b':
                        Grass(self, col, row, '2_shadow_2')
                    if tile == 'd':
                        Wall(self, col, row, '2_wall')
                    if tile == 'f':
                        Grass(self, col, row, '2_wall_sha')
                    if tile == 'e':
                        Wall(self, col, row, '2_box')
                    if tile == 'g':
                        Wall(self, col, row, '2_box_1')
                    if tile == 'h':
                        Grass(self, col, row, '2_box_sha_1')
                    if tile == 'i':
                        Grass(self, col, row, '2_box_sha_2')
                    if tile == 'j':
                        Grass(self, col, row, '2_box_sha_3')
                    if tile == 'k':
                        Grass(self, col, row, '2_box_sha_4')
                    if tile == 'l':
                        Wall(self, col, row, '2_flower')
                    if tile == 'm':
                        Grass(self, col, row, '2_floor_2')
                    if tile == 'n':
                        Wall(self, col, row, '2_wall_2')
            # 마지막에 그려야 우선순위가 다른것 보다 높아져 그위에 올라간다.
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'C':
                        self.challenger = Challenger(self, col, row)

        if self.filename == self.map_name[2]:
            for row, tiles in enumerate(self.map.data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row, '3_fence')
                    if tile == '.':
                        Grass(self, col, row, '3_floor_1')
                    if tile == 'a':
                        Wall(self, col, row, '3_grass')
                    if tile == 'b':
                        Grass(self, col, row, '3_grass_sha_1')
                    if tile == 'c':
                        Grass(self, col, row, '3_grass_sha_2')
                    if tile == 'd':
                        Grass(self, col, row, '3_grass_sha_3')
                    if tile == 'm':
                        Grass(self, col, row, '3_floor_2')
                    if tile == 'e':
                        Wall(self, col, row, '3_box')
                    if tile == 'g':
                        Wall(self, col, row, '3_box_2')
                    if tile == 'h':
                        Grass(self, col, row, '3_box_sha_1')
                    if tile == 'i':
                        Grass(self, col, row, '3_box_sha_2')
                    if tile == 'j':
                        Grass(self, col, row, '3_box_sha_3')
                    if tile == 'k':
                        Grass(self, col, row, '3_box_sha_4')
                    if tile == 'l':
                        Wall(self, col, row, '3_wall_1')
                    if tile == 't':
                        Wall(self, col, row, '3_wall_2')
                    if tile == 'n':
                        Wall(self, col, row, '3_wall_3')
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

        for player_bullet in self.player_bullets:
            wall_hits = pygame.sprite.spritecollide(player_bullet, self.walls, False)
            challenger_hits = pygame.sprite.spritecollide(player_bullet, self.challengers, False)
            if challenger_hits:
                self.p2_hit += 1
                print("p1 -> p2 hit")

            for wall in wall_hits:
                if type(player_bullet) is Bullet_Brock:
                    explode = Explode()
                    explode.rect.centerx = player_bullet.rect.centerx
                    explode.rect.centery = player_bullet.rect.centery
                    if player_bullet.dir == 0:
                        explode.rect.y += 20
                    elif player_bullet.dir == 1:
                        explode.rect.x -= 20
                    elif player_bullet.dir == 2:
                        explode.rect.y -= 20
                    elif player_bullet.dir == 3:
                        explode.rect.x += 20
                    self.all_sprites.add(explode)
                    self.player_explosions.add(explode)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.sound_exploding))
                    self.p_last_ex = time.time()
                self.player_bullets.remove(player_bullet)
                self.all_sprites.remove(player_bullet)

            for challenger in challenger_hits:
                if type(player_bullet) is Bullet_Brock:
                    explode = Explode()
                    explode.rect.centerx = player_bullet.rect.centerx
                    explode.rect.centery = player_bullet.rect.centery
                    if player_bullet.dir == 0:
                        explode.rect.y += 20
                    elif player_bullet.dir == 1:
                        explode.rect.x -= 20
                    elif player_bullet.dir == 2:
                        explode.rect.y -= 20
                    elif player_bullet.dir == 3:
                        explode.rect.x += 20
                    self.all_sprites.add(explode)
                    self.player_explosions.add(explode)
                    self.p_last_ex = time.time()
                challenger.health -= player_bullet.damage
                self.player_bullets.remove(player_bullet)
                self.all_sprites.remove(player_bullet)

        for player_ex in self.player_explosions:
            challenger_exd = pg.sprite.spritecollide(player_ex, self.challengers, False)
            suicide_p = pg.sprite.spritecollide(player_ex, self.players, False)
            for challenger in challenger_exd:
                challenger.health -= player_ex.damage
            for player in suicide_p:
                player.health -= player_ex.damage
                if player.health <= 0:
                    self.player_suicide = True

        for challenger_bullet in self.challenger_bullets:
            wall_hits = pg.sprite.spritecollide(challenger_bullet, self.walls, False)
            player_hits = pg.sprite.spritecollide(challenger_bullet, self.players, False)
            if player_hits:
                self.p1_hit += 1
                print("p2 -> p1 hit")

            for wall in wall_hits:
                if type(challenger_bullet) is Bullet_Brock:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.sound_exploding))
                    explode = Explode()
                    explode.rect.centerx = challenger_bullet.rect.centerx
                    explode.rect.centery = challenger_bullet.rect.centery
                    if challenger_bullet.dir == 0:
                        explode.rect.y += 20
                    elif challenger_bullet.dir == 1:
                        explode.rect.x -= 20
                    elif challenger_bullet.dir == 2:
                        explode.rect.y -= 20
                    elif challenger_bullet.dir == 3:
                        explode.rect.x += 20
                    self.all_sprites.add(explode)
                    self.challenger_explosions.add(explode)
                    self.c_last_ex = time.time()
                self.challenger_bullets.remove(challenger_bullet)
                self.all_sprites.remove(challenger_bullet)

            for player in player_hits:
                if type(challenger_bullet) is Bullet_Brock:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/" + self.sound_exploding))
                    explode = Explode()
                    explode.rect.centerx = challenger_bullet.rect.centerx
                    explode.rect.centery = challenger_bullet.rect.centery
                    if challenger_bullet.dir == 0:
                        explode.rect.y += 20
                    elif challenger_bullet.dir == 1:
                        explode.rect.x -= 20
                    elif challenger_bullet.dir == 2:
                        explode.rect.y -= 20
                    elif challenger_bullet.dir == 3:
                        explode.rect.x += 20
                    self.all_sprites.add(explode)
                    self.challenger_explosions.add(explode)
                    self.c_last_ex = time.time()
                player.health -= challenger_bullet.damage
                self.challenger_bullets.remove(challenger_bullet)
                self.all_sprites.remove(challenger_bullet)

        for challenger_ex in self.challenger_explosions:
            player_exd = pg.sprite.spritecollide(challenger_ex, self.players, False)
            suicide_c = pg.sprite.spritecollide(challenger_ex, self.challengers, False)
            for player in player_exd:
                player.health -= challenger_ex.damage
            for challenger in suicide_c:
                challenger.health -= challenger_ex.damage
                if challenger.health <= 0:
                    self.challenger_suicide = True


if __name__ == '__main__':
    g = broll_stars()
    g.loading()

    while True:
        g.new()
