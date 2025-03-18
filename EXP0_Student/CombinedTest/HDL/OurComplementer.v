module OurComplementer ( // This is a template. 
// You can modify the input-output declerations(width etc.) without changing the names.
    input [3:0] a, // input A
    output [3:0] compout // Complementer output
);

// Fill here
	assign compout = ~a+1;
	
endmodule