#----------------------------------------
# Longest Path - modificato
# file LP_opt.mod
#----------------------------------------

param n integer > 0; # numero nodi
param k integer > 0; # numero max archi da rimuovere
param M integer > 0; #costante grande 
set V := 1..n;

set A within (V cross V); # insieme archi (delle precedenze)

set A1 within (V cross V); #insieme precedenze deboli
set A2 within (V cross V); #insieme precedenze forti

param d{i in V} integer >=0; # durata dell'attività del nodo i

var x{(i, j) in  A1} binary; 	# var. 2.7
var t{i in V} integer; 			# var. 2.6

minimize longest_path_time: sum{(i, j) in  A1} x[i,j] + t[n]; # fz obiettivo

subject to budget_constraint : sum{(i, j) in  A1} x[i,j] <= k; # vinc. 2.3

subject to due_quattro {(i, j) in  A2} : t[j] >= t[i] + d[i]; # vinc. 2.4
subject to due_cinque {(i, j) in  A1} : t[j] >= t[i] + d[i] - M*x[i,j]; # vinc. 2.5

subject to due_sei {i in V} : t[i] >= 0; # vinc. 2.6










