# -*- coding: utf-8 -*-
__author__ = 'peter'

from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse
import itertools
import re

parser = argparse.ArgumentParser(description='Rearrange pdf pages to print and save some trees.')
parser.add_argument('pdf', type=str, help='pdf file to rearrange')
parser.add_argument('pps', type=int, help='number of pages per side')

args = parser.parse_args()

output1 = PdfFileWriter()
output2 = PdfFileWriter()
input = PdfFileReader(open(args.pdf, "rb"))
pages=input.getNumPages()
slice ={2:[lambda x: x,
         lambda x: x+1,
         lambda x: x+1,
         lambda x: x-2],
        4:[lambda x: x,
         lambda x: x+1,
         lambda x: x+2,
         lambda x: x+3,
         lambda x: x-1,
         lambda x: x-4,
         lambda x: x+1,
         lambda x: x-2]}

rearranged=[]

def chunks(list, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(list), n):
        yield list[i:i+n]

for c in chunks(range(0,pages), args.pps*2):
    rearranged.append([x(y) for x, y in zip(slice[args.pps], c) if x(y)<pages-1])

rearranged.append([pages-1])

for pages in rearranged:
    for page in pages[:args.pps]:
        output1.addPage(input.getPage(page))
    for page in pages[args.pps:]:
        output2.addPage(input.getPage(page))

outputStream = file(re.sub(r'(.*)\.pdf', r'\1X1.pdf', args.pdf), "wb")
output1.write(outputStream)

outputStream = file(re.sub(r'(.*)\.pdf', r'\1X2.pdf', args.pdf), "wb")
output2.write(outputStream)