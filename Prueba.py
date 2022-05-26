import pygame, sys
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 800


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Band')


# define game variables
tile_size = 40
main_menu = True
alive = True
win = False

# load images
try:
    cielo_img = pygame.image.load('img/cielo.png')
    restart_img = pygame.image.load('img/restart.png')
    winner_img = pygame.image.load('img/winner.png')
    start_img = pygame.image.load('img/start.png')
    exit_img = pygame.image.load('img/exit.png')
    band_img = pygame.image.load('img/band.png')
    fondo_img = pygame.image.load('img/fondo.jpg')
    youwin_img = pygame.image.load('img/youwin.png')
    exit2_img = pygame.image.load('img/exit2.png')
except FileNotFoundError and NameError:
    print("Una o varias imagenes no se han podido encontrar en tu computador, porfavor intenta volver a cargarla")

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # dibujar el boton
        screen.blit(self.image, self.rect)

        return action

    def checkpos(self,pos):
        # mouse sobre el boton y el click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True


            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return self.clicked


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, alive):
        dx = 0
        dy = 0
        #velocidad de animacion
        walk_cooldown = 10


        if alive == True:
            #botones
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # animacion
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # gravedad
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, enemy_group, False):
                alive = False

             # check for collision with water
            if pygame.sprite.spritecollide(self, agua_group, False):
                alive = False

            if pygame.sprite.spritecollide(self, moneda_group, False):
                final()


            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        elif alive == False:
            self.image = self.dead_image
            if self.rect.y > 0:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image, self.rect)


        return alive

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/fantasma.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        caja_img = pygame.image.load('img/caja.png')
        suelo_img = pygame.image.load('img/suelo.png')


        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(caja_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(suelo_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    enemy_group.add(enemy)
                if tile == 4:
                    agua = Agua(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    agua_group.add(agua)
                if tile == 5:
                    moneda = Moneda(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    moneda_group.add(moneda)



                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/cangrejo.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Agua(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/agua.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Moneda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.monedas = []
        self.monedas.append(pygame.image.load("img/moneda1.png"))
        self.monedas.append(pygame.image.load("img/moneda2.png"))
        self.monedas.append(pygame.image.load("img/moneda3.png"))
        self.monedas.append(pygame.image.load("img/moneda4.png"))
        self.monedas.append(pygame.image.load("img/moneda5.png"))
        self.monedas.append(pygame.image.load("img/moneda6.png"))
        self.moneda_actual = 0
        self.image = pygame.transform.scale(self.monedas[self.moneda_actual],(tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay = 0

    def update(self):
        if alive == True and self.delay == 8:
            if self.moneda_actual < len(self.monedas)-1:
                self.moneda_actual+=1
            else:
                self.moneda_actual=0
            self.image = pygame.transform.scale(self.monedas[self.moneda_actual],(tile_size, tile_size // 2))
            self.delay = 0
        else:
            self.delay +=1




world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
[1, 0, 0, 0, 0, 2, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 2, 2, 4, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



player = Player(100, screen_height - 130)

#grupos
enemy_group = pygame.sprite.Group()
agua_group = pygame.sprite.Group()
moneda_group = pygame.sprite.Group()


world = World(world_data)

# crear bottones y sus posiciones
restart_button = Button(335, 350, restart_img)
start_button = Button(75, 342, start_img)
exit_button = Button(430, 350, exit_img)

def GAME():


    global alive
    run = True
    while run:

        clock.tick(fps)

        #posicion del cielo
        screen.blit(cielo_img, (0,0))


        #dibujar el mundo en general
        world.draw()


        #si el jugador esta vivo actualice la moneda y los cangrejos
        if alive == True:
            enemy_group.update()
            moneda_group.update()

        #dibujar a la moneda, el agua y los cangrejos
        enemy_group.draw(screen)
        agua_group.draw(screen)
        moneda_group.draw(screen)

        #actualizar los datos de si el jugador esta vivo o no
        alive = player.update(alive)

        #si el jugador muere aparece un boton para reiniciar el juego
        if alive == False:
            restart_button.draw()
            if restart_button.checkpos(pygame.mouse.get_pos()):
                player.reset(100, screen_height - 130)
                alive = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if win == True:
            final()

        #actualizar la pantalla
        pygame.display.update()

    #salir del juego
    pygame.quit()



def final():
    while True:

        screen.blit(fondo_img, (0, 0))
        screen.blit(winner_img, (165, 300))
        screen.blit(youwin_img,(170, 50))
        screen.blit(exit2_img,(600,0))

        time.sleep(3)


        if pygame.MOUSEBUTTONDOWN:
            break

        else:
            continue




def main():
    while True:
        screen.blit(fondo_img, (0, 0))
        screen.blit(band_img, (250, 100))
        pos = pygame.mouse.get_pos()

        # dibujar los botones
        exit_button.draw()
        start_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.checkpos(pos):
                    GAME()

                if exit_button.checkpos(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main()