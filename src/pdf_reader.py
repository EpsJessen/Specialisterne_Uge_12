import pymupdf
import pymupdf4llm
from os.path import join
import re
import progressbar
import time
import pathlib

pdf_path = join("data", "fistful_flowers.pdf")
pdf_offset = 2
doc = pymupdf.open(filename=pdf_path, filetype="pdf")
#print(doc[9].get_text())
#print(doc[10].get_text())
keywords = ['HAZARD', '**CREATURE']

def get_text(page_start, page_end):
    output = []
    for i, page in enumerate(doc[page_start+pdf_offset:page_end+pdf_offset+1]):
        text = page.get_text("blocks")
        for j, par in enumerate(text):
            paragraph: str = par[4]
            if re.match("paizo", paragraph) or re.match("([0-9]|[\s])*$", paragraph):
                continue
            output.append(paragraph)
    return output

def concat_md_text(md_list, text_list):
    collected = []
    start_sentence = md_list[2]
    end_sentence = md_list[4]
    print(start_sentence)
    info = False
    for line in text_list:
        line_prime = ' '.join(line.split())
        if not info:
            if start_sentence in line_prime:
                info = True
        if info:
            collected.append(line)
            if end_sentence.strip().strip('-').strip() in line_prime:
                break
    return collected

def extract_info(page_start, page_end):
    descriptions = []
    description_index = -1
    writing = 0
    for i, page in enumerate(doc[page_start-1:page_end]):
        text = page.get_text("blocks")
        for j, par in enumerate(text):
            paragraph: str = par[4]
            if re.match("paizo", paragraph) or re.match("([0-9]|[\s])*$", paragraph):
                continue
            print(paragraph.strip().strip('•').strip())
        #    
        #    found = False
        #    for keyword in keywords:
        #        if keyword in paragraph:
        #            found = keyword
        #    #        print(f"The following keyword was found: {found} in paragraph: {paragraph}")
        #
        #    if (not found) and (writing != 2) and ((len(paragraph) == 1) or (re.match("([A-Z]|[0-9]|[.]|[\s]|’)+\n", paragraph))):
        #        writing = 0
        #        continue
        #    
        #    if found:
        #        descriptions.append([found, i+1])
        #        description_index += 1
        #        writing = 1
        #    if writing != 0:
        #        descriptions[description_index][0] += " " + paragraph
        #        writing += 1
    #print(descriptions)

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

def get_info_md():
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
        prev_page = 0
        prev_line = ''
        for line in text_proper:

            if re.match("[#]+ [*]+[0-9]+[*]+$", line):
                page: str = line.split(' ')[-1]
                page = page.replace('*', '')
                continue

            found = False
            for keyword in keywords:
                if keyword in line:
                    found = keyword.replace('*', '')
                    if writing:
                        description_points[description_index].append(prev_page)
                        description_points[description_index].append(prev_line.replace('*', '').replace('#', ''))
            
            if (not found) and (writing not in [2, 3]) and ((len(line) == 1) or (re.match("([#]+ [*]*[A-Z]([A-Z]|[0-9])*)|(([*]+[A-Z]([A-Z]|[0-9]|’| |[.])*[*]+[ ]*)+$)|([*]+Treasure:[*]+)|([*]+Reward:[*]+)", line))):
                                                            # or re.match("([*]+[A-Z]([A-Z]|[0-9]|’| |[.])*[*]+[ ]*)+$", line) or re.match('[*]+Treasure:[*]+', line) or re.match('[*]+Reward:[*]+', line)):
                if writing:
                    description_points[description_index].append(prev_page)
                    description_points[description_index].append(prev_line.replace('*', '').replace('#', ''))
                writing = 0
                continue

            

            if found:
                description_points.append([found, page])
                description_index += 1
                writing = 1
                description_points[description_index].append(line.replace('*', '').replace('#', ''))
                writing += 1

            elif writing != 0:
                #description_points[description_index][0] += " " + line
                writing += 1
            
            prev_line = line
            prev_page = page
        #print(description_points)
        description = []
        for info in description_points:
            text = get_text(int(info[1]), int(info[3]))
            description.append([info[0], ' '.join(concat_md_text(info, text))])
        return description



            
        #pathlib.Path("data/test.md").write_text(text)
        #with open("data/test.md", "r") as md:
        #    md_content = md.read()
        #    md_content = md_content
        #    for line in md_content:
        #        print(line)
        #print(text_proper)

#print_page_md()
descriptions = get_info_md()
for description in descriptions:
    print("type: " + description[0])
    #print(description[1])
#extract_info(3,3)