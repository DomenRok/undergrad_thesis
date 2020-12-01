""" Main example file """

import typing as t
import dis
import py_compile
import platform
import sys
import marshal

EXAMPLE_PYTHON_FILE = "code_examples/basic.py"


def compile_file(src_file):
    compiled_pyc_file = py_compile.compile(src_file)
    return compiled_pyc_file


def eval_bytecode(pyc_path):
    """ Compiles pyc_path and returns a code object.

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

    header_size = next(s for s, v in reversed(header_sizes)
                       if sys.version_info >= v)

    with open(pyc_path, "rb") as f:
        metadata = f.read(header_size)  # first header_size bytes are metadata
        code = marshal.load(f)  # rest is a marshalled code object
        return code


pyc_path = compile_file(EXAMPLE_PYTHON_FILE)


def show_file(fname):
    f = open(fname, "rb")
    magic = f.read(4)
    moddate = f.read(4)
    modtime = time.asctime(time.localtime(struct.unpack('L', moddate)[0]))
    print "magic %s" % (magic.encode('hex'))
    print "moddate %s (%s)" % (moddate.encode('hex'), modtime)
    code = marshal.load(f)
    show_code(code)


def show_code(code, indent=''):
    print "%scode" % indent
    indent += '   '
    print "%sargcount %d" % (indent, code.co_argcount)
    print "%snlocals %d" % (indent, code.co_nlocals)
    print "%sstacksize %d" % (indent, code.co_stacksize)
    print "%sflags %04x" % (indent, code.co_flags)
    show_hex("code", code.co_code, indent=indent)
    dis.disassemble(code)
    print "%sconsts" % indent
    for const in code.co_consts:
        if type(const) == types.CodeType:
            show_code(const, indent + '   ')
        else:
            print "   %s%r" % (indent, const)
    print "%snames %r" % (indent, code.co_names)
    print "%svarnames %r" % (indent, code.co_varnames)
    print "%sfreevars %r" % (indent, code.co_freevars)
    print "%scellvars %r" % (indent, code.co_cellvars)
    print "%sfilename %r" % (indent, code.co_filename)
    print "%sname %r" % (indent, code.co_name)
    print "%sfirstlineno %d" % (indent, code.co_firstlineno)
    show_hex("lnotab", code.co_lnotab, indent=indent)


def show_hex(label, h, indent):
    h = h.encode('hex')
    if len(h) < 60:
        print "%s%s %s" % (indent, label, h)
    else:
        print "%s%s" % (indent, label)
        for i in range(0, len(h), 60):
            print "%s   %s" % (indent, h[i:i + 60])


show_file(pyc_path)