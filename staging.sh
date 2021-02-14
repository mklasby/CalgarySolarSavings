#!/bin/bash
cp -r mbr-export/* static
cd static
grep -RiIl 'href="assets' | xargs sed -i 's/href="assets/href="static\/assets/g'
grep -RiIl 'src="assets' | xargs sed -i 's/src="assets/src="static\/assets/g'

# https://www.internalpointers.com/post/linux-find-and-replace-text-multiple-files bash magic