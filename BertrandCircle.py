from sympy.geometry import Point, Circle, Line
from Cord import Cord
import math
import random
import matplotlib.pyplot as plt

class BertrandCircle:

    methods = ["Random Endpoints", "Random Radial Method", "Random Midpoint"]

    def __init__(self, center, radius):
        # unit circle centered at (0,0)
        self.x = center[0]
        self.y = center[1]
        self.radius = radius
        self.circle = Circle(Point(self.x, self.y), self.radius)

    def create_random_cord(self, method):

        self.method = method

        line = None
        cord_length = None
        intersection_points = None

        # random cord endpoints
        if method == 1:

            # random angle
            random_a1 = 2 * math.pi * random.uniform(0,1)

            # get x and y of random point on circumference
            x1 = self.radius * math.cos(random_a1)
            y1 = self.radius * math.sin(random_a1)

            random_a2 = 2 * math.pi * random.uniform(0,1)

            # get x and y of another random point on circumference
            x2 = self.radius * math.cos(random_a2)
            y2 = self.radius * math.sin(random_a2)

            # create cord
            line = Line(Point(x1, y1), Point(x2, y2))
            cord_length = math.hypot(x1 - x2, y1 - y2)

            intersection_points = (Point(x1, y1), Point(x2, y2))

        # random radial method
        if method == 2:
            # random angle
            random_a = 2 * math.pi * random.uniform(0,1)
            # random radius
            random_r = random.uniform(0, self.radius)

            # get x and y of random point
            x = random_r * math.cos(random_a) + self.x
            y = random_r * math.sin(random_a) + self.y

            # find perpendicular slope
            m = y / x
            perp_m = -(1 / m)

            # create cord
            line = Line(Point(x, y), slope = perp_m)
            intersect_p1, intersect_p2 = self.circle.intersection(line)[0], self.circle.intersection(line)[1]
            cord_length = math.hypot(intersect_p2.x - intersect_p1.x, intersect_p2.y - intersect_p1.y)

            intersection_points = (intersect_p1, intersect_p2)

        # random midpoint method
        if method == 3:

            # random angle
            random_a = 2 * math.pi * random.uniform(0,1)
            # random radius
            random_r = math.sqrt(random.uniform(0, 1)) * self.radius

            # get x and y of random point
            x = random_r * math.cos(random_a) + self.x
            y = random_r * math.sin(random_a) + self.y

            # find perpendicular slope
            m = y / x
            perp_m = -(1 / m)

            # create cord
            line = Line(Point(x, y), slope = perp_m)
            intersect_p1, intersect_p2 = self.circle.intersection(line)[0], self.circle.intersection(line)[1]
            cord_length = math.hypot(intersect_p2.x - intersect_p1.x, intersect_p2.y - intersect_p1.y)
            intersection_points = (intersect_p1, intersect_p2)

        cord = Cord(line, cord_length, intersection_points)
        return cord

    def generate_cords(self, number_of_cords, method):

        cords = []

        for i in range(number_of_cords):
            cords.append(self.create_random_cord(method))

        # store and return list of cords
        self.cords = cords
        return cords

    def add_cords(self, number_of_cords):
        for i in range(number_of_cords):
            self.cords.append(self.create_random_cord())

    # if circle doesn't touch outside of bigger circle and falls within it
    def within_circle(self, bigger_circle):
        return len(bigger_circle.circle.intersection(self.circle)) <= 1 and math.hypot(self.x - bigger_circle.x, self.y - bigger_circle.y) < bigger_circle.radius

    # returns list of (cut) cords from bigger_circle that pass through this smaller circle
    def filter_cords(self, bigger_circle):

        filtered_cords = []

        for cord in bigger_circle.cords:
            # if cord goes through this circle
            if self.circle.intersection(cord.line):
                intersect_p1, intersect_p2 = self.circle.intersection(cord.line)[0], self.circle.intersection(cord.line)[1]
                cut_cord_length = math.hypot(intersect_p2.x - intersect_p1.x, intersect_p2.y - intersect_p1.y)
                cut_cord = Cord(cord.line, cut_cord_length, (intersect_p1, intersect_p2))
                filtered_cords.append(cut_cord)

        return filtered_cords

    # plot circle using pyplot
    def plot_circle(self):

        plt.ion()
        plt.show()

        circle = plt.Circle((self.x, self.y), self.radius, fill = False)
        # circle2 = plt.Circle((0.5, 0.5), 0.2, color='blue')
        # circle3 = plt.Circle((1, 1), 0.2, color='g', clip_on=False)

        fig, ax = plt.subplots(1, 2) # note we must use plt.subplots, not plt.subplot

        plt.suptitle("Method {method_number} ({method_name})".format(method_number = str(self.method), method_name = self.methods[self.method - 1]))
        ax[0].set(xlim = (-self.x - self.radius, self.x + self.radius), ylim = (-self.y - self.radius, self.y + self.radius))
        ax[0].set_aspect(1)  # 1:1 ratio
        ax[0].add_artist(circle)

        # uncomment to save image
        # fig.savefig('plotcircles.png')

        # fig.canvas.draw()
        # fig.canvas.flush_events()

        # drawing cords
        for cord in self.cords:
            x_range, y_range = [cord.intersection_points[0].x, cord.intersection_points[1].x], [cord.intersection_points[0].y, cord.intersection_points[1].y]
            ax[0].plot(x_range, y_range, color = "red", zorder=1)


        plt.draw()
        plt.pause(0.001)

        self.fig = fig
        self.ax = ax

        return fig, ax

    # plot circle using existing pyplot
    def add_to_plot(self, prev_drawn_circle, og_circle, probabilities, bins):

        # remove previous circle
        if prev_drawn_circle is not None:
            prev_drawn_circle.remove()

        # drawing circle
        circle = plt.Circle((self.x, self.y), self.radius, fill = False, edgecolor = "black", linewidth = 2, zorder = 2)
        drawn_circle = og_circle.ax[0].add_artist(circle)
        og_circle.ax[0].set_title("Circle of radius {radius} centered at ({x}, {y})".format(radius = self.radius, x = str(self.x), y = str(self.y)))

        # histogram draw
        og_circle.ax[1].hist(x = probabilities, bins = bins, color = "blue")
        og_circle.ax[1].set_ylabel("# Circles")
        og_circle.ax[1].set_xlabel("Probability")

        og_circle.fig.subplots_adjust(wspace=1)

        plt.draw()
        plt.pause(0.001)

        return drawn_circle

    def print_probability(self):

        if len(self.cords) == 0:
            print("No cords found")
            return 0

        num_greaterthan_len = 0
        triangle_side_length = 2 * (self.radius * math.cos(math.pi/6))
        for cord in self.cords:
            if cord.length > triangle_side_length:
                num_greaterthan_len += 1

        prob = num_greaterthan_len / len(self.cords)
        print(prob)
        return prob
