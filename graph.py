class Graph:
    def __init__(self, orientovany=False):
        self.orientovany = orientovany
        self.uzly = []
        self.hrany = []  # hrana bude ulozena jako [odkud, kam, vaha]

    def add_node(self, uzel):
        if uzel not in self.uzly:
            self.uzly.append(uzel)

    def add_edge(self, u, v, vaha=None):
        # pokud uzly jeste nejsou v grafu, pridame je
        self.add_node(u)
        self.add_node(v)
        self.hrany.append([u, v, vaha])

    def remove_node(self, uzel):
        if uzel in self.uzly:
            self.uzly.remove(uzel)
        
        # prefiltrujeme hrany, aby tam nezustaly ty se smazanym uzlem
        nove_hrany = []
        for h in self.hrany:
            if h[0] != uzel and h[1] != uzel:
                nove_hrany.append(h)
        self.hrany = nove_hrany

    def remove_edge(self, u, v):
        for h in self.hrany:
            if self.orientovany:
                if h[0] == u and h[1] == v:
                    self.hrany.remove(h)
                    break
            else:
                if (h[0] == u and h[1] == v) or (h[0] == v and h[1] == u):
                    self.hrany.remove(h)
                    break

    # Pomocna metoda pro ziskani sousedu uzlu
    def get_neighbors(self, uzel):
        sousede = []
        for h in self.hrany:
            if h[0] == uzel:
                if h[1] not in sousede:
                    sousede.append(h[1])
            elif not self.orientovany and h[1] == uzel:
                if h[0] not in sousede:
                    sousede.append(h[0])
        return sousede

    def analyze(self):
        print("--- ANALYZA GRAFU ---")
        pocet_uzlu = len(self.uzly)
        pocet_hran = len(self.hrany)
        print("Pocet uzlu:", pocet_uzlu)
        print("Pocet hran:", pocet_hran)

        # 1. Orientovany
        if self.orientovany:
            print("Orientovany: Ano")
        else:
            print("Orientovany: Ne")

        # 2. Ohodnoceny (jestli ma aspon jedna hrana zadanou vahu)
        ohodnoceny = False
        for h in self.hrany:
            if h[2] is not None:
                ohodnoceny = True
                break
        if ohodnoceny:
            print("Ohodnoceny: Ano")
        else:
            print("Ohodnoceny: Ne")

        # 3. Smycky (hrana z uzlu do stejneho uzlu)
        ma_smycky = False
        for h in self.hrany:
            if h[0] == h[1]:
                ma_smycky = True
                break
        if ma_smycky:
            print("Ma smycky: Ano")
        else:
            print("Ma smycky: Ne")

        # 4. Souvislost (zkusime projit graf od prvniho uzlu)
        souvisly = True
        if pocet_uzlu > 0:
            navstivene = [self.uzly[0]]
            fronta = [self.uzly[0]]

            while len(fronta) > 0:
                aktualni = fronta.pop(0)
                for h in self.hrany:
                    # kontrolujeme spojeni obema smery
                    soused = None
                    if h[0] == aktualni:
                        soused = h[1]
                    elif h[1] == aktualni:
                        soused = h[0]
                    
                    if soused is not None and soused not in navstivene:
                        navstivene.append(soused)
                        fronta.append(soused)

            if len(navstivene) != pocet_uzlu:
                souvisly = False

        if souvisly:
            print("Souvisly: Ano")
        else:
            print("Souvisly: Ne")

        # 5. Planarita (Eulerova podminka E <= 3V - 6)
        planarni = True
        if pocet_uzlu >= 3:
            if pocet_hran > (3 * pocet_uzlu - 6):
                planarni = False
        if planarni:
            print("Planarni: Ano")
        else:
            print("Planarni: Ne")

        # 6. Chromaticke cislo (hladove obarvovani uzlu)
        if ma_smycky:
            print("Chromaticke cislo: Nelze urcit (graf ma smycky)")
        elif pocet_uzlu == 0:
            print("Chromaticke cislo: 0")
        else:
            barvy = {}  # slovnik uzel: cislo_barvy
            for uzel in self.uzly:
                pouzite_barvy = []
                # zjistime barvy okolnich uzlu
                for h in self.hrany:
                    soused = None
                    if h[0] == uzel and h[1] != uzel:
                        soused = h[1]
                    elif h[1] == uzel and h[0] != uzel:
                        soused = h[0]
                    
                    if soused in barvy:
                        pouzite_barvy.append(barvy[soused])

                # najdeme nejmensi moznou barvu (od 1 vyse), kterou sousede nemaji
                barva = 1
                while barva in pouzite_barvy:
                    barva += 1
                barvy[uzel] = barva

            max_barva = max(barvy.values())
            print("Chromaticke cislo:", max_barva)
        print("---------------------\n")


# --- Zkouska funkcnosti ---
if __name__ == "__main__":
    g = Graph(orientovany=False)
    
    # Pridani uzlu a hran
    g.add_edge("A", "B", 10)
    g.add_edge("B", "C", 5)
    g.add_edge("C", "A", 8)
    g.add_edge("C", "D", 12)

    g.analyze()

    # Zkouska se smyckou
    g2 = Graph(orientovany=True)
    g2.add_edge(1, 2)
    g2.add_edge(2, 2)  # smycka
    g2.analyze()