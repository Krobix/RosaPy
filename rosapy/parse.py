from bytecode import Opcodes as ops

text_tokens = ("ADD",
"SUB",
"MUL",
"DIV",
"LESS",
"EQUALS",
"MORE",
"STORE",
"DEL",
"SYSWRITE",
"SYSREAD",
"WRITE",
"READ",
"ADDS",
"SUBS",
"MULS",)

NUM_CHARS = "0123456789"

def parse_asm_func_call(cont):
	pass
	
def remove_starting_whitespace(line):
	"self explanatory"
	while line.startswith(" ") or line.startswith("\n"):
		tmp = list(line)
		tmp.pop(0)
		line = "".join(tmp)
	return line

def tokenize_asm_line(line):
	"Returns line, but stripped to a list"
	line = remove_starting_whitespace(line)
	oline = line
	line = line.split(" ")
	line = oline.split(",")
	newline = ""
	for x in line:
		tmpstr = remove_starting_whitespace(x)
		newline += tmpstr
	return newline
	
class RosaBinFile:
	def __init__(self):
		self.code = []
		self._asm_stripped = [] #Only used when assembling
		self.bin_raw_content = b""
		
	def lex_from_asm_text(self, txt):
		non_stripped_lines = txt.split(";")
		for x in non_stripped_lines:
			x = tokenize_asm_line(x)
			self._asm_stripped.append(x)
			
	def assemble_file(self, filename):
		"must call lex_from_asm_text before assembling"
		self.bin_raw_content += b"ROSAPYVM\x81"
		for x in self._asm_stripped:
