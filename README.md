# Parsing google image

This script is use to parse google image with selenium. It can be launched using command lines and allow you to directly download all the images that you want in one query.


## Setup

To setup the environment, simply run **pip install** -r **requirements**.**txt** inside the project directory.

## Using command line

To launch the script, use the following command : **python parse_google_image.py [query] [nb_of_images]**
For example : 

**python parse_google_image.py "damaged apple fruit" 4** 

will give me the first 4 images that we can obtains typing damaged apple fruit in google image.

## Choose your directory

By default, the script will download your images in a folder that has the same name as your query inside a dataset directory. To continue with the precedent example, we will have this organisation :
```
.
+-- dataset
|   +-- damaged_apple_fruit
|   |	+-- damaged_apple_fruit(1).jpg
|   |	+-- damaged_apple_fruit(2).jpg
|   |	+-- damaged_apple_fruit(3).jpg
|   |	+-- damaged_apple_fruit(4).jpg
```
You can use any folder as you want to replace the **dataset** using the option --directory or -d in the command. For example, if I want to store my data inside a **damaged** folder, I can use the command  : 

**python parse_google_image.py "damaged apple fruit" 4 --directory damaged**

## Verbosity

You can put the verbose option to 0, 1 or 2 depending on the output that you want. 0 will hide all the output of the script, 1 will only show how many images you have downloaded, and 2 will show the whole output of the script. This option is added to the command with **--verbose** or with **-v**.
Example : 
```
E:\parse-google-image>python parse_google_image.py "damaged apple fruit" 4 --directory damaged --verbose 2
Search : damaged apple fruit ; number : 4 ; scrolls : 1
damaged/damaged_apple_fruit/damaged_apple_fruit(0).jpg downloaded !
damaged/damaged_apple_fruit/damaged_apple_fruit(1).jpg downloaded !
damaged/damaged_apple_fruit/damaged_apple_fruit(2).jpg downloaded !
damaged/damaged_apple_fruit/damaged_apple_fruit(3).jpg downloaded !
```
## Ways of improvements

For now, the scrolling is overkill and want to load all the images possible without clicking on "show more results" but we can try to scroll the least possible.
Not all the images are downloaded : the urls are handle without problem but some format may cause issues. For example, the **data:image/jpeg;base64** is handled but some other formats are not. The application will probably crash if your query gives absolutely no result.
