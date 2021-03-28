#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)
%bcond_with	tests		# run testsuite (csdp dependant micromega tests fail badly on x86_64)
#
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	The Coq Proof Assistant
Summary(pl.UTF-8):	Coq - narzędzie pomagające w udowadnianiu
Name:		coq
Version:	8.13.1
Release:	1
License:	LGPL v2.1
Group:		Applications/Math
Source0:	https://github.com/coq/coq/archive/V%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	03ebbf1034c224a0a3327db2d5688c29
Source1:	coqide.desktop
Source2:	coqide.xpm
URL:		http://coq.inria.fr/
BuildRequires:	bash
BuildRequires:	hevea
BuildRequires:	netpbm-progs
BuildRequires:	ocaml >= 1:4.05
BuildRequires:	camlp5 >= 5.01
BuildRequires:	ocaml-dune > 2.5.0
BuildRequires:	ocaml-findlib >= 1.8.1
BuildRequires:	ocaml-zarith-devel >= 1.10
BuildRequires:	ocaml-lablgtk3-devel
BuildRequires:	ocaml-lablgtk3-gtksourceview-devel
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
Obsoletes:	coq-emacs < 8.13.1
# same as ocaml-zarith
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
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
- wyciągać program o dowiedzionej poprawności z konstruktywnego dowodu
  jego formalnej specyfikacji.

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

%{__sed} -ri '/FULLCONFIGDIR/s/OLDROOT|COQINSTALLPREFIX/&2/g' Makefile.install
%{__sed} -i 's|-Wall.*-O2|%{rpmcflags} -Wno-unused|' configure.ml
%{__sed} -i "s|-oc|-ccopt '%{rpmldflags}' -g &|" Makefile.build
%{__sed} -i 's,-shared,& -g,g' tools/CoqMakefile.in Makefile.build

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      tools/make-both-single-timing-files.py \
      tools/make-both-time-files.py \
      tools/make-one-time-file.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python2(\s|$),#!%{__python3}\1,' \
      doc/tools/coqrst/notations/fontsupport.py

%build
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
	-docdir %{_docdir}/%{name}-%{version} \
	-configdir %{_sysconfdir}/%{name} \
	-datadir %{_datadir}/%{name} \
	-coqdocdir %{_datadir}/texmf/tex/latex/misc \
%if %{with ocaml_opt}
	-native-compiler yes \
	-coqide opt \
%else
	-byte-only \
	-native-compiler no \
	-coqide byte \
%endif
	-browser "xdg-open %s"

%{__make} world VERBOSE=1 CAML_LD_LIBRARY_PATH=kernel/byterun
%{?with_tests:%{__make} check VERBOSE=1 CAML_LD_LIBRARY_PATH=kernel/byterun} # Use native coq to compile theories

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	COQINSTALLPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	COQINSTALLPREFIX2=$RPM_BUILD_ROOT%{_sysconfdir} \
	OLDROOT=%{_prefix} \
	OLDROOT2=%{_sysconfdir}

# To install only locally the binaries compiled with absolute paths

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

cp -p CONTRIBUTING.md README.md $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/coqc
%attr(755,root,root) %{_bindir}/coqchk
%attr(755,root,root) %{_bindir}/coqdep
%attr(755,root,root) %{_bindir}/coqdoc
%attr(755,root,root) %{_bindir}/coqide*
%attr(755,root,root) %{_bindir}/coq_makefile
%attr(755,root,root) %{_bindir}/coqpp
%attr(755,root,root) %{_bindir}/coqproofworker.opt
%attr(755,root,root) %{_bindir}/coqqueryworker.opt
%attr(755,root,root) %{_bindir}/coqtacticworker.opt
%attr(755,root,root) %{_bindir}/coq-tex
%attr(755,root,root) %{_bindir}/coqtop
%attr(755,root,root) %{_bindir}/coqtop.opt
%attr(755,root,root) %{_bindir}/coqwc
%attr(755,root,root) %{_bindir}/coqworkmgr
%attr(755,root,root) %{_bindir}/ocamllibdep
%attr(755,root,root) %{_bindir}/votour
%dir %{_libdir}/coq
%{_libdir}/coq/*
%{_mandir}/man1/coq_makefile.1*
%{_mandir}/man1/coq-tex.1*
%{_mandir}/man1/coqc.1*
%{_mandir}/man1/coqchk.1*
%{_mandir}/man1/coqdep.1*
%{_mandir}/man1/coqdoc.1*
%{_mandir}/man1/coqide.1*
%{_mandir}/man1/coqtop.1*
%{_mandir}/man1/coqtop.byte.1*
%{?with_ocaml_opt:%{_mandir}/man1/coqtop.opt.1*}
%{_mandir}/man1/coqwc.1*
%{_desktopdir}/coqide.desktop
%{_pixmapsdir}/coqide.xpm
%{_datadir}/%{name}

%files latex
%defattr(644,root,root,755)
%{_datadir}/texmf/tex/latex/misc/coqdoc.sty
