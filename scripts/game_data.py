 
class GameData:
    def __init__(self, game=None, json_data=None):
        if json_data:
            self.init_from_json(json_data)
        
        elif game:
            self = game.get_current_game_data()

        else:
            self.game_state = None
            self.player_turn = 0   # 0 host, 1 client

            self.player_strokes = 0
            self.player_direction = 0.0
            self.player_swingspeed = 0.0
            self.player_club = 0
            self.player_backswing = 0.0

            self.ball_pos = (0, 0, 0)
            self.ball_vel = (0, 0, 0)
            self.ball_in_hole = False
    
    def init_from_json(self, json_data):
        self.game_state = json_data.get("game_state", None)
        self.player_turn = json_data.get("player_turn", 0)

        self.player_strokes = json_data.get("player_strokes", 0)
        self.player_direction = json_data.get("player_direction", 0.0)
        self.player_swingspeed = json_data.get("player_swingspeed", 0.0)
        self.player_club = json_data.get("player_club", 0)
        self.player_backswing = json_data.get("player_backswing", 0.0)

        self.ball_pos = tuple(json_data.get("ball_pos", (0, 0, 0)))
        self.ball_vel = tuple(json_data.get("ball_vel", (0, 0, 0)))
        self.ball_in_hole = json_data.get("ball_in_hole", False)

    def to_json(self):
        return {
            "game_state": self.game_state,
            "player_turn": self.player_turn,

            "player_strokes": self.player_strokes,
            "player_direction": self.player_direction,
            "player_swingspeed": self.player_swingspeed,
            "player_club": self.player_club,
            "player_backswing": self.player_backswing,

            "ball_pos": self.ball_pos,
            "ball_vel": self.ball_vel,
            "ball_in_hole": self.ball_in_hole
        }
