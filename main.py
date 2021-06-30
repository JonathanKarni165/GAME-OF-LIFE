import pygame

from pygame import draw
from pygame import mouse

#constants scalable
WHITE, BLACK = (255,255,255), (0,0,0)
MAX_X = 700
MAX_Y = 500

VOLUME = 20

MAX_TILE_X = int(MAX_X / VOLUME)
MAX_TILE_Y = int(MAX_Y / VOLUME)

pygame.init()

size = (MAX_X, MAX_Y)
screen = pygame.display.set_mode(size)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()

        self.x = x
        self.y = y
        self.width = VOLUME
        self.height = VOLUME

        self.mode = False
        self.change_mode = False

        self.rect = pygame.Rect(x, y, self.width, self.height)

        pygame.draw.rect(screen ,BLACK, self.rect)

    def draw(self):
        color = BLACK
        if self.mode:
            color = WHITE

        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height])

    def switch(self):
        self.mode = not self.mode
        self.draw()

        
    #main game logic
    def update(self, tiles_list, row, col):
        #count live cells around
        cells_alive_around = 0

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                #self tile
                if not(i == 0 and j == 0) and (row + i) >= 0 and (col + j) >= 0:
                    try:
                        if tiles_list[row + i][col + j].mode:
                            cells_alive_around += 1  
                    except:
                        pass
        
        #return cells_alive_around

        #RULE 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        if self.mode and cells_alive_around < 2:
            self.change_mode = True
            return

        #RULE 2: Any live cell with two or three live neighbours lives on to the next generation.
        if self.mode and (cells_alive_around == 1 or cells_alive_around == 2):
            self.change_mode = False
            return 
        
        #RULE 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
        if self.mode and cells_alive_around > 3:
            self.change_mode = True
            return

        #RULE 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        if self.mode is False and cells_alive_around == 3:
            self.change_mode = True
            return          
       
def init():
    tiles_list = [[x for x in range(MAX_TILE_X)] for y in range(MAX_TILE_Y)]

    offset_x = 0
    offset_y = 0
    
    for row in range(MAX_TILE_Y):
        for col in range(MAX_TILE_X):
            new_tile = Tile(offset_x, offset_y, screen)
            tiles_list[row][col] = new_tile

            offset_x += VOLUME
            
        offset_y += VOLUME
        offset_x = 0
        
    
    return tiles_list

def kill_all(tiles_list):
    for row in tiles_list:
        for tile in row:
            tile.mode = False
            tile.draw()

def switch_all(tiles_list):
    for row in tiles_list:
        for tile in row:
            tile.switch()

def update(tiles_list):
    for row in tiles_list:
        for tile in row:
            tile.update(tiles_list, tiles_list.index(row), row.index(tile))

    for row in tiles_list:
        for tile in row:
            if tile.change_mode:
                tile.switch()
                tile.change_mode = False
            tile.draw()


def main():
    pygame.display.set_caption("GAME OF LIFE")

    tiles_list = init()
    pygame.display.flip()

    clock = pygame.time.Clock()
    done = False
    auto_play = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mouse.get_pos()

                for row in tiles_list:
                    for tile in row:
                        if tile.rect.collidepoint(x, y):
                            tile.switch()
                            #print(tile.update(tiles_list, tiles_list.index(row), row.index(tile)))
                            pygame.display.flip()
                            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    update(tiles_list)
                    pygame.display.flip()

                if event.key == pygame.K_RIGHT:
                    auto_play = True
                
                if event.key == pygame.K_c:
                    kill_all(tiles_list)
                    pygame.display.flip()
                
                if event.key == pygame.K_s:
                    switch_all(tiles_list)
                    pygame.display.flip()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    auto_play = False

        if auto_play:
            update(tiles_list)
            pygame.display.flip()
            
           

        
    clock.tick(60)


if __name__ == '__main__':
    main()

