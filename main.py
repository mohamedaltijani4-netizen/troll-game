import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Troll Platformer - Mobile Edition")

# Clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 120, 255)
RED = (230, 50, 50)
BLACK = (30, 30, 30)
GREEN = (50, 200, 100)
GRAY = (200, 200, 200)

class Player:
    def __init__(self):
        self.width = 30
        self.height = 40
        self.x = 100
        self.y = 450
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_strength = -12
        self.gravity = 0.6
        self.is_jumping = False

    def handle_input(self):
        self.vel_x = 0
        
        # Keyboard controls (for testing on PC)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed

        # Touch/Mouse controls (for Android APK)
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < SCREEN_WIDTH // 3:  # Touch left third of screen
                self.vel_x = -self.speed
            elif mouse_x > (SCREEN_WIDTH // 3) * 2:  # Touch right third
                self.vel_x = self.speed

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_strength
            self.is_jumping = True

    def update(self, platforms):
        self.x += self.vel_x
        if self.x < 0: self.x = 0
        if self.x > SCREEN_WIDTH - self.width: self.x = SCREEN_WIDTH - self.width

        self.vel_y += self.gravity
        self.y += self.vel_y

        self.is_jumping = True
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for plat in platforms:
            if player_rect.colliderect(plat.rect):
                if plat.is_trap:
                    plat.triggered = True

                if not plat.triggered:
                    if self.vel_y > 0 and player_rect.bottom - self.vel_y <= plat.rect.top:
                        self.y = plat.rect.top - self.height
                        self.vel_y = 0
                        self.is_jumping = False

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))

class Platform:
    def __init__(self, x, y, w, h, is_trap=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.is_trap = is_trap
        self.triggered = False

    def draw(self, surface):
        if self.is_trap and self.triggered:
            return 
        color = RED if self.is_trap else BLACK
        pygame.draw.rect(surface, color, self.rect)

def draw_mobile_controls(surface):
    # Draw faint lines to show players where to touch
    pygame.draw.line(surface, GRAY, (SCREEN_WIDTH // 3, 0), (SCREEN_WIDTH // 3, SCREEN_HEIGHT), 2)
    pygame.draw.line(surface, GRAY, ((SCREEN_WIDTH // 3) * 2, 0), ((SCREEN_WIDTH // 3) * 2, SCREEN_HEIGHT), 2)
    
    font = pygame.font.SysFont(None, 24)
    surface.blit(font.render("< LEFT", True, GRAY), (20, 50))
    surface.blit(font.render("JUMP", True, GRAY), (SCREEN_WIDTH // 2 - 20, 50))
    surface.blit(font.render("RIGHT >", True, GRAY), (SCREEN_WIDTH - 80, 50))

def main():
    player = Player()
    
    platforms = [
        Platform(0, 520, 800, 80),   
        Platform(200, 400, 150, 20), 
        Platform(400, 300, 150, 20, is_trap=True), # Drops when touched!
        Platform(650, 200, 120, 20), 
        Platform(700, 150, 30, 50)   
    ]

    goal_rect = pygame.Rect(710, 100, 20, 50)

    while True:
        screen.fill(WHITE)
        draw_mobile_controls(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Jump if touching the middle third of the screen
                if SCREEN_WIDTH // 3 <= mouse_x <= (SCREEN_WIDTH // 3) * 2:
                    player.jump()

        player.handle_input()
        player.update(platforms)

        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        if player_rect.colliderect(goal_rect):
            pygame.quit()
            sys.exit()

        for plat in platforms:
            plat.draw(screen)

        pygame.draw.rect(screen, GREEN, goal_rect)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
