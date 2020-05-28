S = Hash(default_value=[])

@export
def add_thing(owner: str, uid: str):
    things_list = S[owner]
    things_list.append(uid)
    S[owner] = things_list

@export
def remove_thing(owner: str, uid: str):
    things_list = S[owner]
    if uid in things_list:
        things_list.remove(uid)
        S[owner] = things_list