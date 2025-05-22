import pygame
import random # library imports
import sys # for checking byte size of objects for data dictionary
from pygame import gfxdraw
pygame.init() # pygame initialisation
pygame.mixer.init()

WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # more pygame initialisation
pygame.display.set_caption("Sigil Wars")
clock = pygame.time.Clock()

background = pygame.image.load('background02.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
message_log = [] # list to store messages
particles = [] # list to store particles
container = pygame.image.load('cont.png') # container image for title screen
container = pygame.transform.scale(container, (350, 400))
glass = pygame.image.load('glass.png') # glass image for title screen
glass = pygame.transform.scale(glass, (325, 300))
lid = pygame.image.load('lid.png') # lid image for title screen
lid = pygame.transform.scale(lid, (325, 100))
# note for the classes there are flipped and non-flipped images as you want a flipped image when the character is facing left and a non-flipped image when the character is facing right
dracula = pygame.image.load('dracula.png') # dracula image
dracula = pygame.transform.scale(dracula, (250, 250))
dracula_flipped = pygame.transform.flip(dracula, True, False) 
spino = pygame.image.load('spino.png') # spino image
spino = pygame.transform.scale(spino, (250, 250))
spino_flipped = pygame.transform.flip(spino, True, False)  
nether = pygame.image.load('nether.png') # neanderthal image
nether_flipped = pygame.transform.scale(nether, (250, 250))
nether = pygame.transform.flip(nether_flipped, True, False)
j = pygame.image.load('jmoney.png') # cleric image
j = pygame.transform.scale(j, (250, 250))
j_flipped = pygame.transform.flip(j, True, False)
adv = pygame.image.load('adv.png') # adventurer image
adv = pygame.transform.scale(adv, (250, 250))
adv_flipped = pygame.transform.flip(adv, True, False)
witch = pygame.image.load('witch.png') # witch image
witch = pygame.transform.scale(witch, (250, 250))
witch_flipped = pygame.transform.flip(witch, True, False)
health = pygame.image.load('health.png') # health icon image
health = pygame.transform.scale(health, (200, 150))
attack = pygame.image.load('attack.png') # attack icon image
attack = pygame.transform.scale(attack, (200, 150))
speed = pygame.image.load('speed.png') # speed icon image
speed = pygame.transform.scale(speed, (200, 150))
background_image = pygame.image.load("arena.png").convert() # background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
scoreboard_imag = pygame.image.load("scoreboard.png").convert_alpha() # had some transparency issues so using convert_alpha here and henceforth
scoreboard_image = pygame.transform.scale(scoreboard_imag, (975, 300))
icon1_image = pygame.image.load('icon1.png').convert_alpha() # attack icon 1
icon1_image = pygame.transform.scale(icon1_image, (150, 150))
icon2_image = pygame.image.load('icon2.png').convert_alpha() # attack icon 2
icon2_image = pygame.transform.scale(icon2_image, (150, 150))
icon3_image = pygame.image.load('icon3.png').convert_alpha() # attack icon 3
icon3_image = pygame.transform.scale(icon3_image, (150, 150))
GREYISH = (55, 55, 55) # colours
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
not_orange = (0, 90, 255)

class Particle: 
    def __init__(self, x, y, color, velocity, lifespan):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.lifespan = lifespan
        self.size = random.randint(2, 5)
    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifespan -= 1
        self.size = max(0, self.size - 0.05)
    def draw(self, surface):
        if self.lifespan > 0:
            gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.size), (*self.color, min(255, self.lifespan*6)))

class Monster:    
    def __init__(self, health, attack, defense, speed, name, x, y, width, height, image, flipped_image):
        self.attack = attack
        self.current_health = health
        self.max_health = health
        self.defense = defense
        self.speed = speed
        self.name = name
        self.alive = True
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.name1 = "Special_01"
        self.name2 = "Special_02"
        self.image = image
        self.flipped_image = flipped_image
        self.poison = 0
        self.stun = 0
        self.cooldown1 = 0
        self.cooldown2 = 0
        self.personality = random.randint(0,1) # 0 = aggressive, 1 = defensive

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def take_damage(self, damage):
        critical_hit = random.randint(1, 5)
        if critical_hit >= 4:
            message_log.append(f"{self.name} has been critically hit!")
        actual_damage = max(1, damage - self.defense + critical_hit)
        self.current_health = max(0, self.current_health - actual_damage)
        if self.current_health == 0:
            self.alive = False
        if critical_hit >= 4:
            for i in range(75):
                particles.append(Particle(self.x + 125, self.y + 125, YELLOW, (random.uniform(-3,3), random.uniform(-3,3)), 50))
                particles.append(Particle(self.x + 125, self.y + 125, RED, (random.uniform(-3,3), random.uniform(-3,3)), 50))
                #add sound here on critical hit
        else:
            for i in range(75):
                particles.append(Particle(self.x + 125, self.y + 125, RED, (random.uniform(-3,3), random.uniform(-3,3)), 50))
        return actual_damage

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def basic_attack(self, target):
        damage = target.take_damage(self.attack)
        target.update()
        return f"{self.name} attacks {target.name} for {damage} damage!"
    
    def special_attack1(self, target):
        pass 

    def special_attack2(self, target):
        pass

    def draw(self, surface, flip=False):
        if flip:
            surface.blit(self.flipped_image, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))
    
    def update(self):
        self.poison = max(0, self.poison - 1)
        if self.poison > 0:
            self.take_damage(5+self.defense)
            message_log.append(f"{self.name} is poisoned and takes 5 damage!")
        self.stun = max(0, self.stun - 1)
        if self.stun > 0:
            self.attack = max(1, self.attack - 2)
            self.cooldown1 += 2
            self.cooldown2 += 2
            message_log.append(f"{self.name} is stunned and cannot attack!")

class Dracula(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 50, "Dracula", x, y, 50, 50, dracula, dracula_flipped)
        self.name3 = "Vampiric Bite"
        self.name4 = "Blood Drain"

    def special_attack1(self, target):
        damage = target.take_damage(self.attack * 2)
        self.heal(damage // 2)
        self.cooldown1 = 2
        return f"{self.name} uses Vampiric Bite for {damage} damage and heals for {damage//2} health!"
    
    def special_attack2(self, target):
        damage = target.take_damage(self.attack * 3 + random.randint(1, 10))
        target.defense = max(0, target.defense - 6)
        self.cooldown2 = 2
        return f"{self.name} uses Blood Drain for {damage} damage and lowers their defense!"

class Witch(Monster):
    def __init__(self, x, y):
        super().__init__(125, 12, 2, 49, "Witch", x, y, 50, 50, witch_flipped, witch)
        self.name3 = "Poisonous Brew"
        self.name4 = "Stunning Concotion"

    def special_attack1(self, target):
        target.poison += 5
        target.update()
        self.cooldown1 = 2
        return f"{self.name} uses Poisonous Brew on {target.name} which poisons them!"
    
    def special_attack2(self, target):
        target.stun += 5
        self.cooldown2 = 2
        target.update()
        return f"{self.name} uses Stunning Concotion on {target.name} which stuns them!"

class Spinosaurus(Monster): # perhaps add another class to switch out from the spino like all the other classes have
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 51, "Spinosaurus", x, y, 50, 50, spino, spino_flipped)
        self.name3 = "Regenerative Roar"
        self.name4 = "Crippling Tail Whip"

    def special_attack1(self, target):
        damage = self.attack * 2
        self.heal(damage)
        self.cooldown1 = 2
        return f"{self.name} uses Regenerative Roar and heals for {damage} health!"

    def special_attack2(self, target):
        damage = target.take_damage(self.attack * 3 + random.randint(1,20))
        target.speed = max(0, target.speed - 12)
        self.cooldown2 = 2
        return f"{self.name} uses Crippling Tail Whip for {damage} damage and lowers their speed!"

class Neanderthal(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 5, "Neanderthal", x, y, 50, 50, nether, nether_flipped)
        self.name3 = "Mammoth Guard"
        self.name4 = "Primal Rage"

    def special_attack1(self, target):
        self.cooldown1 = 2
        target.take_damage(self.attack * 2)
        return f"{self.name} uses Mammoth Guard on {target.name} and deals {self.attack * 2 - target.defense} damage!"

    def special_attack2(self, target):
        self.cooldown2 = 2
        self.attack += 8
        return f"{self.name} uses Primal Rage on {target.name} and increases its attack by 8"

class Cleric(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 500, "Cleric", x, y, 50, 50, j, j_flipped)
        self.name3 = "Divine Smite"
        self.name4 = "Heavenly Fish"

    def special_attack1(self, target):
        damage = self.attack * 3 + target.defense - random.randint(1,15)
        target.take_damage(damage)
        self.cooldown1 = 2
        return f"{self.name} uses Divine Smite on {target.name} for {damage - target.defense} damage"

    def special_attack2(self, target):
        self.cooldown2 = 2
        self.heal(self.attack * 1.5)
        target.take_damage(self.attack * 1.5)
        return f"{self.name} uses Heavenly Fish on {target.name} and heals for {self.attack * 1.5} health"

class Adventurer(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 10, "Adventurer", x, y, 50, 50, adv, adv_flipped)
        self.name3 = "Molotov Bottle"
        self.name4 = "Ambush"
    
    def special_attack1(self, target):
        self.cooldown1 = 2
        damage = self.attack * 2
        target.take_damage(damage)
        return f"{self.name} uses Molotov on {target.name} for {damage} damage!"

    def special_attack2(self, target):
        damage = random.randint(1, 20)
        if damage > 10:
            damage = damage * 3
            target.take_damage(damage)
            return f"{self.name} uses Ambush on {target.name} for {damage} damage"
        else:
            damage = damage * 3
            self.take_damage(damage)
            return f"{self.name} uses Ambush on {target.name} but it fails and damages itself"

def message_display(message_log, font):
    for i, message in enumerate(message_log[-5:]): 
        screen.blit(font.render(message, True, ORANGE), (550, 650 + i * 20))

def draw_text(msg, color, x, y, size, center=True):
    font = pygame.font.SysFont("Trebuchet MS", size)
    screen_text = font.render(msg, True, color)
    rect = screen_text.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(screen_text, rect)

def Turn(action, enemy_monster, char, message_log):
    global start_ticks, started, wait_time
    if char.speed > enemy_monster.speed:
        if action == "attack":
            result = char.basic_attack(enemy_monster)
            message_log.append(result)
        elif action == "special_01":
            result = char.special_attack1(enemy_monster)
            message_log.append(result)
        elif action == "special_02":
            result = char.special_attack2(enemy_monster)
            message_log.append(result)

        if enemy_monster.alive == True:
            if enemy_monster.cooldown1 <= 0:
                enemy_attack = enemy_monster.special_attack1
            elif enemy_monster.cooldown2 <= 0:
                enemy_attack = enemy_monster.special_attack2
            else:
                enemy_attack = enemy_monster.basic_attack
            result = enemy_attack(char)
            message_log.append(result)
    else:
        if enemy_monster.cooldown1 <= 0:
            enemy_attack = enemy_monster.special_attack1
        elif enemy_monster.cooldown2 <= 0:
            enemy_attack = enemy_monster.special_attack2
        else:
            enemy_attack = enemy_monster.basic_attack
        result = enemy_attack(char)
        message_log.append(result)
        if char.alive == True:
            if action == "attack":
                result = char.basic_attack(enemy_monster)
                message_log.append(result)
            elif action == "special_01":
                result = char.special_attack1(enemy_monster)
                message_log.append(result)
            elif action == "special_02":
                result = char.special_attack2(enemy_monster)
                message_log.append(result)
    char.cooldown1 = max(char.cooldown1 - 1, 0)
    char.cooldown2 = max(char.cooldown2 - 1, 0)
    enemy_monster.cooldown1 = max(enemy_monster.cooldown1 - 1, 0)
    enemy_monster.cooldown2 = max(enemy_monster.cooldown2 - 1, 0)
    return message_log

def game_loop(state):
    game_State = state
    running = True
    executed = False
    scaling = 1
    curr = False # current direction stored as a bool, i.e. up/down, true/false
    idle_counter = 0 #amount of frames the character has been going in a certain direction within the idle animation
    row = 0
    global message_log
    #message_log = []
    timer = 0
    global particles
    font = pygame.font.SysFont(None, 24)
    try:
        with open("highscore.txt", "r") as file:
            highscore = int(file.read().strip())
    except FileNotFoundError:
        highscore = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_State == "Menu" and not executed:
            screen.fill(not_orange)
            draw_text('Welcome to Sigil Wars', ORANGE, 725, 100, 64)
            draw_text('Choose your character!', ORANGE, 725, 175, 48)
            draw_text('If you ever need more (i)nformation press i', ORANGE, 725, 230, 24)
            screen.blit(container, (50, 450))
            screen.blit(container, (500, 450))
            screen.blit(container, (1000, 450))
            txt3 = random.choice(["Spinosaurus", "Witch"])
            draw_text(txt3, RED, 150, 350, 24, center=False)
            if txt3 == "Spinosaurus":
                screen.blit(spino, (100, 580))
            else:
                screen.blit(witch, (100, 580))
            txt2 = random.choice(["Adventurer", "Dracula"])
            draw_text(txt2, GREEN, 600, 350, 24, center=False)
            if txt2 == "Adventurer":
                screen.blit(adv, (550, 580))
            else:
                screen.blit(dracula, (550, 580))
            txt1 = random.choice(["Cleric", "Neanderthal"])
            if txt1 == "Cleric":
                screen.blit(j, (1050, 580))
            else:
                screen.blit(nether, (1050, 580))
            draw_text(txt1, YELLOW, 1100, 350, 24, center=False)
            button_1_select = pygame.Rect(50, 450, 350, 400)
            button_2_select = pygame.Rect(500, 450, 350, 400)
            button_3_select = pygame.Rect(1000, 450, 350, 400)
            executed = True
            timer = 0
        if game_State == "Menu":
            timer += 1
            mouse_pos = pygame.mouse.get_pos()
            if button_1_select.collidepoint(mouse_pos):
                pygame.draw.rect(screen, not_orange, (50, 450, 350, 550))
                screen.blit(glass, (60, 550))
                screen.blit(lid, (60, 400))
                if txt3 == "Spinosaurus":
                    screen.blit(spino, (100, 580))
                else:
                    screen.blit(witch, (100, 580))
            elif button_2_select.collidepoint(mouse_pos):
                pygame.draw.rect(screen, not_orange, (500, 450, 350, 550))
                screen.blit(glass, (510, 550))
                screen.blit(lid, (510, 400))
                if txt2 == "Adventurer":
                    screen.blit(adv, (550, 580))
                else:
                    screen.blit(dracula, (550, 580))
            elif button_3_select.collidepoint(mouse_pos):
                pygame.draw.rect(screen, not_orange, (1000, 450, 350, 550))
                screen.blit(glass, (1010, 550))
                screen.blit(lid, (1010, 400))
                if txt1 == "Cleric":
                    screen.blit(j, (1050, 580))
                else:
                    screen.blit(nether, (1050, 580))
            else:
                pygame.draw.rect(screen, not_orange, (50, 350, 350, 550))
                screen.blit(container, (50, 450))
                pygame.draw.rect(screen, not_orange, (1000, 350, 350, 550))
                pygame.draw.rect(screen, not_orange, (500, 350, 350, 550))
                screen.blit(container, (500, 450))
                screen.blit(container, (1000, 450))
                draw_text(txt3, RED, 150, 350, 24, center=False)
                draw_text(txt2, GREEN, 600, 350, 24, center=False)
                draw_text(txt1, YELLOW, 1100, 350, 24, center=False)
                if txt1 == "Cleric":
                    screen.blit(j, (1050, 580))
                else:
                    screen.blit(nether, (1050, 580))
                if txt2 == "Adventurer":
                    screen.blit(adv, (550, 580))
                else:
                    screen.blit(dracula, (550, 580))
                if txt3 == "Spinosaurus":
                    screen.blit(spino, (100, 580))
                else:
                    screen.blit(witch, (100, 580))
            if event.type == pygame.MOUSEBUTTONDOWN and timer> 100:
                mouse_pos = pygame.mouse.get_pos()
                if button_1_select.collidepoint(mouse_pos):
                    if txt3 == "Spinosaurus":
                        char = Spinosaurus(175, 450)
                    elif txt3 == "Witch":
                        char = Witch(175, 450)
                    game_State = "Battle"
                    executed = False
                elif button_2_select.collidepoint(mouse_pos):
                    if txt2 == "Adventurer":
                        char = Adventurer(175, 450)
                    elif txt2 == "Dracula":
                        char = Dracula(175, 450)
                    game_State = "Battle"
                    executed = False
                elif button_3_select.collidepoint(mouse_pos):
                    if txt1 == "Cleric":
                        char = Cleric(175, 450)
                    elif txt1 == "Neanderthal":
                        char = Neanderthal(175, 450)
                    game_State = "Battle"
                    executed = False
                enemy_monster = random.choice([Neanderthal(1150,450), Spinosaurus(1150,450), Dracula(1150,450), Cleric(1150,450), Adventurer(1150,450), Witch(1150,450)])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:
                draw_text("!I! Really? Already? It's a menu. Come on, you can do better than that", ORANGE, 412, 50, 24)
            draw_text(f"Highscore: {highscore}", ORANGE, 50, 10, 24, center=False)
        if game_State == "Battle" and not executed:
            screen.fill(GREYISH)
            screen.blit(background_image, (0, 0))
            screen.blit(scoreboard_image, (750, 550))
            message_log.append(f"You chose {char.name}!")
            message_log.append(f"You are fighting {enemy_monster.name}")
            executed = True
        if game_State == "Battle":
            if char.alive:
                screen.blit(background_image, (0, 0))
                screen.blit(scoreboard_image, (275, 550))
                button_1_select = pygame.Rect(0, 650, 200, 150)
                button_2_select = pygame.Rect(0, 350, 200, 150)
                button_3_select = pygame.Rect(0, 50, 200, 150)
                screen.blit(icon1_image, (0, 650))
                screen.blit(icon2_image, (0, 350))
                screen.blit(icon3_image, (0, 50))
                draw_text("Basic Attack", RED, 25, 625, 24, center=False)
                draw_text(char.name3, BLUE, 25, 325, 24, center=False)
                draw_text(char.name4, YELLOW, 25, 25, 24, center=False)
                char.draw(screen, flip=False)  
                enemy_monster.draw(screen, flip=True)  
                if event.type == pygame.MOUSEBUTTONDOWN and timer > 100:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_1_select.collidepoint(mouse_pos):
                        action = "attack"
                        timer = 0
                        Turn(action, enemy_monster, char, message_log)
                    elif button_2_select.collidepoint(mouse_pos):
                        if char.cooldown1 <= 0:
                            action = "special_01"
                            timer = 0
                            Turn(action, enemy_monster, char, message_log)
                        else:
                            message_log.append(f"{char.name3} is on cooldown for {char.cooldown1} turns")
                            timer = 0
                    elif button_3_select.collidepoint(mouse_pos):
                        if char.cooldown2 <= 0:
                            action = "special_02"
                            timer = 0
                            Turn(action, enemy_monster, char, message_log) 
                        else:
                            message_log.append(f"{char.name4} is on cooldown for {char.cooldown2} turns")
                            timer = 0
            print(sys.getsizeof(char))
            if char.alive == False:
                message_log.append(f"Mission failed, we'll get em next time!") # get sound effect for this off youtube
                game_State = "Menu"
                executed = False
            if enemy_monster.alive == False:
                message_log.append(f"{enemy_monster.name} has been slain!")
                upgrade_tokens = random.randint(1, 3)
                message_log.append(f"You have been awarded {upgrade_tokens} upgrade tokens!")
                with open("highscore.txt", "w") as file:
                    file.write(str(highscore))
                game_State = "Upgrade_Menu"
                executed = False

            if timer%10 == 0:
                if row == 12:
                    row = 0
                    if curr == False:
                        curr = True
                    else:
                        curr = False
                    char.draw(screen, flip=False)  
                    enemy_monster.draw(screen, flip=True)  
                else:
                    row += 1
                    if curr == False:
                        char.y -= 1
                        enemy_monster.y += 1
                        idle_counter += 1
                        char.draw(screen, flip=False)  
                        enemy_monster.draw(screen, flip=True)  
                    elif curr == True:
                        char.y += 1
                        enemy_monster.y -= 1
                        idle_counter += 1
                        char.draw(screen, flip=False)  
                        enemy_monster.draw(screen, flip=True)  
            for particle in particles:
                particle.draw(screen)
                particle.update()
            message_display(message_log, font)
            stats = []
            stats.append(f"Player health: {char.current_health}")
            stats.append(f"Enemy health: {enemy_monster.current_health}")
            stats.append(f"Player attack: {char.attack}")
            stats.append(f"Player defense: {char.defense}")
            stats.append(f"Player speed: {char.speed}")
            stats.append(f"Enemy attack: {enemy_monster.attack}")
            stats.append(f"Enemy defense: {enemy_monster.defense}")
            stats.append(f"Enemy speed: {enemy_monster.speed}")
            for i, message in enumerate(stats[-8:]): 
                message_text = font.render(message, True, ORANGE)
                screen.blit(message_text, (1250, 20 + i * 20))
            timer += 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:
                if enemy_monster.name == "Dracula":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a healing ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a render ability with a cooldown of {enemy_monster.cooldown2}!")
                elif enemy_monster.name == "Witch":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a poison ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a stun ability with a cooldown of {enemy_monster.cooldown2}!")
                elif enemy_monster.name == "Spinosaurus":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a healing ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a speed reduction ability with a cooldown of {enemy_monster.cooldown2}!")
                elif enemy_monster.name == "Neanderthal":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a damaging ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a damage buff ability with a cooldown of {enemy_monster.cooldown2}!")
                elif enemy_monster.name == "Cleric":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a damaging ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a healing ability with a cooldown of {enemy_monster.cooldown2}!")
                elif enemy_monster.name == "Adventurer":
                    message_log.clear()
                    message_log.append(f"{enemy_monster.name} has a damaging ability with a cooldown of {enemy_monster.cooldown1}!")
                    message_log.append(f"{enemy_monster.name} has a damaging ability with a cooldown of {enemy_monster.cooldown2}!")
            message_display(message_log, font)
        if game_State == "Upgrade_Menu" and not executed:
            highscore += 1
            screen.fill(GREYISH)
            screen.blit(background_image, (0, 0))
            message_log.append("Choose your upgrade!")
            #pygame.draw.rect(screen, GREEN, (50, 700, 200, 150))
            draw_text("Attack", RED, 50, 700, 24, center=False)
            #pygame.draw.rect(screen, RED, (500, 700, 200, 150))
            draw_text("Defense", BLUE, 500, 700, 24, center=False)
            #pygame.draw.rect(screen, BLUE, (1000, 700, 200, 150))
            draw_text("Speed", YELLOW, 1000, 700, 24, center=False)
            button_1_select = pygame.Rect(50, 700, 200, 150)
            button_2_select = pygame.Rect(500, 700, 200, 150)
            button_3_select = pygame.Rect(1000, 700, 200, 150)
            timer = 0
            executed = True
        if game_State == "Upgrade_Menu":
            screen.fill(GREYISH)
            screen.blit(background, (0, 0))
            draw_text('Choose Thine Upgrades', ORANGE, 750, 100, 64)
            draw_text('You have ' + str(upgrade_tokens) + ' upgrade tokens!', ORANGE, 750, 175, 48)
            if char.name == "Spinosaurus":
                screen.blit(spino, (WIDTH/2 - 150, HEIGHT/2 - 100))
            elif char.name == "Witch":  
                screen.blit(witch, (WIDTH/2 - 150, HEIGHT/2 - 100))
            elif char.name == "Adventurer":
                screen.blit(adv, (WIDTH/2 - 150, HEIGHT/2 - 100))
            elif char.name == "Dracula":
                screen.blit(dracula, (WIDTH/2 - 150, HEIGHT/2 - 100))
            elif char.name == "Cleric":
                screen.blit(j, (WIDTH/2 - 150, HEIGHT/2 - 100))
            elif char.name == "Neanderthal":
                screen.blit(nether, (WIDTH/2 - 150, HEIGHT/2 - 100))
            screen.blit(attack, (50, 700))
            draw_text("Attack", RED, 100, 675, 24, center=False)
            screen.blit(health, (500, 700))
            draw_text("Defense", GREEN, 550, 675, 24, center=False)
            screen.blit(speed, (1000, 700))
            draw_text("Speed", BLUE, 1050, 675, 24, center=False)
            button_1_select = pygame.Rect(50, 700, 200, 150)
            button_2_select = pygame.Rect(500, 700, 200, 150)
            button_3_select = pygame.Rect(1000, 700, 200, 150)
            if event.type == pygame.MOUSEBUTTONDOWN and timer > 100:
                mouse_pos = pygame.mouse.get_pos()
                if button_1_select.collidepoint(mouse_pos):
                    if upgrade_tokens > 0:
                        char.attack += 5
                        char.cooldown1 = 0
                        char.cooldown2 = 0
                        message_log.append(f"{char.name} has gained 5 attack!")
                        upgrade_tokens -= 1
                        timer = 0
                elif button_2_select.collidepoint(mouse_pos):
                    if upgrade_tokens > 0:
                        char.current_health = char.max_health + 5
                        char.max_health += 5
                        char.defense += 5
                        message_log.append(f"{char.name} has gained 5 health and 5 defense!")
                        upgrade_tokens -= 1
                        timer = 0
                elif button_3_select.collidepoint(mouse_pos):
                    if upgrade_tokens > 0:
                        char.speed += 5
                        message_log.append(f"{char.name} has gained 5 speed!")
                        upgrade_tokens -= 1
                        timer = 0
                if upgrade_tokens == 0:
                    message_log.append("You have no more upgrade tokens!")
                    game_State = "Reset_Battle"
                    executed = False
            timer += 1
        if game_State == "Reset_Battle" and not executed:
            scaling += 1
            enemy_monster = random.choice([Neanderthal(1150,450), Spinosaurus(1150,450), Dracula(1150,450), Cleric(1150,450), Adventurer(1150,450), Witch(1150,450)])
            enemy_monster.current_health = enemy_monster.max_health + 5 * scaling
            enemy_monster.max_health += 5 * scaling
            enemy_monster.attack = enemy_monster.attack + 5 * scaling
            enemy_monster.defense = enemy_monster.defense * scaling
            enemy_monster.speed = enemy_monster.speed * scaling
            enemy_monster.alive = True
            game_State = "Battle"
            executed = True
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    game_loop("Menu")


#sounds anyone?