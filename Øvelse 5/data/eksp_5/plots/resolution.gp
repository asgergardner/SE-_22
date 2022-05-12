#!/usr/bin/gnuplot

# set title 'VMI energy resolution'
set key top left Left opaque
set xrange [0:]
set linetype 10 dashtype 2 linecolor 0 linewidth 2
set linetype 1 pointtype 8
set linetype 2 pointtype 3 pointsize 1.1
set linetype 3 pointtype 10
set linetype 9 pointtype 3
set linetype 6 pointtype 8
set linetype 7 pointsize 0.8
set linetype 5 pointtype 13
set linetype 8 pointtype 6 pointsize 0.8

set terminal pdf enhanced size 5.0in,2.3in
set output "resolution.pdf"

E0 = 24.587 - 0.093

MAY2801s50part2 = "../../../2022/220505_eVMI_calibration/calibration_eVMI_2801_50p/fitresults/tablefg.txt"
MAY2831part2 = "../../../2022/220505_eVMI_calibration/calibration_eVMI_2831/fitresults/tablefg.txt"
MAYEL4D3KVpart2 = "../../../2022/220505_eVMI_calibration/calibration_eVMI_2834_4300V_HE/fitresults/tablefg.txt"
MAYEL4D3KVpart1 = "../../../2022/220505_eVMI_calibration/calibration_eVMI_2834_4300V_LE/fitresults/tablefg.txt"

NOV2801s50part2 = "<awk '!(NR % 2) {print}' ../../../2021/211123_eVMI_calibrations/calibration_eVMI_2801_50p_HE_Nov_28/fitresults/tablefg.txt"
NOV2801s50part1 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2801_50p_LE_Nov_28/fitresults/tablefg.txt"
NOV2801part2 = "<awk '!(NR % 2) {print}' ../../../2021/211123_eVMI_calibrations/calibration_eVMI_2801_HE_Nov_28/fitresults/tablefg.txt"
NOV2801part1 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2801_LE_Nov_28/fitresults/tablefg.txt"
NOV2831part2 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2831_HE_Nov_28/fitresults/tablefg.txt"
NOV2831part1 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2831_LE_Nov_28/fitresults/tablefg.txt"
NOV2833part2 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2833_HE_Nov_28/fitresults/tablefg.txt"
NOV2833part1 = "../../../2021/211123_eVMI_calibrations/calibration_eVMI_2833_LE_Nov_28/fitresults/tablefg.txt"

set macros
using = "using ($1-E0):(200*$3/$2)"

set multiplot
set size 0.46,1

splitAt = 3.6

set origin 0,0
set key top right width -1.5 samplen 1
set xlabel " "
set ylabel "{/Symbol D}E / E"
set format y "%g %%"
set ytics 4
set mytics 2
set grid
set grid mytics
axes = "axes x1y1"
set xrange [0:splitAt]
set yrange [0:18]
plot \
  MAYEL4D3KVpart1 @using @axes linetype 5 notitle "4.3 kV lens (May 22)", \
  NOV2831part1 @using @axes linetype 7 notitle "3.5 kV lens (Nov 21)", \
  MAY2831part2 @using @axes linetype 8 notitle "3.5 kV lens (May 22)", \
  NOV2801part1 @using @axes linetype 2 title "100 % (Nov 21)", \
  NOV2801s50part1 @using @axes linetype 1 title "50 % (Nov 21)", \
  MAY2801s50part2 @using @axes linetype 3 title "50 % (May 22)"

set xlabel sprintf("% -75s", "electron kinetic energy / eV")
set key width -2.5
set size 0.635,1
set origin 0.395,0
axes = "axes x1y2"
set xrange [splitAt:75]
set y2range [0.0:6.3]
unset ylabel
set y2label "{/Symbol D}E / E"
set format y ""
set format y2 "%g %%"
set y2tics 1.4
set grid y2
plot \
  MAYEL4D3KVpart2 @using @axes linetype 5 title "4.3 kV lens (May 22)", \
  NOV2831part2 @using @axes linetype 7 title "3.5 kV lens (Nov 21)", \
  MAY2831part2 @using @axes linetype 8 title "3.5 kV lens (May 22)", \
  NOV2801part2 @using @axes linetype 2 notitle "100 % (Nov 21)", \
  NOV2801s50part2 @using @axes linetype 1 notitle "50 % (Nov 21)", \
  MAY2801s50part2 @using @axes linetype 3 notitle "50 % (May 22)"

unset multiplot
