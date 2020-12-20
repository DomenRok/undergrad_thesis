""" Main interpter file """

from settings import BASE_DIR, EXAMPLE_PYTHON_FILE

import types
import typing as t
import dis
import py_compile
import sys
import struct
import marshal
import logging
import dis, marshal, struct, sys, time, types

logger = logging.getLogger(__name__)


def compile_file(src_file):
    compiled_pyc_file = py_compile.compile(src_file)
    return compiled_pyc_file


def eval_bytecode(pyc_path):
    """Compiles pyc_path and returns a code object.

    Gory details in import.c
    more info: https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html

    Args:
        pyc_path ([path]): [path of the compiled bytecode in .pyc format ]

    Returns:
        [code_object]
    """

    header_sizes = [
        # (size, first version this applies to)
        # pyc files were introduced in 0.9.2 way, way back in June 1991.
        (8, (0, 9, 2)),  # 2 bytes magic number, \r\n, 4 bytes UNIX timestamp
        (12, (3, 6)),  # added 4 bytes file size
        # bytes 4-8 are flags, meaning of 9-16 depends on what flags are set
        # bit 0 not set: 9-12 timestamp, 13-16 file size
        # bit 0 set: 9-16 file hash (SipHash-2-4, k0 = 4 bytes of the file, k1 = 0)
        (16, (3, 7)),  # inserted 4 bytes bit flag field at 4-8
        # future version may add more bytes still, at which point we can extend
        # this table. It is correct for Python versions up to 3.9
    ]

    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    with open(pyc_path, "rb") as f:
        metadata = f.read(header_size)  # first header_size bytes are metadata
        code = marshal.load(f)  # rest is a marshalled code object
        return code


def display_code_obj_metadata(code_object):
    a = code_object
    print(f"{a.co_argcount} {a.co_cellvars}")

    print(f"argcount  {code_object.co_argcount} ")
    print(f"nlocals   {code_object.co_nlocals}  ")
    print(f"stacksize {code_object.co_stacksize}")
    print(f"flags        {code_object.co_flags} ")
    dis.disassemble(code_object)
    for const in code_object.co_consts:
        if type(const) == types.CodeType:
            display_code_obj_metadata(const)
        else:
            print(f"{const}")
    print(f" names {code_object.co_names}")
    print(f" varnames {code_object.co_varnames}")
    print(f" freevars {code_object.co_freevars}")
    print(f" cellvars {code_object.co_cellvars}")
    print(f" filename {code_object.co_filename}")
    print(f" name {code_object.co_name}")
    print(f" firstlineno {code_object.co_firstlineno}")


pyc_path = compile_file(EXAMPLE_PYTHON_FILE)
code_object = eval_bytecode(pyc_path)

display_code_obj_metadata(code_object)
