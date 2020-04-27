Summary:	eSpeak NG - multi-lingual software speech synthesizer
Summary(pl.UTF-8):	eSpeak NG - wielojęzyczny programowy syntezator mowy
Name:		espeak-ng
Version:	1.50
Release:	1
License:	GPL v3+
Group:		Applications/Sound
#Source0Download: https://github.com/espeak-ng/espeak-ng/releases
Source0:	https://github.com/espeak-ng/espeak-ng/releases/download/%{version}/%{name}-%{version}.tgz
# Source0-md5:	85422fd7ccebd32ef4d92e6719efd8be
# so use archive
#Source0:	https://github.com/espeak-ng/espeak-ng/archive/%{version}/%{name}-%{version}.tar.gz
URL:		https://github.com/espeak-ng/espeak-ng/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libtool >= 2:2
BuildRequires:	pcaudiolib-devel
BuildRequires:	ronn
BuildRequires:	sonic-devel
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	espeak
Obsoletes:	speak
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The eSpeak NG (Next Generation) Text-to-Speech program is an open
source speech synthesizer that supports 95 languages and accents. It
is based on the eSpeak engine created by Jonathan Duddington. It uses
spectral formant synthesis by default which sounds robotic, but can be
configured to use Klatt formant synthesis or MBROLA to give it a more
natural sound.

%description -l pl.UTF-8
eSpeak NG (następnej generacji) to mający otwarte źródła program do
syntezy mowy, obsługujący 95 języków i akcentów. Jest oparty na
silniku eSpeak napisanym przez Jonathana Duddingtona. Domyślnie używa
spektralnej syntezy formantowej, która brzmi jak robot, ale może być
skonfigurowany, aby używał syntezy formantowej Klatta lub syntezy
MBROLA, aby brzmiał bardziej naturalnie.

%package libs
Summary:	eSpeak shared libraries
Summary(pl.UTF-8):	eSpeak - biblioteki
Group:		Libraries
Obsoletes:	speak-libs

%description libs
eSpeak shared libraries.

%description libs -l pl.UTF-8
eSpeak - biblioteki dzielone.

%package devel
Summary:	eSpeak NG - development files
Summary(pl.UTF-8):	eSpeak NG - pliki dla programistów
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
eSpeak NG - development files.

%description devel -l pl.UTF-8
eSpeak NG - pliki dla programistów.

%package static
Summary:	eSpeak NG - static libraries
Summary(pl.UTF-8):	eSpeak NG - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
eSpeak NG - static libraries.

%description static -l pl.UTF-8
eSpeak NG - biblioteki statyczne.

%package -n vim-syntax-espeak
Summary:	Vim syntax rules for eSpeak files
Summary(pl.UTF-8):	Reguły składni Vima dla plików eSpeaka
Group:		Applications/Editors
Requires:	vim-rt

%description -n vim-syntax-espeak
Vim syntax rules for eSpeak files.

%description -n vim-syntax-espeak -l pl.UTF-8
Reguły składni Vima dla plików eSpeaka.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-extdict-ru \
	--with-extdict-zh \
	--with-extdict-zhy

# parallel build fails on data
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	vim_addons_ftdetectdir=%{_datadir}/vim/vimfiles/ftdetect \
	vim_addons_syntaxdir=%{_datadir}/vim/vimfiles/syntax

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libespeak-ng*.la
# allow coexistence with espeak
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libespeak.la
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/espeak
# no vim-addon-manager in PLD
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/vim/registry

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md COPYING.{BSD2,IEEE,UCD} README.md docs/{*.md,images,languages,phonemes}
%attr(755,root,root) %{_bindir}/espeak
%attr(755,root,root) %{_bindir}/espeak-ng
%attr(755,root,root) %{_bindir}/speak
%attr(755,root,root) %{_bindir}/speak-ng
%{_datadir}/%{name}-data
%{_mandir}/man1/espeak-ng.1*
%{_mandir}/man1/speak-ng.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libespeak-ng.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libespeak-ng.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libespeak-ng.so
%{_includedir}/espeak-ng
%{_pkgconfigdir}/espeak-ng.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libespeak-ng.a

%files -n vim-syntax-espeak
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/ftdetect/espeakfiletype.vim
%{_datadir}/vim/vimfiles/syntax/espeaklist.vim
%{_datadir}/vim/vimfiles/syntax/espeakrules.vim
