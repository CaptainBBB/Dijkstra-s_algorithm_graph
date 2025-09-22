import math


class Vertex:                       # создаем класс представляющий вершины
    def __init__(self):
        self._links = []            # список всех связей вершины

    def __gt__(self, other):        # метод позволяет сравнивать объекты (точнее, локальное свойство weight)
        if isinstance(other, Vertex):
            return self.weight > other.weight

    @property
    def links(self):                # объект-свойство property возвращает коллекцию links
        return self._links

    @links.setter
    def links(self, link):          # а это объект-свойство работает в качестве сеттера
        if isinstance(link, Link):
            check = link.v2 if link.v1 == self else link.v1
            if not list(filter(lambda x: check in x, self._links)):
                self.links.append(link)


class Link:                                 # класс отвечает за связь между двумя объектами
    def __init__(self, v1, v2, dist=1):
        if isinstance(v1 and v2, Vertex) and type(dist) is int:
            self._v1 = v1
            self._v2 = v2
            self._dist = dist

            v1.links = self                 # в момент создания объекта класса link мы добавляем в вершины связи между
            v2.links = self                 # ними

    def __iter__(self):                     # итератор позволяет перебирать локальные свойства в объекте класса
        return iter(self.__dict__.values())

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, val):
        if type(val) is int:
            self._dist = val


class LinkedGraph:                  # этот класс отвечает за создание карты объектов
    def __init__(self):
        self._links = []            # здесь хранятся все существующие связи
        self._vertex = []           # здесь хранятся все существующие вершины

    def add_vertex(self, v):        # метод добавляет новую вершину в список
        if isinstance(v, Vertex) and v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):       # метод добавляет новую связь в список
        if isinstance(link, Link):
            if not list(filter(lambda x: link.v1 in x and link.v2 in x, self._links)):
                self._links.append(link)
                self.add_vertex(link.v1)
                self.add_vertex(link.v2)

    def find_path(self, start_v, stop_v):
        if isinstance(start_v and stop_v, Vertex):
            copy_v = self._vertex.copy()
            self._rec(start_v, 0, copy_v)

            all_vertexes = []
            all_short_links = []

            node = stop_v
            while node != start_v:
                all_vertexes.append(node)
                all_short_links.append(*node.short_link)            # идём назад по short_link
                node = node.short_link[0].v2 if node.short_link[0].v1 == node else node.short_link[0].v1

            all_vertexes.append(start_v)            # сбрасываем веса, чтобы можно было искать новые пути
            for el in self._vertex:
                el.weight = 100
                el.short_link = []

            return (all_vertexes[::-1], all_short_links[::-1])

    def _rec(self, start_v, w, vxs_copy):            # инициализация
        for v in self._vertex:
            v.weight = 100
            v.short_link = []

        start_v.weight = 0

        while vxs_copy:                              # выбираем вершину с минимальным весом
            node = min(vxs_copy, key=lambda v: v.weight)
            vxs_copy.remove(node)

            for lnk in node.links:
                nxt = lnk.v2 if lnk.v1 == node else lnk.v1
                new_w = node.weight + lnk.dist

                if new_w < nxt.weight:
                    nxt.weight = new_w
                    nxt.short_link = [lnk]


class Station(Vertex):              # в объектах этого класса присутствует имя объекта (строка)
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):              # при печати отобразится имя объекта
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):

        super().__init__(v1, v2, dist)
