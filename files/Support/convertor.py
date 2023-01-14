# конвертатор картинок в txt файл
from PIL import Image

n = 35
names = list(map(str, range(1, n + 1)))
with open("levels.txt", 'w') as f:
    for name in names:
        a = ""
        image = Image.open("levels/" + name + ".png")
        pixels = image.load()
        x, y = image.size
        cell_size = x // 26
        print(name)
        for i in range(26):
            for j in range(26):
                pixel = pixels[6 + i * cell_size, 6 + j * cell_size][:3]
                if pixel == (0, 0, 0):
                    a += "0"
                elif pixel == (160, 96, 32):
                    a += "1"
                elif pixel == (224, 224, 224):
                    a += "2"
                elif pixel == (0, 64, 32):
                    a += "3"
                elif pixel == (192, 192, 192):
                    a += "4"
                elif pixel == (64, 64, 224):
                    a += "5"
                else:
                    a += "9"
        f.write(a + "\n")
# 0 пусто
# 1 кирпич
# 2 бетон
# 3 куст
# 4 лед
# 5 вода
