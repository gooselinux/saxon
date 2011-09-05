# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define resolverdir %{_sysconfdir}/java/resolver

Summary:        Java XSLT processor
Name:           saxon
Version:        6.5.5
Release:        3.5%{?dist}
Epoch:          0
License:        MPLv1.0
Group:          Applications/Text
URL:            http://saxon.sourceforge.net/
Source0:        http://download.sf.net/saxon/saxon6-5-5.zip
Source1:        %{name}.saxon.script
Source2:        %{name}.build.script
Source3:        %{name}.1
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  xml-commons-apis
BuildRequires:  jdom >= 0:1.0
BuildRequires:  ant
Requires:       xml-commons-apis
Requires:       jpackage-utils >= 0:1.6
Requires:       jdom >= 0:1.0

Requires:       jaxp_parser_impl
Requires:       /usr/sbin/update-alternatives
Provides:       jaxp_transform_impl = 0.0.1
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The SAXON package is a collection of tools for processing XML documents.
The main components are:
- An XSLT processor, which implements the Version 1.0 XSLT and XPath
  Recommendations from the World Wide Web Consortium, found at
  http://www.w3.org/TR/1999/REC-xslt-19991116 and
  http://www.w3.org/TR/1999/REC-xpath-19991116 with a number of powerful
  extensions. This version of Saxon also includes many of the new features
  defined in the XSLT 1.1 working draft, but for conformance and portability
  reasons these are not available if the stylesheet header specifies
  version="1.0".
- A Java library, which supports a similar processing model to XSL, but allows
  full programming capability, which you need if you want to perform complex
  processing of the data or to access external services such as a relational
  database.
So you can use SAXON with any SAX-compliant XML parser by writing XSLT
stylesheets, by writing Java applications, or by any combination of the two.

%package        aelfred
Summary:        Java XML parser
Group:          Applications/Text
Requires:       xml-commons-apis

%description    aelfred
A slightly improved version of the AElfred Java XML parser from Microstar.

%package        manual
Summary:        Manual for %{name}
Group:          Documentation

%description    manual
Manual for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
BuildRequires:  java-javadoc
BuildRequires:  jdom-javadoc >= 0:1.0
Requires:       java-javadoc
Requires:       jdom-javadoc >= 0:1.0

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demos for %{name}
Group:          Applications/Text
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%package        jdom
Summary:        JDOM support for %{name}
Group:          Applications/Text
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jdom >= 0:1.0

%description    jdom
JDOM support for %{name}.

%package        scripts
Summary:        Utility scripts for %{name}
Group:          Applications/Text
Requires:       jpackage-utils >= 0:1.6
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    scripts
Utility scripts for %{name}.


%prep
%setup -q -c
unzip -q source.zip
cp -p %{SOURCE2} ./build.xml
# cleanup unnecessary stuff we'll build ourselves
rm -rf *.jar docs/api


%build
export CLASSPATH=%(build-classpath xml-commons-apis jdom)
ant \
  -Dj2se.javadoc=%{_javadocdir}/java \
  -Djdom.javadoc=%{_javadocdir}/jdom

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

cp -p build/lib/%{name}-aelfred.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}-aelfred-%{version}.jar

cp -p build/lib/%{name}-jdom.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{name}-jdom-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
    ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
sed 's,__RESOLVERDIR__,%{resolverdir},' < %{SOURCE1} \
  > $RPM_BUILD_ROOT%{_bindir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
sed 's,__RESOLVERDIR__,%{resolverdir},' < %{SOURCE3} \
  > $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

# jaxp_transform_impl ghost symlink
ln -s %{_sysconfdir}/alternatives \
  $RPM_BUILD_ROOT%{_javadir}/jaxp_transform_impl.jar

# fix newlines in docs
for i in doc/*.html; do
    tr -d \\r < $i > temp_file.html; mv temp_file.html $i
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/%{name}.jar 25

%preun
{
  [ $1 -eq 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%ghost %{_javadir}/jaxp_transform_impl.jar

%files aelfred
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-aelfred*

%files jdom
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-jdom*

%files manual
%defattr(0644,root,root,0755)
%doc doc/*.html

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%files scripts
%defattr(0755,root,root,0755)
%{_bindir}/%{name}
%attr(0644,root,root) %{_mandir}/man1/%{name}.1*

%changelog
* Mon Feb 01 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:6.5.5-3.5
- Resolves: #560798
- Fix rpmlint warnings
- Version jaxp_impl_transform provides statement

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:6.5.5-3.4
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:6.5.5-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:6.5.5-2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:6.5.5-1.3
- drop repotag
- fix license tag

* Sun Mar 11 2007 Vivek Lakshmanan <vivekl@redhat.com> - 0:6.5.5-1jpp.2.fc7
- First build for Fedora
- Resolves: #227114 (Missing BR on ant - Thanks mcepl)

* Wed Feb 14 2007 Deepak Bhole <dbhole@redhat.com> - 0:6.5.5-1jpp.1
- Update to 6.5.5
- Fix per Fedora guidelines

* Tue May 02 2006 Ralph Apel <r.apel@r-apel.de> - 0:6.5.3-4jpp
- First JPP-1.7 release

* Fri Sep 03 2004 Fernando Nasser <fnasser@redhat.com> - 0:6.5.3-3jpp
- Rebuilt with Ant 1.6.2

* Mon Jul 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.3-2jpp
- Apply two patches for known limitations from
  http://saxon.sourceforge.net/saxon6.5.3/limitations.html
- Make the command line script use xml-commons-resolver if it's available.
- Include man page for command line script.
- Add patch to fix command line option handling and document missing options.
- New style versionless javadoc dir symlinking.
- Crosslink with local J2SE javadocs.
- Add missing jdom-javadoc build dependency.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.3-1jpp
- Update to 6.5.3.
- Crosslink with local xml-commons-apis and fop javadocs.

* Tue Jun  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:6.5.2-7jpp
- Non-versioned javadoc symlinking.
- Include Main-Class attribute in saxon.jar.
- Own (ghost) %%{_javadir}/jaxp_transform_impl.jar.
- Remove alternatives in preun instead of postun.

* Thu Apr 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 6.5.2-6jpp
- Rebuild for JPackage 1.5.
- Split shell script to -scripts subpackage.
- Use non-versioned jar in jaxp_transform_impl alternative, and don't remove
  it on upgrade.
- Spec file cleanups.

* Thu Jul 25 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-5jpp
- Fix shell script (again).
- Rebuild with -Dbuild.compiler=modern (saxon-fop won't build with jikes).

* Fri Jul 19 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-4jpp
- First public JPackage release.
- Compile with build.xml by yours truly.
- AElfred no more provides jaxp_parser_impl; it's SAX only, no DOM.
- Fix shell script.

* Mon Jul  1 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-3jpp
- Provides jaxp_parser_impl.
- Requires xml-commons-apis.

* Sun Jun 30 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-2jpp
- Use sed instead of bash 2 extension when symlinking jars.
- Provides jaxp_transform_impl.

* Sat May 11 2002 Ville Skyttä <ville.skytta at iki.fi> 6.5.2-1jpp
- First JPackage release.
- Provides jaxp_parser2 though there's no DOM implementation in this AElfred.
