def liveDrawVisit(screen, start, end, nodes):
    # Draw visited cells
    for node in nodes:
        row, col = node.position
        color = VISIT
        pygame.draw.rect(screen, color, (col * CELL_SIZE + 1, row * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        if (row, col) == start.position:  # Check if it's the start cell
            font = pygame.font.Font(None, 18)
            text = font.render("S", True, BLACK)  # Black "S" for start cell
            text_rect = text.get_rect(center=((col + 0.5) * CELL_SIZE, (row + 0.5) * CELL_SIZE))
            screen.blit(text, text_rect)
    # Apply changes to the screen
    pygame.display.flip()
