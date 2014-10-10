README.TXT
circa August 2013

This folder contains the files needed to create your report using the ACM conference style.

You will need to edit the file, report.tex, and the file, report.bib. The first file contains the text of your paper, and the second file contains the bibliography of cited papers in BiBTeX style. Once both files are edited to your satisfaction, you will need to compile them using LaTeX and BibTeX to generate the required PDF file needed for submission.
	latex report
	bibtex report
	latex report
	latex report

To generate PDF, you may use a dvi2pdf program or replace the above sequence by the following:
	pdflatex report
	bibtex report
	pdflatex report
	pdflatex report

The sequences shown above are critical to generating the correct paper with appropriate citations and cross-references.

Submit the generated report.pdf to the dropbox.

Notes: 
   1. For your convenience, the initial generated pdf has been copied to a separate file REPORT_INITIAL.PDF so that you can refer to it for formatting help and suggestions. Don't submit this file by mistake. 
   2. The file GUIDE.PDF provides more help with the ACM conference style.