These scripts were written for pythong 2.7.11 and were tested in a windows x64 environment.

Useage:
    python main.py

By default, the script will not try to access google trends, but rather rely on locally stored data
This can be changed by editing the main.py file, line 92 and 94, where the second paramenter should
be set to True.

Requirements:
    pytrends
    numpy
    matplotlib
    sklearn
        and any dependencies these packages may have
        
Folder Structure:
    descriptions/
        HPV/
            ssi_dk.txt  - description from ssi.dk on the HPV vaccine
            sundhed_dk.txt - description from sundhed.dk on the HPV vaccine
        PVC/
            as with HPV
    vactionations/
        HPV-[1-3].json
        PVC-[1-3].json
    trends/ - location for the google trends csv files
        HPV/
        PVC/
    stopwords.txt - the stopwords
    main.py       - main file
    regular.py    - script for editing csv files
    tokenizer.py  - script for handling descriptions and stopwords
changing the order of files or folders may render scripts unuseable.