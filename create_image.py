from PIL import Image

c = 75
s = input('From: ')
t = input('To: ')
img = Image.open(s)
img = img.convert('RGBA')
width = img.size[0]
height = img.size[1]
pix = img.load()
for i in range(width):
    for j in range(height):
        if abs(pix[i, j][0] - 240) < c and abs(pix[i, j][1] - 240) < c and abs(pix[i, j][2] - 240) < c:
            pix[i, j] = (pix[i, j][0], pix[i, j][1], pix[i, j][2], 0)
img.save(t)
