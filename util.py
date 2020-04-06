
def execfile(file_name):
     # Probably done in the function scope and therefore doesn't work for libraries
     exec(open(file_name).read())

