# Annotation Instructions

## Overview

Annotations are tedious and time consuming but vital to ensure quality data when used in NLP tasks.
Vukuzenzele is a rich resource featuring articles in low resource South African languages, to utilise this resoure the PDF articles need to be:
- Extracted
- Annotated

## Extraction

Refer to the [readme](../src/data/ReadME.md) in the src/data folder.

1. Identify the date and edition of the paper you would like to extract in vukuzenzele-nlp/data/raw.  
For an example we will use **2019-12-ed1**. It can found [here](../data/raw/2019-12-ed1/).

2. Identify which page the article is on in the eng.pdf and the others.pdf.  
Following on from **2019-12-ed1**, we can see that the story ***Preventing HIV with PrEP*** is the only one translated to the other languages. In the english version of the pdf, this story is on **page 5**, in the translated versions, it is on **page 2**.

3. Once the above has been identified, we can execute the extraction script 
    - Navigate to src/data folder and run the following:  
    <font size=2>`python vukuzenzele-extract.py -f {edition} --eng {page_from}-{page_to} --rest {page_from}-{page_to} --sn {story_number}` </font>
    - For our example: 
    <font size=2>`python vukuzenzele-extract.py -f 2019-12-ed1 --eng 5-5 --rest 2-2 --sn 2` </font>  
    </br>
4. After the script has completed execution, there should be 11 extracted textfiles in a folder named after the edition, i.e. 2019-12-ed1. 
    - These files need to be ***annotated***.

## Annotation

The annotation invovles comparing the extracted text to the original pdf.   
The execution script author stated issues discovered during the extraction process are, 
- There is no definitive way to separate unnecessary information on pdf pages.
- Human intervention would be needed to look for the title, story and author.
- Often times the **title is in the first or the last sentence** of the story.
- The **author** is often also in **the first sentence** of the story.
- Bold subheadings need to be put on their own lines as they combine with proceeding paragraph.

</br>

The desired format for the annotations is the following:
- Article title
- blank line
- Author name OR "Vukuzenzele unnamed" 
- blank line
- Article contents 

An example of an annotated text can be found [here](../data/processed/2020-01-ed1/2020-01-ed1-vukuzenzele-eng-01.txt)

If you have annotated and feel like these instructions can be expanded upon, please do create a github issue detailing the change, it would be most appreciated!

