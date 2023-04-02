from .point import Point

# https://en.wikipedia.org/wiki/Circumscribed_circle#Circumcenter_coordinates
def circumcentre(a, b, c):
    """Return the circumcentre of the triangle with vertices a, b and c."""
    ax2Pay2 = a.x**2 + a.y**2
    bx2Pby2 = b.x**2 + b.y**2
    cx2Pcy2 = c.x**2 + c.y**2
    byMcy, cyMay, ayMby = b.y - c.y, c.y - a.y, a.y - b.y
    oOD = 0.5 / (a.x * byMcy + b.x * cyMay + c.x * ayMby)
    return Point((oOD * (ax2Pay2 * byMcy +
                         + bx2Pby2 * cyMay
                         + cx2Pcy2 * ayMby),
                  oOD * (ax2Pay2 * (c.x - b.x) +
                         + bx2Pby2 * (a.x - c.x)
                         + cx2Pcy2 * (b.x - a.x))))
