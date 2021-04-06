# DOI-finder
This script allows to collect DOI numbers form a set of titles of research articles contained in a single Ms Excel (.xlsx) datasheet. Outputs are the DOI number, URL and title found by the first result of a search in the crossreff.org browser.

How to use:

1. Prepare you input data set. This must be an .xlsx datasheet with only one column containing all articles title listed one below other.
2. On a windows console (cmd) find the DOIFinder path and give as a argument the input datasheet path.
3. That's all, a progress bar should appear in order to let you know how much it rest to finish.
4. A new file will be created on the same script folder which will contains a 4 columns: the original article title searched, the found DOI number, the found URL for the article, the found article name and a measure of the similarity between both article title strings, the original one and the one found by the API. This similarity measure goes from 0 (an complete different string) to 1 (the exact same string).
