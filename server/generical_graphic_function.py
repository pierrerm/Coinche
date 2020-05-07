
#GRAPHIC
import pygame

def wait_or_pass(delay):
  """
  delay the programm for the given time in second or press a key to pass the delay
  """
  tic = time.clock()
  while ((time.clock()-tic)<delay) :
    event = pygame.event.poll()
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: #escape
      break





def draw_text(screen, text, position, color=(0,0,0),
                font_type='mono', font_size = 150,
                background_color=(0,125,0)):
    """
    write text in window
    """
    screen.fill(background_color,position)
    font = pygame.font.SysFont(font_type, font_size)
    surface = font.render(text, True, color)
    surface = pygame.transform.scale(surface,(position[2],position[3]))
    screen.blit(surface, position)
    pygame.display.flip()



def get_mouse(surface):
  """
  return true if the mouse in the surface
  """
  mouse=pygame.mouse.get_pos()
  if mouse[0]>surface[0] and mouse[0]<surface[2]+surface[0] and mouse[1]>surface[1] and mouse[1]<surface[1]+surface[3]:
    return True

def graphic_yesorno(screen,question,question_surface,yes_surface,no_surface, background_color=(0,125,0)):#Green
  """
  do you like to "question" ? if click yes -> True if click no -> False
  """
  result=None
  draw_text(screen, text="YES", position=yes_surface ,background_color=background_color)
  draw_text(screen, text="NO", position=no_surface, background_color=background_color)
  draw_text(screen, text=question, position=question_surface, background_color=background_color)


  while result!=True and result!=False :
     event = pygame.event.poll()

     if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
       break

     if get_mouse(yes_surface):
       if  event.type == pygame.MOUSEBUTTONDOWN :
         result=True

     if get_mouse(no_surface):
       if  event.type == pygame.MOUSEBUTTONDOWN :
         result=False


     pygame.display.flip()
  screen.fill(background_color,question_surface)
  screen.fill(background_color,yes_surface)
  screen.fill(background_color,no_surface)
  pygame.display.flip()

  return result