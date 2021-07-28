import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

imgfile = sys.argv[1]
candy_number = sys.argv[2]
outfile = open(sys.argv[2] + ".txt", "w")

for keymap in plt.rcParams:
    if "keymap." in keymap:
        plt.rcParams[keymap] = ''

fig, ax = plt.subplots()
out = []

def onkey(event):
    if event.key in ['u']:  # undo
        print("UNDO removed", out.pop())
    else:
        print(event.key, event.xdata, event.ydata)
        color = 'w'
        if event.key in ['w', 'y']:
            color = "k"
        plt.text(event.xdata, event.ydata, event.key.upper(), color = color,
                horizontalalignment='center', verticalalignment='center')
        plt.draw()
        out.append('%s\t%0.1f\t%0.1f' % (event.key.upper(), event.xdata, event.ydata))

img = mpimg.imread(sys.argv[1])
imgplot = plt.imshow(img)
cid = fig.canvas.mpl_connect('key_press_event', onkey)
plt.show()

outfile.write("\n".join(out))
outfile.close()


