"""Ovo je čisti kod na žgance, nisam radio funkcije niti klase itd jer sam tulipan i pygame je težak :/.
Što se tiče samog kola sreće, napisani su komentari na većini i piše što šta radi
Random nagrada kada se zaustavi kolo je pohranjena u varijablu 'nagrada' te se može povući tako da se cijeli kod stavi pod funkciju i pozove se kad treba
Sve nagrade su u stringu što znači da kad se povuće nagrada treba provjeriti dali je 'isdigit', ako je super pretvori se broj 
i zbraja se i igrac i funkcija se ponovno pokrece, ako se okrene na bankrot nije 'isdigit'  
te se brisu svi bodovi igraca i prelazi se na slj igraca itd. itd. """

import pygame
import math
import random

def get_nagrada():
    global nagrada
    if nagrada.isdigit():

        return int(nagrada)
    else:
        return 0

def paliKolo():
    pygame.init()
    global nagrada
    # Dimenzije prozora
    duljina_prozora = 800
    sirina_prozora = 600

    # Radijus i pozicija Kolo sreća
    kolo_srece_centar = (duljina_prozora // 2 , sirina_prozora // 2 - 65)
    kolo_srece_radius = 200

    # Definiranje sekcija
    broj_sekcija = 16
    kut_sekcija = 360 / broj_sekcija
    boja_sekcija = []

    # Nagrade na kolu sreće
    nagrade = ["100", "250",  "BT", "500", "5",  "1000", "50", "25", "200",  "10", "700","1", "25", "2500", "75", "900"]
    nagrade_poligoni = {}
    sekcija_kolizija = []

    # Postavljanje glavnog prozora
    screen = pygame.display.set_mode((duljina_prozora, sirina_prozora))
    pygame.display.set_caption("Spinning Wheel Game")

    # Random boje za sekcije kola sreće
    for i in range(1, broj_sekcija + 1):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        boja_sekcija.append((r, g, b))

    # Varijable za aniamciju okretanja kola sreće
    rotation_angle = 0
    spinning = False
    spins = 0
    stop_section = None
    landed_value = None
    rotation_speed = 4

    # Definiranje teksta za gumb "SPIN"
    font = pygame.font.Font(None, 36)
    font_nagrade = pygame.font.Font(None, 72)
    spin_button_text = font.render("SPIN", True, (0, 0, 0))
    spin_button_rect = spin_button_text.get_rect(center=kolo_srece_centar)
    text_positions = {}

    # FPS
    clock = pygame.time.Clock()


    while True:
        #klasično dohvaćanje eventa za quit opciju
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #dohvaćanje miša
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not spinning and spin_button_rect.collidepoint(event.pos):
                    spinning = True
                    spins = 0
                    stop_section = None
                    landed_value = None
                    prize_text = font_nagrade.render("", True, (0, 0, 0))  # Clear prize text

        screen.fill((255, 255, 255))

        # Crtanje kola sreće
        for i in range(broj_sekcija):
            #računanje točaka za crtanje poligona - trokuta
            start_angle = math.radians(i * kut_sekcija + rotation_angle)
            end_angle = math.radians((i + 1) * kut_sekcija + rotation_angle)

            start_point = (kolo_srece_centar[0] + kolo_srece_radius * math.cos(start_angle),
                        kolo_srece_centar[1] + kolo_srece_radius * math.sin(start_angle))

            end_point = (kolo_srece_centar[0] + kolo_srece_radius * math.cos(end_angle),
                        kolo_srece_centar[1] + kolo_srece_radius * math.sin(end_angle))
            
            #crtanje trokuta
            poligon = pygame.draw.polygon(screen, boja_sekcija[i], [kolo_srece_centar, start_point, end_point])
            
            #crtanje linije na rubovima poligona kako bi se snjima provjeravala kolizija sa pokazivačem, 
            #što omogućuje okretanje na random sekciju
            kolizija_linije = pygame.draw.line(screen, (0, 0, 0), start_point , end_point, 2)

            #Svaka linija je pohranjena u dict: Nagrada glumi ključ, dok je svaka linija trokuta value
            nagrade_poligoni[nagrade[i]] = kolizija_linije

            # Mali crni kružići na rubovima spoja trokuta
            pygame.draw.circle(screen, (0, 0, 0), (int(start_point[0]), int(start_point[1])), 4)
            pygame.draw.circle(screen, (0, 0, 0), (int(end_point[0]), int(end_point[1])), 4)

            #pokazivac
            pokazivac = pygame.draw.polygon(screen, (0, 0, 0), [(592, 235), (625, 220), (625, 250)])

            # Upsivanje nagrada iz liste nagrade na sekcije odnosno trokute
            #TODO: nikako ne mogu napraviti da se tekst rotira zajedno sa svojom sekcijom, pa ako itko drugi ima ideju super 
            top_midpoint_x = (start_point[0] + end_point[0]) // 4 + 200
            top_midpoint_y = (start_point[1] + end_point[1]) // 4 + 115

            text_positions[i] = (top_midpoint_x, top_midpoint_y)

            text_surface = font.render(nagrade[i], True, (0, 0, 0))

            text_rect = text_surface.get_rect(center=text_positions[i])
            screen.blit(text_surface, text_rect)

        # Gumb "SPIN"
        pygame.draw.circle(screen, (255, 0, 0), kolo_srece_centar, 40)
        screen.blit(spin_button_text, spin_button_rect)

        #Rotacija sekcija
        if spinning:
            # Rotate the wheel at a constant speed
            rotation_angle += rotation_speed
            spins += 1

            if spins >= random.randint(250, 350):  #Ovo nije 250 spinova, samo sam namjestio dda bude relativno normalno, pokušavam još shvatit logiku
                spinning = False
                #prolazi se kroz riječnik sa nagradama i linijama te se  sa colliderrect provjerava da li postoji kolizija kada se kolo zaustavi
                for key, value in nagrade_poligoni.items():
                    if pokazivac.colliderect(value):
                        #kad dođe do podudaranja, nagrada - odnosno key iz riječnika se pohranjuje u varijablu nagrada.
                        #TU možemo baciti return nagrada kada se ovaj kod pretvori u funkciju.
                        nagrada = key
                        print(nagrada)
                        break

        pygame.display.update()
        clock.tick(60)  # Frame rate - 60 FPS