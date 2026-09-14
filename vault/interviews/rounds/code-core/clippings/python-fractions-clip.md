---
title: fractions — Rational numbers
source: https://docs.python.org/3/library/fractions.html
published: '2026-08-26'
site: Python documentation
clipped: '2026-08-27'
---

# fractions — Rational numbers

# `fractions` — Rational numbers[¶](#module-fractions)

**Source code:** [Lib/fractions.py](https://github.com/python/cpython/tree/3.14/Lib/fractions.py)

The `fractions` module provides support for rational number arithmetic.

A Fraction instance can be constructed from a pair of rational numbers, from a single number, or from a string.

- 
*class* fractions.Fraction(*numerator=0* ,*denominator=1* )[¶](#fractions.Fraction)
- 
*class* fractions.Fraction(*number* )
- 
*class* fractions.Fraction(*string* )
- The first version requires that *numerator* and*denominator* are instances
of[`numbers.Rational`](numbers.html#numbers.Rational) and returns a new`Fraction` instance
with a value equal to`numerator/denominator` .
If*denominator* is zero, it raises a[`ZeroDivisionError`](exceptions.html#ZeroDivisionError) .The second version requires that *number* is an instance of[`numbers.Rational`](numbers.html#numbers.Rational) or has the`as_integer_ratio()` method
(this includes[`float`](functions.html#float) and[`decimal.Decimal`](decimal.html#decimal.Decimal) ).
It returns a`Fraction` instance with exactly the same value.
Assumed, that the`as_integer_ratio()` method returns a pair
of coprime integers and last one is positive.
Note that due to the
usual issues with binary point (see[Floating-Point Arithmetic:  Issues and Limitations](../tutorial/floatingpoint.html#tut-fp-issues) ), the
argument to`Fraction(1.1)` is not exactly equal to 11/10, and so`Fraction(1.1)` does*not* return`Fraction(11, 10)` as one might expect.
(But see the documentation for the[`limit_denominator()`](#fractions.Fraction.limit_denominator) method below.)The last version of the constructor expects a string. The usual form for this instance is: [sign] numerator ['/' denominator] where the optional `sign` may be either ‘+’ or ‘-’ and`numerator` and`denominator` (if present) are strings of
decimal digits (underscores may be used to delimit digits as with
integral literals in code).  In addition, any string that represents a finite
value and is accepted by the[`float`](functions.html#float) constructor is also
accepted by the`Fraction` constructor.  In either form the
input string may also have leading and/or trailing whitespace.
Here are some examples:>>> from fractions import Fraction >>> Fraction(16, -10) Fraction(-8, 5) >>> Fraction(123) Fraction(123, 1) >>> Fraction() Fraction(0, 1) >>> Fraction('3/7') Fraction(3, 7) >>> Fraction(' -3/7 ') Fraction(-3, 7) >>> Fraction('1.414213 \t\n') Fraction(1414213, 1000000) >>> Fraction('-.125') Fraction(-1, 8) >>> Fraction('7e-6') Fraction(7, 1000000) >>> Fraction(2.25) Fraction(9, 4) >>> Fraction(1.1) Fraction(2476979795053773, 2251799813685248) >>> from decimal import Decimal >>> Fraction(Decimal('1.1')) Fraction(11, 10) The `Fraction` class inherits from the abstract base class[`numbers.Rational`](numbers.html#numbers.Rational) , and implements all of the methods and
operations from that class.`Fraction` instances are[hashable](../glossary.html#term-hashable) ,
and should be treated as immutable.  In addition,`Fraction` has the following properties and methods:Changed in version 3.2: The `Fraction` constructor now accepts[`float`](functions.html#float) and[`decimal.Decimal`](decimal.html#decimal.Decimal) instances.Changed in version 3.9: The [`math.gcd()`](math.html#math.gcd) function is now used to normalize the*numerator* and*denominator* .`math.gcd()` always returns an[`int`](functions.html#int) type.
Previously, the GCD type depended on*numerator* and*denominator* .Changed in version 3.11: Underscores are now permitted when creating a `Fraction` instance
from a string, following[**PEP 515**](https://peps.python.org/pep-0515/) rules.Changed in version 3.11: `Fraction` implements`__int__` now to satisfy`typing.SupportsInt` instance checks.Changed in version 3.12: Space is allowed around the slash for string inputs: `Fraction('2 / 3')` .Changed in version 3.12: `Fraction` instances now support float-style formatting, with
presentation types`"e"` ,`"E"` ,`"f"` ,`"F"` ,`"g"` ,`"G"` and`"%""` .Changed in version 3.13: Formatting of `Fraction` instances without a presentation type
now supports fill, alignment, sign handling, minimum width and grouping.Changed in version 3.14: The `Fraction` constructor now accepts any objects with the`as_integer_ratio()` method.
  - 
numerator[¶](#fractions.Fraction.numerator)
  - Numerator of the Fraction in lowest term.
 
  - 
denominator[¶](#fractions.Fraction.denominator)
  - Denominator of the Fraction in lowest terms. Guaranteed to be positive.
 
  - 
as_integer_ratio()[¶](#fractions.Fraction.as_integer_ratio)
  - Return a tuple of two integers, whose ratio is equal to the original Fraction. The ratio is in lowest terms and has a positive denominator. Added in version 3.8.
 
  - 
is_integer()[¶](#fractions.Fraction.is_integer)
  - Return `True` if the Fraction is an integer.Added in version 3.12.
 
  - 
*classmethod* from_float(*f* )[¶](#fractions.Fraction.from_float)
  - Alternative constructor which only accepts instances of [`float`](functions.html#float) or[`numbers.Integral`](numbers.html#numbers.Integral) . Beware that`Fraction.from_float(0.3)` is not the same value as`Fraction(3, 10)` .Note From Python 3.2 onwards, you can also construct a `Fraction` instance directly from a[`float`](functions.html#float) .
 
  - 
*classmethod* from_decimal(*dec* )[¶](#fractions.Fraction.from_decimal)
  - Alternative constructor which only accepts instances of [`decimal.Decimal`](decimal.html#decimal.Decimal) or[`numbers.Integral`](numbers.html#numbers.Integral) .Note From Python 3.2 onwards, you can also construct a `Fraction` instance directly from a[`decimal.Decimal`](decimal.html#decimal.Decimal) instance.
 
  - 
*classmethod* from_number(*number* )[¶](#fractions.Fraction.from_number)
  - Alternative constructor which only accepts instances of [`numbers.Integral`](numbers.html#numbers.Integral) ,[`numbers.Rational`](numbers.html#numbers.Rational) ,[`float`](functions.html#float) or[`decimal.Decimal`](decimal.html#decimal.Decimal) , and objects with
the`as_integer_ratio()` method, but not strings.Added in version 3.14.
 
  - 
limit_denominator(*max_denominator=1000000* )[¶](#fractions.Fraction.limit_denominator)
  - Finds and returns the closest `Fraction` to`self` that has
denominator at most max_denominator.  This method is useful for finding
rational approximations to a given floating-point number:>>> from fractions import Fraction >>> Fraction('3.1415926535897932').limit_denominator(1000) Fraction(355, 113) or for recovering a rational number that’s represented as a float: >>> from math import pi, cos >>> Fraction(cos(pi/3)) Fraction(4503599627370497, 9007199254740992) >>> Fraction(cos(pi/3)).limit_denominator() Fraction(1, 2) >>> Fraction(1.1).limit_denominator() Fraction(11, 10)
 
  - 
__floor__()[¶](#fractions.Fraction.__floor__)
  - Returns the greatest [`int`](functions.html#int)`<= self` .  This method can
also be accessed through the[`math.floor()`](math.html#math.floor) function:>>> from math import floor >>> floor(Fraction(355, 113)) 3
 
  - 
__ceil__()[¶](#fractions.Fraction.__ceil__)
  - Returns the least [`int`](functions.html#int)`>= self` .  This method can
also be accessed through the[`math.ceil()`](math.html#math.ceil) function.
 
  - 
__round__()[¶](#fractions.Fraction.__round__)
  - 
__round__(*ndigits* )
  - The first version returns the nearest [`int`](functions.html#int) to`self` ,
rounding half to even. The second version rounds`self` to the
nearest multiple of`Fraction(1, 10**ndigits)` (logically, if`ndigits` is negative), again rounding half toward even.  This
method can also be accessed through the[`round()`](functions.html#round) function.
 
  - 
__format__(*format_spec* ,*/* )[¶](#fractions.Fraction.__format__)
  - Provides support for formatting of `Fraction` instances via the[`str.format()`](stdtypes.html#str.format) method, the[`format()`](functions.html#format) built-in function, or[Formatted string literals](../reference/lexical_analysis.html#f-strings) .If the `format_spec` format specification string does not end with one
of the presentation types`'e'` ,`'E'` ,`'f'` ,`'F'` ,`'g'` ,`'G'` or`'%'` then formatting follows the general rules for fill,
alignment, sign handling, minimum width, and grouping as described in the[format specification mini-language](string.html#formatspec) . The “alternate
form” flag`'#'` is supported: if present, it forces the output string
to always include an explicit denominator, even when the value being
formatted is an exact integer. The zero-fill flag`'0'` is not
supported.If the `format_spec` format specification string ends with one of
the presentation types`'e'` ,`'E'` ,`'f'` ,`'F'` ,`'g'` ,`'G'` or`'%'` then formatting follows the rules outlined for the[`float`](functions.html#float) type in the[Format specification mini-language](string.html#formatspec) section.Here are some examples: >>> from fractions import Fraction >>> format(Fraction(103993, 33102), '_') '103_993/33_102' >>> format(Fraction(1, 7), '.^+10') '...+1/7...' >>> format(Fraction(3, 1), '') '3' >>> format(Fraction(3, 1), '#') '3/1' >>> format(Fraction(1, 7), '.40g') '0.1428571428571428571428571428571428571429' >>> format(Fraction('1234567.855'), '_.2f') '1_234_567.86' >>> f"{Fraction(355, 113):*>20.6e}" '********3.141593e+00' >>> old_price, new_price = 499, 672 >>> "{:.2%} price increase".format(Fraction(new_price, old_price) - 1) '34.67% price increase'
- 
numerator

See also

- Module [`numbers`](numbers.html#module-numbers)
- The abstract base classes making up the numeric tower.
