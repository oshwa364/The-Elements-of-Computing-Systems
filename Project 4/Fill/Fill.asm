// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

// Initialize

// Not optimal, but it works
@24576
D=A
@n
M=D

@SCREEN
D=A
@point
M=D

(CHECKKBD)
@KBD
D=M
@LOOPFILL
D;JNE
@LOOPDELETE
D;JEQ

(LOOPFILL)
@point
D=M
@n
D=D-M
@CHECKKBD
D;JEQ
@point
A=M
M=-1
@point
M=M+1
@CHECKKBD
0;JMP

(LOOPDELETE)
@point
D=M
@SCREEN
D=D-A
@CHECKKBD
D;JEQ
@point
M=M-1
A=M
M=0
@LOOPDELETE
0;JMP
