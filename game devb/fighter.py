import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player  = player
        self.size = data[0]       
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_image(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.max_energy = 100
        self.energy = self.max_energy
        self.energy_regen_rate = 0.09   # Energy points regenerated per update       
        self.health_regen_rate = 0.05   # Health points regenerated per update

    def load_image(self, sprite_sheet, animation_steps):
        # Extract img from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        print(animation_list)
        return animation_list

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0    
        self.running = False
        self.attack_type = 0
        
        # tombol untuk game
        key = pygame.key.get_pressed()

        # HANYA BISA BEKERJA JIKA LAGI TIDAK MELAKUKAN ATTACK
        if self.attacking == False and self.alive == True and round_over == False:
            #Check for player 1 control
            if self.player == 1:
            #   MOVEMENT
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED 
                    self.running = True 
                # jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if (key[pygame.K_c] or key[pygame.K_v]) and self.energy >= 8:
                    self.attack(target)
                    # determize which attack type was used
                    if key[pygame.K_c]:
                        self.attack_type = 1
                    if key[pygame.K_v]:
                        self.attack_type = 2
                    
             #Check for player 2 control
            if self.player == 2:
            #   MOVEMENT
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED 
                    self.running = True 
                # jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if (key[pygame.K_KP2] or key[pygame.K_KP3]) and self.energy >= 8:
                    self.attack(target)
                    # determize which attack type was used
                    if key[pygame.K_KP2]:
                        self.attack_type = 1
                    if key[pygame.K_KP3]:
                        self.attack_type = 2


        # MEMASUKAN GRAFITI
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        
        # ensure player face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
       
        # update posisi player
        self.rect.x += dx 
        self.rect.y += dy
    
    # handle animation 
    def update(self):
        # Regenerate energy over time
        if self.energy < self.max_energy:
            self.energy += self.energy_regen_rate
            if self.energy > self.max_energy:
                self.energy = self.max_energy

        # Regenerate health over time if not attacking
        if not self.attacking and self.alive:
            self.health += self.health_regen_rate
            if self.health > 100:
                self.health = 100
        
        # check what action player perform
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) # death animation
        elif self.hit:
            self.update_action(5) # hit animaton
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3) # attack1
            elif self.attack_type == 2:
                self.update_action(4) # attack 2
        elif self.jump:
            self.update_action(2) # jump animation
        elif self.running:
            self.update_action(1) # running animation
        else:
            self.update_action(0) # idle animation

        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check time last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check animation finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if player death then end animaton
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check animasi sudah di executed
                if self.action in [3, 4]:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check damage was taken
                if self.action == 5:
                    self.hit = False
                    # if the player middle attack
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0 and self.energy >= 10:
            # execute attacl
            self.attacking = True
            self.attack_sound.play()
            self.energy -= 10
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(self, new_action):
        # check new action different
        if new_action != self.action:
            self.action = new_action
            # update animation setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
