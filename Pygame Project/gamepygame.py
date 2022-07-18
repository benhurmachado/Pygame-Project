import pygame
import os
pygame.font.init()
pygame.mixer.init()


pygame.init()
largura, altura = 800, 500
INI = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("STAR WARS SPACESHIP FIGHT")
WHITE = (255, 255, 255)
BLACK = (200, 100, 20)
RED = (255, 0, 0)
YELLOW = (255, 200, 100)

borda = pygame.Rect(largura//2-5, 0, 10, altura)

fonte_vidas = pygame.font.SysFont('Ariel', 20)
fonte_vencedor = pygame.font.SysFont('Ariel', 120)

fps = 60
velo = 2

velocidade_bala = 7
rajada = 3
largura_nave = 50
altura_nave = 38

nome1 = input("Digite o nome do player 1: ")
emailJogador1 = input("Digite o email do player 1: ")

nome2 = input("Digite o nome do player 2: ")
emailJogador2 = input("Digite o email do player 2: ")

hit_a = pygame.USEREVENT + 1
hit_v = pygame.USEREVENT + 2

imagem_navea = pygame.image.load(os.path.join('jogo', 'nave_a.png'))
nave_a = pygame.transform.rotate(pygame.transform.scale(imagem_navea, (largura_nave, altura_nave)), 90)
imagem_navev = pygame.image.load(os.path.join('jogo', 'nave_v.png'))
nave_v = pygame.transform.rotate(pygame.transform.scale(imagem_navev, (largura_nave, altura_nave)), 270)

fundo = pygame.transform.scale(pygame.image.load(os.path.join('jogo', 'fundo.png')), (largura, altura))

def jogo():
    while True:
        nome1
        emailJogador1
        nome2
        emailJogador2
        f = open("historico.txt", "a")
        f.write("\n")
        f.write(nome1)
        f.write("\n")
        f.write(emailJogador1)
        f.write("\n")
        f.write(nome2)
        f.write("\n")
        f.write(emailJogador2)
        f.write("\n")
        f.close()
        break

def hud_game(vermelho, amarelo, tiros_v, tiros_a, vidas_v, vidas_a):
    INI.blit(fundo, (0, 0))
    pygame.draw.rect(INI, BLACK, borda)
    
    vidas_v_text = fonte_vidas.render("VIDAS : " + str(vidas_v), 1, WHITE)
    vidas_a_text = fonte_vidas.render("VIDAS : " + str(vidas_a), 1, WHITE)

    INI.blit(vidas_v_text, (largura - vidas_v_text.get_width() -10, 10))
    INI.blit(vidas_a_text, (10, 10))

    INI.blit(nave_a, (amarelo.x, amarelo.y))
    INI.blit(nave_v, (vermelho.x, vermelho.y))

    for tiros in tiros_v:
        pygame.draw.rect(INI, RED, tiros)
    for tiros in tiros_a:
        pygame.draw.rect(INI, YELLOW, tiros)

    pygame.display.update()


def navea_movi(teclas, amarelo):
    if teclas[pygame.K_a] and amarelo.x - velo > 0:  
        amarelo.x -= velo
    if teclas[pygame.K_d] and amarelo.x + velo + amarelo.width< borda.x:  
        amarelo.x += velo
    if teclas[pygame.K_w] and amarelo.y - velo > 0:  
        amarelo.y -= velo
    if teclas[pygame.K_s] and amarelo.y + velo + amarelo.height < altura - 15:
        amarelo.y += velo


def navev_movi(teclas, vermelho):
    if teclas[pygame.K_LEFT] and vermelho.x - velo > borda.x + borda.width + 10: 
        vermelho.x -= velo
    if teclas[pygame.K_RIGHT] and vermelho.x + velo + vermelho.width < largura:  
        vermelho.x += velo
    if teclas[pygame.K_UP] and vermelho.y - velo > 0: 
        vermelho.y -= velo
    if teclas[pygame.K_DOWN] and vermelho.y + velo + vermelho.height < altura - 15: 
        vermelho.y += velo

def  movi_tiros(tiros_a, tiros_v, amarelo, vermelho):
    for tiros in tiros_a:
        tiros.x += velocidade_bala
        if vermelho.colliderect(tiros):
            pygame.event.post(pygame.event.Event(hit_v))
            tiros_a.remove(tiros)
        elif tiros.x > largura:
            tiros_a.remove(tiros)
            
    for tiros in tiros_v:
        tiros.x -= velocidade_bala
        if amarelo.colliderect(tiros):
            pygame.event.post(pygame.event.Event(hit_a))
            tiros_v.remove(tiros)
        elif tiros.x < 0:
            tiros_v.remove(tiros)

def texto_vencedor(text):
    draw_text = fonte_vencedor.render(text, 1, WHITE)
    INI.blit(draw_text, (largura//2 - draw_text.get_width()/2, altura/2 - draw_text.get_height()/2))
    pygame.display.update()

    pygame.time.delay(5000)

def main():
    vermelho = pygame.Rect(700, 300, largura_nave, altura_nave)
    amarelo = pygame.Rect(100, 300, largura_nave, altura_nave)
    clock = pygame.time.Clock()

    pygame.mixer.music.load('jogo/duelfates.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)

    tiros_v = []
    tiros_a = []

    vidas_v = 10
    vidas_a = 10

    run = True
    while run:
        clock.tick(fps)
        teclas = pygame.key.get_pressed() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(tiros_a) < rajada:
                    tiros = pygame.Rect(amarelo.x + amarelo.width - 20, amarelo.y + amarelo.height//2 + 5, 10, 5)
                    tiros_a.append(tiros)


                if event.key == pygame.K_RCTRL and len(tiros_v) < rajada:
                    tiros = pygame.Rect(vermelho.x, vermelho.y + vermelho.height//2 + 5, 10, 5)
                    tiros_v.append(tiros)
 

            if event.type == hit_v:
                vidas_v -= 1


            if event.type == hit_a:
                vidas_a -= 1


        vencedormsg = ""
        if vidas_v <= 0:
           vencedormsg = "Amarelo Venceu!"
        if vidas_a <= 0:
           vencedormsg = "Vermelho Venceu!"
        if vencedormsg != "":
           texto_vencedor(vencedormsg)
           break

        navea_movi(teclas, amarelo)
        navev_movi(teclas, vermelho)

        movi_tiros(tiros_a, tiros_v, amarelo, vermelho)

        hud_game(vermelho, amarelo, tiros_v, tiros_a, vidas_v, vidas_a)
    jogo()    
    main()

if __name__ == "__main__":
    main()
