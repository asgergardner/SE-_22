#!/usr/bin/gnuplot

set terminal pdf enhanced size 5in,6in
set output "tof_calibration.pdf"

set title 'Mass calibration for VMI XXXX (DATE)'
set xlabel 'sqrt(mass / u)'
set ylabel 'flight time / ns'
set key at 2.6,1000 reverse samplen -1 left
set linetype 1 pointtype 4
set grid
set label 1 at sqrt(4),1000 "He^{+}" center
set label 2 at sqrt(14),1550 "N^{+}" right
set label 5 at sqrt(28),1650 "N_{2}^{+}"
set label 6 at sqrt(32),2300 "O_{2}^{+}" center

f(x) = t0 + slope*x
fit f(x) "tof_calibration.txt" using (sqrt($2)):1 via slope, t0

set multiplot layout 2,1
plot [0:][0:] \
 "tof_calibration.txt" using (sqrt($2)):1 notitle, \
 f(x) title sprintf("%g + %g * m^{0.5}", t0, slope)

unset title
set ylabel 'residuals in ‰'
plot [0:][*<-4:4<*] "tof_calibration.txt" using (sqrt($2)):(($1 - f(sqrt($2)))/f(sqrt($2))*1000)

unset multiplot
