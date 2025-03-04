import math

class Tree:
    def __init__(self, game, x, z, type):
        self.game = game
        self.pos_x = x
        self.pos_z = z
        self.type = type
        self.img_offset = (-21, -41)

    def check_collision(self, ball_x, ball_y, ball_z):
        dist_sqrd = (self.pos_x - ball_x)**2 + (self.pos_z - ball_z)**2

        if self.type == 1:

            if dist_sqrd <= 38:
                height = 40 - dist_sqrd
                if ball_y <= height:
                    self.game.player.ball.in_tree = True
                    self.game.player.ball.side_spin = 0
                    return
                
        elif self.type == 2:
            pass
        
        self.game.player.ball.in_tree = False

    def render(self, surf, offset):
        img = self.game.images[f"trees/{self.type:02}"]
        surf.blit(img, (offset[0] + self.pos_x + self.img_offset[0], offset[1] + self.pos_z + self.img_offset[1]))
