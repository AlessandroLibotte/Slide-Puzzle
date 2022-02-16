import numpy
import cv2
from random import randint, seed
from os import listdir
from sys import exit


class SlidePuzzle:

    img_folder = "src/"

    def __init__(self):
        seed()

    def _reload(self):

        self.img = None

        self.tiles = []
        self.board = []
        self.correct_bard = None

        self.canvas = None

        cv2.namedWindow("Slide Puzzle")
        cv2.setMouseCallback("Slide Puzzle", self._handle_mouse)

    def _load_img(self, img_path):

        self.img = cv2.imread(img_path)
        self.img = self.img[:self.img.shape[1], :]
        new_size = (int(self.img.shape[0] / (self.img.shape[0]/500)), int(self.img.shape[1] / (self.img.shape[1]/500)))
        self.img = cv2.resize(self.img, new_size)

        self.canvas = numpy.zeros((self.img.shape[0], self.img.shape[1], self.img.shape[2]), numpy.uint8)

    def run(self):

        for f in listdir(self.img_folder):

            self._reload()

            self._load_img(self.img_folder + f)

            self._make_tiles()

            self._shuffle()

            try:
                while cv2.getWindowProperty('Slide Puzzle', 0) >= 0:

                    self._draw_canvas()
                    self._display(self.canvas)


                    if cv2.waitKey() == 27:
                        exit()
                    elif cv2.waitKey() == 13:
                        break
            except cv2.error:
                exit()

    def _handle_mouse(self, event, x, y, _, __):

        if event == cv2.EVENT_LBUTTONDOWN:

            pos = (int(x / (self.img.shape[0]/4)), int(y / (self.img.shape[0]/4)))

            for xy in ((-1, 0), (0, 1), (1, 0), (0, -1)):

                if 0 <= pos[0] + xy[0] < 4 and 0 <= pos[1] + xy[1] < 4:

                    if self.board[pos[1] + xy[1]][pos[0] + xy[0]] == 0:

                        self.swap(pos, (pos[0]+xy[0], pos[1]+xy[1]))

                        self._draw_canvas()
                        self._display(self.canvas)

                        return

    def _make_tiles(self):

        tile_size = int(self.img.shape[0]/4)

        index = 0

        for y in range(4):
            self.tiles.append([])
            self.board.append([])
            for x in range(4):
                if x == 0 and y == 0:
                    self.tiles[y].append(numpy.zeros((tile_size, tile_size, 3), numpy.uint8))
                else:
                    self.tiles[y].append(self.img[x * tile_size:(x+1) * tile_size, y * tile_size:(y+1) * tile_size])
                self.board[y].append(index)
                index += 1

        self.correct_bard = self.board

    def _shuffle(self):

        blank_pos = (0, 0)

        prev = None

        for i in range(12):

            m = randint(0, 3)
            d = ((-1, 0), (0, 1), (1, 0), (0, -1))

            while blank_pos[0] + d[m][0] < 0 or blank_pos[0] + d[m][0] > 3 or blank_pos[1] + d[m][1] < 0 or blank_pos[1] + d[m][1] > 3 or d[m-2] == prev:
                m = randint(0, 3)

            self.swap((blank_pos[0] + d[m][0], blank_pos[1] + d[m][1]), blank_pos)

            blank_pos = (blank_pos[0] + d[m][0], blank_pos[1] + d[m][1])

            prev = d[m]

    def swap(self, xy, t_xy):

        temp = self.tiles[xy[0]][xy[1]]
        temp_b = self.board[xy[1]][xy[0]]

        self.tiles[xy[0]][xy[1]] = self.tiles[t_xy[0]][t_xy[1]]
        self.board[xy[1]][xy[0]] = self.board[t_xy[1]][t_xy[0]]

        self.tiles[t_xy[0]][t_xy[1]] = temp
        self.board[t_xy[1]][t_xy[0]] = temp_b

    def _draw_canvas(self):

        def _concatenate_tiles(_tiles):

            columns = []

            for c in _tiles:
                col = c[0]
                for r in c[1:]:
                    col = numpy.concatenate((col, r))
                columns.append(col)

            _canvas = columns[0]

            for c in columns[1:]:
                _canvas = numpy.concatenate((_canvas, c), axis=1)

            return _canvas

        self.canvas = _concatenate_tiles(self.tiles)

        for c in range(len(self.tiles)):
            self.canvas = cv2.line(self.canvas, (c * int(self.img.shape[1]/4), 0), (c * int(self.img.shape[1]/4), self.img.shape[0]), (0, 0, 0), 2)

        for r in range(len(self.tiles[0])):
            self.canvas = cv2.line(self.canvas, (0, r * int(self.img.shape[0]/4)), (self.img.shape[1], r * int(self.img.shape[0]/4)), (0, 0, 0), 2)

    def _display(self, img=None):
        cv2.imshow("Slide Puzzle", self.img if img is None else img)


def main():


    path = r"C:\Users\aless\Pictures\Biglietto un mese franciccina\IMG_20220107_172308.jpg"

    slide_puzzle = SlidePuzzle()
    slide_puzzle.run()


if __name__ == "__main__":
    main()
