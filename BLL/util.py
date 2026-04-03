class short_ID_generator:
    _id_s = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _id_n = [ 0, 0, 0, -1 ]

    def new_id(self):
        id_s = self._id_s
        id_n = self._id_n #얕은복사

        id_n[3] += 1
        if id_n[3] == 36:
            id_n[3] = 0
            id_n[2] += 1
        if id_n[2] == 36:
            id_n[2] = 0
            id_n[1] += 1
        if id_n[1] == 36:
            id_n[1] = 0
            id_n[0] += 1
        return id_s[id_n[0]] + id_s[id_n[1]] + id_s[id_n[2]] + id_s[id_n[3]]

class var_position_generator:
    def __init__(self):
        self._var_n = 0
        self._list_n = 0

    def new_var(self):
        self._var_n += 1
        return -230, -43 - 24 * self._var_n

    def new_list(self):
        self._list_n += 1
        return 120, -43 - 24 * _list_n