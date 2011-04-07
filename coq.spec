Summary:	The Coq Proof Assistant
Summary(pl.UTF-8):	Coq - narzędzie pomagające w udowadnianiu
Name:		coq
Version:	8.3pl1
Release:	0.1
License:	GPL
Group:		Applications/Math
Vendor:		INRIA Rocquencourt
Source0:	http://coq.inria.fr/V%{version}/files/%{name}-%{version}.tar.gz
# Source0-md5:	1869d22b337f5da59ba3bbe1433f9a3b
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
BuildRequires:	sed >= 4.0
BuildRequires:	texlive-latex-comment
BuildRequires:	texlive-format-pdflatex
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

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's|#!/bin/sh|#!/bin/bash|' test-suite/check

%build
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
	-docdir %{_datadir}/coq/doc \
	-emacs emacs \
	-browser 'iceweasel -remote "OpenURL(%s,new-tab)" || iceweasel %s &' \
	-emacslib %{_datadir}/emacs/site-lisp \
	-opt \
	--coqdocdir %{_datadir}/texmf/tex/latex/misc \
	--coqide opt

%{__make} -j1 world check	# Use native coq to compile theories

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} -e install \
	COQINSTALLPREFIX=$RPM_BUILD_ROOT/
# To install only locally the binaries compiled with absolute paths

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/coq-interface
%attr(755,root,root) %{_bindir}/coq-interface.opt
%attr(755,root,root) %{_bindir}/coq-tex
%attr(755,root,root) %{_bindir}/coq_makefile
%attr(755,root,root) %{_bindir}/coqc
%attr(755,root,root) %{_bindir}/coqdep
%attr(755,root,root) %{_bindir}/coqdoc
%attr(755,root,root) %{_bindir}/coqide*
%attr(755,root,root) %{_bindir}/coqmktop
%attr(755,root,root) %{_bindir}/coqtop
%attr(755,root,root) %{_bindir}/coqtop.byte
%attr(755,root,root) %{_bindir}/coqtop.opt
%attr(755,root,root) %{_bindir}/coqwc
%attr(755,root,root) %{_bindir}/gallina
%attr(755,root,root) %{_bindir}/parser
%attr(755,root,root) %{_bindir}/parser.opt
%dir %{_libdir}/coq
%{_libdir}/coq/*
%{_datadir}/emacs/site-lisp/coq.el
%{_datadir}/emacs/site-lisp/coq-inferior.el
%{_mandir}/man1/coq-tex.1*
%{_mandir}/man1/coqdep.1*
%{_mandir}/man1/gallina.1*
%{_mandir}/man1/coqc.1*
%{_mandir}/man1/coqtop.1*
%{_mandir}/man1/coqtop.byte.1*
%{_mandir}/man1/coqtop.opt.1*
%{_mandir}/man1/coq_makefile.1*
%{_mandir}/man1/coqmktop.1*
%{_mandir}/man1/coq-interface.1*
%{_mandir}/man1/parser.1*
%{_mandir}/man1/coqdoc.1*
%{_mandir}/man1/coqwc.1*
%{_datadir}/texmf/tex/latex/misc/coqdoc.sty
%{_desktopdir}/coqide.desktop
%{_pixmapsdir}/coqide.xpm
