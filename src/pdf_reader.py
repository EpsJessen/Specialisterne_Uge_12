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
keywords = ['HAZARD', '**CREATURE']



def extract_info(page_start, page_end):
    descriptions = []
    description_index = -1
    writing = 0
    for i, page in enumerate(doc[page_start-1:page_end]):
        text = page.get_text("blocks")
        for j, paragraph in enumerate(text):
            paragraph = paragraph[4]
            if re.match("paizo", paragraph) or re.match("([0-9]|[\s])*$", paragraph):
                continue
            
            found = False
            for keyword in keywords:
                if keyword in paragraph:
                    found = keyword
            #        print(f"The following keyword was found: {found} in paragraph: {paragraph}")

            if (not found) and (writing != 2) and ((len(paragraph) == 1) or (re.match("([A-Z]|[0-9]|[.]|[\s]|’)+\n", paragraph))):
                writing = 0
                continue
            
            if found:
                descriptions.append([found, i+1])
                description_index += 1
                writing = 1
            if writing != 0:
                descriptions[description_index][0] += " " + paragraph
                writing += 1
    print(descriptions)

def print_page(page):
    for j, paragraph in enumerate(doc[page].get_text("blocks")):
        paragraph = paragraph[4]
        if re.match("paizo", paragraph) or re.match("([0-9]+[\s]*)+$", paragraph):
            continue
        print(f"{j}:\n{paragraph}")

def print_page_html(start, end):
    with open("data/test.html", "w") as file:
        for i in range(start, end):
            page = doc[i-1].get_text("xhtml")
    
            file.write(page)

def print_page_json(start, end):
    with open("data/test.json", "w") as file:
        for i in range(start, end):
            page = doc[i-1].get_text("rawjson")
    
            file.write(page)

def print_page_md():
        text = pymupdf4llm.to_markdown(pdf_path)
        text = text.split('\n')
        #text = ["If the PCs defeat all of the enemy leshys...",
        #        "**MELIOSA’S LESHYS (4)** **CREATURE 2**",
        #        "**UNIQUE** **N** **SMALL** **LESHY** **PLANT**",
        #        "...",
        #        "##### **Concluding the Adventure**",
        #        "blah blah"
        #        ]
        text_proper = []
        for line in text:
            if line == '' or re.match("[*]*paizo", line) or re.match("([0-9]|[\s])*$", line):
                continue
            text_proper.append(line)
        #text_proper = '\n'.join(text_proper)
        description_points = []
        description_index = -1
        page = 0
        writing = 0
