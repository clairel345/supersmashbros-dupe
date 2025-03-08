
import pygame
import random
import time

# start pygame
pygame.init()

arena_list = [
    'arena.jpeg', 'boxingimg.jpeg', 'ssb_arena.png', 'minecraft_arena.jpeg',
    'mario_kart.jpg'
]

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Kirby vs Panda. A Claire Production")

# Font setup found by ai
font = pygame.font.Font('Gaegu-Bold.ttf', 32)

# Set up the clock
clock = pygame.time.Clock()

running = False


##################     TITLE SCREEN       ####################

arena_img = 'titlepic.jpeg'
instruction = 'instructions.jpeg'

background_img = pygame.image.load(arena_img).convert()

instructionss = pygame.image.load(instruction).convert()
instruction_img = pygame.transform.scale(instructionss, (400, 250))


def playerq(question, x, y):
  showtext = font.render(question, True, (255, 255, 255))
  screen.blit(showtext, (x, y))

def nextbutton():
  global titlescreen
  pygame.draw.rect(screen, (175, 121, 232), (700, 400, 80, 60))
  buttontext = font.render('Play!', True, (0,0,0))
  screen.blit(buttontext, (705, 415))

#makes it a known rectangle for mouse to click on
buttonrect = pygame.Rect(700, 400, 80, 60)


answer1 = ''
answer2 = ''
arena = ''
# ^^ user will fill them out in the titlescreen

titlescreen = True

#so users can press key without pressing specific area
active = False

def linesforinput():
  #first input
  pygame.draw.line(screen, (255,255,255), (270, 48), (410, 48), 2)
  #second input
  pygame.draw.line(screen, (255,255,255), (270, 135), (410, 135), 2)
  #arena
  pygame.draw.line(screen, (255,255,255), (270, 237), (410, 237), 2)
  

firstinput_rect = pygame.Rect(270, 10, 140, 32)
secondinput_rect = pygame.Rect(270, 100, 140, 35)
arenainput_rect = pygame.Rect(270, 200, 140, 37)

try:
  while titlescreen:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        titlescreen = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if buttonrect.collidepoint(pygame.mouse.get_pos()):
          titlescreen = False
          running = True

        if firstinput_rect.collidepoint(
            mouse_pos) or secondinput_rect.collidepoint(
                mouse_pos) or arenainput_rect.collidepoint(mouse_pos):
          active = True

        else:
          active = False
  #ai helped improve the user experience for inputting on screen
      elif event.type == pygame.KEYDOWN:
        if active:  #if mouse on areas for inputs
          if event.key == pygame.K_BACKSPACE:
            # Remove last character from user's input
            if firstinput_rect.collidepoint(pygame.mouse.get_pos()): 
              answer1 = answer1[:-1]
            elif secondinput_rect.collidepoint(pygame.mouse.get_pos()):
              answer2 = answer2[:-1]
            elif arenainput_rect.collidepoint(pygame.mouse.get_pos()):
              arena = arena[:-1]

          else:
            # Add characters to the input seen on the screen
            if firstinput_rect.collidepoint(pygame.mouse.get_pos()):
              answer1 += event.unicode
            if secondinput_rect.collidepoint(pygame.mouse.get_pos()):
              answer2 += event.unicode
            if arenainput_rect.collidepoint(pygame.mouse.get_pos()):
              arena += event.unicode


  #variable for when key is pressed
    keys = pygame.key.get_pressed()

    # resets screen
    screen.fill((255, 255, 255))
    #resets background and player images
    screen.blit(background_img, (0, 0))
    screen.blit(instruction_img, (20,300))


    playerq('Name of Player 1: ', 10, 10)
    #execution came up with ai
    playerq(answer1, 270, 10)

    playerq('Name of Player 2: ', 10, 100)
    playerq(answer2, 270, 100)

    playerq('Arena (Type 1-5): ', 10, 200)
    playerq(arena, 270, 200)

    # Update the screen
    nextbutton()
    linesforinput()
    pygame.display.flip()

    # Cap the frame rate/found method to add time with help of ai
    clock.tick(100)

except Exception as e:
    print(f"An error occurred: {e}")

###########################     GAME       ######################################



#lists asking what name so can say which user wins
names = []
names.append(answer1)
names.append(answer2)

arena_img = 'space.jpeg'

#relates the index to the value
#enumerate learned from ai
for number, pic in enumerate(arena_list):
  try:
    if number == int(arena) - 1:
      arena_img = pic
  except:
    arena_img = 'space.jpeg'


# Load the background image
background_img = pygame.image.load(arena_img).convert()
background_img = pygame.transform.scale(background_img,(screen_width, screen_height))

# Panda
player2 = pygame.image.load('panda.jpeg')
player2_rect = player2.get_rect()

#rescale/resize
player2 = pygame.transform.scale(player2,(114, 120))
player2_rect.centerx = screen_width - 250
player2_rect.centery = screen_height // 2

#new character: kirby
player1 = pygame.image.load('kirby.jpeg')
player1 = pygame.transform.scale(player1, (114, 120))
player1_rect = player1.get_rect()

#coin image
coin = pygame.image.load ('coin.jpeg')
coin = pygame.transform.scale (coin, (50, 50))
coin_rect = coin.get_rect()
coin_rect.center = (screen_width // 2, screen_height // 2)

# Set initial position of the player1
player1_rect.centerx = screen_width - 600
player1_rect.centery = screen_height // 3

#score variables
player1_score = 200
player2_score = 200
winner = "No one"

winning = []


# Move players based on arrow key presses
def player1mvmt():
  if keys[pygame.K_a]:
    player1_rect.x -= one_speed
  if keys[pygame.K_d]:
    player1_rect.x += one_speed
  if keys[pygame.K_w]:
    player1_rect.y -= one_speed
  if keys[pygame.K_s]:
    player1_rect.y += one_speed


def catmvmt():
  if keys[pygame.K_LEFT]:
    player2_rect.x -= two_speed
  if keys[pygame.K_RIGHT]:
    player2_rect.x += two_speed
  if keys[pygame.K_DOWN]:
    player2_rect.y += two_speed
  if keys[pygame.K_UP]:
    player2_rect.y -= two_speed


def renderfirst_score():
  global answer1
#string slicing
  cut_answer1 = answer1[:9]
  firstname_text = font.render(str(cut_answer1), 
    True, (255,255,255))
  player1_score_text = font.render(' Health: '
   + str(player1_score), True, (255, 255, 255))

  screen.blit(firstname_text, (10, 10))
  screen.blit(player1_score_text, (145, 10))


def rendersecond_score():
  global answer2
  cut_answer2 = answer2[:8]
  secondname_text = font.render(str(cut_answer2),True,
    (255,255,255))
  player1_score_text = font.render(' Health: ' 
    + str(player2_score), True,
    (255, 255, 255))
  screen.blit(secondname_text, (480, 10))
  screen.blit(player1_score_text, (600, 10))


rounds = 2

firstwins = 0
secondwins = 0

def playagain():
  pygame.draw.rect(screen, (175, 121, 232), (600, 400, 150, 55))
  againtext = font.render('Play Again', True, (255, 255, 255))
  screen.blit(againtext, (610, 415))


def reset_game():
  global player1_score, player2_score, winner
  # Resets game variables to initial values
  player1_score = 200
  player2_score = 200
  player1_rect.centerx = screen_width - 600
  player1_rect.centery = screen_height // 3
  player2_rect.centerx = screen_width - 250
  player2_rect.centery = screen_height // 2
  game_over(firstwins, secondwins)

  #reloads background image
  screen.blit(background_img, (0, 0))
  pygame.display.flip()
  running = True


def game_over(first_total, second_total):
  global winner, esc_text
  for value in winning:
    if value == 'one':
      first_total += 1
    elif value == 'two':
      second_total += 1

  if first_total > second_total:
    winner = names[0]

  elif second_total > first_total:
    winner = names[1]



  game_over_text = font.render(
      str(winner) + ' is the winner!', True, (255, 255, 255))
  esc_text = font.render("Click Esc to exit", True,
      (255, 255, 255))
  screen.blit(game_over_text, (100, 50))
  screen.blit(esc_text,(140, 200))


def showloss(loser, round):
  youlose_text = font.render(
      str(loser[:10]) + " loses! Time for Round " + str(round), True,
      (255,255,255))
  esc_text = font.render("Click Esc to exit", True,
      (255,255,255))
  screen.blit(youlose_text, (180, 200))
  screen.blit(esc_text, (200, 240))

def winnercount():  #found neater printing method found on ai
  winnercount_text = font.render(f"{firstwins} vs {secondwins}", True,
                                 (255, 255, 255))
  screen.blit(winnercount_text, (350, 10))




#WORKING ON TIMING OF COIN

#timers
show_cointime = 3000 #millisecs
hide_cointime = 1000 #millisecs

#state
show_coin = False
start_time = pygame.time.get_ticks()

#dimensions
coin_width = coin_rect.width
coin_height = coin_rect.height

#figured out with ai
def get_random_position(screen_width, screen_height, coin_width, coin_height):
  x = random.randint(0, screen_width - coin_width)
  y = random.randint(0, screen_height - coin_height)
  return x, y #returns a tuple value for the random coords


def randcoin(show_coin, start_time, show_cointime, hide_cointime, coin_rect, screen_width, screen_height):
  current_time = pygame.time.get_ticks()
  elapsed_time = current_time - start_time

  if show_coin:
    if elapsed_time >= show_cointime:
        show_coin = False
        start_time = current_time
  else:
    if elapsed_time >= hide_cointime:
        show_coin = True
        start_time = current_time
        coin_rect.topleft = get_random_position(screen_width, screen_height, coin_width, coin_height)
  
  return show_coin, start_time

#speed boost stuff for *player 1*
one_fasterspeed = 15
one_normalspeed = 8
one_speed = one_normalspeed

#speed boost stuff for *player 2*
two_fasterspeed = 15
two_normalspeed = 8
two_speed = two_normalspeed

boost_duration = 3000 #how long the boost last
boost_start = None #no boost start active initially; will fill later

game_reset = False

titlepage = True

event = True



#################### Main game loop ###########################################



while running:
  time.sleep(0.1) #it kept showing error without this so

  #makes sure user can quit the game
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Get the keys pressed
  keys = pygame.key.get_pressed()


  player1mvmt()

  catmvmt()

  #fully done by ai but bc randcoin returns show_coin, start_time;..
  #..those variables are being defined rn
  show_coin, start_time = randcoin(
            show_coin, start_time, show_cointime, hide_cointime,
            coin_rect, screen_width, screen_height)


  if keys[pygame.K_1]:
    # Print the coordinates of player1_rect
    onex = player1_rect.x
    oney = player1_rect.y
    print(f"X: {onex}, Y: {oney}")


#python3 performance_task.py

  #prevents player from leaving screen
  if (player1_rect.x < -85):
    player1_rect.x = 770
  if (player1_rect.x > 770):
    player1_rect.x = -85

  if (player2_rect.x > 770):
    player2_rect.x = -85
  if (player2_rect.x < -85):
    player2_rect.x = 770

  if (player1_rect.y > 493):
    player1_rect.y = 493
  if (player1_rect.y < -15):
    player1_rect.y = -15

  if (player2_rect.y > 493):
    player2_rect.y = 493
  if (player2_rect.y < -15):
    player2_rect.y = -15


#harming the players
  if keys[pygame.K_m] and player2_rect.colliderect(player1_rect):
    if player2_rect.right > player1_rect.left and player2_rect.x < player1_rect.x:
      player1_rect.x += 150
      player1_score -= 20
      time.sleep(.2)

    if player2_rect.left < player1_rect.right and player2_rect.x > player1_rect.x:
      player1_rect.x -= 150
      player1_score -= 20
      time.sleep(.2)

  if keys[pygame.K_SPACE] and player1_rect.colliderect(player2_rect):
    if player1_rect.right > player2_rect.left and player1_rect.x < player2_rect.x:
      player2_rect.x += 150
      player2_score -= 20
      time.sleep(.2)
    if player1_rect.left < player2_rect.right and player1_rect.x > player2_rect.x:
      player2_rect.x -= 150
      player2_score -= 20
      time.sleep(.2)

#after a player wins; waits 2 second then resets game adds the player wins to the list
  if (player1_score < 1):
    showloss(answer1, rounds)
    pygame.display.flip()
    time.sleep(2)
    winning.append('two')
    rounds += 1
    secondwins += 1
    game_reset = True
    player1_score = 200
    player2_score = 200


  if (player2_score < 1):
    winning.append('one')
    showloss(answer2, rounds)
    pygame.display.flip()
    time.sleep(2)
    rounds += 1
    firstwins += 1
    game_reset = True
    player1_score = 200
    player2_score = 200

  if firstwins > 2 or secondwins > 2:
    running = False

  if game_reset:
    reset_game()
    game_reset = False

  if keys[pygame.K_1]:
    print(winning)

  if keys[pygame.K_ESCAPE]:
    running = False

  #speed boost things
  if player1_rect.colliderect(coin_rect):
      one_speed = one_fasterspeed
      boost_start = pygame.time.get_ticks()
      show_coin = False
      #start_time = current_time
  
  if player2_rect.colliderect(coin_rect):
      two_speed = two_fasterspeed
      boost_start = pygame.time.get_ticks()
      show_coin = False
      #start_time = current_time

  #chatgpt helped find method
  if boost_start:
    current_time = pygame.time.get_ticks()
    if current_time - boost_start >= boost_duration:
        #determines if its player 1 or 2 that got the boost
        #THIS DOESNT WORK BC THEY COULD BOTH HAVE THE BOOST AHHHHHH
        if one_speed == one_normalspeed:
          two_speed = two_normalspeed

        elif two_speed == two_normalspeed:
          one_speed = one_normalspeed
        boost_start = None #boost start now contains *nothing*


  # Clear the screen
  screen.fill((255, 255, 255))

  screen.blit(background_img, (0, 0))

  if show_coin:
    screen.blit(coin, coin_rect)

  #resets background and player images
  screen.blit(player2, player2_rect)
  screen.blit(player1, player1_rect)

  renderfirst_score()
  rendersecond_score()
  winnercount()
  # Update the display, learned from ai
  pygame.display.flip()

  # Cap the frame rate/found method to add time with help of ai
  clock.tick(100)

############### score/ending screen ################################################

endingg = True

time.sleep(1)

while endingg:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      endingg = False

  keys = pygame.key.get_pressed()

  screen.fill((255, 255, 255))

  if keys[pygame.K_ESCAPE]:
    endingg = False

  #resets background and player images
  screen.blit(background_img, (0, 0))
  game_over(firstwins, secondwins)
  pygame.display.flip()

