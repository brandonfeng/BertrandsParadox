from BertrandCircle import BertrandCircle
from PIL import Image, ImageDraw
import math
import matplotlib.pyplot as plt
import numpy as np

class ProbabilityPrint:

    def __init__(self):
        pass

    def print_all_probabilities(self, circle):

        og_circle = circle

        prev_drawn_circle = None

        while True:

            # basically histogram
            prob2num_circles = {
                (0, 0.15): 0,
                (0.15, 0.25): 0,
                (0.25, 0.35): 0,
                (0.35, 0.45): 0,
                (0.45, 0.55): 0,
                (0.55, 0.65): 0,
                (0.65, 0.75): 0,
                (0.75, 0.85): 0,
                (0.85, 0.100): 0
            }

            probabilities = []
            prob_bins = [0, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1]

            new_r = circle.radius / 10
            # break into circles no smaller than unit 1 circle
            if new_r < 1:
                break

            x = -circle.radius
            y = circle.radius

            while True:
                smaller_circle = BertrandCircle((x, y), new_r)
                if smaller_circle.within_circle(circle):

                    # printing probability for specific circle
                    print("***Probability for circle centered at {coordinates} with radius {radius}: ".format(coordinates = (x,y), radius = new_r))
                    filtered_cords = smaller_circle.filter_cords(circle)
                    smaller_circle.cords = filtered_cords
                    probability = smaller_circle.print_probability()
                    # filling out dictionary
                    for range in prob2num_circles:
                        if probability >= range[0] and probability < range[1]:
                            prob2num_circles[range] += 1

                    # for histogram
                    # probabilities.append(probability)
                    # self.draw_histogram(og_circle)

                    # printing probability scoreboard
                    print("\n***Scoreboard for circles of radius {radius}".format(radius = new_r))
                    # sort_distributions = dict(sorted(distribution2num_circles.items()))
                    print("\tProbability Range | # Circles")
                    for i in prob2num_circles:
                    # for i in sorted(prob2num_circles.keys()):
        	               print("\t" + str(i) + " | " + str(prob2num_circles[i]))
                    print("")

                    # drawing on plot
                    probabilities.append(probability)
                    prev_drawn_circle = smaller_circle.add_to_plot(prev_drawn_circle, og_circle, probabilities, prob_bins)

                x += 1
                if x > circle.radius:
                    y -= 1
                    x = -circle.radius
                if y < -circle.radius:
                    break


            circle = smaller_circle
