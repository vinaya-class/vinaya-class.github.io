#!/bin/bash

MASTER_DIR="../vinaya-class-master"

if [ ! -d "$MASTER_DIR" ]; then
    echo "Clone the master branch to $MASTER_DIR"
    exit 2
fi

if [ -d book ]; then
    mdbook clean
fi

mdbook build

cd book
ln -s ../../vinaya-class-master .git

