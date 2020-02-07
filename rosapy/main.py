# -*- coding: latin-1 -*-

import parse, vm
parse.assemble_file_by_name("src/bios.rasm")

main_vm = vm.Machine()
main_vm.normal_boot()
