#Examples shown after each opcode
class Opcodes:
	#Math OPS
	ADD = 1 #ADD 1, 2; adds 1 and 2
	ADDS = 14 #Same as ADD, but for strings (deprecated because im stupid)
	
	SUB = 2 #SUB 2, 1; subtracts 1 from 2
	SUBS = 15 #Same as SUB, but for strings (deprecated because im stupid)
	
	MUL = 3 #MUL 1, 2; multiplies 1 by 2
	MULS = 16 #Same as MUL, but for strings (deprecated because im stupid)
	
	DIV = 4 #DIV 9, 3; divides 9 by 3
	
	#COMPARISON OPS
	LESS = 5 #LESS 1, 2, 10; jumps to opcode ten
	
	EQUALS = 6 #EQUALS 1, 2, 10; does nothing as 1 and 2 are not equal
	
	MORE = 7 #MORE 2, 1, 10; jumps to opcode 10
	
	#STORE/DELETE OPS
	STORE = 8 #STORE var, 10; Stores 10 as var
	
	DEL = 9 #DEL var; Deletes variable
	
	#READ/WRITE OPS
	SYSWRITE = 10 #SYSWRITE var; Writes var to sys output defined by firm/bios.bin (typically console)
	
	SYSREAD = 11 #SYSREAD var; Reads using method defined in firm/bios.bin to return stack (typically user input)
	
	WRITE = 12 #WRITE "/path/to/file", var; writes var content to "/path/to/file"
	
	READ = 13 #READ "/path/to/file"; pushes contents of file at "/path/to/file" to return stack
	
	READRET = 20 #READRET var; Reads the return mem value and sets vars value to it
	
	#JUMP AND CALL
	JMP = 17 #JMP 10; jumps to opcode ten and continues after opcode ten
	
	CALL = 18 #CALL 10; calls opcode ten and then returns to the previous opcode
	
	CALLPY = 19 #Calls python func with given name and arguments
	
	IMPORT = 21 #IMPORT "file.bin"; executes file with given name and exits the current program  
	
	#OTHER
	EXIT = 22
	
	ERR = 255 #Raises error given
	
	OPSEP = 0
	
	ARGSEP = 1
