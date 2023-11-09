#창 크기
screen_height = 500
screen_width = 500

#color
white = (255, 255,255)
RED =   (255, 0, 0)


game_over = False #게임 루프 조건
winorlose = -1    # 승패 조건
endtime = 50      # 승 or 패배후 게임이 꺼지기 까지 시간
tic = 0           # 1프레임 지나간 횟수
time = 0          # 화면에 표시되는 시간
faze = 0          # 0일때 잡몹 페이즈 1일때 보스페이즈
inboss = False    # 보스 중복 생성을 막기 위해 보스가 있는지 없는지 확인하는 변수
boss = 0          # 보스
bosstime = 1      # 보스 후 흘러간 시간

#object
moblist = [[],[]]
weapons = [[],[]]
bossweapon  = [[],[]]
boxlist = []