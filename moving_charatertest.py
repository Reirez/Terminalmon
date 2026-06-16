from random import randint, choice
from pathlib import Path
import time, sys, json

class Map:
    def __init__(self, pixel):
        self.pixel = pixel
        
    def generate_mapsaved(self, length, width, door_x, door_y):
        """Makes a map based on given WL"""
        self.map = []
        self.width = width
        self.length = length
        for l in range(length):
            y_list = []
            for w in range(width):
                y_list.append(self.pixel)
            self.map.append(y_list)
        """Generates a door on a random point on the map"""
        self.map[door_y][door_x] = "#"
        
    def generate_map(self, length, width):
        """Makes a map based on given WL"""
        self.map = []
        self.width = width
        self.length = length
        for l in range(length):
            y_list = []
            for w in range(width):
                y_list.append(self.pixel)
            self.map.append(y_list)
        """Generates a door on a random point on the map"""
        self.door_x = randint(0, self.width - 1)
        self.door_y = randint(0, self.length - 2)
        self.map[self.door_y][self.door_x] = "#"
    
    def check_tile(self, symbol):
        """checks if symbol still exists in map"""
        idk = 0
        for row in self.map:
            if symbol not in row:
                idk += 1
        if idk == self.length:
            return True
        
    def display_map(self, floor_level):
        """Prints map as a W by L rectangle"""
        print(f"Floor {floor_level}")
        for x_list in self.map:
            x_row = ""
            for x_value in x_list:
                x_row += str(x_value)
            print(x_row)
            
class Character:
    """An attempt to model a movable character"""
    def __init__(self, length, width, look="T"):
        self.look = look
        self.width = width
        self.length = length
    
    def locate_char(self, map):
        """locates character position"""
        yaxis = 0
        for y in map:
            for x in range(len(y)):
                if map[yaxis][x] == self.look:
                    return yaxis, x
            yaxis += 1
        
    def move(self, direction, map, instance):
        """move in the four directions"""
        yaxiz, xaxiz = self.locate_char(map)
        self.pos_x = xaxiz
        self.pos_y = yaxiz
        if direction == "d":
            self.previous_tile = map[yaxiz][(xaxiz + 1) % self.width]
            map[yaxiz][(xaxiz + 1) % self.width] = self.look
            map[yaxiz][xaxiz] = instance.pixel
        elif direction == "w":
            self.previous_tile = map[(yaxiz - 1) % self.length][xaxiz]
            map[(yaxiz - 1) % self.length][xaxiz] = self.look
            map[yaxiz][xaxiz] = instance.pixel
        elif direction == "s":
            self.previous_tile = map[(yaxiz + 1) % self.length][xaxiz]
            map[(yaxiz + 1) % self.length][xaxiz] = self.look
            map[yaxiz][xaxiz] = instance.pixel
        elif direction == "a":
            self.previous_tile = map[yaxiz][xaxiz - 1]
            map[yaxiz][xaxiz - 1] = self.look
            map[yaxiz][xaxiz] = instance.pixel
        elif direction.lower() == "save":
            print("Saved game!")
        else:
            print("\nInvalid move!")
        
    def spawn(self, map, y=-1, x=0):
        """spawns character into map"""
        map[y][x] = self.look
#improve battle mechanics and code FIX previous tile bug 
        #especially code!! Add SAVE Function
class Encounter():
    """An attempt to model random encounters"""
    def __init__(self, monsters, tile):
        self.monsters_save = monsters
        self.monsters = monsters.copy()
        self.tile = tile
        self.player = {"Player": 10}
        self.monster = choice(list(self.monsters.keys()))
        
    def enemy_attack(self):
        """Handles enemy attack"""
        damage = randint(1, 2)
        print(f"{self.monster.title()} attacked you! you lost {damage} health.")
        time.sleep(0.9)
        print(f"Player - {self.player['Player'] - damage}")
        self.player["Player"] = self.player["Player"] - damage
        time.sleep(1)
    
    def player_attack(self):
        """Player attack"""
        damage = randint(1, 3)
        print(f"You attacked {self.monster.title()}! {self.monster.title()} lost {damage} health")
        time.sleep(0.9)
        print(self.monster + f" - {self.monsters[self.monster] - damage}")
        self.monsters[self.monster] = self.monsters[self.monster] - damage
        time.sleep(1)
        if self.health_check():
            return True
        print()
   
    def health_check(self):
        if self.monsters[self.monster] <= 0:
            print("You win!")
            return True
        elif self.player["Player"] <= 0:
            print("You lost! Game Over ! ! ! ")
            sys.exit()
         
    def battle(self):
        """Main battle loop/logic if there's an encounter"""
        print(f"A wild {self.monster.title()} appeared!")
        for i in range(1, 4):
            time.sleep(1)
            print('.')
        print()
        while True:
            print(self.monster.title() + f" - {self.monsters[self.monster]}")
            print()
            print(f"Player - {self.player['Player']}")
            move = input("What will you do?\n(1)Attack\n(2)Run\n: ")
            if move == '1':
                print('\n\n\n\n\n')
                if self.player_attack():
                    break
                self.enemy_attack()
                print()
            else:
                ran_num = randint(1, 3)
                if ran_num == 3:
                    print("You ran away from battle!")
                    break
                print(f"The {self.monster.title()} won't let you escape!")
                time.sleep(0.9)
                self.enemy_attack()
                print()
            if self.health_check():
                break
        
    def random_encounter(self, previous_tile):
        """decides if an encounter happens or not"""
        if previous_tile == self.tile:
            chance = randint(1, 6)
            if chance == 3:
                self.battle()
                return True
        self.monsters = self.monsters_save.copy() #resets monster healths
        
    
class Save_Game():
    """Saving logic"""
    def __init__(self):
        self.savegame = Path("Primitivemon_save_txt")
        
    def save(self, data):
        """Saves data"""
        self.savegame.write_text(json.dumps(data))
        
    def load(self):
        """Reads save data if it exists"""
        if self.savegame.exists():
            information = json.loads(self.savegame.read_text())
            return information
        
    def delete_save(self):
        self.savegame.unlink()
#cleanup saved game code! /messy/ logic not the best
def saved_game_loop(data, savestate, encounter):
    savedata = data
    floor = savedata[3]
    map = Map('-')
    map.generate_mapsaved(savedata[2], savedata[1], savedata[6], savedata[7])
    t = Character(map.length, map.width, look = "B")
    t.spawn(map.map, savedata[5], savedata[4])
    map.display_map(floor)
    while True:
        move = input("Enter move (wasd): ")
        if move.lower() == "save":
            print("saved!")
        t.move(move, map.map, map)
        if map.check_tile('#'):
            floor += 1
            break
        map.display_map(floor)
        if encounter.random_encounter(t.previous_tile):
            map.display_map(floor)
        
def main():
    """main game loop"""
    encounter = Encounter({"zoobat": 10, "crowbat": 11}, "-")
    savestate = Save_Game()
    floor = 0
    if savestate.savegame.exists():
        saved_game_loop(savestate.load(), savestate, encounter)
    while True:
        map = Map('-')
        map.generate_map(randint(2, 5), randint(2, 10))
        t = Character(map.length, map.width, look = "B")
        t.spawn(map.map)
        map.display_map(floor)
        while True:
            move = input("Enter move (wasd): ")
            t.move(move, map.map, map)
            if move.lower() == "save":
                save_data = [1, map.width, map.length, floor, t.pos_x, t.pos_y, map.door_x, map.door_y]
                savestate.save(save_data)
                continue
            if map.check_tile('#'):
                floor += 1
                break
            map.display_map(floor)
            if encounter.random_encounter(t.previous_tile):
                map.display_map(floor)
            
print("Terminalmon.\nB - character\n# - door to next level")
if input("Enter 'y' to start: ").lower() == 'y':
    main()
        