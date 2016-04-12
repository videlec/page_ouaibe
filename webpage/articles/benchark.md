[comment]: # (Copyright 2016 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

Comment mesurer les performances d'un algorithme
================================================

Cet article (en construction) est en fait un petit pense bête. J'ai eu
recemment à faire des comparisons de vitesses d'exécution d'algorithmes
([l'évaluation des polynomes dans Sage][1] et les sommes de puissances
de racines dans Flint, voir [pull/231][1] et [pull/251][3]).
Il contient ce que j'ai pu glaner sur comment faire ça en Python et en C.

Version en C
------------

Calculer le temps pris par un morceau de code n'est pas facile: il y a d'autres
programmes qui tournent en même temps, il y a des évènements qui peuvent
ralentir de manière aléatoire le programme (écriture/lecture disque), ...

La solution radicale est de faire tourner le programme en "temps réel",
c'est-à-dire sans interruption par le système d'exploitation. J'opte pour
une solution douce qui repose sur la librairie `time.h`. La structure de
données qui nous intéresse et les fonctions qui nous intéressent sont tous
simples.

	:::c
    struct timespec {
        time_t   tv_sec;        /* seconds */
        long     tv_nsec;       /* nanoseconds */
    };

    int clock_gettime(clockid_t clk_id, struct timespec *tp);
    double difftime(time_t time1, time_t time0);

Il y a des choses faciles à comprendre: la structure `timespec` contient un
temps, on l'obtient avec `clock_gettime` et on peut faire des différence avec
`difftime`. Il y a quand même des choses bizarres: `time_t`? pourquoi
`difftime(time1, time0)` et pas `time1 - time0`? c'est quoi `colckid_t`?

Le type `time_t` est un type généralement défini dans `<sys/types.h>` est qui
défini un type pour les secondes. Sur ma machine c'est un `long int`. Pour
trouver cela, il suffit de précompiler un fichier C `check_time.c` qui contient
seulement la ligne `#include <time.h>`. En deux lignes

    $ echo "#include <time.h>" > check_time.c
	$ gcc -E check_time.c | grep typedef | grep __time_t
	typedef long int __time_t;
	typedef __time_t time_t;

Cependant, le standard C ne définit aucune norme pour ce type! Seulement qu'il
existe cette fameuse fonction `difftime`.

La fonction `clock_gettime` permet d'avoir accès à différentes horloges, c'est
le fameux premier argument de type `clockid_t`. Les possibilités sont

* `CLOCK_REALTIME`: horloge système

* `CLOCK_MONOTONIC`: horloge monotone depuis un certain départ. L'avantage de
  cette horloge est qu'elle ignore une remise à l'heure de l'ordinateur. Par
  contre elle est sensible aux appels à `adjtime` et NTP.

* `CLOCK_MONOTONIC_RAW` (seulement linux récent): comme la précédente mais ne
  souffre pas aux appels à `adjtime` et NTP.

* `CLOCK_PROCESS_CPUTIME_ID` (seulement linux récent): horloge haute résolution
  qui donne le temps CPU consomé par un processus (fait la somme des threads
  s'il y en a)..

* `CLOCK_THREAD_CPUTIME_ID` (seulement linux récent): consomation du temps CPU
  d'un thread.

Il y a en d'autres plus exotiques (faire un `man clock_gettime` si vous
les voulez toutes).

Ainsi, pour obtenir du temps processus écoulé en millisecondes on pourra faire

    :::c

    #if defined CLOCK_PROCESS_CPUTIME_ID
    #define CLOCKTYPE CLOCK_PROCESS_CPUTIME_ID
    #elif defined CLOCKTYPE_MONOTONIC_RAW
    #define CLOCKTYPE CLOCK_MONOTONIC_RAW
    #else
    #define CLOCKTYPE CLOCK_MONOTONIC
    #endif

    ...

    int main(void)
    {
		struct timespec tsi, tsf;
		double elaps;

        ...

        clock_gettime(CLOCKTYPE, &tsi);
        /* the code to test */
        ...
        /*     up to here   */
        clock_gettime(CLOCKTYPE, &tsf);

        elaps = difftime(tsf.tv_sec, tsi.tv_sec) * 1.0e3;
        elaps += (tsf.tv_nsec - tsi.tv_nsec) / 1.0e6;

        printf("le calcul a pris %f millisecondes\n", elaps);
    }

A suivre...
-----------

* Python timeit

* Faire un joli graphique avec matplotlib

![graphique power sums deg 33 mod 293](graphic_deg33_mod293.png)

Quelques références
-------------------
[1]: http://trac.sagemath.org/ticket/19822
[2]: https://github.com/wbhart/flint2/pull/213
[3]: https://github.com/wbhart/flint2/pull/251
[4]: http://pubs.opengroup.org/onlinepubs/007908775/xsh/time.h.html
[5]: http://pubs.opengroup.org/onlinepubs/007908775/xsh/systypes.h.html
