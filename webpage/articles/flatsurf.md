[comment]: # (Copyright 2015 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

flatsurf package overview
=========================

flatsurf is a [Sagemath](http://sagemath.org) package that I wrote (with some help
from Samuel Lelièvre) to deal with translation surfaces. In order to install it, simply do

    $ sage -p http://www.labri.fr/perso/vdelecro/flatsurf-0.2.spkg

You will find more detailed installation instructions in the file [README.txt](README.txt).

In this article I briefly describe the usage of the package.

General usage
-------------

Once it is installed on your computer and Sage is launched, you need to enter
the following command

    :::pycon
    >>> from surface_dynamics.all import *

It makes accessible a lot of new objects (like `iet`, `AbelianStratum`, `QuadraticStratum`,
`CylinderDiagram`, `Origami` and `OrigamiDatabase`). Recall that to access the documentation
within Sage you need to put a question mark after the command and press enter

    :::pycon
    >>> Origami?
    Signature:      Origami(r, u, sparse=False, check=True, as_tuple=False, positions=None, name=None)
    Docstring:

      Constructor for origami

      INPUT:

      * "r", "u" - two permutations

      ...

Most of the functions in the package are well documented together with examples.

Strata and Interval exchange transformations
--------------------------------------------

The package contains a lot of code to deal with interval exchange transformations.

    :::pycon
    >>> p = iet.Permutation('a b c d', 'd c b a')
    >>> p
    a b c d
    d c b a
    >>> p.stratum()
    H(2)

    >>> q = iet.GeneralizedPermutation('a a', 'b b c c d d e e')
    >>> q.stratum()
    Q_0(1, -1^5)

You can also get one permutation from a given stratum component

    :::pycon
    >>> A = AbelianStratum(4,4)
    >>> cc = A.odd_component()
    >>> cc.permutation_representative()
    0 1 2 3 4 5 6 7 8 9 10
    3 2 5 4 6 8 7 10 9 1 0

    >>> Q = QuadraticStratum(12)
    >>> Q_reg = Q.regular_component()
    >>> Q_irr = Q.irregular_component()
    >>> Q_reg.permutation_representative()
    0 1 2 1 2 3 4 3 4 5
    5 6 7 6 7 0
    >>> Q_irr.permutation_representative()
    0 1 2 3 4 5 6 5
    7 6 4 7 3 2 1 0

It is possible to build the coding of a self-similar interval exchange transformation
using periodic paths in the Rauzy diagram.

    :::pycon
    >>> p = iet.Permutation('a b c d', 'd c b a')
    >>> R = p.rauzy_diagram()
    >>> g = R.path(p, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1)
    >>> s = g.substitution()
    >>> s
    WordMorphism: a->adbbd, b->adbbdbbd, c->adbcbcbd, d->adbcbd
    >>> s.fixed_point('a')
    word: adbbdadbcbdadbbdbbdadbbdbbdadbcbdadbbdad...

In the path `0` corresponds to top Rauzy induction and `1` to bottom. The above example
is exceptional since there are two eigenvalues `1` (while the generic spectrum is simple
by Avila-Viana)

    :::pycon
    >>> g.matrix().eigenvalues()
    [1, 1, 0.1458980337503155?, 6.854101966249684?]

Origamis
--------

To build an origami you just need to enter the two permutations defining it
to the constructor `Origami`

    :::pycon
    >>> from surface_dynamics.all import *
    >>> o = Origami('(1,2)', '(1,3)')
    >>> o
    (1,2)(3)
    (1,3)(2)

By convention the permutation are named `r` (for right) and `u` (for up)

    :::pycon
    >>> o.r()
    (1,2)
    >>> o.u()
    (1,3)

There are also some predefined origamis that are accessible via `origamis`

    :::pycon
    >>> ew = origamis.EierlegendeWollmilchsau()
    >>> ew
    Eierlegende Wollmilchsau
    >>> ew.u()
    (1,5,3,7)(2,8,4,6)
    >>> ew.r()
    (1,2,3,4)(5,6,7,8)

And it is also possible to build them from strata

    :::pycon
    >>> A = AbelianStratum(2,2)
    >>> cc = A.odd_component()
    >>> cc.one_origami(12)
    (1,2,3,4,5,6)
    (1,6)(2)(3,4)(5)

You can then compute many invariants

    :::pycon
    >>> o.stratum()
    H_2(2)
    >>> ew.stratum()
    H_3(1^4)

    >>> G = o.veech_group()
    >>> G
    Arithmetic subgroup with permutations of right cosets
     S2=(2,3)
     S3=(1,2,3)
     L=(1,2)
     R=(1,3)
    >>> G.is_congruence()
    True
    >>> o.lyapunov_exponents_approx()
    [0.333686792523229]
    >>> o.sum_of_lyapunov_exponents()
    4/3

    >>> ew.veech_group()
    Arithmetic subgroup with permutations of right cosets
     S2=()
     S3=()
     L=()
     R=()
    >>> ew.lyapunov_exponents_approx()
    [0.0000483946861896958, 0.0000468061832920360]
    >>> ew.sum_of_lyapunov_exponents()
    1

If you are interested in some statistics of a Teichmüller curve you can
iterate through the origamis it contains. For example we study the
distribution of the number of cylinders in all Teichmüller curves of
the component \( H^{odd}(4) \) (genus 3) with 11 squares

    :::pycon
	>>> for T in cc.arithmetic_teichmueller_curves(11):
    ...     cyls = [0]*3
    ...     for o in T:
    ...         n = len(o.cylinder_decomposition())
    ...         cyls[n-1] += 1
    ...     print cyls
    [1474, 4310, 2016]
    [110, 0, 90]
    [1650, 636, 1114]


The origami database
--------------------

The origami database is a database that contains the list of all arithmetic
Teichmüller curves (up to some number of squares). It is a standard sqlite
database and can also be read from other programs.

    :::pycon
    >>> from surface_dynamics.all import *
    >>> D = OrigamiDatabase()
    >>> q = D.query(stratum=AbelianStratum(2), nb_square=9)
    >>> q.number_of()
    2
    >>> o1,o2 = q.list()
    >>> o1
    (1)(2)(3)(4)(5)(6)(7,8,9)
    (1,2,3,4,5,6,7)(8)(9)
    >>> o2
    (1)(2)(3)(4)(5)(6)(7)(8,9)
    (1,2,3,4,5,6,7,8)(9)

To get the list of columns available in the database you can do

    :::pycon
    >>> D.cols()
    ['representative',
     'stratum',
     'component',
     'primitive',
     'quasi_primitive',
     'orientation_cover',
     'hyperelliptic',
     ...
     'automorphism_group_name']

Each column is available for display

    :::pycon
    >>> q = D.query(stratum=AbelianStratum(2))
    >>> q.cols
    >>> D = OrigamiDatabase()
    >>> q = D.query(('stratum', '=', AbelianStratum(2)), ('nb_squares', '<', 15))
    >>> q.cols('nb_squares', 'veech_group_level', 'teich_curve_nu2',
    ... 'teich_curve_nu3', 'teich_curve_genus', 'monodromy_name')
    >>> q.show()
    Nb squares           vg level             Teich curve nu2      Teich curve genus    Monodromy           
    ---------------------------------------------------------------------------------------------
    3                    2                    1                    0                    S3
    4                    12                   1                    0                    S4
    5                    60                   0                    0                    S5
    5                    15                   1                    0                    A5
    6                    60                   0                    0                    S6
    7                    420                  2                    0                    S7
    7                    105                  0                    0                    A7
    8                    840                  2                    1                    S8
    9                    630                  3                    0                    A9
    9                    2520                 0                    2                    S9
    10                   2520                 0                    4                    S10
    11                   6930                 0                    3                    A11
    11                   27720                3                    6                    S11
    12                   27720                4                    11                   S12
    13                   90090                3                    7                    A13
    13                   360360               0                    14                   S13
    14                   360360               0                    25                   S14

You can get some information about the filling of the database with

    :::pycon
    >>> D.info(genus=3)
    genus 3
    =======
     H_3(4)^hyp   : 163 T. curves (up to 51 squares)
     H_3(4)^odd   : 118 T. curves (up to 41 squares)
     H_3(3, 1)^c  :  72 T. curves (up to 25 squares)
     H_3(2^2)^hyp : 280 T. curves (up to 33 squares)
     H_3(2^2)^odd : 390 T. curves (up to 30 squares)
     H_3(2, 1^2)^c: 253 T. curves (up to 20 squares)
     H_3(1^4)^c   : 468 T. curves (up to 20 squares)


    Total: 1744 Teichmueller curves

More
----

If you have any doubt, question or request, send me an e-mail and I will update
this document.

Note that the package is by no mean complete. There are plenty of things under
development and/or integration. And your help is welcome:

 * interactive plotting (see the code in [this github repository](https://github.com/videlec/sage-flatsurf) written by Pat Hooper and me)

 * enumeration of pseudo-Anosov

 * enumeration of saddle connections and cylinder decompositions (Alex Eskin program)

 * code for testing minimality of an algebraic interval exchange (Michael Boshernitzan algorithm)

 * \( \operatorname{SL}(2, \mathbb{R}) \)-orbit closure of translation surfaces

 * monodromy representation of origamis (i.e. the morphism \( \operatorname{SL}(2, \mathbb{Z}) \to \operatorname{Sp}(2g, \mathbb{Z}) \))

 * more Lyapunov exponents (Charles Fougeron program)

 * ...

The code is publicly available, you can clone the code source using git

    git clone https://daemon@git.math.cnrs.fr/anon/plm/delecroix/flatsurf
