#
# TODO:
#	- package and R: Csdp (https://projects.coin-or.org/Csdp)
#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)
%bcond_with	tests		# run testsuite (csdp dependant micromega tests fail badly on x86_64)
#
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	The Coq Proof Assistant
Summary(pl.UTF-8):	Coq - narzędzie pomagające w udowadnianiu
Name:		coq
Version:	8.6
Release:	1
License:	LGPL v2.1
Group:		Applications/Math
Source0:	http://coq.inria.fr/distrib/V%{version}/files/%{name}-%{version}.tar.gz
# Source0-md5:	e7f1704b85d648468160abe03338f1bd
Source1:	coqide.desktop
Source2:	coqide.xpm
Patch0:		%{name}-lablgtk2.patch
URL:		http://coq.inria.fr/
BuildRequires:	bash
BuildRequires:	emacs
BuildRequires:	hevea
BuildRequires:	netpbm-progs
BuildRequires:	ocaml >= 3.09.0
BuildRequires:	camlp5 >= 5.01
BuildRequires:	ocaml-lablgtk2-devel >= 2.12.0
BuildRequires:	ocaml-lablgtk2-gtksourceview2-devel
BuildRequires:	sed >= 4.0
BuildRequires:	texlive-fonts-cmextra
BuildRequires:	texlive-fonts-cmsuper
BuildRequires:	texlive-fonts-other
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-latex-comment
BuildRequires:	texlive-latex-moreverb
BuildRequires:	texlive-latex-ucs
BuildRequires:	texlive-makeindex
BuildRequires:	texlive-psutils
# hyperref.sty (from latex) requires ifxexex.sty (from xetex)
BuildRequires:	texlive-xetex
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Coq is a proof assistant which:
 - allows to handle calculus assertions,
 - check mechanically proofs of these assertions,
 - helps to find formal proofs,
 - extracts a certified program from the constructive proof of its
   formal specification.

%description -l pl.UTF-8
Coq to narzędzie pomagające w udowadnianiu, które:
- pozwala uporać się z twierdzeniami dotyczącymi rachunku
  różniczkowego,
- mechanicznie sprawdzać dowody tych twierdzeń,
- pomagać w znalezieniu formalnych dowodów,
- wyciągać program o dowiedzionej poprawności z konstruktywnego
  dowodu jego formalnej specyfikacji.

%package emacs
Summary:	Emacs mode and syntax for Coq
Summary(pl.UTF-8):	Tryb i składnia Coq dla Emacsa
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description emacs
Emacs mode and suyntax files for Coq.

%description emacs -l pl.UTF-8
Pliki trybu i składni Coq dla Emacsa.

%package latex
Summary:	Coq documentation style for latex
Summary(pl.UTF-8):	Styl dokumentacji Coq dla latexa
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description latex
Coq documentation style for latex.

%description latex -l pl.UTF-8
Styl dokumentacji Coq dla latexa.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's|#!/bin/sh|#!/bin/bash|' test-suite/check
%{__sed} -i -e 's|\(MAKE_TSOPTS=.*\) -s \(.*\)|\1 \2|' Makefile.build

%build
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
	-docdir %{_docdir}/%{name}-%{version} \
	-configdir %{_sysconfdir}/%{name} \
	-datadir %{_datadir}/%{name} \
	-emacs emacs \
	-browser "xdg-open %s" \
	-emacslib %{_datadir}/emacs/site-lisp \
	%{?with_ocaml_opt:-opt} \
	-coqdocdir %{_datadir}/texmf/tex/latex/misc \
	-coqide %{?with_ocaml_opt:opt}%{!?with_ocaml_opt:byte}

%{__make} -j1 world VERBOSE=1 CAML_LD_LIBRARY_PATH=kernel/byterun
%{?with_tests:%{__make} -j1 check VERBOSE=1 CAML_LD_LIBRARY_PATH=kernel/byterun} # Use native coq to compile theories

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} -e install \
	COQINSTALLPREFIX=$RPM_BUILD_ROOT/
# To install only locally the binaries compiled with absolute paths

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

cp -p CHANGES COMPATIBILITY COPYRIGHT CREDITS README.md $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/coq_makefile
%attr(755,root,root) %{_bindir}/coq-tex
%attr(755,root,root) %{_bindir}/coqc
%attr(755,root,root) %{_bindir}/coqchk
%attr(755,root,root) %{_bindir}/coqdep
%attr(755,root,root) %{_bindir}/coqdoc
%attr(755,root,root) %{_bindir}/coqide*
%attr(755,root,root) %{_bindir}/coqmktop
%attr(755,root,root) %{_bindir}/coqtop
%attr(755,root,root) %{_bindir}/coqtop.byte
%attr(755,root,root) %{_bindir}/coqwc
%attr(755,root,root) %{_bindir}/coqworkmgr
%attr(755,root,root) %{_bindir}/gallina
%dir %{_libdir}/coq
%{_libdir}/coq/*
%{_mandir}/man1/coq_makefile.1*
%{_mandir}/man1/coq-tex.1*
%{_mandir}/man1/coqc.1*
%{_mandir}/man1/coqchk.1*
%{_mandir}/man1/coqdep.1*
%{_mandir}/man1/coqdoc.1*
%{_mandir}/man1/coqide.1*
%{_mandir}/man1/coqmktop.1*
%{_mandir}/man1/coqtop.1*
%{_mandir}/man1/coqtop.byte.1*
%{?with_ocaml_opt:%{_mandir}/man1/coqtop.opt.1*}
%{_mandir}/man1/coqwc.1*
%{_mandir}/man1/gallina.1*
%{_desktopdir}/coqide.desktop
%{_pixmapsdir}/coqide.xpm
%{_datadir}/%{name}

%files emacs
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/coq-font-lock.el
%{_datadir}/emacs/site-lisp/coq-inferior.el
%{_datadir}/emacs/site-lisp/gallina-db.el
%{_datadir}/emacs/site-lisp/gallina-syntax.el
%{_datadir}/emacs/site-lisp/gallina.el

%files latex
%defattr(644,root,root,755)
%{_datadir}/texmf/tex/latex/misc/coqdoc.sty
