CLEAN = $(wildcard fit.log fit.pdf fit.png)

all: fit.pdf

fit.pdf: dofit.gp table.txt
	$(if $(wildcard fit.log),$(RM) fit.log)
	gnuplot $<

clean:
	$(if $(CLEAN),$(RM) $(CLEAN))

.PHONY: clean
