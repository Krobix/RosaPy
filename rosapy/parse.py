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
	newline = []
	line = remove_starting_whitespace(line)
	oline = line
	line = line.split(" ")
	try:
		newline += [line[0], line[1]] 
	except IndexError:
		pass
	line = oline.split(",")
	try:
		for x in line[2:]:
			tmpstr = remove_starting_whitespace(x)
			newline.append(tmpstr)
	except IndexError:
		pass
	return newline
	
class RosaBinFile:
	def __init__(self):
		self.code = []
		self._asm_stripped = [] #Only used when assembling
		self.bin_raw_content = b""
		
	def lex_from_asm_text(self, txt):
		non_stripped_lines = txt.split(";")
		for x in non_stripped_lines:
			if not x.startswith("//"):
				x = tokenize_asm_line(x)
				self._asm_stripped.append(x)
			
	def assemble_file(self, fs):
		"must call lex_from_asm_text before assembling"
		self.bin_raw_content += b"ROSAPYVM\x81"
		for x in self._asm_stripped:
			try:
				bcode = bytes([ops.__dict__[x[0]]])
				self.bin_raw_content += b"\x00"
				self.bin_raw_content += bcode
				for i in x[1:]:
					self.bin_raw_content += b"\x80"
					self.bin_raw_content += i.encode("latin-1")
			except IndexError:
				pass
				
			fs.write(self.bin_raw_content)
			
		def read_from_bin_file(self, filename):
			with open(filename, "rb") as f:
				cont = f.read()
				
			cont = cont.split(b"\x00")[1:]
		
def assemble_file_by_name(fname):
	with open(fname, "r") as fr:
		rbf = RosaBinFile()
		rbf.lex_from_asm_text(fr.read())
		with open("out.bin", "wb") as fw:
			rbf.assemble_file(fw)
