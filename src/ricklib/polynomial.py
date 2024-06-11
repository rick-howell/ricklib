# Polynomial library

# Author: Rick Howell
# rick.howell.arts@gmail.com

class Polynomial:
    '''A class for polynomials. The coefficients are stored in a list, with the index corresponding to the power of x. For example, the polynomial 3x^2 + 2x + 1 would be stored as [1, 2, 3].'''

    def __init__(self, coefficients: list):
        self.coefficients = coefficients
        self.degree = len(coefficients) - 1

    def save(self, filename: str):
        with open(filename, 'w') as f:
            for c in self.coefficients:
                f.write(f'{c}\n')

    def load(self, filename: str):
        with open(filename, 'r') as f:
            self.coefficients = [float(line) for line in f]
            self._update_degree()

    def __call__(self, x: float) -> float:
        return sum([self.coefficients[i] * x ** i for i in range(self.degree + 1)])
    
    def _update_degree(self):
        self.degree = len(self.coefficients) - 1

    def __add__(self, other):
        '''Add two polynomials together'''

        if isinstance(other, (int, float, complex)):
            other = Polynomial([other])

        new_poly = [0.0] * (max(self.degree, other.degree) + 1)

        for i in range(self.degree + 1):
            new_poly[i] += self.coefficients[i]

        for i in range(other.degree + 1):
            new_poly[i] += other.coefficients[i]

        return Polynomial(new_poly)
    
    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        '''Multiply two polynomials together, or a polynomial with a scalar'''

        if isinstance(other, (int, float, complex)):
            return Polynomial([x * other for x in self.coefficients])
        
        # Note, deg(PQ) = deg(P) + deg(Q)
        result = [0] * (self.degree + other.degree + 1)
        for i in range(self.degree + 1):
            for j in range(other.degree + 1):
                result[i + j] += self.coefficients[i] * other.coefficients[j]

        return Polynomial(result)
    
    def __rmul__(self, other):
        return self * other
    
    def __str__(self):
        return ' + '.join([f'{self.coefficients[i]}x^{i}' for i in range(self.degree + 1)])
    
    def __repr__(self):
        return str(self)
    
    def differentiate(self):
        '''Differentiate the polynomial'''
        return Polynomial([i * self.coefficients[i] for i in range(1, self.degree + 1)])
    
    def integrate(self):
        '''Integrate the polynomial'''
        return Polynomial([self.coefficients[i] / (i + 1) for i in range(self.degree + 1)] + [0])
    
    def __eq__(self, other):
        return self.coefficients == other.coefficients
    

def _lag_basis(x_values: list, j: int) -> Polynomial:
    '''Returns l_j (x)'''

    l = Polynomial([1])

    for m in range(0, len(x_values)):
        if m != j:
            weight = 1 / (x_values[j] - x_values[m])
            l *= Polynomial([-x_values[m] * weight, 1 * weight])

    return l

def lagrange_interpolation(points: list) -> Polynomial:
    '''Returns the Lagrange interpolation polynomial for the given points

    points: list of tuples of the form [(x1, y1), (x2, y2), ...]

    Returns: Polynomial object representing the Lagrange interpolation polynomial
    '''

    x_values = [p[0] for p in points]
    y_values = [p[1] for p in points]

    L = Polynomial([0])

    for j in range(len(x_values)):
        L += y_values[j] * _lag_basis(x_values, j)

    return L


def _test():
    a = Polynomial([1, 1])
    b = Polynomial([3, 1])
    print(a * b)

    p1 = Polynomial([1, 2, 3])
    p2 = Polynomial([4, 5, 6])
    print(f'p1 = {p1}')
    print(f'p2 = {p2}')
    print(f'p1 + p2 = {p1 + p2}')
    print(p1 * p2)
    print(p1(2))
    print(p1.differentiate())
    print(p1.integrate())
    p1.save('test_coeffs.dat')
    print(f'Saved polynomial: {p1}')
    p3 = Polynomial([1, 2, 3])
    print(p1 == p3)
 
    print('Lagrange interpolation:')
    points = [(1, 1), (2, 4), (3, 9)]
    print(points)
    p3 = lagrange_interpolation(points)
    print(p3)   # Should be x^2

    p4 = Polynomial([])
    p4.load('test_coeffs.dat')
    print(f'from loaded coefficients: {p4}')

if __name__ == '__main__':
    _test()