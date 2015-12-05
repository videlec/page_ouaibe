[comment]: # (Copyright 2015 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

flatsurf package overview
=========================

flatsurf is a [Sagemath](http://sagemath.org) package that I wrote (with some help
from Samuel Lelièvre) to deal with translation surfaces. In order to install it, simply do

    $ sage -p http://www.labri.fr/perso/vdelecro/flatsurf-0.2.spkg

Or you can follow the more detailed instructions from the [README](README.txt).

In this article I briefly describe its usage.

General usage
-------------

In order to use the code available in the package (and after you install it) you need
to enter the following line

    :::pycon
    >>> from surface_dynamics.all import *


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

    >>> p = iet.Permutation('a b c d', 'd c b a')
    >>> R = p.rauzy_diagram()
    >>> g = R.path(p, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1)
    >>> s = g.substitution
    >>> s
    WordMorphism: a->adbbd, b->adbbdbbd, c->adbcbcbd, d->adbcbd
    >>> s.fixed_point('a')
    word: adbbdadbcbdadbbdbbdadbbdbbdadbcbdadbbdad...

In the path `0` corresponds to top Rauzy induction and `1` to bottom. The above example
is exceptional since there are two eigenvalues `1` (while the generic spectrum is simple
by Avila-Viana)

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
