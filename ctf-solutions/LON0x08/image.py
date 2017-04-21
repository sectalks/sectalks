from PIL import Image
image = Image.open("download.png")
w, h = image.size
im = image.load()

arr = ['0']

for i in range(h):
      for j in range(w):
          rgb = im[j,i]
          if (rgb[0] != rgb[1]):
              if (rgb[1] != rgb[2]):
                  arr.append('0')
              else:
                  arr.append('1')

def chunks(l, n):
        return (l[i:i+n] for i in xrange(0, len(l), n))

result = [chr(int(''.join(i), 2)) for i in chunks(arr, 8)]

print(''.join(result))
