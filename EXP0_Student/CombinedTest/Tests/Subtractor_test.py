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
        self.min_signed = -(1 << (self.width - 1))  # -8 for 4-bit
        self.max_signed = (1 << (self.width - 1)) - 1  # 7 for 4-bit

        # Create rich table for printing
        self.table = Table(title="Combined Test Result")
        self.table.add_column("a", justify="right", style="cyan") 
        self.table.add_column("b", justify="right", style="cyan")
        self.table.add_column("Expected Sub", justify="right", style="green")
        self.table.add_column("DUT Sub", justify="right", style="red")
        self.table.add_column("Expected 2's Complement", justify="right", style="green")
        self.table.add_column("DUT 2's Complement", justify="right", style="red")
        #A model of the verilog code to confirm operation
    def performance_model(self, a,b):
        #A trick to make Python calculate 2's complement    
        self.expected_2scomplement = ((1<< self.width) - b) & self.max_value
        self.expected_sub = a-b
    #function run random tests selected number of times
    async def run_random_test(self, total_test_no):
        
        #Test for specified number of times
        for x in range(total_test_no):
            # Generate a as a signed 4-bit number
            a = random.randint(self.min_signed, self.max_signed)
            
            # Generate b such that a - b stays within range [-8, 7]
            min_b = max(self.min_signed, a - self.max_signed)  # Prevent underflow
            max_b = min(self.max_signed, a - self.min_signed)  # Prevent overflow
            b = random.randint(min_b, max_b)

            #Assign the random values as input for the DUT
            self.dut.a.value=a
            self.dut.b.value=b
            # Wait for a small time step (adder is combinational, so no clock needed)
            await Timer(1, units='us')
            self.performance_model(a,b)
            # Print debug info using Rich tables
            self.table.add_row(str(a), str(b), str(self.expected_sub), str(self.dut.subout.value.signed_integer), str(hex(self.expected_2scomplement)), str(hex(self.dut.compout.value.integer)))
            console.print(self.table)
            #Assert for correctness
            assert self.dut.subout.value.signed_integer == self.expected_sub
            assert self.dut.compout.value.integer == self.expected_2scomplement
            
            
        
@cocotb.test()
async def complementer_modeled_test(dut):
    #create test-bench object and call it's tests
    tb = TB(dut)
    await tb.run_random_test(50)
