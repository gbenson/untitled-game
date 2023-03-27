from PIL import Image
from PIL.ImageDraw import floodfill

# Output the locations of the dark blue nodes in
# https://commons.wikimedia.org/wiki/File:Graph_based_maze_animation.gif
def main():
    img = Image.open("Graph_based_maze_animation.gif")
    out = img.convert("RGB")
    pal = img.getpalette()
    [node_color] = [i // 3
                    for i in range(0, len(pal), 3)
                    if pal[i:i + 3] == [51, 0, 204]]
    img = img.point(lambda i: i == node_color)
    nodes = []
    for y in range(img.height):
        for x in range(img.width):
            xy = x, y
            if img.getpixel(xy) != 1:
                continue
            node_color = len(nodes) + 2
            floodfill(img, xy, node_color)
            box = img.point(lambda i: i == node_color).getbbox()
            left, upper, right, lower = box
            xy = ((left + right) // 2, (upper + lower) // 2)
            out.putpixel(xy, (255, 0, 0))
            nodes.append(xy)
    print(f"{len(nodes)} nodes: {nodes}")
    out.save("out.png")
    out.show()


if __name__ == "__main__":
    main()
