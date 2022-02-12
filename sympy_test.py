from sympy import Point, Circle, Line, Ray
p1, p2, p3 = Point(0, 0), Point(5, 5), Point(6, 0)
p4 = Point(4,0)
c1 = Circle(p1, 5)
print(c1.intersection(p2))
print(c1.intersection(p4))
