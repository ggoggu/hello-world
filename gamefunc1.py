from set import *

#충돌 확인
def crashbox(a,b):
    return ((abs((a.xpos + a.width/2) - (b.xpos + b.width/2)) < a.width/2 + b.width/2) and (abs((a.ypos + a.height/2) - (b.ypos + b.height/2)) < a.height/2 + b.height/2))

#플레이어 무기와 보스의 상호작용
def bosstoweapon(boss,weapons):
    for weapontype in weapons:
        for weapon in weapontype:
            if(crashbox(weapon,boss)):
                boss.life -= weapon.attack
                weapontype.remove(weapon)

#2차원 리스트 생성
def listbilt(moblist):
    for mobn in moblist:
        for mob in mobn:
            mob.bilt()

#2차원 리스트 위치 이동
def listtrans(list):
    for i in list:
        for j in i:
            j.trans(faze)

#무기와 물체 충돌
def listcrash2(attacklist, list):
    for attacktype in attacklist:
        for weapon in attacktype:
            for i in list:
                for j in i:
                    if(crashbox(weapon,j)):
                        j.life -= weapon.attack
                        if(weapon in attacktype):
                            attacktype.remove(weapon)
                        
                        if(j.life <= 0):
                            i.remove(j)


#무기와 플레이어 충돌
def playercrash(player, list):
    for type in list:
        for weapon in type:
            if(crashbox(player,weapon)):
                player.life -= weapon.attack
                type.remove(weapon)
            
                        
#몹 이동
def mobmovement(moblist,player, faze):
    for mobn in moblist:
        for mob in mobn:
            mob.move(player,faze)
            mob.diagonalcorrection()
            mob.trans(faze)

#몹 충돌
def mobcrash(moblist,player, weapons):
    for mobn in moblist:
        for mob in mobn[:]:
            if(crashbox(mob,player)):
                player.life -= mob.attack
                mobn.remove(mob)
            else:
                for weapontype in weapons:
                    for weapon in weapontype:
                        if(crashbox(weapon,mob)):
                            mob.life -= weapon.attack
                            weapontype.remove(weapon)
                            if(mob.life <= 0 and (mob in mobn)):
                                player.kill += 1
                                mobn.remove(mob)
                    

#무기 이동 방법            
def weaponsmove(weapons):
    for wepontype in weapons:
        for wepon in wepontype:
            if(wepon.state == False):
                if(wepon.xpos < 0 or wepon.xpos > screen_width - wepon.width or wepon.ypos < 0 or wepon.ypos > screen_height - wepon.height):
                    wepontype.remove(wepon)
            else:
                if(wepon.xpos < -1 or wepon.xpos > screen_width - wepon.width + 1):
                    wepon.x = -wepon.x
                    wepon.angle += (90 - wepon.angle)*2
                
                if(wepon.ypos < -1 or wepon.ypos > screen_height - wepon.height + 1):
                    wepon.y = -wepon.y
                    wepon.angle += 2*(90 - wepon.angle)

#랜덤 박스 충돌과 효과
def boxcrash(player, list):
    for box in list:
        if(crashbox(box,player)):
            if(box.randomnumber == 0):
                player.statetime += 10 # 특정 시간동안 무기가 벽에 튕김
            elif(box.randomnumber == 1):
                player.life += 3        #생명력 증가
            elif(box.randomnumber == 2):
                player.velocity += 0.1  #속도 증가
            elif(box.randomnumber == 3):
                player.weapon1attack += 0.1     #공격력 증가
                player.weapon2attack += 0.2
            elif(box.randomnumber == 4):
                player.weapon1speed += 0.2      #무기 속도 증가
                player.weapon2speed += 0.1
      
            list.remove(box)


#1차원리스트 생성
def listblit2(list):
    for i in list:
        i.bilt()

#1차원 리스트 중력영향
def listgravity1(list):
    for i in list:
        i.gravity2()

#2차원 리스트 중력영향
def listgravity2(list):
    for i in list:
        for j in i:
            j.gravity()

#1차원 리스트 벽 충돌
def listblock1(list):
    for i in list:
        i.block()

#2차원 리스트 벽 충돌
def listblock2(list):
    for i in list:
        for j in i:
            j.block()

#게임 승패 조건 보스페이즈시
def gameend2(player, boss):
    if(player.life <= 0):
        print("you are lose")
        return 0
    elif(boss.life <= 0):
        print("you are win")
        return 1
    else:
        return -1

#잡몹페이즈시 패배 조건
def gameend1(player):
    if(player.life <= 0):
        print("you are lose")
        return 0
    else:
        return -1