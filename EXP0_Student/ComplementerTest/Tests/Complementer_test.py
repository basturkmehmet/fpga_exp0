# ==============================================================================
# Authors:              Doğu Erkan Arkadaş
#
# Cocotb Testbench:     For Simple Adder
#
# Description:
# ------------------------------------
# Part of the experiment 0 of EE 314
#
# License:
# ==============================================================================


import random

import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue
from rich.console import Console
from rich.table import Table

console = Console()

class TB:
    def __init__(self, dut):
        self.dut = dut
        #Get the width of the inputs for the model
        self.width=4
        self.max_value = (1<<self.width)-1 

        # Create rich table for printing
        self.table = Table(title="Complementer Test Result")
        self.table.add_column("a", justify="right", style="cyan")
        self.table.add_column("Expected 2's Complement", justify="right", style="green")
        self.table.add_column("DUT Output", justify="right", style="red")
        #A model of the verilog code to confirm operation
    def performance_model(self, a):
        #A trick to make Python calculate 2's complement
        self.expected_2scomplement = ((1<< self.width) - a) & self.max_value
    
    #function run random tests selected number of times
    async def run_random_test(self, total_test_no):
        
        #Test for specified number of times
        for x in range(total_test_no):
            #Generate a random value      
            a=random.randint(0, self.max_value)

            #Assign the random value as input for the DUT
            self.dut.a.value=a
            # Wait for a small time step (adder is combinational, so no clock needed)
            await Timer(1, units='us')
            self.performance_model(a)
            # Print debug info using Rich tables
            self.table.add_row(str(hex(a)), str(hex(self.expected_2scomplement)), str(hex(self.dut.compout.value.integer)))
            console.print(self.table)
            #Assert for correctness
            assert self.dut.compout.value.integer == self.expected_2scomplement
            
            
        
@cocotb.test()
async def complementer_modeled_test(dut):
    #create test-bench object and call it's tests
    tb = TB(dut)
    await tb.run_random_test(50)
