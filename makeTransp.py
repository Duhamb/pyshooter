import pygame
screen = pygame.display.set_mode([400,400])
# img = pygame.Surface([400,400]).convert_alpha()
# img.fill([255,255,255])
# array = pygame.surfarray.pixels_alpha(img)
# array[:,:] = 100
# del array
# pygame.image.save(img,"test.png")


# set the default sprites pre-name
default_directory = 'Assets/Images/player/knife/idle/'
default_name = 'survivor-idle_knife_'

# set the total of images
# start at 0
number_of_images = 20

# final folder
directory_to_save = 'new_images/'

# set the new center position based on current position
final_center_position = 105, 113

for i in range(number_of_images):
    current_image_directory = default_directory+default_name + str(i) + '.png'
    image = pygame.image.load(current_image_directory).convert_alpha()
    image_size = image.get_rect().size 
    print(image_size)

    final_size = 2*max([final_center_position[0],image_size[0]-final_center_position[0]]), 2*max([final_center_position[1],image_size[1]-final_center_position[1]])
    background = pygame.Surface(final_size).convert_alpha()
    background.fill([255,255,255])
    array = pygame.surfarray.pixels_alpha(background)
    array[:,:] = 0
    del array

    center_of_new_image = pygame.math.Vector2(background.get_rect().center)
    old_center = pygame.math.Vector2(final_center_position)
    topleft_position = tuple(center_of_new_image - old_center)

    background.blit(image,topleft_position)

    pygame.image.save(background, directory_to_save+default_name+str(i)+'.png')

