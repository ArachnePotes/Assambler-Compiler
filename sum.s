addi x27,x0,1 #mult
addi x28,x0,4 #num
addi x29,x0,1 #i
addi x30,x0,1 #fact

bge x28, x29, cycle #otros
beq x28, x0, fin #!0

cycle:
	addi x30,x30,1
mult:
	add
fin:
addi x0,x0,0