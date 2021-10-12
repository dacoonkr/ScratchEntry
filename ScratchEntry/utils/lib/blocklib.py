class library:
    def __init__(self):
        self.src = open("utils\\lib\\basic.txt", "r").read()
        self.dict = {}
        self.vars = {}
        self.fns = {}
        self.spts = {}
        self.brds = {}
        self.ctms = {}
        now = "nothing"
        for x in self.src.split('\n'):
            if len(x) == 0: continue
            elif x[0] == ':':
                now = x[1:]
            elif x[0] == '/':
                before = x[1:].split()[0]
                after = x[1:].split()[1]
                params = x[1:].split()[2:]
                self.dict[before] = {"type": now, "code": after, "params": params}

    def find(self, opcode: str):
        if opcode in self.dict:
            return self.dict[opcode]
        else: return None

    def create_var(self, before, after):
        self.vars[before] = after

    def get_var(self, before):
        return self.vars[before]

    def create_fn(self, before, after):
        self.fns[before] = after

    def get_fn(self, before):
        return self.fns[before]

    def create_spt(self, before, after):
        self.spts[before] = after

    def get_spt(self, before):
        return self.spts[before]

    def create_brd(self, before, after):
        self.brds[before] = after

    def get_brd(self, before):
        return self.brds[before]["id"]

    def keyconvert(self, keycode):
        if keycode == "space": return 32
        elif keycode == "up arrow": return 38
        elif keycode == "down arrow": return 40
        elif keycode == "left arrow": return 37
        elif keycode == "right arrow": return 39
        elif ord('a') <= ord(keycode) <= ord('z'):
            return ord(keycode) - ord('a') + ord('A')
        elif ord('0') <= ord(keycode) <= ord('9'):
            return ord(keycode)
        return -1

    def add_costume(self, object_number_name, after):
        self.ctms[object_number_name] = after

    def get_costume(self, object_number, name):
        return self.ctms[f"{object_number}::{name}"]