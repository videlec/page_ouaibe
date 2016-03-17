[comment]: # (Copyright 2016 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

Comment mesurer les performances d'un algorithme
================================================

Cet article (en construction) est en fait un petit pense bête. J'ai eu
recemment à faire des comparisons de vitesses d'exécution d'algorithmes
([l'évaluation des polynomes dans Sage][1] et [la série de Newton dans
flint][2]). Il contient ce que j'ai pu glaner sur comment faire ça en Python et
en C.

* Python timeit
* la librarie `time.h` du C (`clock_gettime`, `difftime`, `CLOCK_PROCESS_CPUTIME_ID`, `CLOCK_MONOTONIC`)
* faire des grapiques avec matplotlib

[1]: http://trac.sagemath.org/ticket/19822
[2]: https://github.com/wbhart/flint2/pull/213

