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

    def find_path(self, start_v, stop_v):               # метод отвечает за поиск самого короткого пути с помощью алгоритма Дейкстры
        if isinstance(start_v and stop_v, Vertex):      # копируем все вершины в коллекцию; копия нужна для
            copy_v = self._vertex.copy()                # перебора и удаления всех существующих вершин
            for el in copy_v:
                el.weight = math.inf  # изначальный вес вершины равен бесконечности
                el.short_link = []  # коллекция коротких связей

            self._rec(start_v, 0, copy_v)               # вызываем рекурсивную функцию; она ничего не возвращает, но
                                                        # меняет локальные атрибуты каждой существующей вершины
            all_vertexes = []
            all_short_links = []

            node = stop_v

            while node != start_v:                        # перебираем вершины до тех пор пока не доберемся до стартовой
                all_vertexes.append(node)
                all_short_links.append(*node.short_link)  # добавляем короткую связь, затем вычисляем следующую вершину
                node = node.short_link[0].v2 if node.short_link[0].v1 == node else node.short_link[0].v1

            all_vertexes.append(node)                       # добавляем пропущенную стартовую вершину

            for el in self._vertex:
                el.weight = math.inf
                el.short_link = []               # меняем локальные атрибуты на изначальные

            return (all_vertexes[::-1], all_short_links[::-1])  # поскольку вершины и связи мы добавляем задом наперед,
                                                                # нужно инвертировать списки

    def _rec(self, node, w, vxs_copy):
        while vxs_copy:                                     # проверяем есть ли непройденные вершины
            node.weight = w                                 # инициализируем вес; для начальной точки он будет нулевым
            coll = []                                       # в коллекции мы храним веса из текущей итерации

            for lnk in node.links:                          # перебираем связи в текущей вершине
                nxt_nd = lnk.v2 if lnk.v1 == node else lnk.v1
                                                                  # проверяем, проходили ли мы следующую вершину;
                if nxt_nd in vxs_copy:                            # копии непосещенных вершин хранятся в vxs_copy;
                    coll.append(nxt_nd)                           # минимальную следующую вершину выбираем из coll

                    if (node.weight + lnk.dist) < nxt_nd.weight:  # проверяем вес текущей вершины и прибавляем дистанцию
                        nxt_nd.weight = node.weight + lnk.dist    # сумма должна быть меньше веса следующей вершины
                        nxt_nd.short_link = [lnk]                 # из начальной станции в nxt_nd быстрее всего попасть по текущей связи;
                                                                  # поэтому в nxt_nd в short_link мы добавляем текущую (и единственную!) короткую связь
            if node in vxs_copy:
                vxs_copy.remove(node)                             # удаляем вершину из vxs_copy,
                                                                  # чтобы не проходить уже пройденные;
            if coll:                                              # выбираем минимальный вес из перебранных
                min_obj = min(coll)
            else:                                                 # если все соседние вершины уже перебраны, то в coll ничего не добавится;
                return                                            # в этом случае мы завершаем функцию и по рекурсии возвращаемся к предыдущей вершине

            self._rec(min_obj, min_obj.weight, vxs_copy)

            for lnk in node.links:                                      # по рекурсии возвращаемся обратно и
                nxt_nd = lnk.v2 if lnk.v1 == node else lnk.v1           # проверяем, какой вес больше: текущей вершины
                                                                        # или следующей + дистанция?
                if node.weight > nxt_nd.weight + lnk.dist:
                    node.weight = nxt_nd.weight + lnk.dist
                    node.short_link = [lnk]
        return


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