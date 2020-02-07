from bytecode import Opcodes as ops
import codecs

NUM_CHARS = ".0123456789"
	
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
	print("debugL2 " + str(line))
	oline = line
	line = line.split(" ")
	try:
		if not ("," in oline):
			newline = (line[0], " ".join(line[1:]))
			print("debugL3 " + str(newline))
			return newline 
	except IndexError:
		pass
	if line[1].endswith(","):
		line[1] = list(line[1])
		line[1].pop()
		line[1] = "".join(line[1])
	newline.append(line[0])
	newline.append(line[1])
	line = oline.split(",")
	try:
		for x in line[1:]:
			tmpstr = remove_starting_whitespace(x)
			newline.append(tmpstr)
	except IndexError:
		pass
	print("debugN " + str(newline))
	return newline
	
def r_eval(expr, vm):
	expr = remove_starting_whitespace(expr)
	if expr.startswith("'") or expr.startswith("\""):
		#awful
		return "".join(list(expr)[1:len(list(expr)) - 1])
	else:
		for x in list(NUM_CHARS):
			if expr.startswith(x):
				return int(expr)
		return vm.stack.get(vm.var_address_table[expr])
		
def eval_loop(exprs, vm):
	arr = []
	for x in exprs:
		arr.append(r_eval(x, vm))
	return arr
	
class RosaBinFile:
	def __init__(self):
		self.code = []
		self._asm_stripped = [] #Only used when assembling
		self.bin_raw_content = b""
		
	def lex_from_asm_text(self, txt):
		non_stripped_lines = txt.split(";")
		for x in non_stripped_lines:
			x = remove_starting_whitespace(x)
			if not x.startswith("//") and not x == "":
				x = tokenize_asm_line(x)
				print("debugL " + str(x))
				self._asm_stripped.append(x)
			
	def assemble_file(self, fs):
		"must call lex_from_asm_text before assembling"
		self.bin_raw_content += b"\x8FROSAPYVM\x02"
		for x in self._asm_stripped:
			try:
				bcode = bytes([ops.__dict__[x[0]]])
				print("debugB " + str(bcode))
				print("debugX " + str([x[1:]]))
				self.bin_raw_content += b"\x00"
				self.bin_raw_content += bcode
				for i in x[1:]:
					self.bin_raw_content += b"\x01"
					print("debugARG " + str(i.encode("latin-1")))
					self.bin_raw_content += i.encode("latin-1")
			except IndexError:
				pass
			print("debugRAW" + str(self.bin_raw_content.decode("latin-1")))
				
			fs.write(self.bin_raw_content.decode("latin-1"))
			
	def read_from_bin_file(self, filename):
		with open(filename, "rb", encoding="latin-1") as f:
			cont = f.read().decode("latin-1")
			print("debugRRAW " + str(cont.encode("latin-1")))
			if not cont.startswith("\x8FROSAPYVM\x02"):
				raise ValueError("Cannot execute file: incorrect file format")
			else:
				cont = cont.split("\x00")[1:]
				for x in cont:
					instruct = x.split("\x01")
					instruct[0] = int.from_bytes(instruct[0].encode("latin-1"), byteorder="little")
					self.code.append(instruct)
		
def assemble_file_by_name(fname):
	with open(fname, "r") as fr:
		rbf = RosaBinFile()
		rbf.lex_from_asm_text(fr.read())
		with codecs.open("out.bin", "wb", encoding="latin-1") as fw:
			rbf.assemble_file(fw)
