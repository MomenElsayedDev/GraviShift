import arcade
import random

# --- Global Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "GraviShift: The Inversion Logic"

CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5

# Game States
STATE_START = 0
STATE_GAME = 1
STATE_WIN = 2


class MusicLooper:
    """Helper class to loop music"""

    def __init__(self, sound):
        self.sound = sound
        self.player = None

    def play(self):
        if self.player is None or not self.player.playing:
            self.player = arcade.play_sound(self.sound)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Game state and level tracking
        self.current_state = STATE_START
        self.time_elapsed = 0.0
        self.current_level = 0
        self.total_levels = 4

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.exit_list = None
        self.particles_list = None

        self.player_sprite = None
        self.physics_engine = None

        self.score = 0
        self.gravity_direction = 1  # 1 = normal, -1 = inverted

        # --- Load sounds ---
        self.jump_sound = arcade.load_sound("sounds/RobotSound.wav")
        self.coin_sound = arcade.load_sound("sounds/CoinSound.wav")
        self.win_sound = arcade.load_sound("sounds/Win.wav")
        self.final_win_sound = arcade.load_sound("sounds//GameWin.wav")
        self.start_click_sound = arcade.load_sound("sounds/CoinSound.wav")
        self.menu_music = arcade.load_sound("sounds/Main.wav")
        self.game_music = arcade.load_sound("sounds/GameMusic.wav")
        self.menu_looper = None
        self.game_looper = None

        # --- UI Text ---
        self.ui_title = arcade.Text(
            "GraviShift",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 70,
            arcade.color.NEON_GREEN,
            70,
            bold=True,
            anchor_x="center",
        )
        self.ui_subtitle = arcade.Text(
            "The Inversion Logic",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.AQUA,
            24,
            italic=True,
            anchor_x="center",
        )
        self.ui_start_prompt = arcade.Text(
            "Press ENTER to Start",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.WHITE,
            18,
            anchor_x="center",
        )
        self.ui_score = arcade.Text(f"Score: 0", 20, 550, arcade.color.WHITE, 16)
        self.ui_instruction = arcade.Text(
            "SPACE TO FLIP GRAVITY", 80, 450, arcade.color.GOLD, 14, bold=True
        )
        self.ui_win_label = arcade.Text(
            "VICTORY REACHED!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 20,
            arcade.color.GOLD,
            50,
            bold=True,
            anchor_x="center",
        )
        self.ui_restart_prompt = arcade.Text(
            "Press ENTER to Play Again",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 60,
            arcade.color.WHITE,
            20,
            anchor_x="center",
        )

    def setup(self):
        """Setup game: sprite lists, player, physics, level"""
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.exit_list = arcade.SpriteList()
        self.particles_list = arcade.SpriteList()

        self.score = 0
        self.gravity_direction = 1
        self.ui_score.text = f"Score: {self.score}"

        # Load the first level
        self.load_level(self.current_level)

        # Create player sprite
        self.player_sprite = arcade.Sprite(
            "assets/Robot.png",
            CHARACTER_SCALING,
        )
        self.player_sprite.center_x = 80
        self.player_sprite.center_y = 250
        self.player_list.append(self.player_sprite)

        # Physics engine for platforming
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, gravity_constant=GRAVITY
        )

    def load_level(self, level):
        """Load level data: walls, coins, exit"""
        self.wall_list.clear()
        self.coin_list.clear()
        self.exit_list.clear()

        # --- Floor and Ceiling: green tiles ---
        for x in range(0, SCREEN_WIDTH + 1, 64):
            # Floor
            floor = arcade.Sprite("assets/Grass.png", TILE_SCALING)
            floor.center_x = x
            floor.center_y = 97
            self.wall_list.append(floor)

            # Ceiling
            ceiling = arcade.Sprite(
                "assets/GrassFlip.png", TILE_SCALING
            )
            ceiling.center_x = x
            ceiling.center_y = SCREEN_HEIGHT - 90
            self.wall_list.append(ceiling)

        # --- Level-specific platforms and coins ---
        if level == 0:
            for y in range(96, 300, 64):
                block = arcade.Sprite(
                    ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
                )
                block.center_x = 400
                block.center_y = y
                self.wall_list.append(block)
            coin = arcade.Sprite(":resources:images/items/gold_1.png", 0.6)
            coin.center_x = 600
            coin.center_y = 150
            self.coin_list.append(coin)
            exit_x, exit_y = 740, 115
        elif level == 1:
            for x in range(200, 600, 64):
                platform = arcade.Sprite(
                    ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
                )
                platform.center_x = x
                platform.center_y = 200
                self.wall_list.append(platform)
            coin = arcade.Sprite(":resources:images/items/gold_1.png", 0.6)
            coin.center_x = 400
            coin.center_y = 250
            self.coin_list.append(coin)
            exit_x, exit_y = 740, 115
        elif level == 2:  # Skip deleted level
            self.current_level += 1
            self.load_level(self.current_level)
            return
        elif level == 3:
            for y in range(100, 500, 128):
                wall = arcade.Sprite(
                    ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
                )
                wall.center_x = 400
                wall.center_y = y
                self.wall_list.append(wall)
            coin = arcade.Sprite(":resources:images/items/gold_1.png", 0.6)
            coin.center_x = 200
            coin.center_y = 450
            self.coin_list.append(coin)
            exit_x, exit_y = 740, 115
        elif level == 4:  # Final level
            for x in range(100, 700, 128):
                platform = arcade.Sprite(
                    ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
                )
                platform.center_x = x
                platform.center_y = 300
                self.wall_list.append(platform)
            coin = arcade.Sprite(":resources:images/items/gold_1.png", 0.6)
            coin.center_x = 600
            coin.center_y = 350
            self.coin_list.append(coin)
            exit_x, exit_y = 740, 115

        # --- Exit door ---
        self.exit_door = arcade.Sprite(
            "assets/Exit.png", 0.8
        )
        self.exit_door.center_x = exit_x
        self.exit_door.center_y = exit_y
        self.exit_list.append(self.exit_door)

    def create_explosion(self, x, y):
        """Create particle effect at (x, y)"""
        for i in range(60):
            particle = arcade.SpriteCircle(5, arcade.color.YELLOW)
            particle.center_x = x
            particle.center_y = y
            particle.change_x = random.uniform(-6, 6)
            particle.change_y = random.uniform(-6, 6)
            self.particles_list.append(particle)

    def on_draw(self):
        """Render the screen"""
        self.clear()
        if self.current_state == STATE_START:
            arcade.set_background_color((15, 15, 35))
            self.ui_title.draw()
            self.ui_subtitle.draw()
            if int(self.time_elapsed * 2) % 2 == 0:
                self.ui_start_prompt.draw()
            if self.menu_music and self.menu_looper is None:
                self.menu_looper = MusicLooper(self.menu_music)
            if self.menu_looper:
                self.menu_looper.play()
        elif self.current_state == STATE_GAME:
            arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
            self.wall_list.draw()
            self.coin_list.draw()
            self.exit_list.draw()
            self.player_list.draw()
            self.ui_score.draw()
            self.ui_instruction.draw()
            if self.game_music and self.game_looper is None:
                self.game_looper = MusicLooper(self.game_music)
            if self.game_looper:
                self.game_looper.play()
        elif self.current_state == STATE_WIN:
            self.wall_list.draw()
            self.player_list.draw()
            self.particles_list.draw()
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0, 0, 0, 160)
            )
            self.ui_win_label.draw()
            self.ui_restart_prompt.draw()

    def on_update(self, delta_time):
        """Update game logic"""
        self.time_elapsed += delta_time
        if self.current_state == STATE_WIN:
            self.particles_list.update()
            return
        if self.current_state != STATE_GAME:
            return

        self.physics_engine.update()

        # Prevent player from leaving screen
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

        # Check for coin collection
        coins_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 100
            self.ui_score.text = f"Score: {self.score}"
            arcade.play_sound(self.coin_sound)

        # Check for exit collision
        if arcade.check_for_collision(self.player_sprite, self.exit_door):
            # Different sound for final level
            if self.current_level == self.total_levels - 1:
                arcade.play_sound(self.final_win_sound)
            else:
                arcade.play_sound(self.win_sound)
            self.create_explosion(self.exit_door.center_x, self.exit_door.center_y)
            self.current_level += 1
            if self.current_level >= self.total_levels:
                self.current_state = STATE_WIN
            else:
                self.player_sprite.center_x = 80
                self.player_sprite.center_y = 100
                self.menu_looper = None
                self.game_looper = None
                self.load_level(self.current_level)

    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if self.current_state in [STATE_START, STATE_WIN]:
            if key == arcade.key.ENTER:
                arcade.play_sound(self.start_click_sound)
                self.current_level = 0
                self.menu_looper = None
                self.game_looper = None
                self.setup()
                self.current_state = STATE_GAME
            return

        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            arcade.play_sound(self.jump_sound)
            # Flip gravity
            self.gravity_direction *= -1
            self.physics_engine.gravity_constant = GRAVITY * self.gravity_direction
            self.player_sprite.angle = 180 if self.gravity_direction == -1 else 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


if __name__ == "__main__":
    game = MyGame()
    arcade.run()
