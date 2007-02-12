Summary:	The Coq Proof Assistant
Summary(pl.UTF-8):   Coq - narzędzie pomagające w udowadnianiu
Name:		coq
Version:	8.0pl2
Release:	2
License:	GPL
Group:		Applications/Math
Vendor:		INRIA Rocquencourt
Source0:	ftp://ftp.inria.fr/INRIA/coq/V%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	39ee0fed76e47a11de2f49e2c236ef79
# ftp://ftp.inria.fr/INRIA/coq/V8.0pl2/patch-coq-8.0pl2-ocaml-3.09
Patch0:		%{name}-ocaml-3.09.patch
Patch1:		%{name}-lablgtk26.patch
URL:		http://coq.inria.fr/
BuildRequires:	emacs
BuildRequires:	ocaml >= 3.09.0
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-lablgtk2-devel >= 2.6.0
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
%patch0 -p0
%patch1 -p1

%build
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
	-emacs emacs \
	-emacslib %{_datadir}/emacs/site-lisp \
	-opt \
	--coqdocdir %{_datadir}/texmf/tex/latex/misc \
	--coqide opt \
	-reals all	# Need ocamlc.opt and ocamlopt.opt 

%{__make} world check	# Use native coq to compile theories

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -e install \
	COQINSTALLPREFIX=$RPM_BUILD_ROOT/
# To install only locally the binaries compiled with absolute paths

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
%attr(755,root,root) %{_bindir}/coqide.byte
%attr(755,root,root) %{_bindir}/coqide.opt
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
