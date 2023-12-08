import time

day = 10

lookup_table = {
    "H": len("22"),
    "He": len("13112221133211322112211213322112"),
    "Li": len("312211322212221121123222112"),
    "Be": len("111312211312113221133211322112211213322112"),
    "B": len("1321132122211322212221121123222112"),
    "C": len("3113112211322112211213322112"),
    "N": len("111312212221121123222112"),
    "O": len("132112211213322112"),
    "F": len("31121123222112"),
    "Ne": len("111213322112"),
    "Na": len("123222112"),
    "Mg": len("3113322112"),
    "Al": len("1113222112"),
    "Si": len("1322112"),
    "P": len("311311222112"),
    "S": len("1113122112"),
    "Cl": len("132112"),
    "Ar": len("3112"),
    "K": len("1112"),
    "Ca": len("12"),
    "Sc": len("3113112221133112"),
    "Ti": len("11131221131112"),
    "V": len("13211312"),
    "Cr": len("31132"),
    "Mn": len("111311222112"),
    "Fe": len("13122112"),
    "Co": len("32112"),
    "Ni": len("11133112"),
    "Cu": len("131112"),
    "Zn": len("312"),
    "Ga": len("13221133122211332"),
    "Ge": len("31131122211311122113222"),
    "As": len("11131221131211322113322112"),
    "Se": len("13211321222113222112"),
    "Br": len("3113112211322112"),
    "Kr": len("11131221222112"),
    "Rb": len("1321122112"),
    "Sr": len("3112112"),
    "Y": len("1112133"),
    "Zr": len("12322211331222113112211"),
    "Nb": len("1113122113322113111221131221"),
    "Mo": len("13211322211312113211"),
    "Tc": len("311322113212221"),
    "Ru": len("132211331222113112211"),
    "Rh": len("311311222113111221131221"),
    "Pd": len("111312211312113211"),
    "Ag": len("132113212221"),
    "Cd": len("3113112211"),
    "In": len("11131221"),
    "Sn": len("13211"),
    "Sb": len("3112221"),
    "Te": len("1322113312211"),
    "I": len("311311222113111221"),
    "Xe": len("11131221131211"),
    "Cs": len("13211321"),
    "Ba": len("311311"),
    "La": len("11131"),
    "Ce": len("1321133112"),
    "Pr": len("31131112"),
    "Nd": len("111312"),
    "Pm": len("132"),
    "Sm": len("311332"),
    "Eu": len("1113222"),
    "Gd": len("13221133112"),
    "Tb": len("3113112221131112"),
    "Dy": len("111312211312"),
    "Ho": len("1321132"),
    "Er": len("311311222"),
    "Tm": len("11131221133112"),
    "Yb": len("1321131112"),
    "Lu": len("311312"),
    "Hf": len("11132"),
    "Ta": len("13112221133211322112211213322113"),
    "W": len("312211322212221121123222113"),
    "Re": len("111312211312113221133211322112211213322113"),
    "Os": len("1321132122211322212221121123222113"),
    "Ir": len("3113112211322112211213322113"),
    "Pt": len("111312212221121123222113"),
    "Au": len("132112211213322113"),
    "Hg": len("31121123222113"),
    "Tl": len("111213322113"),
    "Pb": len("123222113"),
    "Bi": len("3113322113"),
    "Po": len("1113222113"),
    "At": len("1322113"),
    "Rn": len("311311222113"),
    "Fr": len("1113122113"),
    "Ra": len("132113"),
    "Ac": len("3113"),
    "Th": len("1113"),
    "Pa": len("13"),
    "U": len("3"),
}

mapping_table: dict[str, tuple] = {
    "H": ("H",),
    "He": ("Hf", "Pa", "H", "Ca", "Li"),
    "Li": ("He",),
    "Be": ("Ge", "Ca", "Li"),
    "B": ("Be",),
    "C": ("B",),
    "N": ("C",),
    "O": ("N",),
    "F": ("O",),
    "Ne": ("F",),
    "Na": ("Ne",),
    "Mg": ("Pm", "Na"),
    "Al": ("Mg",),
    "Si": ("Al",),
    "P": ("Ho", "Si"),
    "S": ("P",),
    "Cl": ("S",),
    "Ar": ("Cl",),
    "K": ("Ar",),
    "Ca": ("K",),
    "Sc": ("Ho", "Pa", "H", "Ca", "Co"),
    "Ti": ("Sc",),
    "V": ("Ti",),
    "Cr": ("V",),
    "Mn": ("Cr", "Si"),
    "Fe": ("Mn",),
    "Co": ("Fe",),
    "Ni": ("Zn", "Co"),
    "Cu": ("Ni",),
    "Zn": ("Cu",),
    "Ga": ("Eu", "Ca", "Ac", "H", "Ca", "Zn"),
    "Ge": ("Ho", "Ga"),
    "As": ("Ge", "Na"),
    "Se": ("As",),
    "Br": ("Se",),
    "Kr": ("Br",),
    "Rb": ("Kr",),
    "Sr": ("Rb",),
    "Y": ("Sr", "U"),
    "Zr": ("Y", "H", "Ca", "Tc"),
    "Nb": ("Er", "Zr"),
    "Mo": ("Nb",),
    "Tc": ("Mo",),
    "Ru": ("Eu", "Ca", "Tc"),
    "Rh": ("Ho", "Ru"),
    "Pd": ("Rh",),
    "Ag": ("Pd",),
    "Cd": ("Ag",),
    "In": ("Cd",),
    "Sn": ("In",),
    "Sb": ("Pm", "Sn"),
    "Te": ("Eu", "Ca", "Sb"),
    "I": ("Ho", "Te"),
    "Xe": ("I",),
    "Cs": ("Xe",),
    "Ba": ("Cs",),
    "La": ("Ba",),
    "Ce": ("La", "H", "Ca", "Co"),
    "Pr": ("Ce",),
    "Nd": ("Pr",),
    "Pm": ("Nd",),
    "Sm": ("Pm", "Ca", "Zn"),
    "Eu": ("Sm",),
    "Gd": ("Eu", "Ca", "Co"),
    "Tb": ("Ho", "Gd"),
    "Dy": ("Tb",),
    "Ho": ("Dy",),
    "Er": ("Ho", "Pm"),
    "Tm": ("Er", "Ca", "Co"),
    "Yb": ("Tm",),
    "Lu": ("Yb",),
    "Hf": ("Lu",),
    "Ta": ("Hf", "Pa", "H", "Ca", "W"),
    "W": ("Ta",),
    "Re": ("Ge", "Ca", "W"),
    "Os": ("Re",),
    "Ir": ("Os",),
    "Pt": ("Ir",),
    "Au": ("Pt",),
    "Hg": ("Au",),
    "Tl": ("Hg",),
    "Pb": ("Tl",),
    "Bi": ("Pm", "Pb"),
    "Po": ("Bi",),
    "At": ("Po",),
    "Rn": ("Ho", "At"),
    "Fr": ("Rn",),
    "Ra": ("Fr",),
    "Ac": ("Ra",),
    "Th": ("Ac",),
    "Pa": ("Th",),
    "U": ("Pa",),
}


def part_1(data):
    iterations = 40
    string = ""
    for _ in range(iterations):
        string = ""
        for num, amount in data:
            string += str(amount) + num
        data = process_string(string)
    return len(string)


def part_2(data):
    iterations = 50
    string = ""
    for _ in range(iterations):
        string = ""
        for num, amount in data:
            string += str(amount) + num
        data = process_string(string)
    return len(string)


def part_1_v2():
    iterations = 40
    elements = ("Yb",)
    for _ in range(iterations):
        new_elements = []
        for element in elements:
            new_elements += mapping_table[element]
        elements = new_elements
    s = 0
    for element in elements:
        s += lookup_table[element]
    return s


def part_2_v2():
    iterations = 50
    elements = ("Yb",)
    for _ in range(iterations):
        new_elements = []
        for element in elements:
            new_elements += mapping_table[element]
        elements = new_elements
    s = 0
    for element in elements:
        s += lookup_table[element]
    return s


def process_string(string: str) -> list[tuple[str, int]]:
    data = []
    last_chr = None
    chr_run = 0
    for char in string:
        if char != last_chr:
            data.append((last_chr, chr_run))
            chr_run = 0
        chr_run += 1
        last_chr = char
    data.append((last_chr, chr_run))
    return data[1:]


def parse_data():
    data = []
    with open(f"day{day}.txt", "r") as f:
        data = process_string(f.read().strip())
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1_v2()
    p1_time = time.perf_counter_ns()
    p2 = part_2_v2()
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 2: {p2}\n"""
        f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
