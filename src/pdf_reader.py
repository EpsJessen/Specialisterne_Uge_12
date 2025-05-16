import pymupdf
import pymupdf4llm
from os.path import join
import re
import progressbar
import time
import pathlib

pdf_path = join("data", "fistful_flowers.pdf")
doc = pymupdf.open(filename=pdf_path, filetype="pdf")
#print(doc[9].get_text())
#print(doc[10].get_text())
