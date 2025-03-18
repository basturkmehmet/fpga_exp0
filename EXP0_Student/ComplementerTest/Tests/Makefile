# Supplied for EE314 Exp 0 by Doğu Erkan Arkadaş

CWD=$(shell pwd)

SIM ?= icarus
TOPLEVEL_LANG ?=verilog

VERILOG_SOURCES =$(CWD)/../HDL/*.v

TOPLEVEL = OurComplementer
MODULE := Complementer_test
COCOTB_HDL_TIMEUNIT=1us
COCOTB_HDL_TIMEPRECISION=1us

# Include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
