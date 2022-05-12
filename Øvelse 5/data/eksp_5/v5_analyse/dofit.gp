#!/usr/bin/gnuplot

set title "eVMI XXX calibration on MONTH DAY, 2022"
set xlabel "R^2 in mm^2"
set ylabel "Photon energy in eV"
set y2label "Residuals in ‰"
set key top left reverse Left
set ytics nomirror
set y2tics
set xrange [0:]
set y2range [*<-5:5<*]
set linetype 2 pointtype 5
set linetype 3 pointtype 6

DATA = "table.txt"
BASENAME = "fit"

E(Rsq) = E0 + p0*Rsq + p1*Rsq**2 + p2*Rsq**3

fit E(x) DATA using ($2**2):1 via E0, p0, p1, p2

set terminal png enhanced
set output BASENAME.".png"

plot \
  E(x) title sprintf("%.3f + (%.5f)R^2 + (%.1e)R^4 + (%.1e)R^6", E0, p0, p1, p2), \
  DATA using ($2**2):1 title "Mean from Gaussian fits", \
  DATA using ($2**2):(($1-E($2**2))/E($2**2)*1000) axes x1y2 title "Residuals"

set terminal png enhanced
set output BASENAME.".png"
replot

set terminal pdf enhanced # size 8in,5in
set output BASENAME.".pdf"
replot

set xlabel "Detector radius / mm"
set ylabel "{/Symbol D}E / E"
set format y "%g %%"
unset y2label
unset y2tics
set ytics mirror
set key top right noreverse width -5
set grid
plot [][0:] \
  DATA u 2:(200*$3/$2) lt 2 title "Energy resolution"

set xlabel "Kinetic energy / eV"  
plot [][0:] \
  DATA u ($1-E0):(200*$3/$2) lt 2 title "Energy resolution"

set linestyle 10 dt 2 lc rgb "gray"
set grid ls 10, ls 0
set mxtics 5
set mytics 5
#set grid mxtics
set grid mytics
plot [][0:3] \
  DATA u ($1-E0):(200*$3/$2) lt 2 title "Energy resolution"