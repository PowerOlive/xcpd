import sys
import copy
import time
from os import *
from random import *

marker="=================================="
spliter='================================================================================================'
selects=['是','否']
maxBlood=100
initKill=0
warnningBlood=50
initSight=0.7
levelSight=0.05
footName='双脚'
footSpeed=5
footTimes=100
handName='双手'
handAttack=1
handBurstAttack=5
handTimes=100
hairName='头发'

levels=['青铜','白银','黄金','铂金','黑金','钻石','战神']

def win(player,message):
    print("\n\n\n")
    print("%s%s%s"%(marker,message,marker))
    print(player)

def choose(array):
    result=''
    for index in range(len(array)):
       result = result + str(index+1) + '. ' + str(array[index]) + ' '
    return result

def getIntInput(message,defaultValue=0):
    answer=input(message)
    try:
        return int(answer)
    except:
        return defaultValue

def chooseBlocks(message,array,choosedMessage,failMessage):
    print(spliter)
    index=getIntInput(message%(choose(array)))
    if index >=1 and index <= len(array):
        print(choosedMessage%(array[index-1]))
        return array[index-1]
    else:
        input(failMessage)
        sys.exit()

def randomItem(array):
    if len(array)-1 < 0:
        return None
    index=randint(0,len(array)-1)
    object=array[index]
    del array[index]
    return object


def chooseObject(player,object,message,choosedMessage,failMessage):
    print("您当前的状态：")
    print(player)
    answer=getIntInput(message%(str(object),choose(selects)))
    if answer == 1:
        if isinstance(object,Vehicle):
            player.vehicle=copy.copy(object)
        elif isinstance(object,Weapon):
            player.weapon=copy.copy(object)
        elif isinstance(object,Helmet):
            player.helmet=copy.copy(object)
        elif isinstance(object,Medkit):
            player.medkit=copy.copy(object)
        else :
            input("您是天神下凡吗？可惜服务器出bug了。。。")
            sys.exit()
        print(choosedMessage%(object))
        print("\n您当前的状态：")
        print(player)
    else:
        print(failMessage%(object))

def winRate(player,enemy):
    playerTotalBlood=player.totalBlood()
    enemyTotalBlood=enemy.totalBlood()
    playerSight=player.sight()
    enemySight=enemy.sight()
    killEnemyTimes=enemyTotalBlood/player.singleAttack()
    killedTimes=playerTotalBlood/enemy.singleAttack()
    return format(killedTimes/killEnemyTimes/(enemySight/playerSight), '.0%')

def chooseFight(player,enemy,message,winMessage,failMessage):
    print("\n\n您当前的状态：")
    print(player)
    answer=getIntInput(message%(str(enemy),"您的胜率：『%s』"%(winRate(player,enemy)),choose(selects)))
    if answer == 1:
        if player.fight(enemy) ==1:
            print(winMessage%(enemy.name))
            return
        else:
            print(failMessage%(enemy.name))
            sys.exit()
    else:
        enemies.append(enemy)
        attacked=enemy.attack()
        player.attacked(attacked)
        print("您被『%s』发现并被攻击『%d』！"%(enemy.name,attacked))
        if player.blood <= 0:
            print(failMessage%(enemy.name))
            sys.exit()

class Medkit:
    name = ''
    value = 0
    def __init__(self,name,value):
        self.name=name
        self.value=value
        
    def __str__(self):
        if self.value >0:
            return "『%s』，补充血量：『%d』"%(self.name,self.value)
        else:
            return "『%s』"%(self.name)

noneMedkit=Medkit('无',0)

class Vehicle:
    name = ''
    speed = 0
    leftTimes = 0
    def __init__(self,name,speed,leftTimes):
        self.name=name
        self.speed=speed
        self.leftTimes=leftTimes
        
    def __str__(self):
        return "『%s』， 速度：『%d』，剩余次数：『%d』"%(self.name,self.speed,self.leftTimes)
    def toFoot(self):
        self.name=footName
        self.speed=footSpeed
        self.leftTimes=footTimes
    def run(self):
        if self.leftTimes > 0 :
            self.leftTimes=self.leftTimes-1
            return self.speed
        else :
            if self.name != footName:
                print("『%s』剩余次数为『0』，自动丢弃！"%(self.name))
                self.toFoot()
                return self.speed
            else:
                print("双脚已经不能支撑您壮硕的娇躯，爬着走吧！！！")
                return 1

foot=Vehicle(footName,footSpeed,footTimes)

class Weapon:
    name = ''
    attackValue = 0
    leftTimes = 0
    totalTimes=0
    def __init__(self,name,attackValue,leftTimes):
        self.name=name
        self.attackValue=attackValue
        self.leftTimes=leftTimes
        self.totalTimes=leftTimes
    def __str__(self):
        return "『%s』， 攻击力：『%d』，剩余攻击次数：『%d』"%(self.name,self.attackValue,self.leftTimes)
    
    def singleAttack(self):
        return self.attackValue*(self.leftTimes/self.totalTimes)+0.1
    def toHand(self):
        self.name=handName
        self.attackValue=handAttack
        self.leftTimes=handTimes
        self.totalTimes=handTimes
    def attack(self):
        if self.leftTimes > 0 :
            self.leftTimes=self.leftTimes-1
            return self.attackValue
        else :
            if self.name != handName:
                print("『%s』剩余攻击力为『0』，自动丢弃！"%(self.name))
                self.toHand()
                return self.attackValue
            else:
                randomInt=randint(0,20)
                if randomInt == 20:
                    print("有一双手获得天神垂青，突然暴起了！！！")
                    return handBurstAttack
                else:
                    print("双手过于疲劳，无力攻击，等天神垂青吧，好悲哀啊。。。")
                    return 0

hand=Weapon(handName,handAttack,handTimes)

class Helmet:
    name = ''
    level = 0
    leftValue = 0
    def __init__(self,name,level,leftValue):
        self.name=name
        self.level=level
        self.leftValue=leftValue
    def __str__(self):
        return "『%s』，剩余防护力：『%d』"%(self.name,self.leftValue)
    def protect(self,value):
        if self.leftValue >= value :
            self.leftValue=self.leftValue-value
            return 0
        else :
            self.leftValue=self.leftValue-value
            returnValue=abs(self.leftValue)
            self.leftValue=0
            if self.name != hairName:
                print("头盔『%s』被打烂"%(self.name))
                self.name=hairName
                self.level=0
                self.leftValue=0
            return returnValue

hair=Helmet(hairName,0,0)

class Person:
    name = ''
    blood = 100
    kill = 0
    weapon=None
    helmet=None
    vehicle=None
    medkit=noneMedkit
    level=''
    def __init__(self,name,blood,kill,vehicle,weapon,helmet,medkit=noneMedkit):
        self.name=name
        self.blood=blood
        self.kill=kill
        self.weapon=weapon
        self.helmet=helmet
        self.vehicle=vehicle
        self.medkit=medkit
        self.setLevel()
    def __str__(self):
        return "名字：『%s』    血量：『%d』    等级：『%s』\n交通：%s\n武器：%s\n头盔：%s\n医疗包：%s"%(self.name,self.blood,self.level,self.vehicle,self.weapon,self.helmet,self.medkit)

    def setLevel(self):
        if self.kill<len(levels):
            self.level=levels[self.kill]
        else:
            self.level=levels[len(levels)-1]
    def addKill(self):
        self.kill=self.kill+1
        self.setLevel()
    def sight(self):
        return self.kill * levelSight+initSight
    def totalBlood(self):
        initTotalBlood=self.blood+self.helmet.leftValue+self.medkit.value
        if initTotalBlood < 0:
            initTotalBlood = 0
        return initTotalBlood
    def totalAttack(self):
        return self.weapon.leftTimes*self.weapon.attackValue+handTimes
    def singleAttack(self):
        return self.weapon.singleAttack()*self.sight()
    def run(self):
        return self.vehicle.run()
    def attack(self):
        initAttack=self.weapon.attack()
        currentSight=random()
        if self.sight() >= currentSight:
            return initAttack
        else:
            print("怎么回事，是等级太低还是风？竟然打偏了，一定是风太大导致的！！！")
            return 0
    def attacked(self,value):
        attackLeft=self.helmet.protect(value)
        self.blood=self.blood-attackLeft
    def fight(self,enemy):
       print("您总血量：『%d』，『%s』总血量：『%d』"%(self.totalBlood(),enemy.name,enemy.totalBlood()))
       while self.blood > 0 and enemy.blood >0:
            if self.blood < warnningBlood and self.medkit != noneMedkit:
                answer=getIntInput("您当前血量『%d』有点危险，有一个医疗包：%s，是否使用：%s"%(self.blood,str(self.medkit),choose(selects)))
                if answer == 1:
                    self.blood=self.blood+self.medkit.value
                    self.medkit=noneMedkit
                    if self.blood > maxBlood:
                        self.blood=maxBlood
            attacked=self.attack()
            enemy.attacked(attacked)
            print("您攻击了『%s』，攻击力『%d』，对方剩余总血量：『%d』"%(enemy.name,attacked,enemy.totalBlood()))
            time.sleep(1)
            if enemy.blood <= 0:
                self.addKill()
                return 1
            attacked=enemy.attack()
            self.attacked(attacked)
            print("您被『%s』攻击了，攻击力『%d』，您剩余总血量：『%d』"%(enemy.name,attacked,self.totalBlood()))
            time.sleep(1)
            if self.blood <= 0:
                enemy.addKill()
                return 0
class Block:
    name = ''
    range = 0
    def __init__(self,name,range):
        self.name=name
        self.range=range
    def __str__(self):
        return "『%s(%d公里)』"%(self.name,self.range)

vehicles=[Vehicle('哈雷摩托',70,10),Vehicle('悍马',50,5),Vehicle('悍马',50,5),Vehicle('吉普',30,10),Vehicle('吉普',30,10),Vehicle('吉普',30,10),Vehicle('自行车',10,100),Vehicle('自行车',10,100),Vehicle('自行车',10,100),Vehicle('自行车',10,100)]
weapons=[Weapon('AWM',130,5),Weapon('AKM',25,40),Weapon('AKM',25,40),Weapon('M416',22,40),Weapon('M416',22,40),Weapon('M4',20,35),Weapon('M4',20,35),Weapon('M4',20,35),Weapon('手枪',15,8),Weapon('手枪',15,8),Weapon('手枪',15,8),Weapon('手枪',15,8),Weapon('撬棍',2,100),Weapon('撬棍',2,100),Weapon('撬棍',2,100),Weapon('撬棍',2,100),Weapon('撬棍',2,100)]
helmets=[Helmet('三级头',3,230),Helmet('破损三级头',3,180),Helmet('残破三级头',3,140),Helmet('二级头',2,150),Helmet('二级头',2,150),Helmet('破损二级头',2,120),Helmet('破损二级头',2,120),Helmet('残破二级头',2,90),Helmet('残破二级头',2,90),Helmet('一级头',1,80),Helmet('一级头',1,80),Helmet('一级头',1,80),Helmet('破损一级头',1,60),Helmet('破损一级头',1,60),Helmet('破损一级头',1,60),Helmet('残破一级头',1,40),Helmet('残破一级头',1,40),Helmet('残破一级头',1,40)]
medkits=[Medkit('医疗盒',50),Medkit('医疗包',30),Medkit('医疗包',30),Medkit('可乐',10),Medkit('可乐',10),Medkit('可乐',10)]
enemies=[Person('大魔王',randint(50,maxBlood),randint(2,6),randomItem(vehicles),randomItem(weapons),randomItem(helmets)),Person('小魔王',randint(20,maxBlood),randint(1,5),randomItem(vehicles),randomItem(weapons),randomItem(helmets)),Person('霸哥',randint(10,maxBlood),randint(0,4),randomItem(vehicles),randomItem(weapons),randomItem(helmets)),Person('萌妹',randint(10,maxBlood),randint(0,3),randomItem(vehicles),randomItem(weapons),randomItem(helmets)),Person('马可波',randint(10,maxBlood),randint(0,3),randomItem(vehicles),randomItem(weapons),randomItem(helmets)),Person('瓦特',randint(10,maxBlood),randint(0,3),randomItem(vehicles),randomItem(weapons),randomItem(helmets))]
blocks=[Block('S城',1000),Block('G港',700),Block('P城',300),Block('自由岛',100)]

print(marker+" 本游戏由香肠派对工作室出品 "+marker)
print("\t\t\t\t    抵制不良游戏 拒绝盗版游戏 \n\t\t\t\t    注意自我保护 谨防受骗上当 \n\t\t\t\t    适度游戏益脑 沉迷游戏伤身 \n\t\t\t\t    合理安排时间 享受健康生活");
print(spliter)

name = input("请输入角色名字：")
player=Person(name,maxBlood,initKill,foot,hand,hair)
print(spliter)
print("欢迎进入香肠派对,您当前的状态：")
print(player)

block=chooseBlocks("准备跳伞，请选择您降落的位置\n%s：",blocks,"您成功落地到：%s","您掉落到未知世界\n您已成盒，从新来过吧^_^")
index=0
while index < block.range:
    print(spliter)
    if len(enemies) == 0:
        win(player,"全部敌人被您消灭，恭喜您提前吃鸡！")
        sys.exit()
    type=randint(0,20)
    if 0<= type <2:
        object=randomItem(medkits)
        if object == None:
            input("好像看到一个医疗包的影子，难道因为我贫血到眼花了吗？")
        else:
            chooseObject(player,object,"\n前方发现一个医疗包 %s\n是否替换现有装备 %s :","成功获取装备：%s","很遗憾，您错过了装备：%s")
    elif 2<= type <5:
        object=randomItem(vehicles)
        if object == None:
            input("此处有轮胎印，是谁把我的车抢了？")
        else:
            chooseObject(player,object,"\n前方发现一个车辆 %s\n是否替换现有装备 %s :","成功获取装备：%s","很遗憾，您错过了装备：%s")
    elif 5<= type <9:
        object=randomItem(weapons)
        if object == None:
            input("就剩点弹壳和没有子弹的空枪，害我白高兴一场！！！")
        else:
            chooseObject(player,object,"\n前方发现一个武器 %s\n是否替换现有装备 %s :","成功获取装备：%s","很遗憾，您错过了装备：%s")
    elif 9<= type <13:
        object=randomItem(helmets)
        if object == None:
            input("谁这么没有素质，用坏的头盔也不知道放到垃圾桶里面去，让我发现是谁，一定不能轻饶了！")
        else:
            chooseObject(player,object,"\n前方发现一个头盔 %s\n是否替换现有装备 %s :","成功获取装备：%s","很遗憾，您错过了装备：%s")
    elif 13<= type <15:
        object=randomItem(enemies)
        if object == None:
            win(player,"全部敌人被您消灭，恭喜您提前吃鸡！")
            sys.exit()
        chooseFight(player,object,"！！！前方发现一个敌人！！！\n%s\n%s\n是否要战斗 %s :","成功打败敌人『%s』","很遗憾，您被『%s』干掉了！")
    else :
        input("跑了这么久啥都没看到，我来错片场了吗？")
    index=index+player.run()
    if index > block.range :
        index=block.range
    print("您当前的位置%d/%d"%(index,block.range))
win(player,"您真是跑毒高手啊，其它人都被毒死了，恭喜您吃鸡！")

