def is_hit_diamonds(player_x, player_y, diamond_x, diamond_y):
    if diamond_y - 20 <= player_y + 20:
        if diamond_y + 20 <= player_y - 20:
            return False
        if player_x - 20 <= diamond_x +20 and diamond_x - 20 <= player_x + 20:
            return True
    return False