#Bibliotecas utilizadas
import pygame
import sys
from PIL import Image
import random

#dimensões do tabuleiro: 3x3
BOARD_SIZE = 3
#varificacao se a jogada está dentro dos limites do tabuleiro
def dentro_limites(x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE
#na classe Tabuleiro estão as funções de jogar, verificar vitória e verificar se o tabuleiro está cheio, 
# bem como a definicao do tamanho do tabuleiro
class Tabuleiro:
    def __init__(self):
        #define o objeto tabuleiro como uma matriz 3x3 vazia
        self.tabuleiro = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    #métopdo para verificar se a jogada está dentro dos limites do tabuleiro, se estiver  e o local 
    # estiver vazio, a jogada é realizada
    def jogar(self, jogador, x, y):
        '''
        Realiza a jogada do jogador na posição (x, y) se estiver dentro dos limites e a posição estiver vazia
        Parâmetros de Entrada: simbolo do jogador ("X" ou "O"), coordenadas x e y
        Saída: True se a jogada foi realizada, False caso contrário
        '''
        if dentro_limites(x, y) and self.tabuleiro[x][y] == "":
            self.tabuleiro[x][y] = jogador
            return True
        return False
    #método para verificar se um jogador venceu. O mverifica linha a linha, coluna a coluna e as diagonais se estão 
    #preenxidas pelo determinado simbolo do jogador
    def verificar_vitoria(self, jogador):
        ''' 
        Verifica se o jogador venceu, linha a linha, coluna a coluna e diagonais
        Entrada: simbolo do jogador ("X" ou "O")
        Saída: True se o jogador venceu, False caso contrário
        '''
        # linhas
        for i in range(BOARD_SIZE):
            if all(self.tabuleiro[i][j] == jogador for j in range(BOARD_SIZE)):
                return True
        # colunas
        for j in range(BOARD_SIZE):
            if all(self.tabuleiro[i][j] == jogador for i in range(BOARD_SIZE)):
                return True
        # diagonal principal
        if all(self.tabuleiro[i][i] == jogador for i in range(BOARD_SIZE)):
            return True
        # diagonal secundária
        if all(self.tabuleiro[i][BOARD_SIZE-1-i] == jogador for i in range(BOARD_SIZE)):
            return True
        return False
    #método para verificar se o tabuleiro está cheio, ou seja, se todas as posições estão preenchidas
    def cheio(self):
        ''' 
        Verifica se o tabuleiro está cheio
        Saída: True se o tabuleiro está cheio, False caso contrário
        '''
        tab_cheio = all(self.tabuleiro[i][j] != "" for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))
        return tab_cheio

# Classe que definime um objeto Computadp. Nessa classe estão os métodos que defininem como o computador deverá
#agir diantes das jogadas do jogador humano
#Defini como uma classe filha do tabuleiro, para que o computador seja capaz de utilizar o método verificar_vitoria, 
#para ser capaz de simular as jogadas antes de realizá-las
class Computador(Tabuleiro):
    def __init__(self, simbolo="O"):
        self.simbolo = simbolo
        self.oponente = "X" # símbolo do jogador humano

    def verificar_possibilidades(self, tabuleiro, jogador):
        ''' 
        Verifica as possibilidades de vitória para o jogador
        Entrada: estado atual do tabuleiro, simbolo do jogador ("O" ou "X")
        Saída: número de possibilidades de vitória  para o jogador'''
        #combinacoes de vitória possíveis
        combinacoes = [
            [(0,0), (0,1), (0,2)],
            [(1,0), (1,1), (1,2)],
            [(2,0), (2,1), (2,2)],
            [(0,0), (1,0), (2,0)],
            [(0,1), (1,1), (2,1)],
            [(0,2), (1,2), (2,2)],
            [(0,0), (1,1), (2,2)],
            [(0,2), (1,1), (2,0)]
        ]
        #veifica qual adversario
        adversario = "O" if jogador == "X" else "X"
        #inicializa o contador de possibilidades
        v = 0
        #verifica no tabuleiro as combinações possíveis de vitória e retorna o contador de possibilidades V
        for comb in combinacoes:
            marcas = [tabuleiro[i][j] for i, j in comb]
            if adversario not in marcas:  
                v += marcas.count(jogador)  # valoriza linhas boas

        return v

    
    def melhor_jogada(self, tabuleiro):
        ''' Determina a melhor jogada para o computador com base na simulacao das jogadass possiveis e 
            naquantidade possivel de vezes que ele pode ganhar
            Entrada: estado atual do tabuleiro
            Saída: coordenadas (x, y) da melhor jogada, priorizando primeiramente a vitória, depois o 
            bloqueio do adversário e, por fim, a jogada com maior pontuação
            '''
        # inicializa variáveis para rastrear a melhor jogada, sua pontuação e a lista de probabilidades
        #definice um score muito baixo para que qualquer jogada seja melhor, mesmo que ela seja menor que zero
        melhor_score = -999
        melhor_movimento = None
        jogada_vitoria = None
        jogada_bloqueio = None
        prob_xo = []

        # Percorre todas as posições do tabuleiro e analisa as possibilidades de vitória para ambos os jogadores
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if tabuleiro.tabuleiro[i][j] == "":
                    Vx = self.verificar_possibilidades(tabuleiro.tabuleiro, "X")
                    Vo = self.verificar_possibilidades(tabuleiro.tabuleiro, "O")
                    prob_xo.append((i, j, Vo - Vx))

        # Executa as simulacões de jogadas para determinar a melhor jogada
        for i, j, score_atual in prob_xo:
            # simula a jogada do computador
            tabuleiro.tabuleiro[i][j] = self.simbolo
            venceu_comp = tabuleiro.verificar_vitoria(self.simbolo)
            tabuleiro.tabuleiro[i][j] = ""

            # simula a jogada do humano
            tabuleiro.tabuleiro[i][j] = "X"
            venceu_humano = tabuleiro.verificar_vitoria("X")
            tabuleiro.tabuleiro[i][j] = ""

            # Decide a melhor jogada com base nas simulações
                    # guarda prioridade
            if venceu_comp:
                jogada_vitoria = (i, j)
            elif venceu_humano:
                jogada_bloqueio = (i, j)
            elif score_atual > melhor_score:
                melhor_score = score_atual
                melhor_movimento = (i, j)

        # decide na ordem de prioridade
        if jogada_vitoria:
            return jogada_vitoria  # prioridade máxima
        elif jogada_bloqueio:
            return jogada_bloqueio
        else:
            return melhor_movimento
    

# Interface implementada utilizando a biblioteca pygame e a biblioteca PIL para exibir gifs animados
#Inicialização do pygame e configuração da tela
pygame.init()
size=(600,600)
FORMAT = "RGBA"
LARGURA, ALTURA = 600, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha")

# Carregar imagens do tabuleiro do jogo e das peças X e O
tabuleiro_img = pygame.image.load("imagens/tabuleiro_jogo.png")
tabuleiro_img = pygame.transform.scale(tabuleiro_img, (LARGURA, ALTURA))

x_img = pygame.image.load("imagens/X.png")
x_img = pygame.transform.scale(x_img, (180, 180))

o_img = pygame.image.load("imagens/O.png")
o_img = pygame.transform.scale(o_img, (180, 180))


# Inicialização do jogo
#inicialliza tabulieor, computador, jogador atual, variavel de controle do loop e vencedor
jogo = Tabuleiro()
computador = Computador(simbolo="O")
jogador_atual = "X"
rodando = True
vencedor = None
# Funções para converter imagens PIL para Pygame e para obter frames de gifs animados
def pil_to_game(img):
    ''' Converte uma imagem PIL para um objeto de imagem Pygame
        Entrada: imagem PIL
        Saída: imagem Pygame'''
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    ''' Obtém um frame específico de um gif animado
        Entrada: imagem PIL (gif), número do frame
        Saída: frame convertido para o formato RGBA'''
    img.seek(frame)
    return  img.convert(FORMAT)

def init():
    '''
    Inicializa o Pygame e configura a tela
    Saída: objeto da tela do Pygame'''
    return pygame.display.set_mode(size)

def main(screen, path_to_image):
    ''' Exibe um gif animado na tela do Pygame
        Entrada: objeto da tela do Pygame, caminho para o arquivo de imagem (gif'
        Saída: None'''
    gif_img = Image.open(path_to_image)
    if not getattr(gif_img, "is_animated", False):
        print(f"Imagem em {path_to_image} não é um gif animado")
        return
    current_frame = 0
    clock = pygame.time.Clock()
    while True:
        frame = pil_to_game(get_gif_frame(gif_img, current_frame))
        frame = pygame.transform.scale(frame, size)  

        screen.blit(frame, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        current_frame = (current_frame + 1) % gif_img.n_frames

        pygame.display.flip()
        clock.tick(10) 

def desenhar():
    ''' Desenha o tabuleiro e as peças na tela do Pygame, e exibe mensagens de vitória ou 
        empate junto com a animação correspondente
        Entrada: None
        Saída: None'''
    TELA.blit(tabuleiro_img, (0, 0))

    # desenha as peças no tabuleiro
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if jogo.tabuleiro[i][j] == "X":
                TELA.blit(x_img, (j * 200 + 10, i * 200 + 10))
            elif jogo.tabuleiro[i][j] == "O":
                TELA.blit(o_img, (j * 200 + 10, i * 200 + 10))
        

    # mensagem de vitória/empate/perdeu
    if vencedor: #o vencedor recebe o valor "X", "O" ou "Empate"
        if vencedor == "X":
            path = 'imagens/Xganhou.gif'
        elif vencedor == "O":
            path = 'imagens/xperdeu.gif'
        else:
            path = 'imagens/Empate.gif'
              
        
        main(TELA, path)# Exibe o gif correspondente ao resultado do jogo
        
        global rodando # controla o loop principal(global define a variavel rodando como global)
        rodando = False
    pygame.time.delay(1000)     
    pygame.display.update() #atualiza a tela
      
   

# Função para determinar a posição do clique do mouse no tabuleiro
def posicao_do_clique(x, y):
    ''' Determina a posição (linha, coluna) do clique do mouse no tabuleiro
        Entrada: coordenadas x e y do clique
        Saída: tupla (linha, coluna)
        '''
    linha = y // 200
    coluna = x // 200
    return linha, coluna

# Loop principal
while rodando:
    # eventos do pygame (entrada do usuário)
    for evento in pygame.event.get(): # pega os eventos do pygame
        if evento.type == pygame.QUIT: #encerra o jogo se a janela for fechada
            rodando = False
            pygame.quit()
            sys.exit()
        #verifica se houve um clique do mouse e se não há vencedor ainda
        if evento.type == pygame.MOUSEBUTTONDOWN and not vencedor:
            x, y = evento.pos
            linha, coluna = posicao_do_clique(x, y)

            # Jogada do humano (X)
            if jogador_atual == "X":
                if jogo.jogar("X", linha, coluna):
                    if jogo.verificar_vitoria("X"):
                        vencedor = "X"
                    elif jogo.cheio():
                        vencedor = "Empate"
                    else:
                        jogador_atual = "O"

    # Jogada do computador (O) se ele nao tiver vencido ainda
    if jogador_atual == "O" and not vencedor:
        jogada = computador.melhor_jogada(jogo)
        if jogada:# se houver uma jogada possível
            i, j = jogada
            jogo.jogar("O", i, j)
            if jogo.verificar_vitoria("O"):
                vencedor = "O"
            elif jogo.cheio():
                vencedor = "Empate"
            else:
                jogador_atual = "X"
    #desenha o tabuleiro e as peças
    desenhar()
