# Polynomial library

# Author: Rick Howell
# rick.howell.arts@gmail.com

class Polynomial:
    '''A class for polynomials. The coefficients are stored in a list, with the index corresponding to the power of x. For example, the polynomial 3x^2 + 2x + 1 would be stored as [1, 2, 3].
    
    This is the basic class for polynomials F[x] for real / complex numbers.
    '''

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
        # Check if coefficients are zero at the end, and if they are, remove them
        while self.coefficients[-1] == 0:
            self.coefficients.pop()
        
        # If all coefficients are zero, set to zero polynomial
        if not self.coefficients:
            self.coefficients = [0]
        
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
    
    def __pow__(self, n: int):
        '''Raise the polynomial to the power of n'''

        result = Polynomial([1])

        for _ in range(n):
            result *= self

        return result
    
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
    
    def std(self) -> str:
        '''Returns a string of the polynomial in standard form
        i.e. highest power of x first'''
    
        s = ''
        for i in range(self.degree, -1, -1):
            if self.coefficients[i] == 0:
                continue

            if self.coefficients[i] > 0:
                s += ' + ' if s else ''
            else:
                s += ' - ' if s else ' - '

            if abs(self.coefficients[i]) != 1 or i == 0:
                s += str(abs(self.coefficients[i]))

            if i > 0:
                s += 'x'
                if i > 1:
                    s += f'^{i}'

        return s

def from_roots(roots: list) -> Polynomial:
    '''Returns a polynomial with the given roots'''

    p = Polynomial([1])

    for r in roots:
        p *= Polynomial([-r, 1])

    return p


def compose(p: Polynomial, q: Polynomial) -> Polynomial:
    '''Returns the composition of two polynomials'''

    result = Polynomial([0])

    for i in range(p.degree + 1):
        result += p.coefficients[i] * q ** i

    return result


def differentiate(p: Polynomial) -> Polynomial:
    '''Returns the derivative of the polynomial p'''

    return p.differentiate()


def integrate(p: Polynomial) -> Polynomial:
    '''Returns the integral of the polynomial p'''

    return p.integrate()


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
    coeff_file = 'tests/test_coeffs.dat'

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
    p1.save(coeff_file)
    print(f'Saved polynomial: {p1}')
    p3 = Polynomial([1, 2, 3])
    print(p1 == p3)
 
    print('Lagrange interpolation:')
    points = [(1, 1), (2, 4), (3, 9)]
    print(points)
    p3 = lagrange_interpolation(points)
    print(p3.std())   # Should be x^2

    p4 = Polynomial([])
    p4.load(coeff_file)
    print(f'from loaded coefficients: {p4}')

    print('Polynomial from roots (x-1)(x-2)(x-3):')
    p5 = from_roots([1, 2, 3])
    print(p5)
    print(p5.std())

    print('Composition of polynomials:')
    p6 = Polynomial([0, 2, 1])
    p7 = Polynomial([2, 3])

    print(f'p6 = {p6.std()}, p7 = {p7.std()}, p6(p7) = {compose(p6, p7).std()}')

if __name__ == '__main__':
    _test()