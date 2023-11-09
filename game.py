import pygame
import sys
import math
import random
from gamefunc1 import*
from set import*

class Model():
    def __init__(self, imgname):
#       self.points
        self.x = 0
        self.y = 0
        self.xpos = 0 
        self.ypos = 0
        self.velocity = 0
        self.img = pygame.image.load(imgname)
        self.size = self.img.get_rect().size
        self.width = self.size[0] # 사진의 넓이
        self.height = self.size[1] #사진의 높이
        self.diagonal = 1.0 #대각선 보정 크기
        self.life = 1
        self.attack = 1
    
    #벽에 막히게 하기
    def block(self):
        if(self.xpos < 0):
            self.xpos = 0
        elif(self.xpos > screen_width - self.width):
            self.xpos = screen_width - self.width
    
        if(self.ypos < 0):
            self.ypos = 0
        elif(self.ypos > screen_height - self.height):
            self.ypos = screen_height - self.height
    
    #화면에 생성
    def bilt(self):
        screen.blit(self.img,(self.xpos,self.ypos))

    #속도에 따라 위치 이동
    def trans(self,faze):
        if(faze == 0):
            self.xpos += (self.x*df)/self.diagonal/10
            self.ypos += (self.y*df)/self.diagonal/10
        elif(faze == 1):
            self.xpos += (self.x*df)/10
            self.ypos += (self.y*df)/10

    #대각선 속도 보정    
    def diagonalcorrection(self):
        self.diagonal = 1.0  
        if(abs(self.x) > 0 and abs(self.y) >0):
            self.diagonal = math.sqrt(pow(self.x,2) + pow(self.y,2))/abs(self.x)
    
    #페이즈2 중력 영향
    def gravity(self):
        self.y += 0.1
    
    #페이즈2 중력 영향 박스만 해당
    def gravity2(self):
        self.ypos += 1
   
class Player(Model):
    def __init__(self):
        super().__init__("image/player.png")
        self.xpos = (screen_width/2) - (self.width/2)
        self.ypos = (screen_height/2) - (self.height/2)
        self.velocity = 2
        self.life = 50
        self.rotation = 0
        self.rotated_img = pygame.transform.rotate(self.img, self.rotation)
        self.weapontype = 0 # 현재 무기 종류
        self.maxweapon = 2 # 무기 최대 갯수
        self.weaponsleep = 0; self.attacksleep0 = 0
        self.state = False
        self.rotation_speed = 4 # 회전 속도
        self.kill = 0
        self.weapon1attack = 0.3; self.weapon1speed = 5; self.weapon2attack = 1; self.weapon2speed = 1 # 무기의 공격력과, 투사체의 속도
        self.jumpcount = 2; self.statetime = 0 # 중력상태의 점프할때 높이와, 무기에 벽에 튕길수 있는 시간
    
    #플레이어 이동방식
    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 97 or event.key == 65:
                self.x -= self.velocity
            elif event.key == 115 or event.key == 83:
                self.y += self.velocity
            elif event.key == 100 or event.key == 68:
                self.x += self.velocity
            elif event.key == 87 or event.key ==  119:
                self.y -= self.velocity
        
        if event.type == pygame.KEYUP:
            if event.key == 97 or event.key ==  65 or event.key == 100 or event.key == 68:
                self.x = 0
            elif event.key == 115 or event.key == 83 or event.key == 87 or event.key == 119:
                self.y = 0


    #보스페이즈 시 이동방식
    def move2(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == 97 or event.key == 65:
                self.x -= self.velocity
            elif event.key == 100 or event.key == 68:
                self.x += self.velocity

        if event.type == pygame.KEYUP:
            if event.key == 97 or event.key ==  65 or event.key == 100 or event.key == 68:
                self.x = 0

    #보스페이즈시 점프
    def jump(self, event):
        if event[pygame.K_w] == True and self.jumpcount > 0:
            self.jumpcount -= 1
            self.y = -3
    
    #점프 조건
    def jumpc(self):
        if self.ypos >= (screen_height - self.height) :
            self.jumpcount = 2
            
    #플레이어 회전 방식
    def rotate(self, event):
        if event[pygame.K_LEFT]:
            self.rotation += self.rotation_speed
        elif event[pygame.K_RIGHT]:
            self.rotation -= self.rotation_speed
        self.rotated_img = pygame.transform.rotate(self.img, self.rotation)
    
    #플레이어 회전방식 2 원래 보스페이즈시 사용할려 했으나 불필요해 보여서 사용하지 않음
    def rotate2(self, event):
        if event[pygame.K_LEFT]:
            self.rotation = 180
        elif event[pygame.K_RIGHT]:
            self.rotation = 0
        elif event[pygame.K_UP]:
            self.rotation = 90
        self.rotated_img = pygame.transform.rotate(self.img, self.rotation)
    
    #회전된 상태 생성
    def bilt2(self):
        screen.blit(self.rotated_img,(self.xpos, self.ypos))

    #공격
    def goattack(self, event):
        if event[pygame.K_SPACE] and self.attacksleep0 <= 0:
            if(self.weapontype == 0):
                weapons[0].append(Weapon("image/weapon0.png", self.weapon1speed, self.weapon1attack, self.state))
                self.attacksleep0 = 10
            if(self.weapontype == 1):
                weapons[1].append(Weapon("image/weapon1.png",self.weapon2speed,self.weapon2attack, self.state))
                self.attacksleep0 = 50
    
    #무기 봐꾸기
    def weaponchange(self,evnet):
        if(self.weaponsleep <= 0):
            if evnet[pygame.K_r]:
                if(self.weapontype < self.maxweapon - 1):
                    self.weapontype += 1
                else:
                    self.weapontype = 0

                self.weaponsleep = 2
    
    #무기 효과 확인
    def changestate(self):
        if(self.statetime > 0):
            self.state = True
        else:
            self.state = False

# player weapon
class Weapon(Model):
    def __init__(self, imgname, speed, attack, state):
        super().__init__(imgname)
        self.angle = player.rotation
        self.velocity = speed
        self.x = math.cos(math.radians(self.angle))*self.velocity
        self.y = -math.sin(math.radians(self.angle))*self.velocity
        self.xpos = player.xpos + player.width/2
        self.ypos = player.ypos + player.height/2
        self.state = state # 벽에 튀길 수 있는지 없는지 확인
        self.attack = attack
        self.type = player.weapontype
        self.rotated_img = pygame.transform.rotate(self.img, self.angle)

    #회전 생성
    def bilt2(self):
        screen.blit(self.rotated_img,(self.xpos, self.ypos))    

# boss weapon
class Weapon2(Model):
    def __init__(self, imgname, speed, attack, angle, xpos, ypos, life = 2):
        super().__init__(imgname)
        self.angle = angle
        self.xpos = xpos
        self.ypos = ypos
        self.state = False
        self.x = speed*math.cos(math.radians(angle))
        self.y = speed*math.sin(math.radians(angle))
        self.attack = attack
        self.life = life
        self.rotated_img = pygame.transform.rotate(self.img, self.angle)

    #이동 방식
    def move(self):
        self.xpos += (self.x*df)/10
        self.ypos += (self.y*df)/10

    #회전 생성
    def bilt2(self):
        screen.blit(self.rotated_img,(self.xpos, self.ypos))      

class Mob(Model):
    def __init__(self, imgname, speed, life, attack):
        super().__init__(imgname)
        self.xpos = random.randrange(self.width,screen_width - self.width)
        self.ypos = random.randrange(self.height,screen_height + self.height)
        self.velocity = speed
        self.life = life
        self.attack = attack
    
    #몹 이동 방식 플레이어 방향으로 쫒아감
    def move(self,player,faze):
        if(faze == 0):
            if(player.xpos > self.xpos):
                self.x = self.velocity
            elif(player.xpos < self.xpos):
                self.x = -self.velocity
        
            if(player.ypos > self.ypos):
                self.y = self.velocity
            elif(player.ypos < self.ypos):
                self.y = -self.velocity
        elif(faze == 1):
            if(player.xpos > self.xpos):
                self.x = self.velocity
            elif(player.xpos < self.xpos):
                self.x = -self.velocity 

class Box(Model):
    def __init__(self, imgname):
        super().__init__(imgname)
        self.xpos = random.randrange(self.width, screen_width - self.width)
        self.ypos = random.randrange(self.height, screen_height - self.height)
        self.randomnumber = random.randrange(0,5)

class Boss(Model):
    def __init__(self, imgname, life):
        super().__init__(imgname)
        self.xpos = screen_width/2 - self.width/2
        self.ypos = 0
        self.life = life

# 보스 공격 패턴        
def bossattack(type,bossweapon):
    if(type == 0):
        for i in range(10):
            bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,90,i*70,1))
    elif(type == 1):
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,0,0,screen_height - 30))
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,0,0,screen_height - 30))
    elif(type == 2):
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,0,0,screen_height - 30))
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,180,screen_width-30,screen_height - 30))
    elif(type == 3):
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,0,0,screen_height - 80))
        bossweapon[0].append(Weapon2("image/bossweapon1.png",4,1,180,screen_width-30,screen_height - 80))

        
#init
pygame.init()
clock = pygame.time.Clock()
font_1 = pygame.font.SysFont("arial",30,True,True)

# screen
screen = pygame.display.set_mode([screen_width,screen_height])
pygame.display.set_caption("test")

#player
player = Player()

#화면에 표시될 글자
timename = font_1.render("time:", True, (0,0,0))
lifename = font_1.render("life:", True, (0,0,0))
killname = font_1.render("kill:", True, (0,0,0))
what = font_1.render("move:wasd,roation:left,right,attack:space", True, (0,0,0))
what2 = font_1.render("weaponchange:r", True, (0,0,0))
win = font_1.render("you are win", True, (0,0,0))
lose = font_1.render("you are lose", True, (0,0,0))

#mob
moblist[0].append(Mob("image/mob1.png",1,1,1))

while not game_over:
    df = clock.tick(60)

    tic += 1

    # 1초당 카운트, 그 시간에 따라 동작 되는 것들
    if(tic == 60):
        time += 1
        player.weaponsleep -= 1

        if(player.statetime > 0):
            player.statetime -= 1
        

        # 몹생성
        if(time < 40):
            moblist[0].append(Mob("image/mob1.png",1,1,1))
        elif(time >= 40 and time < 80):
            moblist[1].append(Mob("image/mob2.png",1.2,2,2))
        elif(time >= 80):
            moblist[0].append(Mob("image/mob1.png",1,1,1))
            moblist[1].append(Mob("image/mob2.png",1.2,2,2))

        #박스 생성
        if(time%5 == 0):
            boxlist.append(Box("image/randombox.png"))

        #보스 생성 후 시간
        if(faze == 1):
            bosstime += 1
        
        #보스 공격 생성
        if(bosstime%4 == 0):
            bossattack(random.randrange(0,4),bossweapon)
            bosstime = 0

        tic = 0

    #공격 속도
    player.attacksleep0 -= 1

    #무기 특수 효과 확인
    player.changestate()

    #화면에 표시되는 변하는 숫자
    screentime = font_1.render(str(time), True, (0,0,0))
    screenlife = font_1.render(str(player.life), True, (0,0,0))
    screenkill = font_1.render(str(player.kill), True, (0,0,0))

    #보스 생성 조건
    if(player.kill > 40 and inboss == False):
        faze = 1
        boss = Boss("image/boss.png",50)
    
    #보스 생성 상태 확인
    if(faze == 1 and inboss == False):
        inboss = True

    #잡몹 페이즈
    elif(faze == 0):
        winorlose = gameend1(player)
        event2 = pygame.key.get_pressed()
        player.rotate(event2)
        player.goattack(event2)
        player.weaponchange(event2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over=True
            
            player.move(event)        

        player.diagonalcorrection()
        player.trans(faze)
        player.block()

        #상호작용
        mobcrash(moblist,player, weapons)
        weaponsmove(weapons)
        listtrans(weapons)
        mobmovement(moblist, player, faze)
        boxcrash(player,boxlist)

        #화면에 띄우기
        screen.fill(white)
        player.bilt2()
        if(time < 10):
            screen.blit(what,(0,100))
            screen.blit(what2,(0,130))
        screen.blit(timename,(0,10))
        screen.blit(screentime,(60,10))
        screen.blit(lifename,(100,10))
        screen.blit(screenlife,(145,10))
        screen.blit(killname,(180,10))
        screen.blit(screenkill,(225,10))
        listbilt(moblist)
        listbilt(weapons)
        listblit2(boxlist)
        
    #보스 페이즈
    elif faze == 1:
        winorlose = gameend2(player,boss)
        event2 = pygame.key.get_pressed()
        player.rotate(event2)
        player.goattack(event2)
        player.weaponchange(event2)
        player.jump(event2)
        player.jumpc()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over=True

            player.move2(event)


        player.diagonalcorrection()
        player.trans(faze)
        player.block()

        #상호작용
        mobcrash(moblist,player, weapons)
        listcrash2(bossweapon,moblist)
        listcrash2(weapons,bossweapon)
        playercrash(player,bossweapon)
        boxcrash(player,boxlist)
        weaponsmove(weapons)
        weaponsmove(bossweapon)
        listtrans(weapons)
        bosstoweapon(boss,weapons)
        mobmovement(moblist, player, faze)
        listgravity1(boxlist)
        listgravity2(moblist)
        listtrans(bossweapon)
        listblock1(boxlist)
        listblock2(moblist)
        player.gravity()

        #화면에 띄우기
        screen.fill(white)
        if(winorlose != 1):
            boss.bilt()
        player.bilt2()
        screen.blit(timename,(0,10))
        screen.blit(screentime,(60,10))
        screen.blit(lifename,(100,10))
        screen.blit(screenlife,(145,10))
        screen.blit(killname,(180,10))
        screen.blit(screenkill,(225,10))
        listbilt(moblist)
        listbilt(weapons)
        listblit2(boxlist)
        listbilt(bossweapon)


    #승패 확인
    if(winorlose == 1):
        endtime -= 0.1
        screen.blit(win,(150,screen_height/2 - 30))
        player.weapon1attack = 0
        player.weapon2attack = 0
        player.life = 100
    elif(winorlose == 0):
        endtime -= 0.1
        screen.blit(lose,(150,screen_width/2 - 30))
        player.weapon1attack = 0
        player.weapon2attack = 0
    
    if(endtime < 0):
        game_over = True


    pygame.display.update()

print("game closed")
pygame.quit()
sys.exit()