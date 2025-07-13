RUNFILE:=run.f

# Default target: run simulation
all: run

# Clean target: remove generated files
clean:
	rm -rf worklib xcelium.d *.log *.history

# Compile and elaborate design
compile:
	xrun -f $(RUNFILE) -compile -access +rwc

# Elaborate design (if already compiled)
elaborate:
	xrun -f $(RUNFILE) -elaborate

# Run simulation
run: elaborate tb/rcu_tb.sv
	xrun -f $(RUNFILE) -R

tb/rcu_tb.sv: ../util/gen_rcu_tb.py
	python3 $< > $@

# Run with GUI
run-gui: elaborate
	xrun -f $(RUNFILE) -gui -access +rwc

# Run simulation with clean build
run-clean: clean compile run

.PHONY: clean
