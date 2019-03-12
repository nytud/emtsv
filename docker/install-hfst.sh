set -ex
git clone https://github.com/hfst/hfst.git
cd hfst
git checkout 683a5f4e8d457bfa5d25014b7a4346d77427ee20
./autogen.sh
./configure --enable-all-tools --with-unicode-handler=glib
make
make install
if [ "$1" ]; then
    cd python
    python3 setup.py install
    python3 setup.py install
fi


