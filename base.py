import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW


WIDTH = 800
HEIGTH = 300
DOT_SIZE = 10

DELAY = 100

RAND_POS = 27

class Board(Canvas):

    def __init__(self, parent):
        super().__init__(
            width=WIDTH, height=HEIGTH, highlightthickness=0,
            background='black'
        )

        self.parent = parent
        self.ini_game()
        self.pack()

    def ini_game(self):

        self.left, self.right, self.up, self.down = False, True, False, False

        self.in_game = True

        self.dot_x = 100
        self.dot_y = 190

        try:
            self.ibody = Image.open('dot.png')
            self.body = ImageTk.PhotoImage(self.ibody)

            self.ihead = Image.open('dot.png')
            self.head = ImageTk.PhotoImage(self.ihead)

            self.idot = Image.open('dot.png')
            self.dot = ImageTk.PhotoImage(self.idot)
        except IOError as e:
            print(str(e))
            sys.exit(1)

        self.focus_get()
        self.create_objects()
        self.bind_all('<Key>', self.on_key_press)
        self.after(DELAY, self.on_time)

    def create_objects(self):
        # Cria a imagem da comida da cobra
        self.create_image(
            self.dot_x, self.dot_y,
            image=self.dot, anchor=NW, tag='dot'
        )

        # Cria a imagem da cabeça da cobra
        self.create_image(
            50, 50,
            image=self.head, anchor=NW, tag='head'
        )

        # Cria a imagem de 2 pedaços para o corpo da cobra
        self.create_image(
            40, 50,
            image=self.body, anchor=NW, tag='body'
        )
        self.create_image(
            30, 50,
            image=self.body, anchor=NW, tag='body'
        )

    def check_dot(self):
        # Retorna a posição dos objetos no Canvas informados através da tag
        dot = self.find_withtag('dot')
        head = self.find_withtag('head')

        # Verificando sobreposição da cabeça da cobra com a comida
        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, x2, y1, y2)

        for ovr in overlap:
            if dot[0] == ovr:
                x, y = self.coords(head)
                self.create_image(
                    x, y, image=self.body, anchor=NW, tag='body'
                )

            self.locate_dot()

    def locate_dot(self):

        # Busca o ponto comido pela cobra e apaga
        dot = self.find_withtag('dot')
        self.delete(dot[0])

        # Criando coordenadas aleatórias para a nova comida
        r = random.randint(0, RAND_POS)
        self.dot_x = r * DOT_SIZE

        r = random.randint(0, RAND_POS)
        self.dot_y = r * DOT_SIZE

        # Criando imagem da nova comida com as novas coordenadas
        self.create_image(
            self.dot_x, self.dot_y, image=self.dot, anchor=NW, tag='dot'
        )

    def do_move(self):
        bodys = self.find_withtag('body')
        head = self.find_withtag('head')

        items = bodys + head

        k = 0
        while( k < len(items) - 1):
            # Pega as coordenadas das imagens consecutivas
            c1 = self.coords(items[k])
            c2 = self.coords(items[k + 1])

            """
                Altera a posição da imagem pegando o segundo item e colocando
                no lugar do primeiro e assim por diante
            """
            self.move(items[k], c2[0] - c1[0], c2[1]-c1[1])

            k += 1

        """
            Lembre-se que o canvas está representado de cabeça para baixo
            pois está em coordenadas polares, x cresce para direita e o y
            cresce para baixo.
        """

        if self.left:
            self.move(head, -DOT_SIZE, 0)

        if self.right:
            self.move(head, DOT_SIZE, 0)

        if self.up:
            self.move(head, 0, -DOT_SIZE)

        if self.down:
            self.move(head, 0, DOT_SIZE)

    def check_collisions(self):
         # Retorna a posição dos objetos no Canvas informados através da tag
        bodys = self.find_withtag('body')
        head = self.find_withtag('head')

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, x2, y1, y2)

        # Verifica se a cobra colidiu com ela mesma
        for body in bodys:
            for ovr in overlap:
                if body == ovr:
                    self.in_game = False

        # Verifica se a cobra colidiu com as paredes
        if x1 < 0 :
            self.in_game = False

        if x1 > WIDTH - DOT_SIZE:
            self.in_game = False

        if y1 < 0:
            self.in_game = False

        if y1 > HEIGTH - DOT_SIZE:
            self.in_game = False

    def on_key_press(self, e):
        key = e.keysym

        if key == 'Left' and not self.right:
            self.left = True
            self.up, self.down = False, False

        if key == 'Right' and not self.left:
            self.right = True
            self.up, self.down = False, False

        if key == 'Up' and not self.down:
            self.up = True
            self.left, self.right = False, False

        if key == 'Down' and not self.up:
            self.down = True
            self.left, self.right = False, False

    def on_time(self):
        if self.in_game:
            self.check_collisions()
            self.check_dot()
            self.do_move()
            self.after(DELAY, self.on_time)
        else:
            self.game_over()

    def game_over(self):
        self.delete(ALL)
        self.create_text(
            self.winfo_width()/2 , self.winfo_height()/2,
            text='Game Over seu arrombado!',
            fill='Red'
        )


class Snake(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        parent.title('Snake')
        self.board = Board(parent)
        self.pack()



def main():
    root = Tk()
    snake = Snake(root)
    root.mainloop()

if __name__ == '__main__':
    main()
