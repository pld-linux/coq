Summary:	The Coq Proof Assistant
Summary(pl):	Coq - narzêdzie pomagaj±ce w udowadnianiu
Name:		coq
Version:	7.4
Release:	1
License:	GPL
Group:		Applications/Math
Vendor:		INRIA Rocquencourt
Source0:	ftp://ftp.inria.fr/INRIA/coq/V7.4/%{name}-%{version}.tar.gz
# Source0-md5:	13ac61f150823e54ad84a9096e2dd646
Patch0:		coq-ocaml-3.07.patch
Icon:		petit-coq.gif
URL:		http://coq.inria.fr/
BuildRequires:	emacs
BuildRequires:	ocaml
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Coq is a proof assistant which:
 - allows to handle calculus assertions,
 - check mechanically proofs of these assertions,
 - helps to find formal proofs,
 - extracts a certified program from the constructive proof of its
   formal specification.

%description -l pl
Coq to narzêdzie pomagaj±ce w udowadnianiu, które:
- pozwala uporaæ siê z twierdzeniami dotycz±cymi rachunku
  ró¿niczkowego,
- mechanicznie sprawdzaæ dowody tych twierdzeñ,
- pomagaæ w znalezieniu formalnych dowodów,
- wyci±gaæ program o dowiedzionej poprawno¶ci z konstruktywnego
  dowodu jego formalnej specyfikacji.

%prep
%setup -q
%patch0 -p0

%build
./configure \
	-bindir %{_bindir} \
	-libdir %{_libdir}/coq \
	-mandir %{_mandir} \
	-emacs emacs \
	-emacslib %{_datadir}/emacs/site-lisp \
	-opt \
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
%attr(755,root,root) %{_bindir}/coqmktop
%attr(755,root,root) %{_bindir}/coqc
%attr(755,root,root) %{_bindir}/coqtop.byte
%attr(755,root,root) %{_bindir}/coqtop.opt
%attr(755,root,root) %{_bindir}/coqtop
%attr(755,root,root) %{_bindir}/coqdep
%attr(755,root,root) %{_bindir}/gallina
%attr(755,root,root) %{_bindir}/coq_makefile
%attr(755,root,root) %{_bindir}/coq-tex
%attr(755,root,root) %{_bindir}/coq-interface
%attr(755,root,root) %{_bindir}/coq-interface.opt
%attr(755,root,root) %{_bindir}/parser
%attr(755,root,root) %{_bindir}/coq_vo2xml
%dir %{_libdir}/coq
%dir %{_libdir}/coq/theories
%dir %{_libdir}/coq/theories/*
%{_libdir}/coq/theories/Init/Datatypes.vo
%{_libdir}/coq/theories/Init/DatatypesSyntax.vo
%{_libdir}/coq/theories/Init/Peano.vo
%{_libdir}/coq/theories/Init/PeanoSyntax.vo
%{_libdir}/coq/theories/Init/Logic.vo
%{_libdir}/coq/theories/Init/Specif.vo
%{_libdir}/coq/theories/Init/LogicSyntax.vo
%{_libdir}/coq/theories/Init/SpecifSyntax.vo
%{_libdir}/coq/theories/Init/Logic_Type.vo
%{_libdir}/coq/theories/Init/Wf.vo
%{_libdir}/coq/theories/Init/Logic_TypeSyntax.vo
%{_libdir}/coq/theories/Init/Prelude.vo
%{_libdir}/coq/theories/Logic/Hurkens.vo
%{_libdir}/coq/theories/Logic/ProofIrrelevance.vo
%{_libdir}/coq/theories/Logic/Classical.vo
%{_libdir}/coq/theories/Logic/Classical_Type.vo
%{_libdir}/coq/theories/Logic/Classical_Pred_Set.vo
%{_libdir}/coq/theories/Logic/Eqdep.vo
%{_libdir}/coq/theories/Logic/Classical_Pred_Type.vo
%{_libdir}/coq/theories/Logic/Classical_Prop.vo
%{_libdir}/coq/theories/Logic/ClassicalFacts.vo
%{_libdir}/coq/theories/Logic/Berardi.vo
%{_libdir}/coq/theories/Logic/Eqdep_dec.vo
%{_libdir}/coq/theories/Logic/Decidable.vo
%{_libdir}/coq/theories/Logic/JMeq.vo
%{_libdir}/coq/theories/Arith/Arith.vo
%{_libdir}/coq/theories/Arith/Gt.vo
%{_libdir}/coq/theories/Arith/Between.vo
%{_libdir}/coq/theories/Arith/Le.vo
%{_libdir}/coq/theories/Arith/Compare.vo
%{_libdir}/coq/theories/Arith/Lt.vo
%{_libdir}/coq/theories/Arith/Compare_dec.vo
%{_libdir}/coq/theories/Arith/Min.vo
%{_libdir}/coq/theories/Arith/Div2.vo
%{_libdir}/coq/theories/Arith/Minus.vo
%{_libdir}/coq/theories/Arith/Mult.vo
%{_libdir}/coq/theories/Arith/Even.vo
%{_libdir}/coq/theories/Arith/EqNat.vo
%{_libdir}/coq/theories/Arith/Peano_dec.vo
%{_libdir}/coq/theories/Arith/Euclid.vo
%{_libdir}/coq/theories/Arith/Plus.vo
%{_libdir}/coq/theories/Arith/Wf_nat.vo
%{_libdir}/coq/theories/Arith/Max.vo
%{_libdir}/coq/theories/Arith/Bool_nat.vo
%{_libdir}/coq/theories/Bool/Bool.vo
%{_libdir}/coq/theories/Bool/IfProp.vo
%{_libdir}/coq/theories/Bool/Zerob.vo
%{_libdir}/coq/theories/Bool/DecBool.vo
%{_libdir}/coq/theories/Bool/Sumbool.vo
%{_libdir}/coq/theories/Bool/BoolEq.vo
%{_libdir}/coq/theories/Bool/Bvector.vo
%{_libdir}/coq/theories/ZArith/Wf_Z.vo
%{_libdir}/coq/theories/ZArith/Zsyntax.vo
%{_libdir}/coq/theories/ZArith/ZArith.vo
%{_libdir}/coq/theories/ZArith/auxiliary.vo
%{_libdir}/coq/theories/ZArith/ZArith_dec.vo
%{_libdir}/coq/theories/ZArith/fast_integer.vo
%{_libdir}/coq/theories/ZArith/Zmisc.vo
%{_libdir}/coq/theories/ZArith/zarith_aux.vo
%{_libdir}/coq/theories/ZArith/Zhints.vo
%{_libdir}/coq/theories/ZArith/Zlogarithm.vo
%{_libdir}/coq/theories/ZArith/Zpower.vo
%{_libdir}/coq/theories/ZArith/Zcomplements.vo
%{_libdir}/coq/theories/ZArith/Zdiv.vo
%{_libdir}/coq/theories/ZArith/Zsqrt.vo
%{_libdir}/coq/theories/ZArith/Zwf.vo
%{_libdir}/coq/theories/ZArith/ZArith_base.vo
%{_libdir}/coq/theories/ZArith/Zbool.vo
%{_libdir}/coq/theories/ZArith/Zbinary.vo
%{_libdir}/coq/theories/Lists/List.vo
%{_libdir}/coq/theories/Lists/PolyListSyntax.vo
%{_libdir}/coq/theories/Lists/ListSet.vo
%{_libdir}/coq/theories/Lists/Streams.vo
%{_libdir}/coq/theories/Lists/PolyList.vo
%{_libdir}/coq/theories/Lists/TheoryList.vo
%{_libdir}/coq/theories/Sets/Classical_sets.vo
%{_libdir}/coq/theories/Sets/Permut.vo
%{_libdir}/coq/theories/Sets/Constructive_sets.vo
%{_libdir}/coq/theories/Sets/Powerset.vo
%{_libdir}/coq/theories/Sets/Cpo.vo
%{_libdir}/coq/theories/Sets/Powerset_Classical_facts.vo
%{_libdir}/coq/theories/Sets/Ensembles.vo
%{_libdir}/coq/theories/Sets/Powerset_facts.vo
%{_libdir}/coq/theories/Sets/Finite_sets.vo
%{_libdir}/coq/theories/Sets/Relations_1.vo
%{_libdir}/coq/theories/Sets/Finite_sets_facts.vo
%{_libdir}/coq/theories/Sets/Relations_1_facts.vo
%{_libdir}/coq/theories/Sets/Image.vo
%{_libdir}/coq/theories/Sets/Relations_2.vo
%{_libdir}/coq/theories/Sets/Infinite_sets.vo
%{_libdir}/coq/theories/Sets/Relations_2_facts.vo
%{_libdir}/coq/theories/Sets/Integers.vo
%{_libdir}/coq/theories/Sets/Relations_3.vo
%{_libdir}/coq/theories/Sets/Multiset.vo
%{_libdir}/coq/theories/Sets/Relations_3_facts.vo
%{_libdir}/coq/theories/Sets/Partial_Order.vo
%{_libdir}/coq/theories/Sets/Uniset.vo
%{_libdir}/coq/theories/IntMap/Adalloc.vo
%{_libdir}/coq/theories/IntMap/Mapcanon.vo
%{_libdir}/coq/theories/IntMap/Addec.vo
%{_libdir}/coq/theories/IntMap/Mapcard.vo
%{_libdir}/coq/theories/IntMap/Addr.vo
%{_libdir}/coq/theories/IntMap/Mapc.vo
%{_libdir}/coq/theories/IntMap/Adist.vo
%{_libdir}/coq/theories/IntMap/Mapfold.vo
%{_libdir}/coq/theories/IntMap/Allmaps.vo
%{_libdir}/coq/theories/IntMap/Mapiter.vo
%{_libdir}/coq/theories/IntMap/Fset.vo
%{_libdir}/coq/theories/IntMap/Maplists.vo
%{_libdir}/coq/theories/IntMap/Lsort.vo
%{_libdir}/coq/theories/IntMap/Mapsubset.vo
%{_libdir}/coq/theories/IntMap/Mapaxioms.vo
%{_libdir}/coq/theories/IntMap/Map.vo
%{_libdir}/coq/theories/Relations/Newman.vo
%{_libdir}/coq/theories/Relations/Operators_Properties.vo
%{_libdir}/coq/theories/Relations/Relation_Definitions.vo
%{_libdir}/coq/theories/Relations/Relation_Operators.vo
%{_libdir}/coq/theories/Relations/Relations.vo
%{_libdir}/coq/theories/Relations/Rstar.vo
%{_libdir}/coq/theories/Wellfounded/Disjoint_Union.vo
%{_libdir}/coq/theories/Wellfounded/Inclusion.vo
%{_libdir}/coq/theories/Wellfounded/Inverse_Image.vo
%{_libdir}/coq/theories/Wellfounded/Lexicographic_Exponentiation.vo
%{_libdir}/coq/theories/Wellfounded/Transitive_Closure.vo
%{_libdir}/coq/theories/Wellfounded/Union.vo
%{_libdir}/coq/theories/Wellfounded/Wellfounded.vo
%{_libdir}/coq/theories/Wellfounded/Well_Ordering.vo
%{_libdir}/coq/theories/Wellfounded/Lexicographic_Product.vo
%{_libdir}/coq/theories/Reals/TypeSyntax.vo
%{_libdir}/coq/theories/Reals/Rdefinitions.vo
%{_libdir}/coq/theories/Reals/Rsyntax.vo
%{_libdir}/coq/theories/Reals/Raxioms.vo
%{_libdir}/coq/theories/Reals/RIneq.vo
%{_libdir}/coq/theories/Reals/DiscrR.vo
%{_libdir}/coq/theories/Reals/Rbase.vo
%{_libdir}/coq/theories/Reals/R_Ifp.vo
%{_libdir}/coq/theories/Reals/Rbasic_fun.vo
%{_libdir}/coq/theories/Reals/R_sqr.vo
%{_libdir}/coq/theories/Reals/SplitAbsolu.vo
%{_libdir}/coq/theories/Reals/SplitRmult.vo
%{_libdir}/coq/theories/Reals/ArithProp.vo
%{_libdir}/coq/theories/Reals/Rfunctions.vo
%{_libdir}/coq/theories/Reals/Rseries.vo
%{_libdir}/coq/theories/Reals/SeqProp.vo
%{_libdir}/coq/theories/Reals/Rcomplete.vo
%{_libdir}/coq/theories/Reals/PartSum.vo
%{_libdir}/coq/theories/Reals/AltSeries.vo
%{_libdir}/coq/theories/Reals/Binomial.vo
%{_libdir}/coq/theories/Reals/Rsigma.vo
%{_libdir}/coq/theories/Reals/Rprod.vo
%{_libdir}/coq/theories/Reals/Cauchy_prod.vo
%{_libdir}/coq/theories/Reals/Alembert.vo
%{_libdir}/coq/theories/Reals/SeqSeries.vo
%{_libdir}/coq/theories/Reals/Rtrigo_fun.vo
%{_libdir}/coq/theories/Reals/Rtrigo_def.vo
%{_libdir}/coq/theories/Reals/Rtrigo_alt.vo
%{_libdir}/coq/theories/Reals/Cos_rel.vo
%{_libdir}/coq/theories/Reals/Cos_plus.vo
%{_libdir}/coq/theories/Reals/Rtrigo.vo
%{_libdir}/coq/theories/Reals/Rlimit.vo
%{_libdir}/coq/theories/Reals/Rderiv.vo
%{_libdir}/coq/theories/Reals/RList.vo
%{_libdir}/coq/theories/Reals/Ranalysis1.vo
%{_libdir}/coq/theories/Reals/Ranalysis2.vo
%{_libdir}/coq/theories/Reals/Ranalysis3.vo
%{_libdir}/coq/theories/Reals/Rtopology.vo
%{_libdir}/coq/theories/Reals/MVT.vo
%{_libdir}/coq/theories/Reals/PSeries_reg.vo
%{_libdir}/coq/theories/Reals/Exp_prop.vo
%{_libdir}/coq/theories/Reals/Rtrigo_reg.vo
%{_libdir}/coq/theories/Reals/Rsqrt_def.vo
%{_libdir}/coq/theories/Reals/R_sqrt.vo
%{_libdir}/coq/theories/Reals/Rtrigo_calc.vo
%{_libdir}/coq/theories/Reals/Rgeom.vo
%{_libdir}/coq/theories/Reals/Sqrt_reg.vo
%{_libdir}/coq/theories/Reals/Ranalysis4.vo
%{_libdir}/coq/theories/Reals/Rpower.vo
%{_libdir}/coq/theories/Reals/Ranalysis.vo
%{_libdir}/coq/theories/Reals/NewtonInt.vo
%{_libdir}/coq/theories/Reals/RiemannInt_SF.vo
%{_libdir}/coq/theories/Reals/RiemannInt.vo
%{_libdir}/coq/theories/Reals/Integration.vo
%{_libdir}/coq/theories/Reals/Reals.vo
%{_libdir}/coq/theories/Setoids/Setoid.vo
%{_libdir}/coq/theories/Sorting/Heap.vo
%{_libdir}/coq/theories/Sorting/Permutation.vo
%{_libdir}/coq/theories/Sorting/Sorting.vo
%{_libdir}/coq/contrib/omega/Omega.vo
%dir %{_libdir}/coq/contrib
%dir %{_libdir}/coq/contrib/*
%{_libdir}/coq/contrib/romega/ReflOmegaCore.vo
%{_libdir}/coq/contrib/romega/ROmega.vo
%{_libdir}/coq/contrib/ring/ArithRing.vo
%{_libdir}/coq/contrib/ring/Ring_normalize.vo
%{_libdir}/coq/contrib/ring/Ring_theory.vo
%{_libdir}/coq/contrib/ring/Ring.vo
%{_libdir}/coq/contrib/ring/ZArithRing.vo
%{_libdir}/coq/contrib/ring/Ring_abstract.vo
%{_libdir}/coq/contrib/ring/Quote.vo
%{_libdir}/coq/contrib/ring/Setoid_ring_normalize.vo
%{_libdir}/coq/contrib/ring/Setoid_ring.vo
%{_libdir}/coq/contrib/ring/Setoid_ring_theory.vo
%{_libdir}/coq/contrib/field/Field_Compl.vo
%{_libdir}/coq/contrib/field/Field_Theory.vo
%{_libdir}/coq/contrib/field/Field_Tactic.vo
%{_libdir}/coq/contrib/field/Field.vo
%{_libdir}/coq/contrib/correctness/Arrays.vo
%{_libdir}/coq/contrib/correctness/Correctness.vo
%{_libdir}/coq/contrib/correctness/Exchange.vo
%{_libdir}/coq/contrib/correctness/ArrayPermut.vo
%{_libdir}/coq/contrib/correctness/ProgBool.vo
%{_libdir}/coq/contrib/correctness/ProgInt.vo
%{_libdir}/coq/contrib/correctness/Sorted.vo
%{_libdir}/coq/contrib/correctness/Tuples.vo
%{_libdir}/coq/contrib/fourier/Fourier_util.vo
%{_libdir}/coq/contrib/fourier/Fourier.vo
%{_libdir}/coq/contrib/interface/Centaur.vo
%{_libdir}/coq/contrib/cc/CC.vo
%dir %{_libdir}/coq/states
%{_libdir}/coq/states/barestate.coq
%{_libdir}/coq/states/initial.coq
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
%{_mandir}/man1/coq_vo2xml.1*
