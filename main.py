import math


# ---------- Utility functions ----------

def get_function(expression, variables):
    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "e": math.e,
    }

    def f(*values):
        names = allowed.copy()
        for i in range(len(variables)):
            names[variables[i]] = values[i]
        return eval(expression, {"__builtins__": {}}, names)

    return f


def read_values(message, n):
    while True:
        values = list(map(float, input(message).split()))
        if len(values) == n:
            return values
        print("Please enter exactly", n, "values.")


def print_matrix(a):
    for row in a:
        print(" ".join(f"{value:10.5f}" for value in row))


# ---------- Module 1 ----------

def fixed_point():
    print("\nFIXED POINT ITERATION")

    print("Enter g(x) for the equation x = g(x).")
    expression = input("g(x) = ")

    g = get_function(expression, ["x"])

    x = float(input("Enter initial value of x: "))
    tolerance = float(input("Enter tolerance: "))
    max_iter = int(input("Enter maximum iterations: "))

    print("\nIteration       x_n          g(x_n)       Difference")
    print("-----------------------------------------------------")

    for i in range(1, max_iter + 1):
        try:
            x_new = g(x)
        except Exception:
            print("Invalid function or value.")
            return

        difference = abs(x_new - x)

        print(f"{i:5d}       {x:.4f}       {x_new:.4f}       {difference:.4f}")

        if difference < tolerance:
            print("\nRequired accuracy reached.")
            print(f"Approximate root = {x_new:.4f}")
            return

        x = x_new

    print("\nMaximum number of iterations reached.")
    print(f"Approximate value = {x_new:.4f}")

def secant():
    print("\nSECANT METHOD")

    expression = input("Enter f(x): ")
    f = get_function(expression, ["x"])

    x0 = float(input("Enter first approximation x0: "))
    x1 = float(input("Enter second approximation x1: "))
    tolerance = float(input("Enter tolerance: "))
    max_iter = int(input("Enter maximum iterations: "))

    print("\nIteration       x0          x1          f(x0)       f(x1)       x2       Difference")
    print("-----------------------------------------------------------------------------------")

    for i in range(1, max_iter + 1):

        try:
            f0 = f(x0)
            f1 = f(x1)
        except Exception:
            print("Invalid function or value.")
            return

        if abs(f1 - f0) < 1e-14:
            print("Division by zero encountered.")
            return

        x2 = x1 - (f1 * (x1 - x0)) / (f1 - f0)

        difference = abs(x2 - x1)

        print(
            f"{i:5d}     "
            f"{x0:.4f}     "
            f"{x1:.4f}     "
            f"{f0:.4f}     "
            f"{f1:.4f}     "
            f"{x2:.4f}     "
            f"{difference:.4f}"
        )

        if difference < tolerance:
            print("\nRequired accuracy reached.")
            print(f"Approximate root = {x2:.4f}")
            return

        x0 = x1
        x1 = x2

    print("\nMaximum number of iterations reached.")
    print(f"Approximate value = {x2:.4f}")

def gauss_seidel():
    print("\nGAUSS-SEIDEL METHOD")

    n = int(input("Enter number of equations: "))

    a = []

    print("\nEnter the augmented matrix row by row.")
    print("Each row should contain", n + 1, "values.")

    for i in range(n):
        row = read_values(f"Row {i + 1}: ", n + 1)
        a.append(row)

    x = read_values("\nEnter initial approximations: ", n)

    print("\nIteration", end="")

    for i in range(n):
        print(f"       x{i + 1}", end="")

    print()
    print("-" * (12 + 12 * n))

    iteration = 1

    while True:

        old = x.copy()

        for i in range(n):

            if abs(a[i][i]) < 1e-14:
                print("\nZero diagonal element encountered.")
                print("Rearrange the equations before applying Gauss-Seidel.")
                return

            total = 0

            for j in range(n):
                if j != i:
                    total += a[i][j] * x[j]

            x[i] = (a[i][n] - total) / a[i][i]

        print(f"{iteration:5d}", end="")

        for value in x:
            print(f"       {value:.3f}", end="")

        print()

        # Check whether successive approximations are equal
        same = True

        for i in range(n):
            if round(x[i], 3) != round(old[i], 3):
                same = False
                break

        if same:
            print("\nSuccessive approximations are equal.")
            print("Therefore, the iteration is stopped.")

            print("\nFinal solution:")
            for i in range(n):
                print(f"x{i + 1} = {x[i]:.3f}")

            break

        iteration += 1

# ---------- Module 2 ----------

def fitting_of_curves():
    print("\n========================================")
    print("          FITTING OF CURVES")
    print("========================================")
    print("1. Fitting of Straight Line")
    print("2. Fitting of Second-Degree Polynomial")
    print("3. Fitting of Power Curve")
    print("4. Exponential Curve (y = ae^bx)")
    print("5. Exponential Curve (y = ab^x)")
    print("6. Back to Module 2")
    print("========================================")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        straight_line_fit()

    elif choice == 2:
        second_degree_polynomial()

    elif choice == 3:
        power_curve()

    elif choice == 4:
        exponential_curve_1()

    elif choice == 5:
        exponential_curve_2()

    elif choice == 6:
        return

    else:
        print("Invalid choice.")


# --------------------------------------------------
# 1. STRAIGHT LINE
# y = a + bx
# --------------------------------------------------

def straight_line_fit():

    print("\nFITTING OF STRAIGHT LINE")
    print("Equation: y = a + bx")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_x2 = 0

    for i in range(n):
        sum_x += x[i]
        sum_y += y[i]
        sum_xy += x[i] * y[i]
        sum_x2 += x[i] ** 2

    denominator = n * sum_x2 - sum_x ** 2

    if denominator == 0:
        print("Straight line cannot be fitted.")
        return

    b = (n * sum_xy - sum_x * sum_y) / denominator
    a = (sum_y - b * sum_x) / n

    print("\nCalculated values:")
    print(f"Σx   = {sum_x:.4f}")
    print(f"Σy   = {sum_y:.4f}")
    print(f"Σxy  = {sum_xy:.4f}")
    print(f"Σx²  = {sum_x2:.4f}")

    print("\nNormal equations:")
    print(f"{n}a + ({sum_x:.4f})b = {sum_y:.4f}")
    print(f"({sum_x:.4f})a + ({sum_x2:.4f})b = {sum_xy:.4f}")

    print("\nConstants:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")

    print("\nFitted equation:")
    print(f"y = {a:.4f} + ({b:.4f})x")


# --------------------------------------------------
# 2. SECOND-DEGREE POLYNOMIAL
# y = a + bx + cx²
# --------------------------------------------------

def second_degree_polynomial():

    print("\nFITTING OF SECOND-DEGREE POLYNOMIAL")
    print("Equation: y = a + bx + cx²")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    sx = sy = sx2 = sx3 = sx4 = sxy = sx2y = 0

    for i in range(n):
        sx += x[i]
        sy += y[i]
        sx2 += x[i] ** 2
        sx3 += x[i] ** 3
        sx4 += x[i] ** 4
        sxy += x[i] * y[i]
        sx2y += (x[i] ** 2) * y[i]

    # Normal equations:
    # na + bΣx + cΣx² = Σy
    # aΣx + bΣx² + cΣx³ = Σxy
    # aΣx² + bΣx³ + cΣx⁴ = Σx²y

    A = [
        [n, sx, sx2],
        [sx, sx2, sx3],
        [sx2, sx3, sx4]
    ]

    B = [sy, sxy, sx2y]

    # Gaussian elimination

    for i in range(3):

        for j in range(i + 1, 3):

            factor = A[j][i] / A[i][i]

            for k in range(i, 3):
                A[j][k] -= factor * A[i][k]

            B[j] -= factor * B[i]

    c = B[2] / A[2][2]
    b = (B[1] - A[1][2] * c) / A[1][1]
    a = (B[0] - A[0][1] * b - A[0][2] * c) / A[0][0]

    print("\nCalculated values:")
    print(f"Σx    = {sx:.4f}")
    print(f"Σy    = {sy:.4f}")
    print(f"Σx²   = {sx2:.4f}")
    print(f"Σx³   = {sx3:.4f}")
    print(f"Σx⁴   = {sx4:.4f}")
    print(f"Σxy   = {sxy:.4f}")
    print(f"Σx²y  = {sx2y:.4f}")

    print("\nConstants:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")
    print(f"c = {c:.4f}")

    print("\nFitted equation:")
    print(f"y = {a:.4f} + ({b:.4f})x + ({c:.4f})x²")


# --------------------------------------------------
# 3. POWER CURVE
# y = ax^b
# --------------------------------------------------

def power_curve():

    print("\nFITTING OF POWER CURVE")
    print("Equation: y = ax^b")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    sum_X = 0
    sum_Y = 0
    sum_XY = 0
    sum_X2 = 0

    for i in range(n):

        if x[i] <= 0 or y[i] <= 0:
            print("x and y values must be positive for power curve.")
            return

        X = math.log(x[i])
        Y = math.log(y[i])

        sum_X += X
        sum_Y += Y
        sum_XY += X * Y
        sum_X2 += X ** 2

    denominator = n * sum_X2 - sum_X ** 2

    if denominator == 0:
        print("Power curve cannot be fitted.")
        return

    b = (n * sum_XY - sum_X * sum_Y) / denominator
    A = (sum_Y - b * sum_X) / n

    a = math.exp(A)

    print("\nUsing logarithmic transformation:")
    print("X = log(x)")
    print("Y = log(y)")

    print("\nCalculated values:")
    print(f"ΣX   = {sum_X:.4f}")
    print(f"ΣY   = {sum_Y:.4f}")
    print(f"ΣXY  = {sum_XY:.4f}")
    print(f"ΣX²  = {sum_X2:.4f}")

    print("\nConstants:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")

    print("\nFitted equation:")
    print(f"y = {a:.4f}x^({b:.4f})")


# --------------------------------------------------
# 4. EXPONENTIAL CURVE
# y = ae^bx
# --------------------------------------------------

def exponential_curve_1():

    print("\nFITTING OF EXPONENTIAL CURVE")
    print("Equation: y = ae^bx")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    sum_x = 0
    sum_Y = 0
    sum_xY = 0
    sum_x2 = 0

    for i in range(n):

        if y[i] <= 0:
            print("y values must be positive.")
            return

        Y = math.log(y[i])

        sum_x += x[i]
        sum_Y += Y
        sum_xY += x[i] * Y
        sum_x2 += x[i] ** 2

    denominator = n * sum_x2 - sum_x ** 2

    if denominator == 0:
        print("Exponential curve cannot be fitted.")
        return

    b = (n * sum_xY - sum_x * sum_Y) / denominator
    A = (sum_Y - b * sum_x) / n

    a = math.exp(A)

    print("\nUsing logarithmic transformation:")
    print("Y = log(y)")

    print("\nCalculated values:")
    print(f"Σx   = {sum_x:.4f}")
    print(f"ΣY   = {sum_Y:.4f}")
    print(f"ΣxY  = {sum_xY:.4f}")
    print(f"Σx²  = {sum_x2:.4f}")

    print("\nConstants:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")

    print("\nFitted equation:")
    print(f"y = {a:.4f}e^({b:.4f}x)")


# --------------------------------------------------
# 5. EXPONENTIAL CURVE
# y = ab^x
# --------------------------------------------------

def exponential_curve_2():

    print("\nFITTING OF EXPONENTIAL CURVE")
    print("Equation: y = ab^x")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    sum_x = 0
    sum_Y = 0
    sum_xY = 0
    sum_x2 = 0

    for i in range(n):

        if y[i] <= 0:
            print("y values must be positive.")
            return

        Y = math.log(y[i])

        sum_x += x[i]
        sum_Y += Y
        sum_xY += x[i] * Y
        sum_x2 += x[i] ** 2

    denominator = n * sum_x2 - sum_x ** 2

    if denominator == 0:
        print("Exponential curve cannot be fitted.")
        return

    B = (n * sum_xY - sum_x * sum_Y) / denominator
    A = (sum_Y - B * sum_x) / n

    a = math.exp(A)
    b = math.exp(B)

    print("\nUsing logarithmic transformation:")
    print("Y = log(y)")

    print("\nCalculated values:")
    print(f"Σx   = {sum_x:.4f}")
    print(f"ΣY   = {sum_Y:.4f}")
    print(f"ΣxY  = {sum_xY:.4f}")
    print(f"Σx²  = {sum_x2:.4f}")

    print("\nConstants:")
    print(f"a = {a:.4f}")
    print(f"b = {b:.4f}")

    print("\nFitted equation:")
    print(f"y = {a:.4f}({b:.4f})^x")

def lagrange():
    print("\nLAGRANGE INTERPOLATION")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    for i in range(n):
        for j in range(i + 1, n):
            if x[i] == x[j]:
                print("x values must be different.")
                return

    xp = float(input("Enter the value of x to interpolate: "))

    # Calculate interpolated value
    result = 0

    for i in range(n):

        term = y[i]

        for j in range(n):
            if i != j:
                term = term * (xp - x[j]) / (x[i] - x[j])

        result += term

    # Find polynomial coefficients
    # Start with zero polynomial
    coefficients = [0] * n

    for i in range(n):

        # Polynomial for:
        # product (x - x[j]) / (x[i] - x[j])

        term = [1.0]
        denominator = 1.0

        for j in range(n):
            if i != j:
                denominator *= (x[i] - x[j])

                new_term = [0] * (len(term) + 1)

                for k in range(len(term)):
                    new_term[k] += -x[j] * term[k]
                    new_term[k + 1] += term[k]

                term = new_term

        for k in range(len(term)):
            coefficients[k] += y[i] * term[k] / denominator

    print("\nLagrange Interpolation Polynomial:")

    polynomial = ""

    # Print from highest power to constant
    for power in range(n - 1, -1, -1):

        coefficient = coefficients[power]

        if abs(coefficient) < 1e-10:
            continue

        if polynomial == "":
            if coefficient < 0:
                polynomial += "-"
        else:
            if coefficient >= 0:
                polynomial += " + "
            else:
                polynomial += " - "

        coefficient = abs(coefficient)

        if power == 0:
            polynomial += f"{coefficient:.2f}"

        elif power == 1:
            polynomial += f"{coefficient:.2f}x"

        else:
            polynomial += f"{coefficient:.2f}x^{power}"

    print("P(x) =", polynomial)

    print("\nInterpolated value:")
    print(f"P({xp:.2f}) = {result:.2f}")
    

def cubic_spline():
    print("\nCUBIC SPLINE INTERPOLATION")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of values must be equal to number of data points.")
        return

    if n < 3:
        print("At least 3 data points are required.")
        return

    for i in range(n - 1):
        if x[i] >= x[i + 1]:
            print("x values must be in increasing order.")
            return

    xp = float(input("Enter the value of x to interpolate: "))

    if xp < x[0] or xp > x[n - 1]:
        print("The value of x must be within the given range.")
        return

    h = []

    for i in range(n - 1):
        h.append(x[i + 1] - x[i])

    # Calculate the coefficients of the tridiagonal system

    a = [0] * (n - 2)
    b = [0] * (n - 2)
    c = [0] * (n - 2)
    d = [0] * (n - 2)

    for i in range(n - 2):
        a[i] = h[i]
        b[i] = 2 * (h[i] + h[i + 1])
        c[i] = h[i + 1]

        d[i] = 6 * (
            (y[i + 2] - y[i + 1]) / h[i + 1]
            - (y[i + 1] - y[i]) / h[i]
        )

    # Thomas algorithm for tridiagonal system

    for i in range(1, n - 2):
        factor = a[i] / b[i - 1]

        b[i] = b[i] - factor * c[i - 1]
        d[i] = d[i] - factor * d[i - 1]

    m = [0] * n

    if n > 2:

        m[n - 2] = d[n - 3] / b[n - 3]

        for i in range(n - 4, -1, -1):
            m[i + 1] = (
                d[i] - c[i] * m[i + 2]
            ) / b[i]

    # Natural spline:
    # m[0] = 0 and m[n-1] = 0

    for i in range(n - 1):

        if x[i] <= xp <= x[i + 1]:

            hi = x[i + 1] - x[i]

            term1 = m[i] * (x[i + 1] - xp) ** 3 / (6 * hi)
            term2 = m[i + 1] * (xp - x[i]) ** 3 / (6 * hi)

            term3 = (
                y[i] - m[i] * hi ** 2 / 6
            ) * (x[i + 1] - xp) / hi

            term4 = (
                y[i + 1] - m[i + 1] * hi ** 2 / 6
            ) * (xp - x[i]) / hi

            result = term1 + term2 + term3 + term4

            break

    print("\nSecond derivatives:")
    for i in range(n):
        print(f"M{i} = {m[i]:.2f}")

    print("\nInterpolated value:")
    print(f"y({xp:.2f}) = {result:.2f}")


# ============================================================
# MODULE 3
# ============================================================

# ------------------------------------------------------------
# 1. NUMERICAL DIFFERENTIATION
#    Newton's Forward Interpolation
#    First and Second Derivative
# ------------------------------------------------------------

def numerical_differentiation():

    print("\n========================================")
    print("      NUMERICAL DIFFERENTIATION")
    print("========================================")
    print("Method: Newton's Forward Interpolation")
    print("Finding First and Second Derivatives")

    n = int(input("Enter number of data points: "))

    x = list(map(float, input("Enter x values: ").split()))
    y = list(map(float, input("Enter y values: ").split()))

    if len(x) != n or len(y) != n:
        print("Number of x and y values must be equal to number of data points.")
        return

    if n < 3:
        print("At least 3 data points are required.")
        return

    # Check equal spacing
    h = x[1] - x[0]

    for i in range(1, n - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-10:
            print("x values must be equally spaced.")
            return

    xp = float(input("Enter the value of x at which derivative is required: "))

    # --------------------------------------------------------
    # Forward Difference Table
    # --------------------------------------------------------

    difference_table = [y.copy()]

    for j in range(1, n):

        previous = difference_table[j - 1]
        current = []

        for i in range(len(previous) - 1):
            current.append(previous[i + 1] - previous[i])

        difference_table.append(current)

    # Display difference table
    print("\nForward Difference Table")
    print("----------------------------------------")

    print("x\t", end="")

    for j in range(n):
        if j == 0:
            print("y\t", end="")
        else:
            print(f"Δ^{j}y\t", end="")

    print()

    for i in range(n):

        print(f"{x[i]:.4f}\t", end="")

        for j in range(n - i):
            print(f"{difference_table[j][i]:.4f}\t", end="")

        print()

    # --------------------------------------------------------
    # Calculate u
    # --------------------------------------------------------

    u = (xp - x[0]) / h

    # --------------------------------------------------------
    # First derivative
    #
    # dy/dx = 1/h [
    # Δy0
    # + (2u-1)/2 Δ²y0
    # + (3u²-6u+2)/6 Δ³y0
    # + ...
    # ]
    # --------------------------------------------------------

    first_derivative = 0

    if n >= 2:
        first_derivative += difference_table[1][0]

    if n >= 3:
        first_derivative += (
            (2 * u - 1) / 2
        ) * difference_table[2][0]

    if n >= 4:
        first_derivative += (
            (3 * u ** 2 - 6 * u + 2) / 6
        ) * difference_table[3][0]

    if n >= 5:
        first_derivative += (
            (4 * u ** 3 - 18 * u ** 2 + 22 * u - 6) / 24
        ) * difference_table[4][0]

    if n >= 6:
        first_derivative += (
            (5 * u ** 4 - 40 * u ** 3 + 105 * u ** 2
             - 100 * u + 24) / 120
        ) * difference_table[5][0]

    first_derivative = first_derivative / h

    # --------------------------------------------------------
    # Second derivative
    #
    # d²y/dx² = 1/h² [
    # Δ²y0
    # + (u-1) Δ³y0
    # + (6u²-18u+11)/12 Δ⁴y0
    # + ...
    # ]
    # --------------------------------------------------------

    second_derivative = 0

    if n >= 3:
        second_derivative += difference_table[2][0]

    if n >= 4:
        second_derivative += (
            (u - 1)
        ) * difference_table[3][0]

    if n >= 5:
        second_derivative += (
            (6 * u ** 2 - 18 * u + 11) / 12
        ) * difference_table[4][0]

    if n >= 6:
        second_derivative += (
            (4 * u ** 3 - 18 * u ** 2 + 22 * u - 6) / 12
        ) * difference_table[5][0]

    second_derivative = second_derivative / (h ** 2)

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("\nCalculated values:")
    print(f"h = {h:.4f}")
    print(f"u = {u:.4f}")

    print("\nFirst derivative:")
    print(f"dy/dx = {first_derivative:.4f}")

    print("\nSecond derivative:")
    print(f"d²y/dx² = {second_derivative:.4f}")

# ------------------------------------------------------------
# 2. GAUSSIAN QUADRATURE
#    2-Point Gaussian Quadrature
# ------------------------------------------------------------

def gaussian_quadrature():

    print("\n========================================")
    print("        GAUSSIAN QUADRATURE")
    print("========================================")
    print("Method: 2-Point Gaussian Quadrature")

    print("\nEnter the function f(x).")

    expression = input("f(x) = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "e": math.e,
    }

    def f(x):

        names = allowed.copy()
        names["x"] = x

        return eval(expression, {"__builtins__": {}}, names)

    a = float(input("Enter lower limit: "))
    b = float(input("Enter upper limit: "))

    # 2-point Gaussian values
    z1 = -1 / math.sqrt(3)
    z2 = 1 / math.sqrt(3)
    w1=1
    w2=1

    x1 = ((b - a) / 2) * z1 + ((b + a) / 2) 
    x2 = ((b - a) / 2) * z2 + ((b + a) / 2)

    try:
        f1 = f(x1)
        f2 = f(x2)
    except Exception:
        print("Invalid function or value.")
        return

    result = ((b - a) / 2) * (w1*f1 + w2*f2)

    print("\nGaussian points:")
    print(f"x1 = {x1:.2f}")
    print(f"x2 = {x2:.2f}")

    print("\nFunction values:")
    print(f"f(x1) = {f1:.2f}")
    print(f"f(x2) = {f2:.2f}")

    print("\nResult:")
    print(f"Integral = {result:.2f}")


# ------------------------------------------------------------
# 3. DOUBLE INTEGRATION
#    Trapezoidal Rule
# ------------------------------------------------------------

def double_integration():

    print("\n========================================")
    print("          DOUBLE INTEGRATION")
    print("========================================")
    print("Method: Trapezoidal Rule")

    print("\nEnter the function f(x,y).")
    print("Example: x + y")

    expression = input("f(x,y) = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    def f(x, y):
        names = allowed.copy()
        names["x"] = x
        names["y"] = y

        return eval(expression, {"__builtins__": {}}, names)

    print("\nEnter limits for x:")
    x0 = float(input("Lower limit of x: "))
    x1 = float(input("Upper limit of x: "))

    print("\nEnter limits for y:")
    y0 = float(input("Lower limit of y: "))
    y1 = float(input("Upper limit of y: "))

    # Enter step sizes directly
    hx = float(input("\nEnter step size h for x: "))
    hy = float(input("Enter step size k for y: "))

    if hx <= 0 or hy <= 0:
        print("Step size must be positive.")
        return

    # Calculate number of intervals
    nx = round((x1 - x0) / hx)
    ny = round((y1 - y0) / hy)

    # Check whether step size divides the interval exactly
    if abs(nx * hx - (x1 - x0)) > 1e-10:
        print("Step size h for x does not divide the x interval exactly.")
        return

    if abs(ny * hy - (y1 - y0)) > 1e-10:
        print("Step size h for y does not divide the y interval exactly.")
        return

    total = 0

    for i in range(nx + 1):

        x = x0 + i * hx

        if i == 0 or i == nx:
            wx = 1
        else:
            wx = 2

        for j in range(ny + 1):

            y = y0 + j * hy

            if j == 0 or j == ny:
                wy = 1
            else:
                wy = 2

            try:
                value = f(x, y)
            except Exception:
                print("Invalid function or value.")
                return

            total += wx * wy * value

    result = (hx * hy / 4) * total

    print("\nCalculated values:")
    print(f"h_x = {hx:.4f}")
    print(f"h_y = {hy:.4f}")
    print(f"Number of intervals in x = {nx}")
    print(f"Number of intervals in y = {ny}")

    print("\nResult:")
    print(f"Double integral = {result:.4f}")

# ============================================================
# MODULE 3 MENU
# ============================================================

def module3():

    while True:

        print("\n========================================")
        print("              MODULE 3")
        print("========================================")
        print("1. Numerical Differentiation")
        print("2. Gaussian Quadrature")
        print("3. Double Integration")
        print("4. Back to Main Menu")
        print("========================================")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            numerical_differentiation()

        elif choice == 2:
            gaussian_quadrature()

        elif choice == 3:
            double_integration()

        elif choice == 4:
            break

        else:
            print("Invalid choice.")



# ============================================================
# MODULE 4
# ============================================================


# ------------------------------------------------------------
# 1. EULER'S METHOD
# ------------------------------------------------------------

def euler_method():

    print("\n========================================")
    print("            EULER'S METHOD")
    print("========================================")

    print("\nEnter the differential equation:")
    print("Use x and y as variables.")

    expression = input("dy/dx = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
    }

    def f(x, y):
        names = allowed.copy()
        names["x"] = x
        names["y"] = y

        return eval(expression, {"__builtins__": {}}, names)

    x = float(input("Enter initial value of x: "))
    y = float(input("Enter initial value of y: "))
    h = float(input("Enter step size h: "))
    target = float(input("Enter the value of x at which y is required: "))

    steps = round((target - x) / h)

    if steps <= 0 or abs(x + steps * h - target) > 1e-10:
        print("Target x must be greater than initial x and reachable using the given step size.")
        return

    print("\nIteration        x            y")
    print("--------------------------------")

    print(f"{0:5d}       {x:.4f}       {y:.4f}")

    for i in range(1, steps + 1):

        try:
            slope = f(x, y)
        except Exception:
            print("Invalid function or value.")
            return

        y = y + h * slope
        x = x + h

        print(f"{i:5d}       {x:.4f}       {y:.4f}")

    print("\nFinal result:")
    print(f"y({x:.4f}) = {y:.4f}")

def runge_kutta():

    print("\n========================================")
    print("       RUNGE-KUTTA 4TH ORDER")
    print("========================================")

    print("\nEnter the differential equation.")
    print("Example: x + y")

    expression = input("dy/dx = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    def f(x, y):
        names = allowed.copy()
        names["x"] = x
        names["y"] = y
        return eval(expression, {"__builtins__": {}}, names)

    x = float(input("Enter initial value of x: "))
    y = float(input("Enter initial value of y: "))
    h = float(input("Enter step size h: "))
    target = float(input("Enter the value of x at which y is required: "))

    steps = round((target - x) / h)

    if steps <= 0 or abs(x + steps * h - target) > 1e-10:
        print("Target x must be greater than initial x and reachable using the given step size.")
        return

    print("\nIteration        x            y")
    print("--------------------------------")

    print(f"{0:5d}       {x:.4f}       {y:.4f}")

    for i in range(1, steps + 1):

        try:
            k1 = h * f(x, y)
            k2 = h * f(x + h / 2, y + k1 / 2)
            k3 = h * f(x + h / 2, y + k2 / 2)
            k4 = h * f(x + h, y + k3)

        except Exception:
            print("Invalid function or value.")
            return

        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x = x + h

        print(f"{i:5d}       {x:.4f}       {y:.4f}")

    print("\nFinal result:")
    print(f"y({x:.4f}) = {y:.4f}")

# ------------------------------------------------------------
# 3. MILNE'S METHOD
# ------------------------------------------------------------

def milnes_method():

    print("\n========================================")
    print("            MILNE'S METHOD")
    print("========================================")

    print("\nEnter the differential equation.")
    print("Example: x + y")

    expression = input("dy/dx = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    def f(x, y):
        names = allowed.copy()
        names["x"] = x
        names["y"] = y

        return eval(expression, {"__builtins__": {}}, names)

    print("\nEnter the four initial values.")

    x0 = float(input("Enter x0: "))
    y0 = float(input("Enter y0: "))

    h = float(input("Enter step size h: "))

    y = [0, 0, 0, 0]
    x = [0, 0, 0, 0]

    x[0] = x0
    y[0] = y0

    for i in range(1, 4):
        x[i] = x0 + i * h
        y[i] = float(input(f"Enter y{i}: "))

    target = float(input("\nEnter the value of x at which y is required: "))

    steps = round((target - x[3]) / h)

    if steps < 0 or abs(x[3] + steps * h - target) > 1e-10:
        print("Target x must be greater than x3 and reachable using the given step size.")
        return

    print("\nInitial values:")
    print("i          x            y")
    print("--------------------------------")

    for i in range(4):
        print(f"{i}       {x[i]:.4f}       {y[i]:.4f}")

    # --------------------------------------------------------
    # Milne Predictor-Corrector
    # --------------------------------------------------------

    for step in range(steps):

        f0 = f(x[0], y[0])
        f1 = f(x[1], y[1])
        f2 = f(x[2], y[2])
        f3 = f(x[3], y[3])

        # Predictor
        yp = y[0] + (4 * h / 3) * (
            2 * f3 - f2 + 2 * f1
        )

        xp = x[3] + h

        # Corrector
        fp = f(xp, yp)

        yc = y[2] + (h / 3) * (
            f2 + 4 * f3 + fp
        )

        # Second correction
        fp = f(xp, yc)

        yc = y[2] + (h / 3) * (
            f2 + 4 * f3 + fp
        )

        print("\nStep:", step + 1)
        print(f"Predicted y = {yp:.4f}")
        print(f"Corrected y  = {yc:.4f}")

        # Shift values
        x[0] = x[1]
        x[1] = x[2]
        x[2] = x[3]
        x[3] = xp

        y[0] = y[1]
        y[1] = y[2]
        y[2] = y[3]
        y[3] = yc

    print("\nFinal result:")
    print(f"x = {x[3]:.4f}")
    print(f"y = {y[3]:.4f}")

# ============================================================
# MODULE 4 MENU
# ============================================================

def module4():

    while True:

        print("\n========================================")
        print("              MODULE 4")
        print("========================================")
        print("1. Euler's Method")
        print("2. Runge-Kutta 4th Order Method")
        print("3. Milne's Method")
        print("4. Back to Main Menu")
        print("========================================")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            euler_method()

        elif choice == 2:
            runge_kutta()

        elif choice == 3:
            milnes_method()

        elif choice == 4:
            break

        else:
            print("Invalid choice.")

# ---------- Module 5 ----------

def laplace_equation():
    print("\n========================================")
    print("          LAPLACE EQUATION")
    print("========================================")

    print("\nEquation:")
    print("d2u/dx2 + d2u/dy2 = 0")

    rows = int(input("\nEnter number of grid points in y direction: "))
    cols = int(input("Enter number of grid points in x direction: "))

    u = []

    print("\nEnter the initial grid values.")
    print("Enter boundary values and use 0 for unknown interior values.")

    for i in range(rows):
        row = list(map(float, input(f"Row {i + 1}: ").split()))

        if len(row) != cols:
            print("Number of values must match the number of columns.")
            return

        u.append(row)

    iteration = 1

    while True:
        old = [row.copy() for row in u]

        # Gauss-Seidel iteration
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                u[i][j] = (
                    u[i - 1][j]
                    + u[i + 1][j]
                    + u[i][j - 1]
                    + u[i][j + 1]
                ) / 4

        same = True

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if round(u[i][j], 4) != round(old[i][j], 4):
                    same = False
                    break

            if not same:
                break

        if same:
            break

        iteration += 1

    print("\nFinal solution:")
    print("-" * (12 * cols))

    for i in range(rows):
        for j in range(cols):
            print(f"{u[i][j]:10.4f}", end=" ")
        print()

    print("\nNumber of iterations =", iteration)

def poisson_equation():
    print("\n========================================")
    print("          POISSON EQUATION")
    print("========================================")

    print("\nEquation:")
    print("d2u/dx2 + d2u/dy2 = f(x,y)")

    expression = input("\nf(x,y) = ")

    allowed = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sqrt": math.sqrt,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    def f(x, y):
        names = allowed.copy()
        names["x"] = x
        names["y"] = y
        return eval(expression, {"__builtins__": {}}, names)

    rows = int(input("\nEnter number of grid points in y direction: "))
    cols = int(input("Enter number of grid points in x direction: "))

    h = float(input("Enter grid spacing h: "))

    u = []

    print("\nEnter the initial grid values.")
    print("Enter boundary values and use 0 for unknown interior values.")

    for i in range(rows):
        row = list(map(float, input(f"Row {i + 1}: ").split()))

        if len(row) != cols:
            print("Number of values must match the number of columns.")
            return

        u.append(row)

    iteration = 1

    while True:
        old = [row.copy() for row in u]

        # Gauss-Seidel iteration
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):

                x = j * h
                y = i * h

                try:
                    value = f(x, y)
                except Exception:
                    print("\nInvalid function or value.")
                    return

                u[i][j] = (
                    u[i - 1][j]
                    + u[i + 1][j]
                    + u[i][j - 1]
                    + u[i][j + 1]
                    - h**2 * value
                ) / 4

        same = True

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if round(u[i][j], 4) != round(old[i][j], 4):
                    same = False
                    break

            if not same:
                break

        if same:
            break

        iteration += 1

    print("\nFinal solution:")
    print("-" * (12 * cols))

    for i in range(rows):
        for j in range(cols):
            print(f"{u[i][j]:10.4f}", end=" ")
        print()

    print("\nNumber of iterations =", iteration)

def heat_equation():
    print("\n========================================")
    print("       HEAT EQUATION - EXPLICIT")
    print("========================================")

    print("\nEquation:")
    print("du/dt = alpha * d2u/dx2")

    length = float(input("\nEnter length of rod: "))
    total_time = float(input("Enter total time: "))

    h = float(input("Enter space step h: "))
    k = float(input("Enter time step k: "))

    alpha = float(input("Enter thermal diffusivity alpha: "))

    if h <= 0 or k <= 0 or alpha <= 0:
        print("\nStep sizes and alpha must be positive.")
        return

    nx = round(length / h)
    nt = round(total_time / k)

    if abs(nx * h - length) > 1e-10:
        print("\nSpace step h does not divide the rod length exactly.")
        return

    if abs(nt * k - total_time) > 1e-10:
        print("\nTime step k does not divide the total time exactly.")
        return

    r = alpha * k / (h ** 2)

    print(f"\nr = {r:.4f}")

    if r > 0.5:
        print("\nThe explicit method is unstable because r > 0.5.")
        print("Choose a smaller time step k.")
        return

    print("\nEnter the initial temperature values.")
    print(f"Enter {nx + 1} values from x = 0 to x = {length}.")

    initial = list(map(float, input("Initial values: ").split()))

    if len(initial) != nx + 1:
        print(f"Please enter exactly {nx + 1} values.")
        return

    left_boundary = float(input("\nEnter left boundary temperature: "))
    right_boundary = float(input("Enter right boundary temperature: "))

    # Initial temperature distribution
    u = initial.copy()

    # Apply boundary values
    u[0] = left_boundary
    u[nx] = right_boundary

    print("\nTemperature table:")
    print("-" * 70)

    print("Time", end="")
    for i in range(nx + 1):
        x = i * h
        print(f"{x:10.4f}", end="")
    print()

    print("-" * 70)

    # Initial row
    print(f"{0:6.4f}", end="")
    for value in u:
        print(f"{value:10.4f}", end="")
    print()

    # Explicit calculations
    for n in range(1, nt + 1):

        old = u.copy()

        for i in range(1, nx):
            u[i] = (
                r * old[i - 1]
                + (1 - 2 * r) * old[i]
                + r * old[i + 1]
            )

        # Boundary values remain fixed
        u[0] = left_boundary
        u[nx] = right_boundary

        time = n * k

        print(f"{time:6.4f}", end="")

        for value in u:
            print(f"{value:10.4f}", end="")

        print()

    print("\nFinal temperature distribution:")

    for i in range(nx + 1):
        x = i * h
        print(f"u({x:.4f}) = {u[i]:.4f}")

# ---------- Module menus ----------

def module1():
    while True:
        print("\n========== MODULE 1 ==========")
        print("1. Fixed Point Iteration")
        print("2. Secant Method")
        print("3. Gauss-Seidel Method")
        print("4. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            fixed_point()
        elif choice == 2:
            secant()
        elif choice == 3:
            gauss_seidel()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def module2():
    while True:
        print("\n========== MODULE 2 ==========")
        print("1. Fitting of Curves")
        print("2. Lagrange Interpolation")
        print("3. Cubic Spline Interpolation")
        print("4. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            print("\nSelect curve fitting method:")
            print("1. Straight Line Fit")
            print("2. Second-Degree Polynomial Fit")
            print("3. Power Curve Fit")
            print("4. Exponential Curve Fit (y = ae^(bx))")
            print("5. Exponential Curve Fit (y = ab^x)")
            curve_choice = int(input("Enter your choice: "))

            if curve_choice == 1:
                straight_line_fit()
            elif curve_choice == 2:
                second_degree_polynomial()
            elif curve_choice == 3:
                power_curve()
            elif curve_choice == 4:
                exponential_curve_1()
            elif curve_choice == 5:
                exponential_curve_2()
            else:
                print("Invalid choice.")
        elif choice == 2:
            lagrange()
        elif choice == 3:
            cubic_spline()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def module3():
    while True:
        print("\n========== MODULE 3 ==========")
        print("1. Newton Forward Numerical Differentiation")
        print("2. Gaussian Quadrature")
        print("3. Double Integration")
        print("4. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            numerical_differentiation()
        elif choice == 2:
            gaussian_quadrature()
        elif choice == 3:
            double_integration()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def module4():
    while True:
        print("\n========== MODULE 4 ==========")
        print("1. Euler's Method")
        print("2. Runge-Kutta Fourth Order")
        print("3. Milne's Method")
        print("4. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            euler_method()
        elif choice == 2:
            runge_kutta()
        elif choice == 3:
            milnes_method()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


def module5():
    while True:
        print("\n========== MODULE 5 ==========")
        print("1. Laplace Equation")
        print("2. Poisson Equation")
        print("3. Heat Equation - Explicit Method")
        print("4. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            laplace_equation()
        elif choice == 2:
            poisson_equation()
        elif choice == 3:
            heat_equation()
        elif choice == 4:
            break
        else:
            print("Invalid choice.")


# ---------- Main switch ----------

def main():
    while True:
        print("\n========================================")
        print("       NUMERICAL APPLICATIONS")
        print("========================================")
        print("1. Module 1")
        print("2. Module 2")
        print("3. Module 3")
        print("4. Module 4")
        print("5. Module 5")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            module1()
        elif choice == 2:
            module2()
        elif choice == 3:
            module3()
        elif choice == 4:
            module4()
        elif choice == 5:
            module5()
        elif choice == 6:
            print("Program ended.")
            break
        else:
            print("Invalid choice. Please try again.")


main()
