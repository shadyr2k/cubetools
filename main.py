import sys
import kociemba
import random
import pycuber as pc

kociemba_map = {"w":"U", "r":"R", "g":"F", "y":"D", "o":"L", "b":"B"}
moves = ["U","U'","U2","R","R'","R2","F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2"]
wide_moves = {"R":"M'", "L":"M", "U":"E'", "D":"E", "F":"S", "B":"S'"}

def fix_wide_moves(alg: str):
    move_list = []
    for pieces in alg.split():
        move = pieces[0]
        move_upper = move.upper()
        suffix = pieces[1:]

        if move_upper in wide_moves and (move.islower() or 'w' in suffix.lower()):
            new_suffix = suffix.replace('w','').replace('W','')
            face_move = f"{move_upper}{new_suffix}"
            slice_move = f"{wide_moves[move_upper]}{new_suffix}"

            if slice_move.endswith("2") and "'" in slice_move:
                slice_move = slice_move.replace("'","")
            if slice_move.endswith("''"):
                slice_move = slice_move[:-2]

            move_list += [face_move, slice_move]
        else:
            move_list.append(pieces)
    return " ".join(move_list)

def generate_scramble(min_len=8, max_len=25, mode=15):
    length = int(random.triangular(min_len, max_len, mode))
    seq = []
    while len(seq) < length:
        move = random.choice(moves)
        if not seq or move[0] != seq[-1][0]:
            seq.append(move)
    return " ".join(seq)

def cube_solver():
    cube_state = cube_solver_prompt()
    cube_sol = kociemba.solve(cube_state)
    print("\nsol:", cube_sol)

def cube_solver_prompt():
    print("hold your cube w/ white top & green front. rotate from this orientation and input sticker colors.`")
    print("enter the sticker colors for each face ROW by ROW, LEFT to RIGHT using w,r,g,y,o,b for colors")
    faces = ["white", "red", "green", "yellow", "orange", "blue"]
    face_list = []
    for face in faces:
        while True:
            user_input = input(f"enter colors for the {face} face: ").strip().lower()
            if len(user_input) == 9 and all(c in kociemba_map for c in user_input):
                face_list.append(user_input)
                break
            print("⚠️ input is invalid")
    face_string = ''.join(face_list)
    return ''.join(kociemba_map[c] for c in face_string)

def get_valid_oll(cube, face_key="U"):
    face = cube.get_face(face_key)
    center_color = face[1][1].colour

    edges = [(0,1),(1,0),(1,2),(2,1)]
    corners = [(0,0),(2,0),(0,2),(2,2)]

    check_edges = [1 if face[i][j].colour == center_color else 0 for (i,j) in edges]
    check_corners = [1 if face[i][j].colour == center_color else 0 for (i,j) in corners]

    if sum(check_edges) in (1,3):
        return None

    return tuple(check_edges + check_corners)

def oll_trainer():
    cube = pc.Cube()
    cube("r U R' U R U2 r'")
    print(generate_scramble(min_len=5,max_len=15,mode=10))
    print(get_valid_oll(cube, face_key="U"))

def pll_trainer():
    print("n/a")

def fix_user_string():
    return None

MENU = {
    "1": ("cube solver", cube_solver),
    "2": ("OLL trainer", oll_trainer),
    "3": ("PLL trainer", pll_trainer),
    "0": ("quit",        lambda: sys.exit(0)),
}

def menu():
    while True:
        for i,(j,_) in MENU.items():
            print(f"{i}. {j}")
        user_input = input("⇨ ")
        run_method = MENU.get(user_input)
        if run_method:
            run_method[1]()
        else:
            print("\n")

if __name__ == "__main__":
    menu()
