import sys
import copy
import kociemba
import random
import pycuber as pc

kociemba_map = {"w":"U", "r":"R", "g":"F", "y":"D", "o":"L", "b":"B"}
moves = ["U","U'","U2","R","R'","R2","F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2"]
wide_moves = {"R":"M'", "L":"M", "U":"E'", "D":"E", "F":"S", "B":"S'"}

upper_face_edges = {
    (0,1): ("B", 0,1),
    (1,0): ("L", 0,1),
    (1,2): ("R", 0,1),
    (2,1): ("F", 0,1),
} #UB, UL, UR, UF

upper_face_corners = {
    (0,0): [("B", 0,2), ("L", 0,0)],
    (0,2): [("B", 0,0), ("R", 0,2)],
    (2,0): [("F", 0,0), ("L", 0,2)],
    (2,2): [("F", 0,2), ("R", 0,0)],
} #UBL, UBR, UFL, UFR

oll_algs = [
    "R U2 R2 F R F' U2 R' F R F'",
    "R U' R2 D' r U r' D R2 U R'",
    "f R U R' U' f' U' F R U R' U' F'",
    "f R U R' U' f' U F R U R' U' F'",
    "r' U2 R U R' U r",
    "r U2 R' U' R U' r'",
    "r U R' U R U2 r'",
    "R' F' r U' r' F2 R",
    "R U R' U' R' F R2 U R' U' F'",
    "R U R' U R' F R F' R U2 R'",
    "r' R2 U R' U R U2 R' U M'",
    "M' R' U' R U' R' U2 R U' M",
    "F U R U2 R' U' R U R' F'",
    "r U R' U' r' F R2 U R' U' F'",
    "r' U' r R' U' R U r' U r",
    "R' F R U R' U' F' R U' R' U2 R",
    "F R' F' R U S' R U' R' S",
    "R U2 R2 F R F' U2 M' U R U' r'",
    "S' R U R' S U' R' F R F'",
    "S' R U R' S U' M' U R U' r'",
    "R U2 R' U' R U R' U' R U' R'",
    "R U2 R2 U' R2 U' R2 U2 R",
    "R2 D R' U2 R D' R' U2 R'",
    "r U R' U' r' F R F'",
    "F' r U R' U' r' F R",
    "R U2 R' U' R U' R'",
    "R U R' U R U2 R'",
    "r U R' U' M U R U' R'",
    "r2 D' r U r' D r2 U' r' U' r",
    "F U R U2 R' U' R U2 R' U' F'",
    "R' U' F U R U' R' F' R",
    "S R U R' U' R' F R f'",
    "R U R' U' R' F R F'",
    "R U R2 U' R' F R U R U' F'",
    "R U2 R2 F R F' R U2 R'",
    "R U2 r D r' U2 r D' r' R'",
    "F R' F' R U R U' R'",
    "R U R' U R U' R' U' R' F R F'",
    "f' r U r' U' r' F r S",
    "R' F R U R' U' F' U R",
    "R U R' U R U2 R' F R U R' U' F'",
    "R' U' R U' R' U2 R F R U R' U' F'",
    "f' L' U' L U f",
    "f R U R' U' f'",
    "F R U R' U' F'",
    "R' U' R' F R F' U R",
    "F R' F' R U2 R U' R' U R U2 R'",
    "F R U R' U' R U R' U' F'",
    "r U' r2 U r2 U r2 U' r",
    "r' U r2 U' r2 U' r2 U r'",
    "f R U R' U' R U R' U' f'",
    "R' F' U' F U' R U R' U R",
    "r' U2 R U R' U' R U R' U r",
    "r U R' U R U' R' U R U2 r'",
    " R' F U R U' R2 F' R2 U R' U' R",
    "r U r' U R U' R' U R U' R' r U' r'",
    "R U R' U' M' U R U' r'"
]

oll_alglist = {num: alg for num, alg in list(enumerate(oll_algs, start=1))}

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

def get_oll_ss(cube, face_key="U"):
    face = cube.get_face(face_key)
    center_color = face[1][1].colour

    # check edges
    edge_codes = []
    for (i,j), (side, side_i, side_j) in upper_face_edges.items():
        if face[i][j].colour == center_color:
            edge_codes.append(0)
        else:
            alt_color = cube.get_face(side)[side_i][side_j].colour
            if alt_color == center_color:
                edge_codes.append(1)
            else:
                raise ValueError("⚠️ invalid OLL case!")

    # check corners
    corner_codes = []
    for (i,j), side_list in upper_face_corners.items():
        if face[i][j].colour == center_color:
            corner_codes.append(0)
        else:
            corner_code = -1
            for code, (side, side_i, side_j) in enumerate(side_list, start=1):
                if cube.get_face(side)[side_i][side_j].colour == center_color:
                    corner_code = code
                    break
            if corner_code < 0:
                raise ValueError("⚠️ invalid OLL case!")
            corner_codes.append(corner_code)

    if sum(edge_codes) in (1,3):
        raise ValueError("⚠️ invalid OLL case!")

    return tuple(edge_codes + corner_codes)

def get_oll_case(cube, face_key="U"):
    possible_cases = [get_oll_ss(cube, face_key)]
    for _ in range(3):
        cube("U")
        possible_cases.append(get_oll_ss(cube, face_key))

    cube("U") #undo the setup moves
    return min(possible_cases)

def oll_trainer():
    cube = pc.Cube()
    cube("L U L' U' L' B L B'")
    print(generate_scramble(min_len=5,max_len=15,mode=10))
    print(get_oll_case(cube, face_key="U"))

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
