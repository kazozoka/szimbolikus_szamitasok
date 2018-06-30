import unittest
from simplify import *

class HelperTests(unittest.TestCase):
    def test_base(self):
        a = Var("a")
        f = Function("f")
        p = Function('+', 1)
        q = Fraction(1,2)
        x = Function('^', 1, 2)

        self.assertEqual(base(a), a)
        self.assertEqual(base(f), f)
        self.assertEqual(base(q), None)
        self.assertEqual(base(p), p)
        self.assertEqual(base(1), None)
        self.assertEqual(base(x), 1)

    def test_exponent(self):
        a = Var("a")
        f = Function("f")
        p = Function('+', 1)
        q = Fraction(1,2)
        x = Function('^', 1, 2)

        self.assertEqual(exponent(a), 1)
        self.assertEqual(exponent(f), 1)
        self.assertEqual(exponent(q), None)
        self.assertEqual(exponent(p), 1)
        self.assertEqual(exponent(1), None)
        self.assertEqual(exponent(x), 2)

    def test_const(self):
        self.assertEqual(const(Var("a")), 1)
        self.assertEqual(const(Function("a")), 1)
        self.assertEqual(const(Function('*', 1, Var("x"))), 1)
        expr = Function('*', Var("x"), Var("y"))
        self.assertEqual(const(expr), 1)
        self.assertEqual(const(Fraction(1,2)), None)
        self.assertEqual(const(1), None)

    def test_term(self):
        self.assertEqual(term(Var("a")), Function('*', Var("a")))
        self.assertEqual(term(Function("a")), Function('*', Function("a")))
        self.assertEqual(term(Function('*', 1, Var("x"))), Function('*', Var("x")))
        expr = Function('*', Var("x"), Var("y"))
        self.assertEqual(term(expr), expr)
        self.assertEqual(term(Fraction(1,2)), None)
        self.assertEqual(term(1), None)

class GcdTest(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(None, 1), None)
        self.assertEqual(gcd(1, None), None)
        self.assertEqual(gcd(None, None), None)
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(-1, 1), 1)
        self.assertEqual(gcd(-1, -1), 1)
        self.assertEqual(gcd(4, 6), 2)

class OrderingTests(unittest.TestCase):
    def test_numbers(self):
        self.assertTrue(less(1, 2))
        self.assertFalse(less(1, 1))
        self.assertFalse(less(2, 1))

    def test_fractions(self):
        self.assertTrue(less(Fraction(1,4), Fraction(1,2)))
        self.assertTrue(less(Fraction(1,4), 1))
        self.assertFalse(less(1, Fraction(1,4)))
 
    def test_variables(self):
        self.assertTrue(less(Var("x"), Var("y")))
        self.assertFalse(less(Var("x"), Var("u")))

    def test_sums(self):
        a = Function('+', 1, 1)
        b = Function('+', 1, 1, 1)
        c = Function('+', 2)
        self.assertTrue(less(a, b))
        self.assertFalse(less(b, a))
        self.assertFalse(less(b, b))
        self.assertTrue(less(a, c))

    def test_prods(self):
        a = Function('*', 1, 1)
        b = Function('*', 1, 1, 1)
        c = Function('*', 2)
        self.assertTrue(less(a, b))
        self.assertFalse(less(b, a))
        self.assertFalse(less(b, b))
        self.assertTrue(less(a, c))

    def test_powers(self):
        a = Function('^', 1, 2)
        b = Function('^', 1, 3)
        c = Function('^', 2, 1)
        self.assertTrue(less(a, b))
        self.assertFalse(less(b, a))
        self.assertFalse(less(b, b))
        self.assertTrue(less(a, c))

    def test_functions(self):
        a = Function("a")
        b = Function("b")
        self.assertTrue(less(a, b))
        self.assertFalse(less(b, a))
        self.assertFalse(less(a, a))
        aa = Function("a", 1, 1)
        ab = Function("a", 1, 1, 1)
        ac = Function("a", 2)
        self.assertTrue(less(aa, ab))
        self.assertFalse(less(ab, aa))
        self.assertFalse(less(ab, ab))
        self.assertTrue(less(aa, ac))

    def test_number_vs_nonnumber(self):
        a = Function("a")
        b = Fraction(1,2)
        c = 1
        self.assertTrue(less(b, a))
        self.assertTrue(less(c, a))
        self.assertFalse(less(a, c))
        self.assertFalse(less(a, b))

    def test_prod_vs_nonprod(self):
        a = Function('*', 1, 2)
        b = Var("x")
        c = Function('+', 1)
        self.assertTrue(less(a, b))
        self.assertTrue(less(a, c))

    def test_sum_vs_nonsum(self):
        a = Function('+', 1, 2)
        b = Var("x")
        c = Function('-', 1)
        self.assertTrue(less(a, b))
        self.assertTrue(less(a, c))

    def test_power_vs_nonpower(self):
        a = Function('^', 1, 2)
        b = Var("x")
        c = Function('+', 1)
        d = Function('^', Var('x'), 1)
        f = Function("f")
        self.assertTrue(less(a, b))
        self.assertTrue(less(a, c))
        self.assertFalse(less(d, b))
        self.assertTrue(less(a, f))

    def test_sum_vs_nonsum(self):
        a = Function('+', 1, 2)
        b = Var("x")
        c = Function("c")
        self.assertTrue(less(a, b))
        self.assertTrue(less(a, c))

    def test_var_vs_func(self):
        self.assertTrue(less(Var("f"), Function("g")))

class RationalTest(unittest.TestCase):
    def test_numer(self):
        self.assertEqual(numer(1), 1)
        self.assertEqual(numer(Fraction(1, 2)), 1)
        self.assertEqual(numer(None), None)

    def test_denom(self):
        self.assertEqual(denom(2), 1)
        self.assertEqual(denom(Fraction(1, 2)), 2)
        self.assertEqual(denom(None), None)

    def test_simplify_rational_number(self):
        self.assertEqual(simplify_rational_number(1), 1)
        self.assertEqual(simplify_rational_number(Fraction(4, 2)), 2)
        self.assertEqual(simplify_rational_number(Fraction(6, 4)), Fraction(3, 2))
        self.assertEqual(simplify_rational_number(Fraction(-6, 4)), Fraction(-3, 2))
        self.assertEqual(simplify_rational_number(Fraction(6, -4)), Fraction(-3, 2))
        self.assertEqual(simplify_rational_number(Fraction(-6, -4)), Fraction(3, 2))

    def test_eval_prod(self):
        self.assertEqual(eval_prod(2, 3), Fraction(6, 1))
        self.assertEqual(eval_prod(2, Fraction(3, 4)), Fraction(6, 4))
        self.assertEqual(eval_prod(Fraction(2, 3), Fraction(3, 4)), Fraction(6, 12))
        self.assertEqual(eval_prod(2, Fraction(3, 0)), None)

    def test_eval_diff(self):
        self.assertEqual(eval_diff(2, 3), Fraction(-1, 1))
        self.assertEqual(eval_diff(1, Fraction(1,2)), Fraction(1,2))
        self.assertEqual(eval_diff(Fraction(1,2), Fraction(1,2)), Fraction(0,4))
        self.assertEqual(eval_diff(Fraction(1,2), Fraction(-1,2)), Fraction(4,4))
        self.assertEqual(eval_diff(1, Fraction(1,0)), None)

    def test_eval_sum(self):
        self.assertEqual(eval_sum(2, 3), Fraction(5, 1))
        self.assertEqual(eval_sum(1, Fraction(1,2)), Fraction(3,2))
        self.assertEqual(eval_sum(Fraction(1,2), Fraction(1,2)), Fraction(4,4))
        self.assertEqual(eval_sum(1, Fraction(1,0)), None)

    def test_eval_quot(self):
        self.assertEqual(eval_quot(1, 2), Fraction(1,2))
        self.assertEqual(eval_quot(2, 0), None)
        self.assertEqual(eval_quot(2, Fraction(1,2)), Fraction(4,1))

    def test_eval_power(self):
        self.assertEqual(eval_power(0, 1), 0)
        self.assertEqual(eval_power(0, 0), None)
        self.assertEqual(eval_power(0, -1), None)
        self.assertEqual(eval_power(2, 3), Fraction(8, 1))
        self.assertEqual(eval_power(Fraction(1, 2), 3), Fraction(1, 8))
        self.assertEqual(eval_power(2, -3), Fraction(1, 8))
        self.assertEqual(eval_power(Fraction(1, 2), -3), Fraction(8, 1))
        self.assertEqual(eval_power(Fraction(1, 2), -1), Fraction(2, 1))

    def test_simplify_rne_rec(self):
        self.assertEqual(simplify_rne_rec(1), 1)
        self.assertEqual(simplify_rne_rec(Fraction(2, 4)), Fraction(2,4))
        self.assertEqual(simplify_rne_rec(Fraction(2, 0)), None)
        self.assertEqual(simplify_rne_rec(Function('+', 1, 2)), Fraction(3, 1))
        self.assertEqual(simplify_rne_rec(Function('-', 1, 2)), Fraction(-1, 1))
        self.assertEqual(simplify_rne_rec(Function('*', 1, 2)), Fraction(2, 1))
        self.assertEqual(simplify_rne_rec(Function('/', 1, 2)), Fraction(1, 2))
        self.assertEqual(simplify_rne_rec(Function('^', 1, 2)), Fraction(1, 1))
        self.assertEqual(simplify_rne_rec(Function('^', Fraction(1, 0), 2)), None)

    def test_simplify_rne(self):
        self.assertEqual(simplify_rne(1), 1)
        self.assertEqual(simplify_rne(Fraction(1,2)), Fraction(1,2))
        self.assertEqual(simplify_rne(Fraction(2,1)), 2)
        self.assertEqual(simplify_rne(Fraction(4,2)), 2)
        self.assertEqual(simplify_rne(Fraction(2,0)), None)

class SimplifyExprTest(unittest.TestCase):
    def test_simplify_int_power(self):
        self.assertEqual(simplify_int_power(2, 2), 4)
        self.assertEqual(simplify_int_power(Fraction(1,2), 2), Fraction(1,4))
        self.assertEqual(simplify_int_power(Var("x"), 0), 1)
        self.assertEqual(simplify_int_power(Var("x"), 1), Var("x"))
        self.assertEqual(simplify_int_power(Var("x"), 2), Function('^', Var("x"), 2))
        self.assertEqual(simplify_int_power(Function('^', Var("x"), 2), 2), Function('^', Var("x"), 4))
        self.assertEqual(simplify_int_power(Function('^', Var("x"), Var("y")), 2), Function('^', Var("x"), Function('*', 2, Var("y"), commutative = True, associative = 1)))
        self.assertEqual(simplify_int_power(Function('*', Var("x"), Var("y")), 2), Function('*', Function('^', Var("x"), 2), Function('^', Var("y"), 2)))

    def test_simplify_power(self):
        self.assertEqual(simplify_power(Function('^', 1, None)), None)
        self.assertEqual(simplify_power(Function('^', None, 1)), None)
        self.assertEqual(simplify_power(Function('^', None, None)), None)
        self.assertEqual(simplify_power(Function('^', 0, 1)), 0)
        self.assertEqual(simplify_power(Function('^', 0, Fraction(1,2))), 0)
        self.assertEqual(simplify_power(Function('^', 1, Var("x"))), 1)
        self.assertEqual(simplify_power(Function('^', Var("x"), 2)), Function('^', Var("x"), 2))

    def test_simplify_diff(self):
        self.assertEqual(simplify_diff(Function('-', Var("a"), Var("b"))), Function('+', Var("a"), Function('*', -1, Var("b"))))

    def test_simplify_quot(self):
        self.assertEqual(simplify_quot(Function('/', Var("a"), Var("b"))), Function('*', Var("a"), Function('^', Var("b"), -1)))

if __name__ == '__main__':
    unittest.main(verbosity=2)
