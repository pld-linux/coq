#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)
%bcond_without	sse2		# SSE2 instructions (i387 maths not supported as of 8.15)
%bcond_with	doc		# documentation
%bcond_with	tests		# run testsuite (csdp dependant micromega tests fail badly on x86_64)
#
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif

%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	The Coq Proof Assistant
Summary(pl.UTF-8):	Coq - narzędzie pomagające w udowadnianiu
Name:		coq
Version:	8.15.0
Release:	1
License:	LGPL v2.1
Group:		Applications/Math
#Source0Download: https://github.com/coq/coq/releases
Source0:	https://github.com/coq/coq/archive/V%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cfa91d270e013b0ebe49120c2101d010
Source1:	coqide.desktop
Source2:	coqide.xpm
Patch0:		%{name}-dune-prefix.patch
URL:		https://coq.inria.fr/
BuildRequires:	bash
BuildRequires:	ocaml >= 1:4.05
BuildRequires:	camlp5 >= 5.01
BuildRequires:	ocaml-dune >= 2.5.0
BuildRequires:	ocaml-findlib >= 1.8.1
BuildRequires:	ocaml-zarith-devel >= 1.10
BuildRequires:	ocaml-lablgtk3-devel >= 3.1.0
BuildRequires:	ocaml-lablgtk3-gtksourceview-devel >= 3.1.0
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3 >= 1:3
# TODO (and adjust package name)
BuildRequires:	python3-antlr4-python3-runtime >= 4.7.1
BuildRequires:	python3-bs4 >= 4.0.6
BuildRequires:	python3-pexpect >= 4.2.1
BuildRequires:	python3-sphinx_rtd_theme >= 0.4.3
# TODO (and adjust package name)
BuildRequires:	python3-sphinxcontrib-bibtex >= 0.4.2
BuildRequires:	sphinx-pdg >= 2.3.1
# TODO: update texlive packages list (or drop pdf building leaving only html)
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
%endif
%if %{with sse2}
Requires:	cpuinfo(sse2)
%endif
Requires:	ocaml-coq-devel = %{version}-%{release}
Obsoletes:	coq-emacs < 8.13.1
# same as ocaml-zarith
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Exclude private ocaml interfaces
%define		_noautoreq	ocamlx?\\\((Configwin_types|Interface|Richpp|Serialize|Xml_p(arser|rinter)|Xmlprotocol)\\\)

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

%package -n ocaml-coq
Summary:	Coq Proof Assistant - OCaml runtime libraries
Summary(pl.UTF-8):	Asystent udowadniania Coq - biblioteki uruchomieniowe OCamla
Group:		Libraries
%requires_eq	ocaml-runtime

%description -n ocaml-coq
Coq Proof Assistant - OCaml runtime libraries.

%description -n ocaml-coq -l pl.UTF-8
Asystent udowadniania Coq - biblioteki uruchomieniowe OCamla.

%package -n ocaml-coq-devel
Summary:	Coq Proof Assistant - OCaml development libraries
Summary(pl.UTF-8):	Asystent udowadniania Coq - biblioteki programistyczne OCamla
Group:		Development/Libraries
Requires:	ocaml-coq = %{version}-%{release}
%requires_eq	ocaml

%description -n ocaml-coq-devel
Coq Proof Assistant - OCaml development libraries.

%description -n ocaml-coq-devel -l pl.UTF-8
Asystent udowadniania Coq - biblioteki programistyczne OCamla.

%package latex
Summary:	Coq documentation style for LaTeX
Summary(pl.UTF-8):	Styl dokumentacji Coq dla LaTeXa
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description latex
Coq documentation style for LaTeX.

%description latex -l pl.UTF-8
Styl dokumentacji Coq dla LaTeXa.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i 's|-Wall.*-O2|%{rpmcflags} -Wno-unused|' tools/configure/configure.ml
%if %{without sse2}
%{__sed} -i -e '/cflags_sse2/ s/-msse2 -mfpmath=sse//' tools/configure/configure.ml
%endif
%{__sed} -i 's,-shared,& -g,g' tools/CoqMakefile.in

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
      tools/make-both-single-timing-files.py \
      tools/make-both-time-files.py \
      tools/make-one-time-file.py

%{__sed} -i -e '1s,/usr/bin/env python2,%{__python3},' \
      doc/tools/coqrst/notations/fontsupport.py

%build
./configure \
	-prefix %{_prefix} \
	-configdir %{_sysconfdir}/%{name} \
	-datadir %{_datadir}/%{name} \
	-docdir %{_docdir}/%{name}-%{version} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
%if %{with ocaml_opt}
	-coqide opt \
	-native-compiler yes \
%else
	-byte-only \
	-coqide byte \
	-native-compiler no \
%endif
	-browser "xdg-open %s" \
	%{?with_doc:-with-doc yes}

%{__make} world \
	CAML_LD_LIBRARY_PATH=kernel/byterun \
	_DDISPLAY=verbose \
	VERBOSE=1
%{?with_tests:%{__make} check VERBOSE=1 CAML_LD_LIBRARY_PATH=kernel/byterun} # Use native coq to compile theories

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_sysconfdir}/%{name}}

%{__make} install \
	_DDISPLAY=verbose \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

cp -p CREDITS README.md $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/coq-core/*/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/coq-core/*/*/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/coq-core/*/*/*/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/coqide-server/*/*.ml
# build time
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/ocaml/coq-core/tools

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%dir %{_sysconfdir}/%{name}
%attr(755,root,root) %{_bindir}/coq-tex
%attr(755,root,root) %{_bindir}/coq_makefile
%attr(755,root,root) %{_bindir}/coqc
%attr(755,root,root) %{_bindir}/coqc.byte
%attr(755,root,root) %{_bindir}/coqchk
%attr(755,root,root) %{_bindir}/coqdep
%attr(755,root,root) %{_bindir}/coqdoc
%attr(755,root,root) %{_bindir}/coqide
%attr(755,root,root) %{_bindir}/coqidetop.byte
%attr(755,root,root) %{_bindir}/coqidetop.opt
%attr(755,root,root) %{_bindir}/coqnative
%attr(755,root,root) %{_bindir}/coqpp
%attr(755,root,root) %{_bindir}/coqproofworker.opt
%attr(755,root,root) %{_bindir}/coqqueryworker.opt
%attr(755,root,root) %{_bindir}/coqtacticworker.opt
%attr(755,root,root) %{_bindir}/coqtop
%attr(755,root,root) %{_bindir}/coqtop.byte
%attr(755,root,root) %{_bindir}/coqtop.opt
%attr(755,root,root) %{_bindir}/coqwc
%attr(755,root,root) %{_bindir}/coqworkmgr
%attr(755,root,root) %{_bindir}/csdpcert
%attr(755,root,root) %{_bindir}/ocamllibdep
%attr(755,root,root) %{_bindir}/votour
%dir %{_libdir}/coq
%{_libdir}/coq/theories
%{_libdir}/coq/user-contrib
%{_mandir}/man1/coq_makefile.1*
%{_mandir}/man1/coq-tex.1*
%{_mandir}/man1/coqc.1*
%{_mandir}/man1/coqchk.1*
%{_mandir}/man1/coqdep.1*
%{_mandir}/man1/coqdoc.1*
%{_mandir}/man1/coqide.1*
%{_mandir}/man1/coqnative.1*
%{_mandir}/man1/coqtop.1*
%{_mandir}/man1/coqtop.byte.1*
%{?with_ocaml_opt:%{_mandir}/man1/coqtop.opt.1*}
%{_mandir}/man1/coqwc.1*
%{_desktopdir}/coqide.desktop
%{_pixmapsdir}/coqide.xpm
%{_datadir}/%{name}

%files -n ocaml-coq
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/coq-core
%{_libdir}/ocaml/coq-core/META
%{_libdir}/ocaml/coq-core/revision
%dir %{_libdir}/ocaml/coq-core/boot
%{_libdir}/ocaml/coq-core/boot/*.cma
%dir %{_libdir}/ocaml/coq-core/clib
%{_libdir}/ocaml/coq-core/clib/*.cma
%dir %{_libdir}/ocaml/coq-core/config
%{_libdir}/ocaml/coq-core/config/*.cma
%dir %{_libdir}/ocaml/coq-core/engine
%{_libdir}/ocaml/coq-core/engine/*.cma
%dir %{_libdir}/ocaml/coq-core/gramlib
%{_libdir}/ocaml/coq-core/gramlib/*.cma
%dir %{_libdir}/ocaml/coq-core/interp
%{_libdir}/ocaml/coq-core/interp/*.cma
%dir %{_libdir}/ocaml/coq-core/kernel
%{_libdir}/ocaml/coq-core/kernel/*.cma
%dir %{_libdir}/ocaml/coq-core/lib
%{_libdir}/ocaml/coq-core/lib/*.cma
%dir %{_libdir}/ocaml/coq-core/library
%{_libdir}/ocaml/coq-core/library/*.cma
%dir %{_libdir}/ocaml/coq-core/parsing
%{_libdir}/ocaml/coq-core/parsing/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins
%dir %{_libdir}/ocaml/coq-core/plugins/btauto
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/cc
%{_libdir}/ocaml/coq-core/plugins/cc/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/derive
%{_libdir}/ocaml/coq-core/plugins/derive/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/extraction
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/firstorder
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/funind
%{_libdir}/ocaml/coq-core/plugins/funind/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/ltac
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/ltac2
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/micromega
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/nsatz
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/number_string_notation
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/ring
%{_libdir}/ocaml/coq-core/plugins/ring/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/rtauto
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/ssreflect
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/ssrmatching
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/tauto
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/tutorial
%dir %{_libdir}/ocaml/coq-core/plugins/tutorial/p0
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/tutorial/p1
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/tutorial/p2
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/tutorial/p3
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cma
%dir %{_libdir}/ocaml/coq-core/plugins/zify
%{_libdir}/ocaml/coq-core/plugins/zify/*.cma
%dir %{_libdir}/ocaml/coq-core/pretyping
%{_libdir}/ocaml/coq-core/pretyping/*.cma
%dir %{_libdir}/ocaml/coq-core/printing
%{_libdir}/ocaml/coq-core/printing/*.cma
%dir %{_libdir}/ocaml/coq-core/proofs
%{_libdir}/ocaml/coq-core/proofs/*.cma
%dir %{_libdir}/ocaml/coq-core/stm
%{_libdir}/ocaml/coq-core/stm/*.cma
%dir %{_libdir}/ocaml/coq-core/sysinit
%{_libdir}/ocaml/coq-core/sysinit/*.cma
%dir %{_libdir}/ocaml/coq-core/tactics
%{_libdir}/ocaml/coq-core/tactics/*.cma
%dir %{_libdir}/ocaml/coq-core/top_printers
%{_libdir}/ocaml/coq-core/top_printers/*.cma
%dir %{_libdir}/ocaml/coq-core/toplevel
%{_libdir}/ocaml/coq-core/toplevel/*.cma
%dir %{_libdir}/ocaml/coq-core/vernac
%{_libdir}/ocaml/coq-core/vernac/*.cma
%dir %{_libdir}/ocaml/coq-core/vm
%{_libdir}/ocaml/coq-core/vm/*.cma
%dir %{_libdir}/ocaml/coqide
%{_libdir}/ocaml/coqide/META
%dir %{_libdir}/ocaml/coqide-server
%{_libdir}/ocaml/coqide-server/META
%dir %{_libdir}/ocaml/coqide-server/core
%{_libdir}/ocaml/coqide-server/core/*.cma
%dir %{_libdir}/ocaml/coqide-server/protocol
%{_libdir}/ocaml/coqide-server/protocol/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/coq-core/boot/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/clib/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/config/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/engine/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/gramlib/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/interp/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/kernel/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/lib/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/library/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/parsing/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/btauto/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/cc/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/derive/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/extraction/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/funind/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/ltac/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/micromega/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/ring/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/tauto/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/plugins/zify/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/pretyping/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/printing/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/proofs/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/stm/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/sysinit/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/tactics/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/top_printers/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/toplevel/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/vernac/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coq-core/vm/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coqide-server/core/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/coqide-server/protocol/*.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcoqrun_stubs.so

%files -n ocaml-coq-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/coq-core/dune-package
%{_libdir}/ocaml/coq-core/opam
%{_libdir}/ocaml/coq-core/boot/*.cmi
%{_libdir}/ocaml/coq-core/boot/*.cmt
%{_libdir}/ocaml/coq-core/boot/*.cmti
%{_libdir}/ocaml/coq-core/boot/*.mli
%{_libdir}/ocaml/coq-core/clib/*.cmi
%{_libdir}/ocaml/coq-core/clib/*.cmt
%{_libdir}/ocaml/coq-core/clib/*.cmti
%{_libdir}/ocaml/coq-core/clib/*.mli
%{_libdir}/ocaml/coq-core/config/*.cmi
%{_libdir}/ocaml/coq-core/config/*.cmt
%{_libdir}/ocaml/coq-core/config/*.cmti
%{_libdir}/ocaml/coq-core/config/*.mli
%{_libdir}/ocaml/coq-core/engine/*.cmi
%{_libdir}/ocaml/coq-core/engine/*.cmt
%{_libdir}/ocaml/coq-core/engine/*.cmti
%{_libdir}/ocaml/coq-core/engine/*.mli
%{_libdir}/ocaml/coq-core/gramlib/*.cmi
%{_libdir}/ocaml/coq-core/gramlib/*.cmt
%{_libdir}/ocaml/coq-core/gramlib/*.cmti
%{_libdir}/ocaml/coq-core/gramlib/*.mli
%{_libdir}/ocaml/coq-core/interp/*.cmi
%{_libdir}/ocaml/coq-core/interp/*.cmt
%{_libdir}/ocaml/coq-core/interp/*.cmti
%{_libdir}/ocaml/coq-core/interp/*.mli
%{_libdir}/ocaml/coq-core/kernel/*.cmi
%{_libdir}/ocaml/coq-core/kernel/*.cmt
%{_libdir}/ocaml/coq-core/kernel/*.cmti
%{_libdir}/ocaml/coq-core/kernel/*.mli
%{_libdir}/ocaml/coq-core/lib/*.cmi
%{_libdir}/ocaml/coq-core/lib/*.cmt
%{_libdir}/ocaml/coq-core/lib/*.cmti
%{_libdir}/ocaml/coq-core/lib/*.mli
%{_libdir}/ocaml/coq-core/library/*.cmi
%{_libdir}/ocaml/coq-core/library/*.cmt
%{_libdir}/ocaml/coq-core/library/*.cmti
%{_libdir}/ocaml/coq-core/library/*.mli
%{_libdir}/ocaml/coq-core/parsing/*.cmi
%{_libdir}/ocaml/coq-core/parsing/*.cmt
%{_libdir}/ocaml/coq-core/parsing/*.cmti
%{_libdir}/ocaml/coq-core/parsing/*.mli
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cmi
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cmt
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cmti
%{_libdir}/ocaml/coq-core/plugins/btauto/*.mli
%{_libdir}/ocaml/coq-core/plugins/cc/*.cmi
%{_libdir}/ocaml/coq-core/plugins/cc/*.cmt
%{_libdir}/ocaml/coq-core/plugins/cc/*.cmti
%{_libdir}/ocaml/coq-core/plugins/cc/*.mli
%{_libdir}/ocaml/coq-core/plugins/derive/*.cmi
%{_libdir}/ocaml/coq-core/plugins/derive/*.cmt
%{_libdir}/ocaml/coq-core/plugins/derive/*.cmti
%{_libdir}/ocaml/coq-core/plugins/derive/*.mli
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cmi
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cmt
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cmti
%{_libdir}/ocaml/coq-core/plugins/extraction/*.mli
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmi
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmt
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmti
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.mli
%{_libdir}/ocaml/coq-core/plugins/funind/*.cmi
%{_libdir}/ocaml/coq-core/plugins/funind/*.cmt
%{_libdir}/ocaml/coq-core/plugins/funind/*.cmti
%{_libdir}/ocaml/coq-core/plugins/funind/*.mli
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cmi
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cmt
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cmti
%{_libdir}/ocaml/coq-core/plugins/ltac/*.mli
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmi
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmt
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmti
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.mli
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cmi
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cmt
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cmti
%{_libdir}/ocaml/coq-core/plugins/micromega/*.mli
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmi
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmt
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmti
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.mli
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmi
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmt
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmti
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.mli
%{_libdir}/ocaml/coq-core/plugins/ring/*.cmi
%{_libdir}/ocaml/coq-core/plugins/ring/*.cmt
%{_libdir}/ocaml/coq-core/plugins/ring/*.cmti
%{_libdir}/ocaml/coq-core/plugins/ring/*.mli
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmi
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmt
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmti
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.mli
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmi
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmt
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmti
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.mli
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmi
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmt
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmti
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.mli
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cmi
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cmt
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cmti
%{_libdir}/ocaml/coq-core/plugins/tauto/*.mli
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmi
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmt
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmti
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.mli
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmi
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmt
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmti
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.mli
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmi
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmt
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmti
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.mli
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmi
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmt
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmti
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.mli
%{_libdir}/ocaml/coq-core/plugins/zify/*.cmi
%{_libdir}/ocaml/coq-core/plugins/zify/*.cmt
%{_libdir}/ocaml/coq-core/plugins/zify/*.cmti
%{_libdir}/ocaml/coq-core/plugins/zify/*.mli
%{_libdir}/ocaml/coq-core/pretyping/*.cmi
%{_libdir}/ocaml/coq-core/pretyping/*.cmt
%{_libdir}/ocaml/coq-core/pretyping/*.cmti
%{_libdir}/ocaml/coq-core/pretyping/*.mli
%{_libdir}/ocaml/coq-core/printing/*.cmi
%{_libdir}/ocaml/coq-core/printing/*.cmt
%{_libdir}/ocaml/coq-core/printing/*.cmti
%{_libdir}/ocaml/coq-core/printing/*.mli
%{_libdir}/ocaml/coq-core/proofs/*.cmi
%{_libdir}/ocaml/coq-core/proofs/*.cmt
%{_libdir}/ocaml/coq-core/proofs/*.cmti
%{_libdir}/ocaml/coq-core/proofs/*.mli
%{_libdir}/ocaml/coq-core/stm/*.cmi
%{_libdir}/ocaml/coq-core/stm/*.cmt
%{_libdir}/ocaml/coq-core/stm/*.cmti
%{_libdir}/ocaml/coq-core/stm/*.mli
%{_libdir}/ocaml/coq-core/sysinit/*.cmi
%{_libdir}/ocaml/coq-core/sysinit/*.cmt
%{_libdir}/ocaml/coq-core/sysinit/*.cmti
%{_libdir}/ocaml/coq-core/sysinit/*.mli
%{_libdir}/ocaml/coq-core/tactics/*.cmi
%{_libdir}/ocaml/coq-core/tactics/*.cmt
%{_libdir}/ocaml/coq-core/tactics/*.cmti
%{_libdir}/ocaml/coq-core/tactics/*.mli
%{_libdir}/ocaml/coq-core/top_printers/*.cmi
%{_libdir}/ocaml/coq-core/top_printers/*.cmt
%{_libdir}/ocaml/coq-core/top_printers/*.cmti
%{_libdir}/ocaml/coq-core/top_printers/*.mli
%{_libdir}/ocaml/coq-core/toplevel/*.cmi
%{_libdir}/ocaml/coq-core/toplevel/*.cmt
%{_libdir}/ocaml/coq-core/toplevel/*.cmti
%{_libdir}/ocaml/coq-core/toplevel/*.mli
%{_libdir}/ocaml/coq-core/vernac/*.cmi
%{_libdir}/ocaml/coq-core/vernac/*.cmt
%{_libdir}/ocaml/coq-core/vernac/*.cmti
%{_libdir}/ocaml/coq-core/vernac/*.mli
%{_libdir}/ocaml/coq-core/vm/libcoqrun_stubs.a
%{_libdir}/ocaml/coq-core/vm/*.cmi
%{_libdir}/ocaml/coq-core/vm/*.cmt
%{_libdir}/ocaml/coqide/dune-package
%{_libdir}/ocaml/coqide/opam
%{_libdir}/ocaml/coqide-server/dune-package
%{_libdir}/ocaml/coqide-server/opam
%{_libdir}/ocaml/coqide-server/core/*.cmi
%{_libdir}/ocaml/coqide-server/core/*.cmt
%{_libdir}/ocaml/coqide-server/core/*.cmti
%{_libdir}/ocaml/coqide-server/core/*.mli
%{_libdir}/ocaml/coqide-server/protocol/*.cmi
%{_libdir}/ocaml/coqide-server/protocol/*.cmt
%{_libdir}/ocaml/coqide-server/protocol/*.cmti
%{_libdir}/ocaml/coqide-server/protocol/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/coq-core/boot/boot.a
%{_libdir}/ocaml/coq-core/boot/*.cmx
%{_libdir}/ocaml/coq-core/boot/*.cmxa
%{_libdir}/ocaml/coq-core/clib/clib.a
%{_libdir}/ocaml/coq-core/clib/*.cmx
%{_libdir}/ocaml/coq-core/clib/*.cmxa
%{_libdir}/ocaml/coq-core/config/config.a
%{_libdir}/ocaml/coq-core/config/*.cmx
%{_libdir}/ocaml/coq-core/config/*.cmxa
%{_libdir}/ocaml/coq-core/engine/engine.a
%{_libdir}/ocaml/coq-core/engine/*.cmx
%{_libdir}/ocaml/coq-core/engine/*.cmxa
%{_libdir}/ocaml/coq-core/gramlib/gramlib.a
%{_libdir}/ocaml/coq-core/gramlib/*.cmx
%{_libdir}/ocaml/coq-core/gramlib/*.cmxa
%{_libdir}/ocaml/coq-core/interp/interp.a
%{_libdir}/ocaml/coq-core/interp/*.cmx
%{_libdir}/ocaml/coq-core/interp/*.cmxa
%{_libdir}/ocaml/coq-core/kernel/kernel.a
%{_libdir}/ocaml/coq-core/kernel/*.cmx
%{_libdir}/ocaml/coq-core/kernel/*.cmxa
%{_libdir}/ocaml/coq-core/lib/lib.a
%{_libdir}/ocaml/coq-core/lib/*.cmx
%{_libdir}/ocaml/coq-core/lib/*.cmxa
%{_libdir}/ocaml/coq-core/library/library.a
%{_libdir}/ocaml/coq-core/library/*.cmx
%{_libdir}/ocaml/coq-core/library/*.cmxa
%{_libdir}/ocaml/coq-core/parsing/parsing.a
%{_libdir}/ocaml/coq-core/parsing/*.cmx
%{_libdir}/ocaml/coq-core/parsing/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/btauto/btauto_plugin.a
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cmx
%{_libdir}/ocaml/coq-core/plugins/btauto/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/cc/cc_plugin.a
%{_libdir}/ocaml/coq-core/plugins/cc/*.cmx
%{_libdir}/ocaml/coq-core/plugins/cc/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/derive/derive_plugin.a
%{_libdir}/ocaml/coq-core/plugins/derive/*.cmx
%{_libdir}/ocaml/coq-core/plugins/derive/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/extraction/extraction_plugin.a
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cmx
%{_libdir}/ocaml/coq-core/plugins/extraction/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/firstorder/firstorder_plugin.a
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmx
%{_libdir}/ocaml/coq-core/plugins/firstorder/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/funind/funind_plugin.a
%{_libdir}/ocaml/coq-core/plugins/funind/*.cmx
%{_libdir}/ocaml/coq-core/plugins/funind/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/ltac/ltac_plugin.a
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cmx
%{_libdir}/ocaml/coq-core/plugins/ltac/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/ltac2/ltac2_plugin.a
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmx
%{_libdir}/ocaml/coq-core/plugins/ltac2/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/micromega/micromega_plugin.a
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cmx
%{_libdir}/ocaml/coq-core/plugins/micromega/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/nsatz/nsatz_plugin.a
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmx
%{_libdir}/ocaml/coq-core/plugins/nsatz/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/number_string_notation_plugin.a
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmx
%{_libdir}/ocaml/coq-core/plugins/number_string_notation/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/ring/ring_plugin.a
%{_libdir}/ocaml/coq-core/plugins/ring/*.cmx
%{_libdir}/ocaml/coq-core/plugins/ring/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/rtauto/rtauto_plugin.a
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmx
%{_libdir}/ocaml/coq-core/plugins/rtauto/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/ssreflect/ssreflect_plugin.a
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmx
%{_libdir}/ocaml/coq-core/plugins/ssreflect/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/ssrmatching_plugin.a
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmx
%{_libdir}/ocaml/coq-core/plugins/ssrmatching/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/tauto/tauto_plugin.a
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cmx
%{_libdir}/ocaml/coq-core/plugins/tauto/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/tuto0_plugin.a
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmx
%{_libdir}/ocaml/coq-core/plugins/tutorial/p0/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/tuto1_plugin.a
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmx
%{_libdir}/ocaml/coq-core/plugins/tutorial/p1/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/tuto2_plugin.a
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmx
%{_libdir}/ocaml/coq-core/plugins/tutorial/p2/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/tuto3_plugin.a
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmx
%{_libdir}/ocaml/coq-core/plugins/tutorial/p3/*.cmxa
%{_libdir}/ocaml/coq-core/plugins/zify/zify_plugin.a
%{_libdir}/ocaml/coq-core/plugins/zify/*.cmx
%{_libdir}/ocaml/coq-core/plugins/zify/*.cmxa
%{_libdir}/ocaml/coq-core/pretyping/pretyping.a
%{_libdir}/ocaml/coq-core/pretyping/*.cmx
%{_libdir}/ocaml/coq-core/pretyping/*.cmxa
%{_libdir}/ocaml/coq-core/printing/printing.a
%{_libdir}/ocaml/coq-core/printing/*.cmx
%{_libdir}/ocaml/coq-core/printing/*.cmxa
%{_libdir}/ocaml/coq-core/proofs/proofs.a
%{_libdir}/ocaml/coq-core/proofs/*.cmx
%{_libdir}/ocaml/coq-core/proofs/*.cmxa
%{_libdir}/ocaml/coq-core/stm/stm.a
%{_libdir}/ocaml/coq-core/stm/*.cmx
%{_libdir}/ocaml/coq-core/stm/*.cmxa
%{_libdir}/ocaml/coq-core/sysinit/sysinit.a
%{_libdir}/ocaml/coq-core/sysinit/*.cmx
%{_libdir}/ocaml/coq-core/sysinit/*.cmxa
%{_libdir}/ocaml/coq-core/tactics/tactics.a
%{_libdir}/ocaml/coq-core/tactics/*.cmx
%{_libdir}/ocaml/coq-core/tactics/*.cmxa
%{_libdir}/ocaml/coq-core/top_printers/top_printers.a
%{_libdir}/ocaml/coq-core/top_printers/*.cmx
%{_libdir}/ocaml/coq-core/top_printers/*.cmxa
%{_libdir}/ocaml/coq-core/toplevel/toplevel.a
%{_libdir}/ocaml/coq-core/toplevel/*.cmx
%{_libdir}/ocaml/coq-core/toplevel/*.cmxa
%{_libdir}/ocaml/coq-core/vernac/vernac.a
%{_libdir}/ocaml/coq-core/vernac/*.cmx
%{_libdir}/ocaml/coq-core/vernac/*.cmxa
%{_libdir}/ocaml/coq-core/vm/coqrun.a
%{_libdir}/ocaml/coq-core/vm/*.cmx
%{_libdir}/ocaml/coq-core/vm/*.cmxa
%{_libdir}/ocaml/coqide-server/core/core.a
%{_libdir}/ocaml/coqide-server/core/*.cmx
%{_libdir}/ocaml/coqide-server/core/*.cmxa
%{_libdir}/ocaml/coqide-server/protocol/protocol.a
%{_libdir}/ocaml/coqide-server/protocol/*.cmx
%{_libdir}/ocaml/coqide-server/protocol/*.cmxa
%endif

%files latex
%defattr(644,root,root,755)
%{_datadir}/texmf/tex/latex/misc/coqdoc.sty
