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

        # Create rich table for logging
        self.table = Table(title="Adder Test Result")
        self.table.add_column("a", justify="right", style="cyan")
        self.table.add_column("b", justify="right", style="cyan")
        self.table.add_column("Expected Sum", justify="right", style="green")
        self.table.add_column("DUT Output", justify="right", style="red")
        #A model of the verilog code to confirm operation
    def performance_model(self, a, b):
        #answer to return
        self.expected_sum = a+b
    
    #function run random tests selected number of times
    async def run_random_test(self, total_test_no):
        
        #Test for specified number of times
        for x in range(total_test_no):
            # Generate a as a signed 4-bit number
            a = random.randint(self.min_signed, self.max_signed)
            
            # Generate b such that a + b stays within range [-8, 7]
            min_b = max(self.min_signed, -a + self.min_signed)  # Prevent overflow on the negative side
            max_b = min(self.max_signed, -a + self.max_signed)  # Prevent overflow on the positive side
            b = random.randint(min_b, max_b)


            #Assign the random values as input for the DUT
            self.dut.a.value=a
            self.dut.b.value=b
            # Wait for a small time step (adder is combinational, so no clock needed)
            await Timer(1, units='us')
            self.performance_model(a,b)
            # Print debug info using Rich tables
            self.table.add_row(str(a), str(b), str(self.expected_sum), str(self.dut.sum.value.signed_integer))
            console.print(self.table)
            #Assert for correctness
            assert self.dut.sum.value.signed_integer == self.expected_sum
            
            
        
@cocotb.test()
async def adder_modeled_test(dut):
    #create test-bench object and call it's tests
    tb = TB(dut)
    await tb.run_random_test(50)
