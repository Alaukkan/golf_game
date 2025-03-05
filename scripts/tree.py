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
                    return True
                
        elif self.type == 2:
            
            if dist_sqrd <= 100:
                r = 0.001 * dist_sqrd**2
                tree_top = 27 - r
                tree_bottom = 7 + r

                if ball_y <= tree_top and ball_y >= tree_bottom:
                    return True
                
                elif dist_sqrd <= 1 and ball_y < tree_bottom: # hits the tree trunk
                    self.game.player.ball.hit_tree_trunk()

        return False

    def render(self, surf, offset):
        img = self.game.images[f"trees/{self.type:02}"]
        surf.blit(img, (offset[0] + self.pos_x + self.img_offset[0], offset[1] + self.pos_z + self.img_offset[1]))
