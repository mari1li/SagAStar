import pygame
import math
import decimal

pygame.init()

WIDTH, HEIGHT =  1000, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
AU = 149.6e9
G = -6.67428e-11
M =  4.06e6*1.989e30
x_SCALE = 0.09/AU #math.log(AU, 10e10)
y_SCALE = 0.09/AU

#color palette :>
BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
GREEN = (0,255,0)
MAGENTA = (249,132,229)
DARK_GREY = (80, 78, 81)
GranGranie = (220,73,58)

FONT = pygame.font.SysFont("comicsans", 16)

image = pygame.image.load("C:\\Users\\Linh\\Pictures\\Saved Pictures\\blackhole.jpg").convert()
IMAGE_SIZE_X = 50
IMAGE_SIZE_Y = 50
IMAGE_POSITION = ((WIDTH/2) - (IMAGE_SIZE_X/2), (HEIGHT/2) - (IMAGE_SIZE_Y/2))



class Stars:
    TIME = 3600*24*30
    def __init__(self, name, x, y, radius, color, coordinate, realTime): #set up the properties (fields) of an object in class Stars
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.coordinate = coordinate
        self.realTime = realTime
        #self.orbitrad = orbitrad

        self.x_vel = 0
        self.y_vel = 0

        self.orbit = []
        self.Time_period = 0
        self.orbitTurn = 0
        self.orbPeriod = 0

    def timecal(self, Time_period):
        time = self.Time_period
        return time


    def draw(self, win): #loop to draw the individual stars
        x = self.x * x_SCALE + WIDTH/2
        y = self.y * y_SCALE + HEIGHT/2
        
        Period = FONT.render("0", 1, WHITE)
        distance_text = FONT.render(f"{self.y}", 1, WHITE)

        pygame.draw.circle(win, DARK_GREY, (WIDTH/2,HEIGHT/2), 12)
        blackholeImg = pygame.transform.scale(image, (IMAGE_SIZE_X, IMAGE_SIZE_Y))
        win.blit(blackholeImg, IMAGE_POSITION)
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * x_SCALE + WIDTH / 2
                y = y * y_SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

            if self.x > 0 and self. y < 0 and self.orbitTurn == 0:
                self.orbitTurn = 1
            
            if self.x > 0 and self. y > 0 and self.orbitTurn == 1:
                self.orbPeriod = self.timecal(self.Time_period) / (3600 * 24 * 365)
                self.orbitTurn = 2
            
            if self.orbitTurn == 2:
                TimeDisplay = FONT.render(f"{self.name}'s period: {self.orbPeriod:.2f}" + " years", 1, self.color)
                realTime = FONT.render(f"{self.name}'s Calculated period: {self.realTime:.2f}" + " years", 1, self.color)
                Error = (abs(self.orbPeriod - self.realTime)/self.realTime) * 100
                ErrorDis = FONT.render(f"{self.name}'s error: {Error:.2f}" + " %", 1, self.color)
                win.blit(TimeDisplay, (0, self.coordinate))
                win.blit(ErrorDis, (0, self.coordinate+20))
                Justtime = FONT.render("Time: " + f"{(self.Time_period / (3600 * 24 * 365)):.2f}" + " years", 1, GranGranie)
                win.blit(Justtime, (700, 0))

            
            
    def new_position(self): #function updating the position
        distance = math.sqrt(self.x**2 + self.y**2)
        grav_acc = G * M / (distance**2)
        theta = math.atan2(self.y,self.x)
        x_acc = grav_acc * math.cos(theta)
        y_acc = grav_acc * math.sin(theta)
        
        self.x_vel += x_acc * self.TIME
        self.y_vel += y_acc * self.TIME

        self.x += self.x_vel * self.TIME
        self.y += self.y_vel * self.TIME
        self.Time_period += self.TIME

        self.orbit.append((self.x, self.y))

#Run the main function includes all the stars and blackhole
def main():
    run = True
    clock = pygame.time.Clock()
    S1 = Stars("S1",3296*AU,0, 6, WHITE, 0, 94.1) #3296
    S1.y_vel = 1.05e6

    S2 = Stars("S2", 980.8*AU,0, 6, MAGENTA, 50, 15.24) 
    S2.y_vel = 1.92e6

    S8 = Stars("S8", 2632*AU,0, 6, RED, 100, 67.2) 
    S8.y_vel = 1.17e6
    
    S12 = Stars("S12", 2288*AU,0, 6, YELLOW, 150, 54.4) 
    S12.y_vel = 1.25e6

    S13 = Stars("S13", 1752*AU,0, 6, BLUE, 200, 36) 
    S13.y_vel = 1.43e6

    S14 = Stars("S14", 1800*AU,0, 6, GREEN, 250, 38) 
    S14.y_vel = 1.41e6

    stars = [S1,S2,S8,S12,S13,S14] #S1,S2,S8,S12,S13,S14

    while run:
        clock.tick(100) #change the speed of the program
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for star in stars:
            star.new_position()
            star.draw(WIN)

        pygame.display.update()
    
    pygame.quit()


main()

#update the stars position according to their orbital radius
