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

# For an acute triangle (all angles smaller than a right angle), the
# circumcenter always lies inside the triangle.
#
# For a right triangle, the circumcenter always lies at the midpoint
# of the hypotenuse.
#
# For an obtuse triangle (a triangle with one angle bigger than a
# right angle), the circumcenter always lies outside the triangle.
#
# https://en.wikipedia.org/wiki/Circumscribed_circle#Location_relative_to_the_triangle
#
# When two vectors are at right angles to each other the dot product is zero.

# https://www.mathsisfun.com/algebra/vectors-dot-product.html
def is_circumcentre_within_triangle(a, b, c):
    for p, q, r in ((c, a, b), (a, b, c), (b, c, a)):
        qpx = p.x - q.x
        qpy = p.y - q.y
        qrx = r.x - q.x
        qry = r.y - q.y
        if qpx * qrx + qpy * qry <= 0:
            return False
    return True
