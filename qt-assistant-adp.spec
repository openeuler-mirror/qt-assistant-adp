Name:       qt-assistant-adp
Version:    4.6.3
Release:    20
Summary:    Compatibility version of Qt Assistant
License:    LGPLv2 with exceptions or GPLv3 with exceptions
Url:        https://download.qt.io/archive/qt/4.6/
Source0:    https://download.qt.io/archive/qt/4.6/qt-assistant-qassistantclient-library-compat-src-%{version}.tar.gz
Source1:    QAssistantClient
Source2:    QtAssistant
Patch0001:  01_build_system.diff

BuildRequires: qt4-devel >= 4.7.0
%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}

%description
The old version of Qt Assistant, based on Assistant Document Profile (.adp)
files, and the associated QtAssistantClient library, for compatibility with
applications providing help in that format.

New applications should use the new version of Qt Assistant introduced in Qt
4.4, based on the Qt Help Framework also introduced in Qt 4.4, instead.


%package devel
Summary:    Development filesoftheqt-assistant-adppackage
Requires:   %{name} = %{version}-%{release} qt4-devel

%description devel
Development files of the qt-assistant-adp package.

%prep
%autosetup -n qt-assistant-qassistantclient-library-compat-version-%{version} -p1
install -d include
install -p %{SOURCE1} %{SOURCE2} include/


%build
%{qmake_qt4} QT_PRODUCT=OpenSource
%make_build

cd lib
%{qmake_qt4} CONFIG=create_prl
%make_build
cd -

cd translations
lrelease-qt4 assistant_adp_*.ts
cd -


%install
%make_install INSTALL_ROOT=%{buildroot}
%make_install INSTALL_ROOT=%{buildroot} -C lib

install -d %{buildroot}%{_qt4_translationdir}
install -p -m644 translations/assistant_adp_*.qm %{buildroot}%{_qt4_translationdir}/

install -D -p -m644 features/assistant.prf \
                    %{buildroot}%{_qt4_datadir}/mkspecs/features/assistant.prf

install -p -m644 include/Q* %{buildroot}%{_qt4_headerdir}/QtAssistant/

sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{_qt4_libdir}/*.prl

install -d %{buildroot}%{_bindir}
cd %{buildroot}%{_qt4_bindir}
mv assistant_adp ../../../bin/
ln -s ../../../bin/assistant_adp .
cd -

cd %{buildroot}%{_qt4_libdir}
echo "INPUT(-lQtAssistantClient)" >libQtAssistantClient_debug.so
cd -

%find_lang assistant_adp --with-qt --without-mo

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files -f assistant_adp.lang
%doc LGPL_EXCEPTION.txt LICENSE.LGPL LICENSE.GPL3
%{_bindir}/assistant_adp
%{_qt4_bindir}/{assistant_adp,libQtAssistantClient.so.4*}

%files devel
%{_qt4_headerdir}/QtAssistant/
%{_qt4_libdir}/*
%{_libdir}/pkgconfig/QtAssistantClient.pc
%{_qt4_datadir}/mkspecs/features/assistant.prf


%changelog
* Wed Feb 19 2020 daiqianwen <daiqianwen@huawei.com> - 4.6.3-20
- Package init
