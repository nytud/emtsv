# Installation instructions

## Remarks on installing external packages on Ubuntu 18.04

- HFST: `apt-get install hfst`
- Hunspell: `apt-get install libhunspell-dev hunspell-hu`
- OpenJDK 8 JDK (we are transitioning to OpenJDK 11): `apt-get install openjdk-8-jdk`
- `git-lfs`: __[Requires root]__ Can be installed by running the [installation script](https://packagecloud.io/github/git-lfs/install)
    - __[Without root]__ If you download the [`git-lfs` binary](https://github.com/git-lfs/git-lfs/releases) for your operating system and put it in the `PATH` (eg. in `~/bin` and add `PATH="$HOME/bin:$PATH"` into `.bashrc`)
    - __[Without `git-lfs`]__ You can choose to omit installing `git-lfs` if you use `emtsv.download()` or `download_models.py` to download large files directly
- UTF-8 locale is set by default. Can be checked by typing `locale` . Lines should end with '.UTF-8'.

## Clone the repository

Clone together with submodules (it takes about 3 minutes):

`git lfs clone --recurse-submodules https://github.com/dlt-rilmta/emtsv`

- _Note:_ please ignore the deprecation warning. (This command checks and ensures that `git-lfs` is installed and working.)
- _Note2:_ If you are sure that `git-lfs` is installed, you can use `git clone` to avoid the warning. (This command also works without `git-lfs` installed, but `emtsv` might not work as the model files will not be downloaded. See [Troubleshooting](troubleshooting.md) section for details.)
- _Note3:_ Just use `git clone` if you intend to install large files with `emtsv.download()` or `download_models.py` to download large files directly

## Install Python dependencies

__Note__: You don't have to install all modules, only the ones you intend to use in `emtsv`

- `pip3 install Cython`
    - Required for `PyJNIus` (`PurePOS`, `emDep`, `emCons`) and it must be installed in a separate step
- `pip3 install -r requirements.txt`  # Only for using the model downloader!
- `pip3 install -r xtsv/requirements.txt`
- `pip3 install -r emmorphpy/requirements.txt`
- `pip3 install -r hunspellpy/requirements.txt`
- `pip3 install -r purepospy/requirements.txt`
- `pip3 install -r emdeppy/requirements.txt`
- `pip3 install -r HunTag3/requirements.txt`
- `pip3 install -r emudpipe/requirements.txt`
- Download `emToken` binary: `make -C emtokenpy/ all`

## Building Docker image

With the provided `Dockerfile` (see `docker` folder for other files used in the docker image):

```bash
docker build -t emtsv:stable .
```
