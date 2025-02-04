import os
from PIL import Image
from database import get_user, update_user_level_xp, update_profile_image, remove_profile_image

class User:
    def __init__(self):
        user_data = get_user()
        if user_data:
            (self.id, self.name, self.user_class, self.race, self.level, self.xp, self.max_xp, self.dark_mode, self.profile_image) = user_data
        else:
            self.id = None
            self.name = ""
            self.user_class = ""
            self.race = ""
            self.level = 0
            self.xp = 0
            self.max_xp = 100
            self.dark_mode = False
            self.profile_image = None

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp += 100
        update_user_level_xp(self.level, self.xp, self.max_xp)

    def save_profile_image(self, uploaded_file):
        # Erstelle Ordner für Profilbilder, falls nicht vorhanden
        os.makedirs('profile_images', exist_ok=True)
        
        # Speicherpfad für das Bild
        image_path = f'profile_images/user_{self.id}_profile.png'
        
        # Bild öffnen und quadratisch zuschneiden
        with Image.open(uploaded_file) as img:
            # Bestimme die kürzere Seite für quadratischen Zuschnitt
            min_side = min(img.size)
            # Berechne Beschneidungsbox
            left = (img.width - min_side) / 2
            top = (img.height - min_side) / 2
            right = left + min_side
            bottom = top + min_side
            
            # Bild zuschneiden und auf 200x200 skalieren
            img = img.crop((left, top, right, bottom))
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            
            # Als PNG speichern
            img.save(image_path, 'PNG')
        
        # Pfad in Datenbank speichern
        update_profile_image(image_path)
        self.profile_image = image_path

    def delete_profile_image(self):
        if self.profile_image and os.path.exists(self.profile_image):
            os.remove(self.profile_image)
        remove_profile_image()
        self.profile_image = None


