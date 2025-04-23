import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Randomon")
clock = pygame.time.Clock()

def load_image(name, size=(250, 250)):
    img = pygame.image.load(f'{name}.png')
    return pygame.transform.scale(img, size)

dracula = load_image('dracula')
dracula_flipped = pygame.transform.flip(dracula, True, False)
spino = load_image('spino')
spino_flipped = pygame.transform.flip(spino, True, False)
nether = load_image('nether')
nether_flipped = pygame.transform.flip(nether, True, False)
j = load_image('jmoney')
j_flipped = pygame.transform.flip(j, True, False)
adv = load_image('adv')
adv_flipped = pygame.transform.flip(adv, True, False)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

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
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 60
        self.alpha = 255

    def update(self):
        self.lifetime -= 1
        self.y -= 0.5
        self.alpha = max(0, self.alpha - 4)

    def draw(self, surface):
        font = pygame.font.SysFont('Arial', 24)
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        surface.blit(text_surface, (self.x, self.y))

class Monster:
    def __init__(self, health, attack, defense, speed, name, x, y, image, flipped_image):
        self.max_health = health
        self._current_health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.name = name
        self.alive = True
        self.x = x
        self.y = y
        self.image = image
        self.flipped_image = flipped_image
        self.status_effects = {}
        self.buffs = {'attack': 0, 'defense': 0}
        self.animation_offset = 0
        self.animation_dir = 1
        self.attack_anim = 0
        self.hit_flash = 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - (self.defense + self.buffs['defense']))
        self._current_health -= actual_damage
        self.hit_flash = 5
        if self._current_health <= 0:
            self.alive = False
        return actual_damage

    def basic_attack(self, target):
        damage = self.attack + self.buffs['attack']
        actual_damage = target.take_damage(damage)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, (200, 200, 200), 
                    (random.uniform(-2, 2), random.uniform(-2, 2)), 15) for _ in range(10)]
        return f"{self.name} attacks {target.name} for {actual_damage} damage!", particles

    def heal(self, amount):
        self._current_health = min(self.max_health, self._current_health + amount)

    def apply_status(self, effect, damage, turns):
        self.status_effects[effect] = {'damage': damage, 'turns': turns}

    def process_status(self):
        results = []
        for effect, data in list(self.status_effects.items()):
            self._current_health -= data['damage']
            data['turns'] -= 1
            results.append(f"{self.name} takes {data['damage']} from {effect}!")
            if data['turns'] <= 0:
                del self.status_effects[effect]
        return results

    def update_animation(self):
        if self.attack_anim <= 0:
            self.animation_offset += 0.2 * self.animation_dir
            if abs(self.animation_offset) > 3:
                self.animation_dir *= -1
        else:
            self.attack_anim -= 1
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def trigger_attack_anim(self):
        self.attack_anim = 10

    def draw(self, surface, flip=False):
        y_pos = self.y + self.animation_offset
        if self.attack_anim > 0:
            y_pos -= 5 + self.attack_anim
        img = self.flipped_image if flip else self.image
        if self.hit_flash > 0:
            flash_surf = img.copy()
            flash_surf.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(flash_surf, (self.x, y_pos))
        else:
            surface.blit(img, (self.x, y_pos))
        self.draw_health_bar(surface, self.x, y_pos - 20)
        self.draw_status_effects(surface, self.x, y_pos - 40)

    def draw_health_bar(self, surface, x, y):
        ratio = self._current_health / self.max_health
        pygame.draw.rect(surface, RED, (x, y, 100, 10))
        pygame.draw.rect(surface, GREEN, (x, y, 100 * ratio, 10))

    def draw_status_effects(self, surface, x, y):
        for i, effect in enumerate(self.status_effects):
            color = RED if effect == "poison" else ORANGE
            pygame.draw.circle(surface, color, (x + 20 + i * 15, y), 5)

class Dracula(Monster):
    def __init__(self, x, y):
        super().__init__(100, 10, 5, 50, "Dracula", x, y, dracula, dracula_flipped)
        self.name3 = "Vampiric Bite"
        self.name4 = "Blood Drain"

    def special_attack1(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 2)
        self.heal(damage // 2)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, RED, 
                    (random.uniform(-3, 3), random.uniform(-3, 3)), 30) for _ in range(20)]
        return f"{self.name} uses Vampiric Bite on {target.name} for {damage} damage!", particles

    def special_attack2(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 3)
        target.defense = max(0, target.defense - 3)
        target.apply_status("poison", 2, 3)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, PURPLE, 
                    (random.uniform(-2, 2), random.uniform(-2, 2)), 40) for _ in range(15)]
        return f"{self.name} uses Blood Drain! {target.name} loses 3 defense and is poisoned!", particles

class Spinosaurus(Monster):
    def __init__(self, x, y):
        super().__init__(100, 12, 8, 45, "Spinosaurus", x, y, spino, spino_flipped)
        self.name3 = "Tail Whip"
        self.name4 = "Regenerate"

    def special_attack1(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 1.5)
        target.speed = max(0, target.speed - 5)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, (200, 200, 100), 
                    (random.uniform(-2, 2), random.uniform(-2, 2)), 25) for _ in range(15)]
        return f"{self.name} whips {target.name} for {damage} damage and lowers speed!", particles

    def special_attack2(self, target):
        heal_amount = self.attack * 2
        self.heal(heal_amount)
        self.defense += 2
        self.trigger_attack_anim()
        particles = [Particle(self.x + 125, self.y + 125, GREEN, 
                    (random.uniform(-1, 1), random.uniform(-1, 1)), 40) for _ in range(20)]
        return f"{self.name} regenerates {heal_amount} HP and gains 2 defense!", particles

class Neanderthal(Monster):
    def __init__(self, x, y):
        super().__init__(120, 15, 10, 30, "Neanderthal", x, y, nether, nether_flipped)
        self.name3 = "Bash"
        self.name4 = "Enrage"

    def special_attack1(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 2.5)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, ORANGE, 
                    (random.uniform(-4, 4), random.uniform(-4, 4)), 20) for _ in range(25)]
        return f"{self.name} bashes {target.name} for {damage} damage!", particles

    def special_attack2(self, target):
        self.buffs['attack'] += 5
        self.trigger_attack_anim()
        particles = [Particle(self.x + 125, self.y + 125, (255, 100, 100), 
                    (random.uniform(-1, 1), random.uniform(-1, 1)), 50) for _ in range(15)]
        return f"{self.name} enrages! Attack increased by 5!", particles

class Cleric(Monster):
    def __init__(self, x, y):
        super().__init__(90, 8, 4, 55, "Cleric", x, y, j, j_flipped)
        self.name3 = "Heal"
        self.name4 = "Smite"

    def special_attack1(self, target):
        heal_amount = self.attack * 3
        self.heal(heal_amount)
        self.trigger_attack_anim()
        particles = [Particle(self.x + 125, self.y + 125, YELLOW, 
                    (random.uniform(-1, 1), random.uniform(-1, 1)), 60) for _ in range(25)]
        return f"{self.name} heals for {heal_amount} HP!", particles

    def special_attack2(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 2 + target.defense)
        target.trigger_attack_anim()
        particles = []
        for i in range(10, 110, 10):
            particles.append(Particle(target.x + 125, target.y + 125 - i, YELLOW, (0, -1), 15))
        return f"{self.name} smites {target.name} for {damage} damage (ignores defense)!", particles

class Adventurer(Monster):
    def __init__(self, x, y):
        super().__init__(85, 18, 3, 60, "Adventurer", x, y, adv, adv_flipped)
        self.name3 = "Quick Strike"
        self.name4 = "Lucky Crit"

    def special_attack1(self, target):
        damage = target.take_damage((self.attack + self.buffs['attack']) * 1.2)
        target.trigger_attack_anim()
        particles = [Particle(target.x + 125, target.y + 125, PURPLE, 
                    (random.uniform(-5, 5), random.uniform(-5, 5)), 15) for _ in range(10)]
        return f"{self.name} quickly strikes {target.name} for {damage} damage!", particles

    def special_attack2(self, target):
        crit_chance = random.random()
        if crit_chance > 0.7:
            damage = target.take_damage((self.attack + self.buffs['attack']) * 3)
            target.trigger_attack_anim()
            particles = [Particle(target.x + 125, target.y + 125, (255, 215, 0), 
                        (random.uniform(-6, 6), random.uniform(-6, 6)), 20) for _ in range(30)]
            return f"CRITICAL HIT! {self.name} deals {damage} damage!", particles
        else:
            damage = target.take_damage((self.attack + self.buffs['attack']) * 1.5)
            target.trigger_attack_anim()
            particles = [Particle(target.x + 125, target.y + 125, PURPLE, 
                        (random.uniform(-3, 3), random.uniform(-3, 3)), 15) for _ in range(10)]
            return f"{self.name} attacks {target.name} for {damage} damage!", particles

class BattleSystem:
    def __init__(self):
        self.message_log = []
        self.particles = []
        self.floating_texts = []
        self.screen_shake = 0
        self.shake_offset = [0, 0]
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 32)
        self.state = "menu"
        self.player = None
        self.enemy = None
        self.turn_in_progress = False
        self.turn_timer = 0
        self.current_action = None

    def start_battle(self, player_class, enemy_class):
        self.player = player_class(200, 150)
        self.enemy = enemy_class(1000, 150)
        self.state = "battle"
        self.message_log = [
            f"A wild {self.enemy.name} appears!",
            f"Go {self.player.name}!"
        ]

    def process_turn(self, action):
        if self.turn_in_progress:
            return

        self.turn_in_progress = True
        self.turn_timer = 0
        self.current_action = action

        if action == "attack":
            result = self.player.basic_attack(self.enemy)
            self.message_log.append(result)
        elif action == "special1":
            result, particles = self.player.special_attack1(self.enemy)
            self.message_log.append(result)
            self.particles.extend(particles)
        elif action == "special2":
            result, particles = self.player.special_attack2(self.enemy)
            self.message_log.append(result)
            self.particles.extend(particles)
            if "CRITICAL" in result:
                self.screen_shake = 10

        if self.enemy.alive:
            enemy_move = self.choose_enemy_move()
            if enemy_move == "attack":
                result = self.enemy.basic_attack(self.player)
                self.message_log.append(result)
            elif enemy_move == "special1":
                result, particles = self.enemy.special_attack1(self.player)
                self.message_log.append(result)
                self.particles.extend(particles)
            elif enemy_move == "special2":
                result, particles = self.enemy.special_attack2(self.player)
                self.message_log.append(result)
                self.particles.extend(particles)

        status_results = self.player.process_status()
        self.message_log.extend(status_results)
        status_results = self.enemy.process_status()
        self.message_log.extend(status_results)

    def choose_enemy_move(self):
        if self.enemy._current_health < self.enemy.max_health * 0.3 and hasattr(self.enemy, 'special_attack1') and "Heal" in self.enemy.name3:
            return "special1"
        
        moves = []
        weights = []
        
        moves.append("attack")
        weights.append(40)
        
        if hasattr(self.enemy, 'special_attack1'):
            moves.append("special1")
            weight = 30
            if "Heal" in self.enemy.name3 and self.enemy._current_health < self.enemy.max_health * 0.6:
                weight = 60
            weights.append(weight)
        
        if hasattr(self.enemy, 'special_attack2'):
            moves.append("special2")
            weight = 30
            if "Bash" in self.enemy.name4 or "Smite" in self.enemy.name4:
                weight = 50
            weights.append(weight)
        
        total = sum(weights)
        weights = [w/total for w in weights]
        
        rand = random.random()
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand <= cumulative:
                return moves[i]
        return "attack"

    def update(self):
        if self.player:
            self.player.update_animation()
        if self.enemy:
            self.enemy.update_animation()

        for particle in self.particles[:]:
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

        for text in self.floating_texts[:]:
            text.update()
            if text.lifetime <= 0:
                self.floating_texts.remove(text)

        if self.screen_shake > 0:
            self.shake_offset = [random.randint(-5, 5), random.randint(-5, 5)]
            self.screen_shake -= 1
        else:
            self.shake_offset = [0, 0]

        if self.turn_in_progress:
            self.turn_timer += 1
            if self.turn_timer > 60:
                self.turn_in_progress = False
                self.current_action = None

                if not self.player.alive:
                    self.message_log.append(f"{self.player.name} was defeated!")
                    self.state = "game_over"
                elif not self.enemy.alive:
                    self.message_log.append(f"{self.enemy.name} was defeated!")
                    self.state = "victory"

    def draw(self, screen):
        screen.fill(BLACK)
        offset_surface = pygame.Surface((WIDTH, HEIGHT))
        offset_surface.fill(BLACK)

        if self.player:
            self.player.draw(offset_surface, flip=False)
        if self.enemy:
            self.enemy.draw(offset_surface, flip=True)

        for particle in self.particles:
            particle.draw(offset_surface)

        for text in self.floating_texts:
            text.draw(offset_surface)

        self.draw_ui(offset_surface)
        screen.blit(offset_surface, self.shake_offset)

    def draw_ui(self, surface):
        pygame.draw.rect(surface, (30, 30, 30), (50, 700, 1400, 250))
        for i, message in enumerate(self.message_log[-4:]):
            try:
                text = self.font.render(message, True, WHITE)
                surface.blit(text, (70, 720 + i * 30))
            except:
                pass

        if self.state == "battle" and not self.turn_in_progress:
            pygame.draw.rect(surface, BLUE, (50, 600, 200, 80))
            text = self.font.render("Attack", True, WHITE)
            surface.blit(text, (150 - text.get_width()//2, 640 - text.get_height()//2))

            if hasattr(self.player, 'special_attack1'):
                pygame.draw.rect(surface, GREEN, (300, 600, 200, 80))
                text = self.font.render(self.player.name3, True, WHITE)
                surface.blit(text, (400 - text.get_width()//2, 640 - text.get_height()//2))

            if hasattr(self.player, 'special_attack2'):
                pygame.draw.rect(surface, RED, (550, 600, 200, 80))
                text = self.font.render(self.player.name4, True, WHITE)
                surface.blit(text, (650 - text.get_width()//2, 640 - text.get_height()//2))

        elif self.state == "menu":
            text = self.big_font.render("Choose Your Fighter", True, WHITE)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, 100))

            pygame.draw.rect(surface, BLUE, (200, 300, 200, 200))
            text = self.font.render("Dracula", True, WHITE)
            surface.blit(text, (300 - text.get_width()//2, 400 - text.get_height()//2))

            pygame.draw.rect(surface, GREEN, (500, 300, 200, 200))
            text = self.font.render("Spinosaurus", True, WHITE)
            surface.blit(text, (600 - text.get_width()//2, 400 - text.get_height()//2))

            pygame.draw.rect(surface, RED, (800, 300, 200, 200))
            text = self.font.render("Neanderthal", True, WHITE)
            surface.blit(text, (900 - text.get_width()//2, 400 - text.get_height()//2))

            pygame.draw.rect(surface, YELLOW, (1100, 300, 200, 200))
            text = self.font.render("Cleric", True, WHITE)
            surface.blit(text, (1200 - text.get_width()//2, 400 - text.get_height()//2))

        elif self.state == "game_over":
            text = self.big_font.render("Game Over", True, RED)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

            text = self.font.render("Press R to restart", True, WHITE)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))

        elif self.state == "victory":
            text = self.big_font.render("Victory!", True, GREEN)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))

            text = self.font.render("Press R to restart", True, WHITE)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))

    def handle_click(self, pos):
        if self.state == "menu":
            if 200 <= pos[0] <= 400 and 300 <= pos[1] <= 500:
                self.start_battle(Dracula, random.choice([Spinosaurus, Neanderthal, Cleric, Adventurer]))
            elif 500 <= pos[0] <= 700 and 300 <= pos[1] <= 500:
                self.start_battle(Spinosaurus, random.choice([Dracula, Neanderthal, Cleric, Adventurer]))
            elif 800 <= pos[0] <= 1000 and 300 <= pos[1] <= 500:
                self.start_battle(Neanderthal, random.choice([Dracula, Spinosaurus, Cleric, Adventurer]))
            elif 1100 <= pos[0] <= 1300 and 300 <= pos[1] <= 500:
                self.start_battle(Cleric, random.choice([Dracula, Spinosaurus, Neanderthal, Adventurer]))

        elif self.state == "battle" and not self.turn_in_progress:
            if 50 <= pos[0] <= 250 and 600 <= pos[1] <= 680:
                self.process_turn("attack")
            elif hasattr(self.player, 'special_attack1') and 300 <= pos[0] <= 500 and 600 <= pos[1] <= 680:
                self.process_turn("special1")
            elif hasattr(self.player, 'special_attack2') and 550 <= pos[0] <= 750 and 600 <= pos[1] <= 680:
                self.process_turn("special2")

def main():
    battle_system = BattleSystem()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                battle_system.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and battle_system.state in ("game_over", "victory"):
                    battle_system = BattleSystem()

        battle_system.update()
        battle_system.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()