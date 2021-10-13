import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import math
from timeit import default_timer as timer
from scipy import stats

data = [16, 12, 9, 7, 7, 6, 4.2, 2, 5, 6.5, 7, 12.7, 13, 16, 20]
ds = len(data)

x_data = []
for x in range(ds):
    x_data.append(x)

class Line:
    def __init__(self, m, b):
        self.m = m
        self.b = b

    def data(self, nx):
        d = []
        for x in range(nx):
            d.append(self.m * x + self.b)
        return d

class NFit:
    def __init__(self, co):
        # [c, x, x^2, x^3, ... x^n]
        self.vals = co

    def data(self, nx):
        d = []
        for x in range(nx):
            dsum = self.vals[0]
            for i in range(1, len(self.vals)):
                dsum += self.vals[i] * (x ** i)
            d.append(dsum)
        return d

    def __repr__(self):
        rep = ''
        for i in range(len(self.vals)-1, -1, -1):
            if i > 1:
                rep += '%fx^%d + ' % (self.vals[i], i)
            if i == 1:
                rep += '%fx + ' % (self.vals[i])
            if i == 0:
                rep += '%f' % self.vals[i]
        print(rep)
        return rep

def random_lines(n, slope_range, inter_range):
    l = []
    for i in range(n):
        line = Line(rnd.randrange(slope_range[0], slope_range[1]),
                    rnd.randrange(inter_range[0], inter_range[1]))
        l.append(line)
    return l

def random_nfits(nlines, degree):
    l = []
    for i in range(nlines):
        coefs = []
        for d in range(degree+1):
            coefs.append(rnd.randrange(-max(data), max(data)))
        line = NFit(coefs)
        l.append(line)
        
    return l

def fitness(line):
    s = 0
    ssum = 0
    line_data = line.data(ds)
    for i in range(ds):
        ssum += (line_data[i] - data[i]) ** 2

    s = math.sqrt( (1 / (ds-1)) * ssum)
    return s

def linear_offspring(n, best_line, best_line2):
    new_lines = [best_line, best_line2]

    for i in range(n-2):
        m1 = best_line.m
        b1 = best_line2.b
        if i % 2 == 0:
            m1 = best_line2.m
            b1 = best_line.b
        nl = Line(best_line.m, best_line2.b)
        nl.m += rnd.uniform(-1.0, 1.0)
        nl.b += rnd.uniform(-1.0, 1.0)
        new_lines.append(nl)
    return new_lines

def nonlinear_offspring(n, bl, bl2):
    new_lines = [bl, bl2]

    for i in range(n-2):
        nvals = len(bl.vals)
        nl = NFit([])
        if i % 2 == 0:
            nl.vals = bl.vals[:nvals//2]+bl2.vals[nvals//2:]
        else:
            nl.vals = bl2.vals[:nvals//2]+bl.vals[nvals//2:]

        for n in range(nvals):
            nl.vals[n] += rnd.uniform(-1.0, 1.0)

        new_lines.append(nl)
    return new_lines

def evolution(n, gens, degree):
    #lines = random_lines(n, (-10, 10), (-5, 5))
    lines = random_nfits(n, degree)
    
    for gen in range(gens):
        
        line_scores = []
        for l in lines:
            line_scores.append(fitness(l))    

        best = min(line_scores)
        best_index = line_scores.index(best)
        best_line = lines[best_index]
        line_scores.remove(best)

        best2 = min(line_scores)
        best_index2 = line_scores.index(best2)
        best_line2 = lines[best_index2]
        line_scores.remove(best2)

        #new_lines = linear_offspring(n, best_line, best_line2)
        new_lines = nonlinear_offspring(n, best_line, best_line2)
        lines = new_lines
        
        
    
        
    return lines[0]

def main():

    start = timer()
    best = evolution(100, 100, 2)
    end = timer()
    print('Seconds: %f' % (end - start))

    start = timer()
    slope, intercept, r,p,e = stats.linregress(x_data, data)
    end = timer()
    print('SciPy timer: %f' % (end-start))
    sci_line = Line(slope, intercept)
    plt.plot(sci_line.data(ds), 'g-')
    
    #plt.title('y = %fx + %f' % (best.m, best.b))
    plt.title(str(best))
    plt.plot(best.data(ds))
    plt.plot(data, 'ro')
    
    
    plt.show()

if __name__ == '__main__':
    main()
