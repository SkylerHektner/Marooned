# Sound_Class.py
# Spring 2016
# Team Windstorm

import pygame.mixer, pygame.time
import random
pygame.mixer.init()

class SoundController(object):
    
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 8192)
        pygame.mixer.init()
        self.HeadHunter = HeadHunter()
        self.WitchDoctor = WitchDoctor()
        self.Brute = Brute()
        self.Music = Music()
        self.Char = Char()
        self.Consumables = Consumables()
        self.firePit = firePit()
        self.TreasureChest = TreasureChest()
        

class Music(object):
    
    def __init__(self):
        self.LoadingMusic = pygame.mixer.Sound('Resources/Sound/Music/loading_music.wav')
        self.PlayingMusic = pygame.mixer.Sound('Resources/Sound/Music/One_eyed_Maestro.wav')
        self.PlayingMusic.set_volume(.25)
        self.DeathMusic = pygame.mixer.Sound('Resources/Sound/death.wav')
        
class Char(object):
    
    def __init__(self):
        self.Damage1 = pygame.mixer.Sound('Resources/Sound/Char/CharDamage1.wav')
        self.Damage2 = pygame.mixer.Sound('Resources/Sound/Char/CharDamage2.wav')
        self.Damage3 = pygame.mixer.Sound('Resources/Sound/Char/CharDamage3.wav')
        self.Damage4 = pygame.mixer.Sound('Resources/Sound/Char/CharDamage4.wav')
        
        self.blunderFire = pygame.mixer.Sound('Resources/Sound/Char/shotgun.wav')
        self.blunderFire.set_volume(.7)
        
        self.swrd_slash1 = pygame.mixer.Sound('Resources/Sound/Char/swrd_slash1.wav')
        self.swrd_slash2 = pygame.mixer.Sound('Resources/Sound/Char/swrd_slash2.wav')
        self.swrd_slash3 = pygame.mixer.Sound('Resources/Sound/Char/swrd_slash3.wav')
        self.swrd_slash4 = pygame.mixer.Sound('Resources/Sound/Char/swrd_slash4.wav')
        
        self.walking = pygame.mixer.Sound('Resources/Sound/Char/walking grass.wav')
        self.walking.set_volume(.2)
        
    def playDamage(self):
        r = random.randint(1,4)
        if r == 1: self.Damage1.play()
        elif r == 2: self.Damage2.play()
        elif r == 3: self.Damage3.play()
        elif r == 4: self.Damage4.play()
    
    def playSlash(self):
        r = random.randint(1,4)
        if r == 1: self.swrd_slash1.play()
        elif r == 2: self.swrd_slash2.play()
        elif r == 3: self.swrd_slash3.play()
        elif r == 4: self.swrd_slash4.play()
        
    def playBlunder(self):
        self.blunderFire.play()
        
    def playWalking(self):
        self.walking.play(loops = -1)
        
    def stopWalking(self):
        self.walking.stop()
    
class HeadHunter(object):
    
    def __init__(self):
        self.Chasing1 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_chasing.wav')
        self.Chasing2 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_chasing2.wav')
        
        self.Damage = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_damage.wav')
        
        self.Notice1 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_notices.wav')
        self.Notice2 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_notices2.wav')
        self.Notice3 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_notices3.wav')
        
        self.Attack1 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_attack.wav')
        self.Attack2 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_attack2.wav')
        self.Attack3 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_attack3.wav')
        self.Attack4 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_attack4.wav')
        self.Attack5 = pygame.mixer.Sound('Resources/Sound/HeadHunter/cannibal_attack5.wav')
        
    def playNotice(self):
        r = random.randint(1,3)
        
        if r == 1: self.Notice1.play()
        elif r == 2: self.Notice2.play()
        elif r == 3: self.Notice3.play()
        
    def playChasing(self):
        r = random.randint(1,1000)
        if r == 30:
            r = random.randint(1,2)
            if r == 1: self.Chasing1.play()
            elif r == 2: self.Chasing1.play()
        
    def playDamage(self):
        self.Damage.play()
        
    def playAttack(self):
        r = random.randint(1,5)
            
        if r == 1: self.Attack1.play()
        elif r == 2: self.Attack2.play()
        elif r == 3: self.Attack3.play()
        elif r == 4: self.Attack4.play()
        elif r == 5: self.Attack5.play()
        
        
class Brute(object):
    
    def __init__(self):
        self.Chasing1 = pygame.mixer.Sound('Resources/Sound/Brute/brute_follows.wav')
        
        self.Damage1 = pygame.mixer.Sound('Resources/Sound/Brute/brute_damaged.wav')
        self.Damage2 = pygame.mixer.Sound('Resources/Sound/Brute/brute_damaged2.wav')
        self.Damage3 = pygame.mixer.Sound('Resources/Sound/Brute/brute_damaged3.wav')
        
        self.Notice1 = pygame.mixer.Sound('Resources/Sound/Brute/brute_notices.wav')
        self.Notice2 = pygame.mixer.Sound('Resources/Sound/Brute/brute_notices2.wav')
        
        self.Attack1 = pygame.mixer.Sound('Resources/Sound/Brute/brute_attacks2.wav')
        self.Attack2 = pygame.mixer.Sound('Resources/Sound/Brute/brute_attacks3.wav')

        
    def playNotice(self):
        r = random.randint(1,2)
        if r == 1: self.Notice1.play()
        elif r == 2: self.Notice2.play()
        
    def playChasing(self):
        r = random.randint(1,1000)
        if r == 30:
            self.Chasing1.play()
        
    def playDamage(self):
        r = random.randint(1,3)
        if r == 1: self.Damage1.play()
        elif r == 2: self.Damage2.play()
        elif r == 3: self.Damage3.play()        
        
    def playAttack(self):
        r = random.randint(1,2)  
        if r == 1: self.Attack1.play()
        elif r == 2: self.Attack2.play()
        
class WitchDoctor(object):
    def __init__(self):
        self.BlowGun = pygame.mixer.Sound('Resources/Sound/WitchDoctor/blow gun.wav')
        
        self.Damage1 = pygame.mixer.Sound('Resources/Sound/WitchDoctor/WitchDoctor_Damage1.wav')
        self.Damage2 = pygame.mixer.Sound('Resources/Sound/WitchDoctor/WitchDoctor_Damage2.wav')
        self.Damage3 = pygame.mixer.Sound('Resources/Sound/WitchDoctor/WitchDoctor_Damage3.wav')
        
        self.Notice = pygame.mixer.Sound('Resources/Sound/WitchDoctor/WitchDoctor_Notice1.wav')
        self.Notice.set_volume(.7)
    
    def playBlowGun(self):
        self.BlowGun.play()
        
    def playDamage(self):
        r = random.randint(1,3)
        if r == 1: self.Damage1.play()
        elif r == 2: self.Damage2.play()
        elif r == 3: self.Damage3.play()    
        
    def playNotice(self):
        self.Notice.play()
        
class firePit(object):
    def __init__(self):
        self.Fire = pygame.mixer.Sound('Resources/Sound/firePit/Fire.wav')
        self.played = False
    
    def playFire(self):
        self.Fire.play(loops = -1, fade_ms = 300)
    
    def stopFire(self):
        self.Fire.fadeout(1500)
        
class Consumables(object):
    def __init__(self):
        self.Gulp = pygame.mixer.Sound('Resources/Sound/Consumables/gulp.wav')
        self.Reload = pygame.mixer.Sound('Resources/Sound/Consumables/reload.wav')
        
    def playGulp(self):
        self.Gulp.play()
    def playReload(self):
        self.Reload.play()
        
class TreasureChest(object):
    def __init__(self):
        self.Win = pygame.mixer.Sound('Resources/Sound/Win.wav')