import pygame

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotate Around Its Own Center")

# Load the image
image = pygame.image.load("graphics/sprites/UI/wind_direction.png").convert_alpha()
original_image = image  # Keep the original for repeated rotations

# Define the visible center of the image
visible_center = (4, 7)  # Relative to the top-left corner of the original image

# Define the screen center
screen_center = (400, 300)  # Center of the screen

# Rotation angle
angle = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Increment the rotation angle
    angle += 1
    angle %= 360  # Keep the angle within 0-359 degrees

    # Rotate the image
    rotated_image = pygame.transform.rotate(original_image, angle)

    # Get the new rect for the rotated image
    rotated_rect = rotated_image.get_rect()

    # Calculate the offset to adjust for the visible center
    offset_x = visible_center[0] - original_image.get_width() // 2
    offset_y = visible_center[1] - original_image.get_height() // 2

    # Adjust the rotated rect to ensure the visible center stays at the screen center
    rotated_rect.center = (
        screen_center[0] - offset_x,
        screen_center[1] - offset_y,
    )

    # Blit the rotated image
    screen.blit(rotated_image, rotated_rect.topleft)

    # Draw the screen center for visualization
    #pygame.draw.circle(screen, (255, 0, 0), screen_center, 5)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
