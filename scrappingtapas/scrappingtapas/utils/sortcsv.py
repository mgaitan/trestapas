import csv
import sys
import operator

if __name__ == '__main__':
    writenames = ['url_articulo', 'antetitulo', 'fecha', 'texto', 'autor',
            'bajada', 'titulo', 'url_imagen', 'orden']

    inputpath = sys.argv[1]
    infile = open(inputpath)
    outfile = open(inputpath + '.sorted', 'w')

    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    # don't forget to open both files in binary mode (2.x)
    # or with `newline=''` (3.x)

    readnames = reader.next()
    name2index = dict((name, index) for index, name in enumerate(readnames))
    writeindices = [name2index[name] for name in writenames]
    reorderfunc = operator.itemgetter(*writeindices)
    writer.writerow(writenames)
    for row in reader:
        writer.writerow(reorderfunc(row))

    outfile.close()
