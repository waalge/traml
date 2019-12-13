This is a quick demo of a reformatted project structure. 
This is only a suggestion. 

## Directories 

Following the common convention: 

* A directory for the code, sharing name with project. 
* A directory for examples.
* A directory for tests (it might be a bit premature for the appearance of this just yet). 
* A directory for docs (again, early days, but bare this in mind. See [sphinx](http://www.sphinx-doc.org/en/master/)). 

See [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) for ideas.

I also put a directory ``data`` for the data.  

## Gitignore, data and secrets

Use a ``.gitignore`` to exclude large data files/ large amounts of data and secret API keys.

Git handles and tracks code well but handles data badly. 
Data for ML projects is important, and should be kept linked to the code repo, but not committed to it.
There are different ways to keep project data linked to the code repo. 
E.g: 

* [git-lfs](https://git-lfs.github.com/)
* [dvc](https://dvc.org/)

To instruct git not to follow any data files, I added ``data/`` to the ``.gitignore``. 

((I use [pre-commit](https://pre-commit.com/) to make sure not big files stray into my repos. 
I recommend looking at this at some point))

In general, people who give you API keys ask you to keep them secret. 
Git is instructed to ignore the file in which the API keys are stored.
I added ``*secrets*`` to the ``.gitignore``. 
Thus any file containing the word 'secrets' will be ignored by git, and not made public. 

I made another file called ``my_sea_crates.yaml`` demo-ing the format. 

