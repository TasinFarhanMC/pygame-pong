import sys
from typing import Any
import pygame
from pygame.locals import *
from ui import *
import random
import math

TICK_TIME = 1 / 30
WIN_SIZE = 1024, 567

win_sur: pygame.Surface
clock: pygame.time.Clock
running = True
delta_t = 0
scene: Any


class StartScene:
    def __init__(self):
        self.title = Text("Pong", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 128), (WIN_SIZE[0] / 2, 128))
        self.start_but = Button(Text("Start", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 64), (WIN_SIZE[0] / 2, 288)))
        self.quit_but = Button(Text("Quit", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 64), (WIN_SIZE[0] / 2, 384)))

    def handle_events(self, event):
        global running, scene

        mouse_pos = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if self.quit_but.is_hovering(mouse_pos):
                running = False
            elif self.start_but.is_hovering(mouse_pos):
                scene = GameScene()

    def update(self):
        pass

    def render(self):
        global win_sur

        self.title.render(win_sur)
        self.start_but.render(win_sur)
        self.quit_but.render(win_sur)


class GameScene:
    def __init__(self):
        self.player_y = WIN_SIZE[1] / 2 - 60
        self.player_dy = 0
        self.player_dy_stop = False
        self.enemy_y = WIN_SIZE[1] / 2 - 60
        self.enemy_dy = 0
        self.enemy_dy_stop = False
        self.ball_pos = [WIN_SIZE[0] / 2, WIN_SIZE[1] / 2]
        self.ball_vel = [0.0, 0.0]
        self.ball_moving = False
        self.border = pygame.image.load("res/border.png")

        self.player_rect = pygame.Rect(0, 0, 0, 0)
        self.enemy_rect = pygame.Rect(0, 0, 0, 0)
        self.ball_rect = pygame.Rect(0, 0, 0, 0)

        self.player_score = 0
        self.enemy_score = 0
        self.win = False

        self.player_score_text = Text("0", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 64), (WIN_SIZE[0] - 60, 60))
        self.enemy_score_text = Text("0", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 64), (60, 60))
        self.win_text = Text("Red WINS!", pygame.font.Font(
            "res/Comic Marker Deluxe.ttf", 128), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2))

    def start_ball_vel(self, start_dir):
        angle = math.radians(random.uniform(-45, 45))
        self.ball_vel = [
            start_dir * 420 * math.cos(angle),
            420 * math.sin(angle)
        ]

    def handle_events(self, event):
        global running, scene

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                scene = StartScene()
            elif event.key == K_UP:
                if not self.ball_moving:
                    self.start_ball_vel(1)
                    self.ball_moving = True

                self.player_dy -= 420
            elif event.key == K_DOWN:
                if not self.ball_moving:
                    self.start_ball_vel(1)
                    self.ball_moving = True

                self.player_dy += 420
            elif event.key == K_w:
                if not self.ball_moving:
                    self.start_ball_vel(1)
                    self.ball_moving = True

                self.enemy_dy -= 420
            elif event.key == K_s:
                if not self.ball_moving:
                    self.start_ball_vel(1)
                    self.ball_moving = True

                self.enemy_dy += 420
        elif event.type == KEYUP:
            if event.key == K_UP:
                self.player_dy += 420
            elif event.key == K_DOWN:
                self.player_dy -= 420
            elif event.key == K_w:
                self.enemy_dy += 420
            elif event.key == K_s:
                self.enemy_dy -= 420

    def update(self):
        if self.ball_pos[1] <= 0:
            self.ball_pos[1] = 0
            self.ball_vel[1] *= -1
        elif self.ball_pos[1] >= WIN_SIZE[1]:
            self.ball_pos[1] = WIN_SIZE[1]
            self.ball_vel[1] *= -1

        if self.ball_rect.colliderect(self.player_rect):
            self.ball_vel[0] *= -1.0
            self.ball_vel[1] = (
                (self.ball_pos[1] - self.player_rect.top) / 120 - 0.5) * 1320

        if self.ball_rect.colliderect(self.enemy_rect):
            self.ball_vel[0] *= -1.0
            self.ball_vel[1] = (
                (self.ball_pos[1] - self.enemy_rect.top) / 120 - 0.5) * 1320

        if self.ball_pos[0] < 0:
            self.ball_pos = [WIN_SIZE[0] / 2, WIN_SIZE[1] / 2]
            self.start_ball_vel(1)
            self.player_score += 1
            self.player_score_text = Text(str(self.player_score), pygame.font.Font(
                "res/Comic Marker Deluxe.ttf", 64), (WIN_SIZE[0] - 60, 60))
        elif self.ball_pos[0] > WIN_SIZE[0]:
            self.ball_pos = [WIN_SIZE[0] / 2, WIN_SIZE[1] / 2]
            self.start_ball_vel(-1)
            self.enemy_score += 1
            self.enemy_score_text = Text(str(self.enemy_score), pygame.font.Font(
                "res/Comic Marker Deluxe.ttf", 64), (60, 60))

        if self.player_score == 10:
            self.win = True
        elif self.enemy_score == 10:
            self.win = True
            self.win_text = Text("Blue WINS!", pygame.font.Font(
                "res/Comic Marker Deluxe.ttf", 128), (WIN_SIZE[0] / 2, WIN_SIZE[1] / 2))

    def render(self):
        global win_sur, delta_t

        if not self.win:
            self.player_y += self.player_dy * delta_t
            self.enemy_y += self.enemy_dy * delta_t

            self.ball_pos[0] += self.ball_vel[0] * delta_t
            self.ball_pos[1] += self.ball_vel[1] * delta_t

            self.player_rect = pygame.Rect(896, self.player_y, 20, 120)
            self.enemy_rect = pygame.Rect(128, self.enemy_y, 20, 120)
            self.ball_rect = pygame.Rect(
                self.ball_pos[0] - 10, self.ball_pos[1] - 10, 10, 10)
            self.player_score_text.render(win_sur)
            self.enemy_score_text.render(win_sur)
            win_sur.blit(self.border, (WIN_SIZE[0] / 2 - 10, 0))
            pygame.draw.rect(win_sur, pygame.Color("red"), self.player_rect)
            pygame.draw.rect(win_sur, pygame.Color("blue"), self.enemy_rect)
            pygame.draw.circle(win_sur, pygame.Color(
                "yellow"), self.ball_pos, 10)
        else:
            self.win_text.render(win_sur)


def init():
    global win_sur, clock, draw_u, acc_t, title, start_but, scene

    pygame.init()
    pygame.font.init()

    scene = StartScene()

    win_sur = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()


def handle_events():
    global running, scene

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if type(scene) == StartScene:
                    running = False
                else:
                    scene = StartScene()

        scene.handle_events(event)


def main():
    global win_sur, clock, running, delta_t, scene

    init()

    acc_t = 0
    while running:
        while acc_t > TICK_TIME:
            handle_events()
            scene.update()

            if not running:
                break
            acc_t -= TICK_TIME

        delta_t = clock.tick() / 1000
        acc_t += delta_t

        win_sur.fill(pygame.Color("Black"))

        scene.render()

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
