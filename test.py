from BertrandCircle import BertrandCircle
from ProbabilityPrint import ProbabilityPrint
import matplotlib.pyplot as plt

bertrand_circle = BertrandCircle((0, 0), 10)
method = 3
num_cords = 100
cords = bertrand_circle.generate_cords(num_cords, method)
print("*** Finished generating cords for original circle with method {method} ***".format(method = method))
print("Probability = ")
bertrand_circle.print_probability()
bertrand_circle.plot_circle()

prob_print = ProbabilityPrint()
prob_print.print_all_probabilities(bertrand_circle)

# hack - to keep plot up - probably better way
while True:
    pass
