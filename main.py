import pygame
import asyncio
import sys
import os
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Maximum number of entities
MAX_ENTITIES = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Entity colors
ENTITY_COLORS = {
    "rock": RED,
    "paper": GREEN,
    "scissors": BLUE
}

# Entity class
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((20, 20))
        self.image.fill(ENTITY_COLORS[type])
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = random.randint(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self, all_entities):
        # Find the nearest entity of the type that can be defeated
        nearest_entity = None
        min_distance = float('inf')
        for other_entity in all_entities:
            if other_entity != self and self.can_defeat(other_entity):
                distance = math.sqrt((other_entity.rect.centerx - self.rect.centerx) ** 2 +
                                     (other_entity.rect.centery - self.rect.centery) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_entity = other_entity

        # If a target is found, move towards it
        if nearest_entity:
            dx = nearest_entity.rect.centerx - self.rect.centerx
            dy = nearest_entity.rect.centery - self.rect.centery
            self.angle = math.atan2(dy, dx)

        # Move in the current direction
        self.rect.x += self.velocity * math.cos(self.angle)
        self.rect.y += self.velocity * math.sin(self.angle)

        # Bounce off walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.angle = math.pi - self.angle
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.angle = -self.angle

    def can_defeat(self, other_entity):
        if self.type == "rock" and other_entity.type == "scissors":
            return True
        elif self.type == "paper" and other_entity.type == "rock":
            return True
        elif self.type == "scissors" and other_entity.type == "paper":
            return True
        else:
            return False

# Function to check collision and change entities accordingly
def check_collision(entity, all_entities):
    for other_entity in all_entities:
        if entity != other_entity and entity.rect.colliderect(other_entity.rect):
            if (entity.type == "rock" and other_entity.type == "scissors") or \
               (entity.type == "paper" and other_entity.type == "rock") or \
               (entity.type == "scissors" and other_entity.type == "paper"):
                entity.type = other_entity.type
                entity.image.fill(ENTITY_COLORS[entity.type])
                return

# Function to check if only one color remains
def one_color_remaining(all_entities):
    colors = set()
    for entity in all_entities:
        colors.add(entity.type)
    return len(colors) == 1

# Main function
async def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Rock Paper Scissors")

    # Create a sprite group for entities
    all_entities = pygame.sprite.Group()

    # Create random entities
    for _ in range(MAX_ENTITIES):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        type = random.choice(["rock", "paper", "scissors"])
        entity = Entity(x, y, type)
        all_entities.add(entity)

    clock = pygame.time.Clock()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and one_color_remaining(all_entities):
                # If only one color remains, reset entities
                all_entities.empty()
                for _ in range(MAX_ENTITIES):
                    x = random.randint(0, SCREEN_WIDTH)
                    y = random.randint(0, SCREEN_HEIGHT)
                    type = random.choice(["rock", "paper", "scissors"])
                    entity = Entity(x, y, type)
                    all_entities.add(entity)

        # Update entities
        all_entities.update(all_entities)

        # Check collision and change entities accordingly
        for entity in all_entities:
            check_collision(entity, all_entities)

        # Clear the screen
        screen.fill(WHITE)

        # Draw entities
        for entity in all_entities:
            screen.blit(entity.image, entity.rect)

        # If only one color remains, display reset button
        if one_color_remaining(all_entities):
            font = pygame.font.SysFont(None, 36)
            text = font.render("Click to Reset", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

 

 
        await asyncio.sleep(0)  # Very important, and keep it 0
    pygame.quit()

asyncio.run(main())