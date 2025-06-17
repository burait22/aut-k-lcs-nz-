from datetime import date

# === Alaposztály: Auto ===
class Auto:
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.elerheto = True

    def __str__(self):
        return f"{self.tipus} ({self.rendszam}) - {self.berleti_dij} Ft/nap"

# === Személyautó ===
class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ulesek_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ulesek_szama = ulesek_szama

# === Teherautó ===
class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

# === Bérlés osztály ===
class Berles:
    def __init__(self, auto, datum: date):
        self.auto = auto
        self.datum = datum

    def __str__(self):
        return f"Bérlés: {self.auto.tipus} ({self.auto.rendszam}), Dátum: {self.datum}, Ár: {self.auto.berleti_dij} Ft"

# === Autókölcsönző osztály ===
class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaad(self, auto):
        self.autok.append(auto)

    def berles_hozzaad(self, rendszam, datum):
        auto = self._keres_auto(rendszam)
        if auto and auto.elerheto and datum >= date.today():
            berles = Berles(auto, datum)
            self.berlesek.append(berles)
            auto.elerheto = False
            print(f"Sikeres bérlés: {berles}")
        elif auto and not auto.elerheto:
            print("Ez az autó jelenleg nem elérhető.")
        else:
            print("Hibás rendszám vagy érvénytelen dátum.")

    def berles_lemondas(self, rendszam):
        for berles in self.berlesek:
            if berles.auto.rendszam == rendszam:
                berles.auto.elerheto = True
                self.berlesek.remove(berles)
                print("Bérlés sikeresen lemondva.")
                return
        print("Nem található ilyen bérlés.")

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincs aktív bérlés.")
        else:
            for berles in self.berlesek:
                print(berles)

    def _keres_auto(self, rendszam):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None

    def listaz_autokat(self):
        for auto in self.autok:
            status = "Elérhető" if auto.elerheto else "Foglalt"
            print(f"{auto} [{status}]")

# === Inicializálás ===
def rendszer_inditasa():
    kolcsonzo = Autokolcsonzo("CityCar Kölcsönző")

    # Autók hozzáadása
    a1 = Szemelyauto("ABC-123", "Toyota Corolla", 10000, 5)
    a2 = Teherauto("DEF-456", "Ford Transit", 15000, 1200)
    a3 = Szemelyauto("GHI-789", "Suzuki Swift", 8000, 4)

    kolcsonzo.auto_hozzaad(a1)
    kolcsonzo.auto_hozzaad(a2)
    kolcsonzo.auto_hozzaad(a3)

    # Bérlések előre feltöltve
    kolcsonzo.berlesek.append(Berles(a1, date(2025, 6, 17)))
    kolcsonzo.berlesek.append(Berles(a2, date(2025, 6, 18)))
    a1.elerheto = False
    a2.elerheto = False

    return kolcsonzo

# === Egyszerű felhasználói interfész ===
def menu(kolcsonzo: Autokolcsonzo):
    while True:
        print("\n--- AUTÓKÖLCSÖNZŐ ---")
        print("1. Autók listázása")
        print("2. Autó bérlése")
        print("3. Bérlés lemondása")
        print("4. Bérlések listázása")
        print("5. Kilépés")

        valasztas = input("Választás: ")

        if valasztas == "1":
            kolcsonzo.listaz_autokat()
        elif valasztas == "2":
            rendszam = input("Adja meg az autó rendszámát: ").strip().upper()
            datum_str = input("Bérlés dátuma (ÉÉÉÉ-HH-NN): ")
            try:
                ev, ho, nap = map(int, datum_str.split("-"))
                datum = date(ev, ho, nap)
                kolcsonzo.berles_hozzaad(rendszam, datum)
            except:
                print("Hibás dátumformátum.")
        elif valasztas == "3":
            rendszam = input("Adja meg a rendszámot a lemondáshoz: ").strip().upper()
            kolcsonzo.berles_lemondas(rendszam)
        elif valasztas == "4":
            kolcsonzo.listaz_berlesek()
        elif valasztas == "5":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás!")

# === Program indítása ===
if __name__ == "__main__":
    kolcsonzo = rendszer_inditasa()
    menu(kolcsonzo)
