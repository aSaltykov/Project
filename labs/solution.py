from abc import ABC,abstractmethod


class Singleton:
    __instance = None

    def __new__(cls, *val):
        if Singleton.__instance is None:
            Singleton.__instance = object.__new__(cls)
        Singleton.__instance.val = val

        return Singleton.__instance


class Game(Singleton):
    def __init__(self):
        self.obj = []
        self.level = 0
        self.score = 0
        self._game = True
        self.map = None
        self.mini_map = True
        self.knight = None
        self.gen_level = None
        self.gen_knight = None
        self.member = set()
        self._object_size = 1

    def notice(self, message):
        for el in self.member:
            el.update(message)

    def knight_create(self):
        self.knight = self.gen_knight.create()

    def start_new_game(self):
        self.knight_create()
        self.level = 1
        self.score = 0
        self.notice({"start": "new game"})
        pass


class KnightFactory:

    def create(self):
        obj = Lib.textures["knight"]["object"]
        return Knight(STATS, obj)
    

class AbstractObj(ABC):
    @abstractmethod
    def __init__(self):
        self._object = []

    @abstractmethod
    def draw(self,display):
        pass
    
    @property
    def object(self):
        return self._object[0]
    
    @object.setter
    def object(self, value):
        self._object = value if isinstance(value, list) else [value]


class AbsAction(ABC):
    @classmethod
    @abstractmethod
    def use(cls, level, knight):
        pass


class NextLevel(AbsAction):
    @classmethod
    def use(cls, level, knight):
        level.next_level()


class Interactive(ABC):
    @abstractmethod
    def interact(self, knight, engine):
        pass


class HpError(Exception):

    def __init__(self, hp, message = "little health"):
        self.hp = hp
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.hp} -> {self.message}'


class Map:

    def __init__(self,_map):
        self._map = _map

    @property
    def size(self):
        return len(self._map[0]),len(self._map)

    def __getitem__(self, number):
        if not isinstance(number, tuple):
            raise TypeError
        elif number[0] < len(self._map[0]) and number[1] < len(self._map):
            return self._map[number[1]][number[0]]
        else:
            raise IndexError


class ObjGenerate:

    def __init__(self):
        self.enemy = dict()

    def get(self, _map):
        return {}


class MapGenerate(ObjGenerate):

    def get(self, _map):
        return {(1, 1): "Knight"}


class HealthRecovery(AbsAction):
    @classmethod
    def use(cls, level, knight):
        level.score += 1
        try:
            if knight.max_hit_points < knight.hit_points:
                knight.hit_points = knight.max_hit_point
            else:
                raise HpError(int(knight.hit_points))
        except HpError as e:
            pass


class Entity(AbstractObj):

    def __init__(self, stats, position ,image):
        self._object = image 
        self.hit_points = 0
        self.max_hit_points = 0
        self.stats = stats
        self.position = position
        self.max_()
        self.hit_points = self.max_hit_points

    def draw(self,display):
        pass

    def max_(self):
        self.max_hit_points = 8 + self.stats["stamina"] + self.stats["power"]
        if self.max_hit_points < self.hit_points:
            self.hit_points = self.max_hit_points


class Knight(Entity):
    def __init__(self,stats, image):
        self.level = 1
        self.experience = 0
        super().__init__(image, stats, [1, 1])

    @property
    def max_experience(self):
        pass


    def level(self):
        while self.experience >= self.max_experience:
            self.max_()
            self.hit_points = self.max_hit_points
            self.level += 1
            self.stats["stamina"] += 3
            self.stats["power"] += 3
            yield "Level up"


class Mate(AbstractObj, Interactive):
    
    def __init__(self, position, action, image):
        self._object = image
        self.position = position
        self.action = action

    def interact(self, knight, engine):
        self.action(engine, knight)

    def draw(self,display):
        pass


class Effect(Entity):

    def __init__(self,basic):
        self.basic = basic
        self.use_effect()

    @property
    def hit_points(self):
        return self.basic.hit_points

    @hit_points.setter
    def hit_points(self,value):
        self.basic.hit_points = value

    @property
    def max_hit_points(self):
        return self.basic.max_hit_points

    @max_hit_points.setter
    def max_hit_points(self,value):
            self.basic.max_hit_points = value

    @property
    def gold(self):
        return self.basic.gold

    @gold.setter
    def gold(self, value):
        self.basic.gold = value

    @property
    def experience(self):
        return self.basic.experience

    @experience.setter
    def experience(self, value):
        self.basic.experience = value

    @abstractmethod
    def use_effect(self):
        self.max_hit_points()
        try:
            if self.max_hit_points < self.hit_points:
                self.hit_points = self.max_hit_points
            else:
                raise HpError(int(self.hit_points))
        except HpError as e:
            pass


class Debility(Effect):
    def use_effect(self):
        self.stats["power"] -= 5
        self.stats["stamina"] -= 5
        super().use_effect()


class Buff(Effect):
    def use_effect(self):
        self.stats["power"] += 5
        self.stats["intellect"] += 5
        self.stats["stamina"] += 3
        super().use_effect()


class Violent(Effect):
    def use_effect(self):
        self.stats["power"] += 5
        self.stats["intellect"] -= 2
        self.stats["stamina"] += 5
        super().use_effect()
        
        
class Lib:
    class Getter:
        def __init__(self, name):
            self.name = name

        def __get__(self, instance, host):
            return host._obj.get(self.name, dict())

    _obj = dict()
    _generate = {"object": None, "action": None}
    mate = Getter("mate")
    textures = Getter("textures")

    @classmethod
    def set_generate(cls, generate_obj=None, generate_action=None):
        cls._generate["object"] = generate_obj
        cls._generate["action"] = generate_action

    @classmethod
    def clear(cls):
        cls._obj = dict()


def create_game():
    obj_create = Game()
    obj_create.gen_knight = KnightFactory()
    obj_create.start_new_game()
    pass
    return obj_create


STATS = {
    "power": 10,
    "stamina": 10,
    "intellect": 5
}

