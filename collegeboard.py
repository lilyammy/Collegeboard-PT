import pygame, random, sys, math

  #background https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtr83gni_FSycPowjmh7NAET7EFojHmfXg-w&usqp=CAU
  #gift https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM-Qrn-v5aDRfOclTLQGUwoWfaRSnyXgicYQ&usqp=CAU
  #star https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTV-WTE1xi6Pkz8TPElWkdp-znxylRuoQ7qd_GQpUSuNQ&s
  #lava2 https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/aa/Flowing_Lava_%28placeholder_texture%29_LCE2.png/revision/latest?cb=20210621115650
  
  
width = 900
height = 650
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("game")
bgimage = pygame.transform.scale(pygame.image.load('bgpic.jpg').convert(), (900,650))
running = True

#platform   characteristics
plat_width = 150
plat_height = 20
plat_speed = 2
count = 0


#gravity for player
gravity = 1
jump = -10




def color1():
    return (255,0,0)

def color2():
    return (0,255,0)

def color3():
    return(0,0,255)

def random_choice():
    color_functions = [color1,color2,color3]
    random_color_function = random.choice(color_functions)
    return random_color_function()
    


class Baseground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Baseground, self).__init__()
        self.image = pygame.image.load('lava2.jpg').convert()
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (1000,500))
        self.rect = self.image.get_rect(center = (x,y))




class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Platform, self).__init__()
        self.image = pygame.Surface((plat_width,plat_height))
        self.image.convert_alpha()
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = plat_speed

    def update(self):
        self.rect.x += self.vx

        # Reverse direction if platform reaches edge of screen
        if self.rect.right > width or self.rect.left < 0:
            self.vx *= -1
            

class Badplatform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Badplatform, self).__init__()
        self.image = pygame.Surface((plat_width,plat_height))
        self.image.convert_alpha()
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = plat_speed

    def update(self):
        self.rect.x += self.vx

        # Reverse direction if platform reaches edge of screen
        if self.rect.right > width or self.rect.left < 0:
            self.vx *= -1
            
           
   
           
            
            
           
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        self.image = pygame.image.load('star.jpg').convert()
        self.image.set_colorkey((255, 255, 255))
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center = ((random.randint(0,890),random.randint(-650,500))))
        
    def fall(self):
        self.rect.centery += 4
        if self.rect.bottom > 690:
            self.rect =self.image.get_rect(center = ((random.randint(0,890),random.randint(-650,100))))
            


class Gift(pygame.sprite.Sprite):
    def __init__(self):
        super(Gift, self).__init__()
        self.image = pygame.image.load('gift.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center = (random.randint(0,790), random.randint(10,590)))


       
    def relocate(self):
        self.rect.center = (random.randint(10,790), random.randint(10,590))
    
        
       

class Player(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super(Player, self).__init__()
        self.image = pygame.Surface((25,25), pygame.SRCALPHA, 32)
        self.color = color
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 50
        self.vy =0
        self.vx =0
       
       
    def recolor(self):
        self.image.fill(random_choice())
        
  

    #moving and gravity  https://opensource.com/article/19/11/simulate-gravity-python
    def update(self):
        
            
            self.vx = 0 
              
            self.vy += gravity
            self.rect.y += self.vy
           
            
            #Collision - https://www.pygame.org/docs/ref/rect.html?highlight=collide#:~:text=inside%20the%20rectangle.-,For%20collision%20detection%20between%20a%20rect%20and%20a%20line,()%20method%20can%20be%20used.&text=Returns%20true%20if%20any%20portion,()%20method%20can%20be%20used.
            touch_plat = pygame.sprite.spritecollideany(self, platforms)
            if touch_plat:
                if self.vy > 0:
                    self.rect.bottom = touch_plat.rect.top
                    self.vy = 0  # Stop falling
                    self.vy += gravity 
            self.rect.x += self.vx
      
    
            bad_touch = pygame.sprite.spritecollideany(self, badplatforms)
            if bad_touch:
                if self.vy > 0:
                        self.rect.bottom = bad_touch.rect.top
                        self.recolor()
                        self.fall_damage(5)
                        self.vy = 0  # Stop falling
                        self.vy += gravity 
            self.rect.x += self.vx
            
            
            touch_base = pygame.sprite.collide_rect(self, baseground)
            if touch_base:
                self.rect.bottom =baseground.rect.top
                self.vy = 0
                self.image.fill("purple")
                self.fall_damage(2)
                
        


    def fall_damage(self ,damage):
                while self.hp > 0:
                    self.hp = self.hp - damage
                    print(self.hp)
                    if self.color == "purple":
                        self.hp = self.hp -damage+1
                        print(self.hp)
                    return self.hp
                self.kill()
                print("You're dead")
               
                
                
                
 

        

main_sprites = pygame.sprite.Group()
platforms =  pygame.sprite.Group()
badplatforms = pygame.sprite.Group()

obstacle = pygame.sprite.Group()
for i in range(4):
    obstacle.add(Obstacle())


gift = pygame.sprite.Group()
for i in range(3):
    gift.add(Gift())



#https://www.geeksforgeeks.org/python-moving-an-object-in-pygame/
platform1 = Platform(100, height - 100)
platform2 = Platform(width - 300, height - 150)
platform3 = Platform(100, height - 500)
platform4 = Platform(400, height- 400)
badplatform1 = Badplatform(200, height - 200)
badplatform2 = Badplatform(width - 200, height - 350)
badplatform3 = Badplatform(100, height - 500)
badplatforms.add(badplatform1,badplatform2,badplatform3)
platforms.add(platform1, platform2,platform3,platform4)
main_sprites.add(platform1, platform2,platform3,platform4, badplatform1,badplatform2,badplatform3)



player = Player("white",100,150)
main_sprites.add(player)


baseground = (Baseground(500,850))
main_sprites.add(baseground)


    


while running:

    #starter code 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
   
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] and player.rect.centerx >5:
        player.rect.centerx -= 5
    
    
    if keys[pygame.K_d] and player.rect.centerx <900:
        player.rect.centerx += 5
  
    if keys[pygame.K_w] and player.rect.centery >100:
        player.rect.centery == 500
        player.vy = jump
        
  
     
 
                    



    for o in obstacle:
        o.fall()  
        if o.rect.colliderect(player.rect):
            player.kill()
            

    
    for g in gift:
        if g.rect.colliderect(player.rect):
            count += 1
            print("the amount of gifts you've currently collected is", count)
            player.hp += 20
            g.relocate()
            if count == 10:
                running = False
                print("you won")
                
            
            
            
   
                
    main_sprites.update()
          

                

        
   

    screen.blit(bgimage,(0,0))
    platforms.draw(screen)
    main_sprites.draw(screen)
    obstacle.draw(screen)
    gift.draw(screen)
    pygame.display.update()
  

    
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
