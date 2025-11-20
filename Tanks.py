import random

class Tank:
    """Template of tanks"""

    def __init__(self, model, armor, min_damage, max_damage, health):
        self.model = model
        self.armor = armor
        self.damage = random.randint(min_damage, max_damage)
        self.health = health

    def print_info(self):
            print(f"{self.model} имеет лобовую броню {self.armor}мм при {self.health}ед. здоровья и урон в {self.damage} единиц")

    def health_down(self, enemy_damage):
            self.health -= enemy_damage
            print(f"\n{self.model}:")
            print(f"Командир, по экипажу {self.model} попали, у нас осталось {self.health} очков здоровья")


    def shot(self, enemy):
            if enemy.health <= 0 or self.damage >= self.health:
                self.health = 0
                print(f"Экипаж танка {enemy.model} уничтожен")
            else:
                enemy.health_down(enemy.damage)
                print(f"\n{self.model}:")
                print(f"Точно в цель, у противника {enemy.model} осталось {enemy.health} единиц здоровья")

class SuperTank(Tank):
    """Template of superTanks"""
    def __init__(self, model, armor, min_damage, max_damage, health):
        super().__init__(model, armor, min_damage, max_damage, health)
        self.forceArmor = True


    def health_down(self, enemy_damage):
        super().health_down(enemy_damage / 2)


tank1 = Tank("T-34", 90, 20, 30, 100)
tank2 = Tank("Tiger", 120, 10, 50, 120)
tank1.print_info()
tank2.print_info()

tank1.shot(tank2)
tank1.shot(tank2)
tank1.shot(tank2)
tank1.shot(tank2)
tank1.shot(tank2)
tank1.shot(tank2)
tank1.shot(tank2)