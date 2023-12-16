import tempfile
import os
import platform

def remove_empty_lines_at_ends(text):
    lines = text.splitlines()
    
    # Remove empty lines from the beginning
    while lines and not lines[0].strip():
        lines.pop(0)
    
    # Remove empty lines from the end
    while lines and not lines[-1].strip():
        lines.pop()

    # Re-join the lines
    return '\n'.join(lines)

# @register_cell_magic
def dockerexec(args, cell):
#    cell = cell.split('\n',1)[1]
    cell = remove_empty_lines_at_ends(cell)
    tmpf, filename = tempfile.mkstemp(dir='.')
    os.write(tmpf, bytes(cell, "utf8"))
    if platform.system() == "Windows" :
        get_ipython().run_cell_magic("bash","","docker exec -i {0} bash < {1}".format(args, os.path.basename(filename)))
    else :
        get_ipython().system("docker exec -i {0} bash < {1}".format(args, filename))
    os.close(tmpf)
    os.remove(os.path.basename(filename))
    
# @register_cell_magic
def dockerwrite(args, cell):
#    cell = cell.split('\n',1)[1]
    cell = remove_empty_lines_at_ends(cell)
    tmpf, filename = tempfile.mkstemp(dir='.')
    os.write(tmpf, bytes(cell, "utf8"))
    writefile = ":".join(args.split())
    if platform.system() == "Windows" :
        get_ipython().run_cell_magic("bash","","docker cp {0} {1}".format(os.path.basename(filename),writefile))
    else :
        get_ipython().system("docker cp {0} {1}".format(filename,writefile))
    os.close(tmpf)
    os.remove(os.path.basename(filename))

# @register_cell_magic
def dockerecho(args, cell):
    cell = remove_empty_lines_at_ends(cell)
    print(cell)

def load_ipython_extension(ipython):
    """This function is called when the extension is
    loaded. It accepts an IPython InteractiveShell
    instance. We can register the magic with the
    `register_magic_function` method of the shell
    instance."""
    os.environ["PATH"] = "/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin"
    ipython.register_magic_function(dockerexec, 'cell')
    ipython.register_magic_function(dockerwrite, 'cell')
    ipython.register_magic_function(dockerecho, 'cell')

