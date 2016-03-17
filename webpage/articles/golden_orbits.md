[comment]: # (Copyright 2015 Vincent Delecroix <vincent.delecroix@labri.fr>)
[comment]: # (Cet article est publié sous la licence Creative Commons Attribution-NonCommercial 4.0 International License.)
[comment]: # (This article is published under the Creative Commons Attribution-NonCommercial 4.0 International License)

Golden teichmüller geodesics
============================

These computations are related to my owngoing work with Michael Boshernitzan.

A *golden torus* is a torus of the form \( \mathbb{C} / g_t \Lambda \) where
\( \Lambda = \mathbb{Z} (-1,1) \oplus \mathbb{Z} (\phi,-1, \phi) \) where
\( \phi = \frac{\sqrt{5}+1}{2} \). The associated geodesics on the modular
surface is known to enjoy two properties

* it is the shortest geodesic

* it is the geodesic that maximize the minimum of the (flat) systole

We proved together with Michael that in general, Teichmüller geodesics that
enjoy the second property are exactly the ones that are obtained as 
ramified covers of a golden torus. During a talk in CIRM (Marseille) in July
2015, Curtis McMullen asked the following question: what do we know on the
*lengths* of these geodesics? Indeed, they are unlikely to be shortest
geodesics in their stratum component.

The number of preimages of a golden torus in a given translation surface
can be effectively computed using character theory. Hence this gives
the cumulated lengths of these golden geodesics. But what about the
shortest? the longest?

Using the flatsurf package, I wrote up a small program and get this
interesting data

| Component of stratum | Nb golden sts | Nb geod. | min length | max length |
|----------------------|---------------|----------|------------|------------|
| H(2)^hyp             |             3 |        1 |          3 |          3 |
| H(1^2)^hyp           |            10 |        4 |          2 |          3 |
| H(4)^hyp             |            18 |        2 |          3 |         15 |
| H(2^2)^hyp           |            57 |        7 |          3 |         18 |
| H(6)^hyp             |           143 |       15 |          1 |         21 |
| H(3^2)^hyp           |           450 |       34 |          3 |         36 |
| H(8)^hyp             |          1326 |       28 |          3 |        321 |
| H(4^2)^hyp           |          4262 |       88 |          2 |        681 |
| H(8)^hyp             |          1326 |       28 |          3 |        321 |
| H(6)^even            |           412 |       34 |          1 |         66 |
| H(4, 2)^even         |          2009 |       83 |          1 |        324 |
| H(8)^even            |         34821 |      521 |          1 |        888 |
| H(2^3)^even          |          1996 |      110 |          1 |        102 |
| H(6, 2)^even         |        151521 |     1771 |          1 |       1796 |
| H(4^2)^even          |         65568 |     1618 |          1 |       1390 |
| H(4)^odd             |            22 |        6 |          3 |          5 |
| H(2^2)^odd           |            69 |       11 |          1 |          9 |
| H(6)^odd             |           697 |       47 |          1 |         78 |
| H(4, 2)^odd          |          2459 |       95 |          1 |        183 |
| H(2^3)^odd           |          2296 |      108 |          1 |        312 |
| H(6, 2)^odd          |        160632 |     1900 |          1 |       1596 |
| H(4^2)^odd           |         69694 |     1781 |          1 |        768 |
| H(3, 1)^c            |           124 |       15 |          1 |         24 |
| H(2, 1^2)^c          |           360 |       22 |          8 |         33 |
| H(5, 1)^c            |          5866 |      230 |          1 |        340 |
| H(3^2)^nonhyp        |          2174 |      195 |          1 |         88 |
| H(1^4)^c             |           302 |       41 |          1 |         81 |
| H(4, 1^2)^c          |         16396 |      648 |          1 |        390 |
| H(3, 2, 1)^c         |         26416 |      540 |          1 |        762 |
| H(7, 1)^c            |        408956 |     4284 |          1 |       2354 |
| H(5, 3)^c            |        269047 |     3427 |          1 |       2332 |
| H(3, 1^3)^c          |         31758 |      719 |          1 |        711 |
| H(2^2, 1^2)^c        |         48308 |     1741 |          1 |        603 |

Here is the function that was used for these computations. It decomposes the set of golden surfaces
in a given stratum into Teichmüller geodesics.

    :::python
	def orbits(cc):
	    d = cc.stratum().dimension()-1
	    O = cc.origamis(d)
	    res = []
	    while O:
	        orbit = []
	        o = O.pop()
	        orbit.append(o)
	        o = o.horizontal_twist().vertical_twist()
	        o.relabel(inplace=True)
	        while o in O:
	            O.remove(o)
	            orbit.append(o)
	            o = o.horizontal_twist().vertical_twist()
	            o.relabel(inplace=True)
	        res.append(orbit)
	    return res
