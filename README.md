# CD Booklet Processing

## Description

This contains python scripts for processing scans of CD Booklets. These scripts assist in creating the bash commands for splitting images using ImageMagick.

## Typical workflow

1. Scan files
2. Use an application like pdfimages to convert pdf files to PNG images.
3. Run `identify` on each image file and redirect the results to a file. (For example, `image_info.txt` contains the results of an application of this command on a set of images.)
4. Transform the file output in the previous step into a csv file containing only file names and their dimensions.
5. The file `parse_image_info.py` contains the results of a `*bpython*` session that transforms a csv file as produced in the previous step into a json file containing file names, dimensions, and a map of original file names to left and right page numbers.
6. Use crop_command_maker.py to create a script that uses the json file produced in the prececeding set to derive the crop commands.
7. The result file (`crop_commands.sh`) can be used to create a set of individual pages from the CD booklet.
