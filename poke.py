import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Randomon")

dracula_img = pygame.image.load('dracula.png')
dracula = pygame.transform.scale(dracula_img, (250, 250))
dracula_flipped = pygame.transform.flip(dracula, True, False) 

spino_img = pygame.image.load('spino.png')
spino = pygame.transform.scale(spino_img, (250, 250))
spino_flipped = pygame.transform.flip(spino, True, False)  

nether_img = pygame.image.load('nether.png')
nether_flipped = pygame.transform.scale(nether_img, (250, 250))
nether = pygame.transform.flip(nether_flipped, True, False)

j_img = pygame.image.load('jmoney.png')
j = pygame.transform.scale(j_img, (250, 250))
j_flipped = pygame.transform.flip(j, True, False)

adv_img = pygame.image.load('adv.png')
adv = pygame.transform.scale(adv_img, (250, 250))
adv_flipped = pygame.transform.flip(adv, True, False)

fire_img = pygame.image.load('fireball.png')
fire = pygame.transform.scale(fire_img, (100, 100))
fire_flipped = pygame.transform.flip(fire, True, False)

WHITE = (55, 55, 55)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

particles = []

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
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))


class Monster:    
    def __init__(self, health, attack, defense, speed, name, x, y, width, height, image, flipped_image):
        self.health = health
        self.attack = attack
        self._current_health = health
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
        self.status_effects = {}
        self.cooldown1 = 0
        self.cooldown2 = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self._current_health = max(0, self._current_health - actual_damage)
        if self._current_health == 0:
            self.alive = False
        return actual_damage

    def heal(self, amount):
        self._current_health = min(self.max_health, self._current_health + amount)

    def basic_attack(self, target):
        damage = target.take_damage(self.attack)
        for i in range(100):
            particles.append(Particle(self.x + 10 * i, self.y - 25, RED, (random.uniform(-10,10), random.uniform(-10,10)), 30))
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
        for i in range(len(self.status_effects)):
            self.status_effects[i] -= 1

class Dracula(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 50, "Dracula", x, y, 50, 50, dracula, dracula_flipped)
        self.name3 = "Vampiric Bite"
        self.name4 = "Blood Drain"

    def special_attack1(self, target):
        damage = target.take_damage(self.attack * 2)
        self.heal(damage // 2)
        self.cooldown1 = 2
        return f"{self.name} uses Vampiric Bite on {target.name} for {damage} damage and heals for {damage//2} health!"
    

    def special_attack2(self, target):
        damage = target.take_damage(self.attack * 3 + random.randint(1, 10))
        target.defense = max(0, target.defense - 6)
        self.cooldown2 = 2
        return f"{self.name} uses Blood Drain on {target.name} for {damage} damage and lowers their defense by 6!"

class Spinosaurus(Monster):
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
        return f"{self.name} uses Crippling Tail Whip on {target.name} for {damage} damage and lowers their speed by 12!"

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
        timer69 = 0
        x = self.x
        y = self.y
        while timer69 < 1000:
            if timer69%5 == 0:
                screen.blit(fire, (x, y))
                x += 10
            timer69 += 1
        return f"{self.name} uses Divine Smite on {target.name} for {damage - target.defense} damage, ignoring all defense!"

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
        return f"{self.name} uses Molotov Bottle on {target.name} for {damage} damage!"

    def special_attack2(self, target):
        damage = random.randint(1, 20)
        if damage > 10:
            damage = damage * 3
            target.take_damage(damage)
            return f"{self.name} uses Ambush on {target.name} for {damage} damage and preforms a critical hit!"
        else:
            damage = damage * 3
            self.take_damage(damage)
            return f"{self.name} uses Ambush on {target.name} but it fails and damages itself for {damage} damage!"

def message_display(message_log, font):
    log_y = 400
    for i, message in enumerate(message_log[-5:]): 
        message_text = font.render(message, True, (205,205,205))
        screen.blit(message_text, (250, log_y + i * 20))

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
        if action == "attack":
            result = char.basic_attack(enemy_monster)
            message_log.append(result)
        elif action == "special_01":
            result = char.special_attack1(enemy_monster)
            message_log.append(result)
        elif action == "special_02":
            result = char.special_attack2(enemy_monster)
            message_log.append(result)
    char.cooldown1 -= 1
    char.cooldown2 -= 1
    enemy_monster.cooldown1 -= 1
    enemy_monster.cooldown2 -= 1
    return message_log

def game_loop(state):
    game_State = state
    running = True
    executed = False
    curr = False
    idle_counter = 0
    row = 0
    timer3 = 0
    message_log = []
    timer = 0
    global particles
    font = pygame.font.SysFont(None, 24)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if game_State == "Menu" and not executed:
            screen.fill(WHITE)
            message_log.append("Choose your fighter to begin!")
            pygame.draw.rect(screen, GREEN, (50, 700, 200, 150))
            draw_text("Spinosaurus", RED, 50, 700, 24, center=False)
            pygame.draw.rect(screen, RED, (500, 700, 200, 150))
            txt2 = random.choice(["Adventurer", "Dracula"])
            draw_text(txt2, BLUE, 500, 700, 24, center=False)
            pygame.draw.rect(screen, BLUE, (1000, 700, 200, 150))
            txt1 = random.choice(["Cleric", "Neanderthal"])
            draw_text(txt1, YELLOW, 1000, 700, 24, center=False)
            button_1_select = pygame.Rect(50, 700, 200, 150)
            button_2_select = pygame.Rect(500, 700, 200, 150)
            button_3_select = pygame.Rect(1000, 700, 200, 150)
            executed = True
            pygame.display.update()
        if game_State == "Menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_1_select.collidepoint(mouse_pos):
                    char = Spinosaurus(200, 150)
                    game_State = "Battle"
                    executed = False
                elif button_2_select.collidepoint(mouse_pos):
                    if txt2 == "Adventurer":
                        char = Adventurer(200, 150)
                    elif txt2 == "Dracula":
                        char = Dracula(200, 150)
                    game_State = "Battle"
                    executed = False
                elif button_3_select.collidepoint(mouse_pos):
                    if txt1 == "Cleric":
                        char = Cleric(200, 150)
                    elif txt1 == "Neanderthal":
                        char = Neanderthal(200, 150)
                    game_State = "Battle"
                    executed = False
                enemy_monster = random.choice([Neanderthal(1000,150), Spinosaurus(1000,150), Dracula(1000,150), Cleric(1000,150), Adventurer(1000,150)])
        if game_State == "Battle" and not executed:
            screen.fill(WHITE)
            message_log.append(f"You chose {char.name}!")
            message_log.append(f"You are fighting {enemy_monster.name}")
            executed = True
            pygame.draw.rect(screen, GREEN, (50, 700, 200, 150))
            draw_text("Basic Attack", RED, 50, 700, 24, center=False)
            pygame.draw.rect(screen, RED, (500, 700, 200, 150))
            draw_text(char.name3, BLUE, 500, 700, 24, center=False)
            pygame.draw.rect(screen, BLUE, (1000, 700, 200, 150))
            draw_text(char.name4, YELLOW, 1000, 700, 24, center=False)
            char.draw(screen, flip=False)  
            enemy_monster.draw(screen, flip=True)  
        if game_State == "Battle":
            if char.alive and enemy_monster.alive and timer > 100:
                if event.type == pygame.MOUSEBUTTONDOWN:
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
            pygame.draw.rect(screen, (55, 55, 55), (150, 400, 900, 300))
            pygame.draw.rect(screen, (55,55,55), (50, 0, 160, 400))
            if timer3%10 == 0:
                pygame.draw.rect(screen, (55,55,55), (char.x, char.y-100, 1000, 500))
                pygame.draw.rect(screen, (55,55,55), (enemy_monster.x, enemy_monster.y-100, 1000, 500))
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
            stats.append(f"Player health: {char._current_health}")
            stats.append(f"Enemy health: {enemy_monster._current_health}")
            stats.append(f"Player attack: {char.attack}")
            stats.append(f"Player defense: {char.defense}")
            stats.append(f"Player speed: {char.speed}")
            stats.append(f"Enemy attack: {enemy_monster.attack}")
            stats.append(f"Enemy defense: {enemy_monster.defense}")
            stats.append(f"Enemy speed: {enemy_monster.speed}")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_i]:
                for i, message in enumerate(stats[-8:]): 
                    message_text = font.render(message, True, (205,205,205))
                    screen.blit(message_text, (50, 0 + i * 20))
            timer += 1
            timer3 += 1
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    game_loop("Menu")