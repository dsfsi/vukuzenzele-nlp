How to Run the vukuzenzele-extract.py:

1. Identify the date and edition of the paper you would like to extract in vukuzenzele-nlp/data/raw.
2. Open the files and identify the page numbers of the English version and other translated languages.
3. Run the file from command line:
   - python vukuzenzele-extract.py -f "folder name" --eng "Pagefrom-PageTo" --rest "Pagefrom-PageTo" --sn "StoryNumber"
   -  "--eng" English version page numbers, "--rest" for the translated languages.
   - No quotation marks needed.

4. 11 .txt files to be refined are then available in the vukuzenzele-nlp/data/interim folder after running.
5. Save completed files to vukuzenzele-nlp/data/processed.

6. For assistance on the format type:
   - python vukuzenzele-extract.py -h

Issue that have arised with Automatic extraction:
- There is no definitive way to separate unnecessary information on pdf pages.
- Human intervention would be needed to look for the title, story and author.
- Often times the title is in the first or the last sentence of the story.
- The author is often also in the first sentence of the story.
- Bold subheadings need to be put on their own lines as they combine with proceeding paragraph.
- Other past papers that are not viable would need manual extraction from the vukuzenzele raw folder itself.


Automatic extraction:
- The script detects full stops that lead to a second section then marks the point.
- All the columns are then turned to rows.
- Pages are clearly separated and page numbers are provided in each of the 11 .txt files.
- Words that run on two lines are added back together.
- Encoding = utf-8
- The pdf article should be used hand-in-hand for verification purposes on where sections should be.
