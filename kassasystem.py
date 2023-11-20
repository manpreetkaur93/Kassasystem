import datetime

# Produktklassen representerar varje produkt i affären
class Produkt:
    def __init__(self, produktid, pris, pris_typ, produktnamn): # Konstruktor för att skapa en ny produkt
        self.produktid = produktid
        self.pris = pris
        self.pris_typ = pris_typ
        self.produktnamn = produktnamn
        self.kampanjer = [] # En lista för att lagra kampanjer för produkten

    def hamta_kampanjpris(self):  # Metod för att hämta kampanjpriset för produkten baserat på dagens datum
        idag = datetime.datetime.now().strftime("%Y-%m-%d")
        for kampanj in self.kampanjer:
            startdatum, slutdatum, kampanjpris = kampanj
      # Om dagens datum är inom intervallet av kampanjen, returnera kampanjpriset
            if startdatum <= idag <= slutdatum:
                return kampanjpris
     # Om ingen kampanj är aktiv, returnera det vanliga priset
        return self.pris

# Kassaklassen hanterar försäljningen och sparar kvitton
class Kassa:
    kvitton_nummer = 1

    def __init__(self):
        # Konstruktor för att skapa en ny kassa och initiera försäljningslistan
        self.forsaljning = []

    def ny_kund(self):
         # Metod för att börja en ny kundsession genom att återställa försäljningslistan
        self.forsaljning = [] 

    def lagg_till_produkt(self, produkt, antal):
        # Metod för att lägga till en viss mängd av en produkt i försäljningslistan
        for i in range(int(antal)):
            self.forsaljning.append(produkt)

    def betala(self):
      now = datetime.datetime.now()
      formatted_date = now.strftime("%Y%m%d")
    # Öppna filen "kvitto.txt" för att spara kvittot
      with open(f"RECEIPT_{formatted_date}.txt", "a") as fil:
        # Skriv kvittots rubrik med löpnummer och aktuellt datum och tid
        fil.write(f"RECEIPT {Kassa.kvitton_nummer} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Loopar igenom varje produkt i försäljningen och skriver detaljer till filen
        for produkt in set(self.forsaljning):
            # Beräknar antalet sålda enheter av produkten
            antal_sald = self.forsaljning.count(produkt)
            
            # Hämtar kampanjpriset för produkten
            kampanjpris = produkt.hamta_kampanjpris()
            
            # Skriv produktinformationen till filen (produktnamn, sålt antal, kampanjpris, pris_typ)
            fil.write(f"{produkt.produktnamn}\t{antal_sald}\t{kampanjpris}\t{produkt.pris_typ}\n")
            
            # Skriv priset för fler antal av samma produkt
            if antal_sald > 1:
                fil.write(f"Pris för {antal_sald} st: {kampanjpris * antal_sald} kr\n")
        
        # Skriv det totala priset för försäljningen till filen
        totalt_pris = sum(produkt.hamta_kampanjpris() * self.forsaljning.count(produkt) for produkt in set(self.forsaljning))
        fil.write(f"Totalt: {totalt_pris} kr\n\n")
    
      Kassa.kvitton_nummer += 1  # Ökar löpnummer för nästa kvitto


# AdminVerktygsklassen hanterar administration och ändringar i affären
class AdminVerktyg:
    def __init__(self):
        # Konstruktor för att skapa adminverktyget och initiera listan över produkter samt adminlösenordet
        self.produkter = []
        self.lösenord = "admin123"

    def verifiera_admin(self, inmatat_lösenord):
        # Metod för att verifiera admin med inmatat lösenord
        return inmatat_lösenord == self.lösenord

    def lagg_till_produkt(self, produkt):
        # Metod för att lägga till en produkt i listan över produkter
        self.produkter.append(produkt)

    def andra_namn_och_pris(self, produktid, nytt_namn, nytt_pris):
      # Metod för att ändra namn och pris för en specifik produkt
        for produkt in self.produkter:
            if produkt.produktid == produktid:
                produkt.produktnamn = nytt_namn
                produkt.pris = nytt_pris

    def lagg_till_kampanj(self, produkt, startdatum, slutdatum, kampanjpris):
        # Metod för att lägga till en kampanj för en produkt
        produkt.kampanjer.append((startdatum, slutdatum, kampanjpris))

    def ta_bort_kampanj(self, produkt, kampanj):
      # Metod för att ta bort en kampanj från en produkt
        produkt.kampanjer.remove(kampanj)

    def visa_produkter(self):
        # Metod för att visa en lista över alla produkter i affären
        print("Produkter i affären:")
        for produkt in self.produkter:
            print(f"{produkt.produktid} - {produkt.produktnamn}: {produkt.pris} kr/{produkt.pris_typ}")

# Exempel på att skapa produkter och kampanjer
bananer = Produkt("300", 10, "styck", "Bananer")
mjolk = Produkt("301", 15, "förpackning", "Mjölk")
brod = Produkt("302", 20, "styck", "Bröd")
pasta = Produkt("303", 12, "förpackning", "Pasta")
kottfars = Produkt("304", 50, "förpackning", "Köttfärs")

# Skapa adminverktygsobjekt och lägg till produkter och kampanjer
admin = AdminVerktyg()

admin.lagg_till_produkt(bananer)
admin.lagg_till_produkt(mjolk)
admin.lagg_till_produkt(brod)
admin.lagg_till_produkt(pasta)
admin.lagg_till_produkt(kottfars)

# Huvudloopen för programmet
while True:
    print("1. Ny kund")
    print("2. Administrera")
    print("3. Avsluta")
    val = input("Välj ett alternativ: ")

    if val == "1":         # Alternativ för en ny kund och genomföra köp
        admin.visa_produkter()
        kassa = Kassa()
        kassa.ny_kund()
        while True:
           try:
             input_line = input("Ange produktid och antal (0 för att avsluta köp, 'pay' för att betala): ")
             inputs = input_line.split() #denna kommer att splita inputs i listan
        
             if inputs[0] == "0":
              break
             elif inputs[0].lower() == "pay":
              kassa.betala()
              print("Klart! Kvitto sparades")
              break
             produkt_id, antal = inputs[0], inputs[1]  # ändrade funktionen till detta så att två inputs kan tas emot
             produkt = next((p for p in admin.produkter if p.produktid == produkt_id), None)
             if produkt:
              kassa.lagg_till_produkt(produkt, antal)
              print(f"<{produkt_id}> <{antal}>")
             else:
               print("Produkt {} finns inte.".format(produkt_id))
           except (ValueError, IndexError):
                    print("Ogiltig inmatning. Ange både produktid och antal.")

        #kassa.betala()
        #print(f"Kvitto sparades i filen: kvitto.txt")

    elif val == "2":         # Alternativ för administratörsfunktioner
        admin_lösenord = input("Ange admin lösenord: ")
        if admin.verifiera_admin(admin_lösenord):
            print("1. Lägg till kampanj")
            print("2. Ändra produktnamn och pris")
            print("3. Ta bort kampanj")
            print("4. Visa produkter")
            print("5. Tillbaka")
            admin_val = input("Välj ett alternativ: ")

            if admin_val == "1":                 # Lägg till kampanj för en produkt
                admin.visa_produkter()
                produktid = input("Ange produktid för den produkt du vill lägga till kampanj på: ")
                startdatum = input("Ange startdatum för kampanjen (YYYY-MM-DD): ")
                slutdatum = input("Ange slutdatum för kampanjen (YYYY-MM-DD): ")
                kampanjpris = input("Ange kampanjpris: ")
                produkt = next((p for p in admin.produkter if p.produktid == produktid), None)
                if produkt:
                    admin.lagg_till_kampanj(produkt, startdatum, slutdatum, kampanjpris)
                    print("Kampanj tillagd.")
                else:
                    print("Produkt {} finns inte.".format(produktid))
 
            elif admin_val == "2":                   # Ändra namn och pris för en produkt
                admin.visa_produkter()
                produktid = input("Ange produktid för den produkt du vill ändra: ")
                nytt_namn = input("Ange det nya namnet för produkten: ")
                nytt_pris = input("Ange det nya priset för produkten: ")
                admin.andra_namn_och_pris(produktid, nytt_namn, nytt_pris)
                print("Produkten har ändrats.")
                         # Administrera kampanjer för produkter
            elif admin_val == "3":
                         # Visa produkterna för användaren att välja från
                admin.visa_produkter()
                    # Be användaren ange produktid för den produkt de vill ta bort kampanj från
                produktid = input("Ange produktid för den produkt du vill ta bort kampanj från: ")
                     # Hitta produkten med det angivna produktid
                produkt = next((p for p in admin.produkter if p.produktid == produktid), None)
                      # Om produkten och dess kampanjer finns      
                if produkt and produkt.kampanjer:
                    print("Kampanjer för {}:".format(produkt.produktnamn))
                    # Loopa igenom kampanjerna för produkten och visa dem
                    for i, kampanj in enumerate(produkt.kampanjer, 1):
                        startdatum, slutdatum, kampanjpris = kampanj
                        print("{}. {} - {}: {} kr".format(i, startdatum, slutdatum, kampanjpris))
                    # Be användaren välja vilken kampanj de vill ta bort
                    vald_kampanj = int(input("Välj kampanj att ta bort (1-{}): ".format(len(produkt.kampanjer))))
                    # Anropa AdminVerktyg-metoden för att ta bort kampanjen
                    admin.ta_bort_kampanj(produkt, produkt.kampanjer[vald_kampanj - 1])
                    print("Kampanjen har tagits bort.")
                     # Om produkten inte finns
                elif not produkt:
                    print("Produkt {} finns inte.".format(produktid))
                    # Om produkten saknar kampanjer
                else:
                    print("Inga kampanjer att ta bort för {}.".format(produkt.produktnamn))
        
        # Administrera produkter genom att visa dem
            elif admin_val == "4":
                admin.visa_produkter()

        # Gå tillbaka till huvudmenyn
            elif admin_val == "5":
                pass

        # Ogiltigt adminval, be användaren välja igen
            else:
                print("Ogiltigt adminval. Vänligen välj 1, 2, 3, 4 eller 5.")
        
        # Om adminlösenordet är felaktigt
        else:
            print("Felaktigt admin lösenord.")

# Om användaren väljer att avsluta programmet
    elif val == "3":
        break


    else:
        print("Ogiltigt val. Vänligen välj 1, 2 eller 3.")