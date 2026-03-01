import config
import pygame
# screen layout
# Information
score_info_pos = (config.WIDTH * 0.05, config.HEIGHT * 0.05, config.WIDTH  / 100 * 15, config.HEIGHT / 100 * 8)
time_info_pos = (config.WIDTH * 0.80, config.HEIGHT * 0.05, config.WIDTH  / 100 * 15, config.HEIGHT / 100 * 8)
# Game Map
outer_circle_radius = int(config.WIDTH // 2)
inner_circle_radius = int(outer_circle_radius // 6)
judge_circle_radius = int(inner_circle_radius * 1.5)

circle_center_x, circle_center_y = config.WIDTH // 2, config.HEIGHT

level_dict = {1:5, 2:7, 3:9}

# event ID
GAME2_TIMER_ALERT = pygame.event.Event(pygame.event.custom_type())

level_info_dict = {
    "level_1":{
        "time":90,
        "pass_score":300,
        "marble_speed":10,
        "marble_map":{
            "1":[0,1,0,0,2,0,0,1,0,0,2,0,0,1,0,2,0,0,0,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "2":[0,0,1,0,0,2,0,0,2,0,0,1,0,1,0,2,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "3":[0,0,0,1,0,0,2,0,0,1,0,0,2,0,0,0,0,1,0,2,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }
    },
    "level_2":{
        "time":90,
        "pass_score":500,
        "marble_speed":10,
        "marble_map":{
            "1":[],
            "2":[],
            "3":[]
        }
    },
    "level_3":{
        "time":90,
        "pass_score":500,
        "marble_speed":10,
        "marble_map": {
            "1":[],
            "2":[],
            "3":[]
        }
    }
}