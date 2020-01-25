import PyPDF2
import re, sys

# Input through Command line arguments
if len(sys.argv)<2:
    print('Also give a PDF filepath on which script will work')
    exit(1)
else:
    in_fpath= int(sys.argv[1])

if len(sys.argv)==3: # To give output file path
	out_fpath = int(sys.argv[2])
else:   # Replace the same file
	out_fpath = in_fpath


# Initialize PDF reader & writer objects
infile = PyPDF2.PdfFileReader(in_fpath, 'rb') 
out_file = PyPDF2.PdfFileWriter()

# To extract text from a PDF page
def extract_text(pageObj):
    # Works fine for PDFs I tested with, yet it may fail for others
    # See: https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
    text = pageObj.extractText()
    return re.sub('[\n\r\s]+', '', text)


prev_pg_text = extract_text(infile.getPage(0))
del_pages = []

for pgNo in range(1, infile.numPages):
    pg_text = extract_text(infile.getPage(pgNo))
    # If current page contains all text of previous page
    if pg_text.startswith(prev_pg_text):
        del_pages.append(pgNo-1) # Delete previous page
    prev_pg_text = pg_text

# To delete pages, have to write a new PDF excluding those
for pgNo in range(infile.numPages):
    if pgNo not in del_pages:
        pg = infile.getPage(pgNo)
        out_file.addPage(pg)
  
with open('newfile.pdf', 'wb') as f:
    out_file.write(f)