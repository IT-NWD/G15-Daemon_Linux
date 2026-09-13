LLIBDIR=@LIBDIR@

ACLOCAL_AMFLAGS = -I m4

SUBDIRS =  libg15daemon_client g15daemon plugins
AM_CFLAGS =  -I$(top_srcdir)/libg15daemon_client -I$(top_srcdir)/g15daemon

EXTRA_DIST = contrib Documentation gui/g15-profile-editor.in \
	tests/test-configs.sh tests/test-profile-model.py tests/test-install-helper.py \
	README.usage FAQ LICENSE images README.Linux README.FreeBSD README.Solaris

check_PROGRAMS = tests/test-settings
tests_test_settings_SOURCES = tests/test-settings.c g15daemon/settings.c
tests_test_settings_CPPFLAGS = -I$(top_srcdir)/g15daemon

TESTS = tests/test-settings tests/test-configs.sh tests/test-profile-model.py tests/test-install-helper.py

nodist_bin_SCRIPTS = gui/g15-profile-editor
dist_libexec_SCRIPTS = gui/g15-profile-install
g15guidir = $(datadir)/g15daemon/gui
dist_g15gui_DATA = gui/g15_profile.py gui/g15_keyd.py gui/g15_platform.py
desktopdir = $(datadir)/applications
dist_desktop_DATA = gui/io.github.it_nwd.G15ProfileEditor.desktop

CLEANFILES = gui/g15-profile-editor

docdir = @docdir@
doc_DATA = FAQ README.usage README ChangeLog TODO AUTHORS NEWS LICENSE README.Linux README.FreeBSD README.Solaris \
	Documentation/G15-PROFILES.md Documentation/DEVELOPMENT.md

examplesdir = $(docdir)/examples
examples_DATA = contrib/keyd/g15.conf contrib/init/g15daemon.conf

man1_MANS = $(top_srcdir)/Documentation/g15daemon.1
man3_MANS = $(top_srcdir)/Documentation/g15daemon_client_devel.3

imagedir = $(prefix)/share/g15daemon/splash
image_DATA = images/g15logo3.wbmp

install-data-hook:
if KEXT_INSTALL
	cp -Rf $(top_srcdir)/contrib/libusbshield.kext @KEXT_LOCATION@
	chown -R root:wheel @KEXT_LOCATION@/libusbshield.kext
endif

#dist-hook:
#	rm -rf `find $(distdir)/debian -name .svn`
#	rm -rf `find $(distdir)/contrib -name .svn`
#	rm -rf `find $(distdir)/Documentation -name .svn`
#	rm -rf `find $(distdir)/lang-bindings -name .svn`
#	rm -rf `find $(distdir)/patches -name .svn`
#	rm -rf `find $(distdir)/rpm -name .svn`
#	rm -rf `find $(distdir)/plugins -name .svn`
#	rm -rf `find $(distdir)/images -name .svn`

#dist-rpm: dist-bzip2
#	rpmbuild -ts $(distdir).tar.bz2

#dist-archives:
#	$(MAKE) dist-bzip2
#	$(MAKE) dist-rpm                
