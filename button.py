import pygame
# импорт библиотек
class Button:   # объявляем класс
    def __init__(self, x, y, width, height, text, image_path, hover, sound, color):  # Функция инициализации
        # класс кнопок принимает на вход последовательные значения:
        # расположение x и y ; ширину и высоту кнопки; текст на кнопке, если нужен;
        # ссылка на картинку кнопки или переменная содержащая её;
        # ссылка на изображения выделенной кнопки; звук, цвет(если не надо - чёрный)
        # ПЕРЕПРИСВАЕМ ПЕРЕМЕННЫЕ
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_img = self.image
        if hover:
            self.hover_img = pygame.image.load(hover)
            self.hover_img = pygame.transform.scale(self.hover_img, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        self.is_hovered = False

    def draw(self, screen):  # рисуем текст на кнопке
        current_img = self.hover_img if self.is_hovered else self.image
        screen.blit(current_img, self.rect.topleft)

        font = pygame.font.Font('FONTS/menu/Involve-SemiBold.ttf', 24)
        text_surface = font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):   # проверяем вхождение мыши в область кнопки
        self.is_hovered = self.rect.collidepoint(mouse_pos)  # Проверяем входит ли мышка в область кнопки

    def handle_event(self, event):  # проверяем была ли нажата левая кнопка мыши для взаимодействия с кнопкой
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()   # в случае нажатия проигрываем звук
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
