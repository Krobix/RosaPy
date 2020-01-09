from bytecode import Opcodes as ops
import parse

class Stack:
	def __init__(self):
		self.arr = []
		self._length = 0
		
	def push(self, val):
		val = list(str(val))
		for x in val:
			self.arr.append(x)
		self.arr.append("\E")
		self._length += 1
			
	def retrieve_index_start(self, index):
		ind_count = 0
		ind_true_count = 0
		for x in self.arr:
			if ind_count == index:
				return ind_true_count
			else:
				ind_true_count += 1
				if x == "\E":
					ind_count += 1
					
	def retrieve_index_start_and_end(self, index):
		start = self.retrieve_index_start(index)
		tmpnum = 0
		for x in self.arr[start:]:
			if x == "\E":
				end = tmpnum
				return (start, end)
			else:
				tmpnum += 1
		
	def get(self, index):
		start_end = self.retrieve_index_start_and_end(index)
		return "".join(self.arr[start_end[0]:start_end[1]])
		
	def top(self):
		return self.get(self.arr[len(self) - 1])
		
	def pop(self, num):
		s = self.retrieve_index_start_and_end(num)
		index = self.arr[s[0]:s[1]]
		for x in index:
			self.arr.pop(s[0] + index.index(x))
		
	def __len__(self):
		return self._length
		
class Machine:
	def __init__(self, file):
		self.instruction_ptr = 0
		self.stack = Stack()
		self.retval = ""
		self.func_stack = []
		self.var_address_table = {}
		self.file = file
		
	def exec_opcode(self, op, args):
		if op == ops.ADD:
			self.retval = (parse.r_eval(args[0]) + parse.r_eval(args[1]))
			
		elif op == ops.SUB:
			self.retval = (parse.r_eval(args[0], self) - parse.r_eval(args[1], self))
			
		elif op == ops.MUL:
			self.retval = (parse.r_eval(args[0], self) * parse.r_eval(args[1], self))
			
		elif op == ops.DIV:
			self.retval = (parse.r_eval(args[0], self) / parse.r_eval(args[1], self))
			
		elif op == ops.LESS:
			if parse.r_eval(args[0], self) < parse.r_eval(args[1], self):
				self.exec_opcode(ops.JMP, [args[2]])
				
		elif op == ops.EQUALS:
			if parse.r_eval(args[0], self) == parse.r_eval(args[1], self):
				self.exec_opcode(ops.JMP, [args[2]])
				
		elif op == ops.MORE:
			if parse.r_eval(args[0], self) > parse.r_eval(args[1], self):
				self.exec_opcode(ops.JMP, [args[2]])
				
		elif op == ops.STORE:
			self.stack.push(str(parse.r_eval(args[1], self)))
			self.var_address_table[args[0]] = len(self.stack) - 1
			
		elif op == ops.DEL:
			del_addr = self.var_address_table[args[0]]
			self.stack.pop(del_addr)
			
		elif op == ops.SYSWRITE:
			var = args[0]
			exec(self.stack.get(self.var_address_table["__sysout"]))
			
		elif op == ops.SYSREAD:
			var = args[0]
			exec(self.stack.get(self.var_address_table["__sysin"]))
			
		elif op == ops.WRITE:
			with open(parse.r_eval(args[0], self), "w") as f:
				f.write(parse.r_eval(args[1], self))
				
		elif op == ops.READ:
			with open(parse.r_eval(args[0], self), "r") as f:
				self.retval = f.read()
				
		elif op == ops.READRET:
			self.exec_opcode(ops.STORE, [args[0], self.retval]) 
			
		elif op == ops.JMP:
			self.instruction_ptr = parse.r_eval(args[0])
			
		elif op == ops.CALL:
			self.exec_opcode_by_location(parse.r_eval(args[0], self))
			
		elif op == ops.CALLPY:
			globals()[parse.r_eval(args[0])](*parse.eval_loop(args[1:]))
			
		elif op == ops.IMPORT:
			self.exec_file_by_name(parse.r_eval(args[0], self))
			
	def exec_opcode_by_location(self, location):
		code = self.file.code[location]
		self.exec_opcode(code[0], code[1:])
