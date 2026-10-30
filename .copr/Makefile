# Called by COPR ("Build SRPM with: make srpm") as:
#   make -f .copr/Makefile srpm outdir=<dir> spec=<path to spec>
.PHONY: srpm
srpm:
	dnf -y install rpm-build /usr/bin/spectool
	spectool -g -C $(abspath $(dir $(spec))) $(spec)
	rpmbuild -bs \
	  --define "_sourcedir $(abspath $(dir $(spec)))" \
	  --define "_srcrpmdir $(outdir)" \
	  $(spec)
