# This is a sample Python script.
import random
import time as Time


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# [X] Making a basic canvas and player
# [X] Moving player
# [X] Player attack
# [] Player enemy interaction
# [] Display improvement
# [] Enemy movement
# [] Make this dynamic

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


class Bullet:
    def __init__(self, position, attack_dir):
        self.current_position = position
        self.direction = attack_dir
        self.bullets = list()

    def update_position(self):
        for bullet in self.bullets:
            bullet.current_position = bullet.current_position - bullet.direction


class Canvas:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.obstacles = set()

    def create_obstacles(self):
        random.seed(128)
        n_obstacles = random.randint(0, self.length * self.width // 3)
        for _ in range(n_obstacles):
            self.obstacles.add((random.randint(1, self.length), random.randint(1, self.width)))

    def display_canvas(self):
        for i in range(0, self.length):
            for j in range(0, self.width):
                if (i, j) not in self.obstacles:
                    print('_', end='')
                else:
                    print('O', end='')
            print()


class Display:
    def __init__(self, canvas, player, spawner):
        self.canvas = canvas
        self.player = player
        self.player_position = self.player.position
        self.spawner = spawner
        self.enemy = spawner.enemies


    def display(self):
        bullet_position = list()
        enemy_position = list()
        l = self.canvas.length
        w = self.canvas.width
        for bullet in self.spawner.bullets:
            bullet_position.append(bullet.current_position)
        for enemy in self.enemy:
            enemy_position.append(enemy.position)
        for i in range(l):
            for j in range(w):
                if (i, j) not in self.canvas.obstacles:
                    if (i, j) in enemy_position:
                        print('.', end='')
                    elif (i, j) == self.player_position:
                        print('#', end='')
                    elif (i, j) in bullet_position:
                        print('-', end='')
                    else:
                        print('_', end='')
                else:
                    print('O', end='')
            print()



class Enemy:
    def __init__(self, position):
        self.position = position

    def update_position(self, position, player_position):
        p_pos = player_position
        

class Player:
    def __init__(self, spawner, canvas):
        self.attack = None
        self.canvas = canvas
        self.health = 100
        self.position = spawner.player
        self.spawner = spawner

    def move_player(self, event):
        move = event
        pos_x, pos_y = self.position
        if move == 'UP' and pos_x - 1 >= 0 and (pos_x - 1, pos_y) not in self.canvas.obstacles:
            self.position = (pos_x - 1, pos_y)
        elif move == 'DOWN' and pos_x + 1 < self.canvas.length and (pos_x + 1, pos_y) not in self.canvas.obstacles:
            self.position = (pos_x + 1, pos_y)
        elif move == 'RIGHT' and pos_y + 1 < self.canvas.width and (pos_x, pos_y + 1) not in self.canvas.obstacles:
            self.position = (pos_x, pos_y + 1)
        elif move == 'LEFT' and pos_y - 1 >= 0 and (pos_x, pos_y - 1) not in self.canvas.obstacles:
            self.position = (pos_x, pos_y - 1)

    def get_direction(self, event):
        if event == 'UP':
            return 1, 0

    def player_attack(self, event):
        attack = event
        init_pos = self.position
        x_pos, y_pos = self.get_direction(attack)
        x_init, y_init = init_pos
        bullet = Bullet((x_init - x_pos, y_init - y_pos), (x_pos, y_pos))
        self.spawner.add_bullet(bullet)


class Spawner:
    def __init__(self, canvas):
        self.canvas = canvas
        self.seed = 4
        self.obstacles = self.canvas.obstacles
        self.n_enemies = None
        self.enemies = set()
        self.player = None
        self.bullets = list()

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def spawn_enemies(self):
        random.seed(self.seed)
        self.n_enemies = (self.canvas.length * self.canvas.width) // 4
        k = random.randint(0, self.n_enemies)
        while k:
            i, j = random.randint(0, self.canvas.length), random.randint(0, self.canvas.width)
            if (i, j) not in self.obstacles:
                e = Enemy((i, j))
                self.enemies.add(e)
                k -= 1
        return self.enemies

    def spawn_player(self):
        i, j = random.randint(0, self.canvas.length), random.randint(0, self.canvas.width)
        while (i, j) in self.obstacles or (i, j) in [enemy.position for enemy in self.enemies]:
            i, j = random.randint(0, self.canvas.length), random.randint(0, self.canvas.width)
        self.player = (i, j)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Player 1')
    c = Canvas(10, 10)
    c.create_obstacles()
    s = Spawner(c)
    s.spawn_enemies()
    s.spawn_player()
    p = Player(s, c)
    d = Display(c, p, s)
    d.display()
    print()
    p.player_attack('UP')
    d.display()
    print()
    p.move_player('UP')
    d2 = Display(c, p, s)
    #p.player_attack('UP')
    d2.display()