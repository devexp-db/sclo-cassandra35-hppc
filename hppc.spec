%{?scl:%scl_package hppc}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}hppc
Version:	0.7.1
Release:	4%{?dist}
Summary:	High Performance Primitive Collections for Java
License:	ASL 2.0
URL:		http://labs.carrotsearch.com/%{pkg_name}.html
Source0:	https://github.com/carrotsearch/%{pkg_name}/archive/%{version}.tar.gz

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-plugin
BuildRequires:	%{?scl_prefix_maven}sonatype-oss-parent
BuildRequires:	%{?scl_prefix}guava >= 18.0
BuildRequires:	%{?scl_prefix}antlr3-java
BuildRequires:	%{?scl_prefix}stringtemplate
BuildRequires:	%{?scl_prefix}stringtemplate4
BuildRequires:	%{?scl_prefix}treelayout
BuildRequires:	%{?scl_prefix}antlr4
BuildRequires:	%{?scl_prefix}antlr4-runtime
BuildRequires:	%{?scl_prefix}antlr4-maven-plugin
%{?scl:Requires: %scl_runtime}

%if 0
# hppc-benchmarks deps
BuildRequires: mvn(it.unimi.dsi:fastutil)
BuildRequires: mvn(net.openhft:koloboke-impl-jdk6-7:0.6.6)
BuildRequires: mvn(org.openjdk.jmh:jmh-core)
BuildRequires: mvn(org.openjdk.jmh:jmh-generator-annprocess)

# test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(com.carrotsearch.randomizedtesting:junit4-maven-plugin)
BuildRequires: mvn(com.carrotsearch.randomizedtesting:randomizedtesting-runner)
BuildRequires: mvn(org.assertj:assertj-core)
%endif

BuildArch:	noarch

%description
Fundamental data structures (maps, sets, lists, stacks, queues) generated for
combinations of object and primitive types to conserve JVM memory and speed
up execution.

%package templateprocessor
Summary:	HPPC Template Processor

%description templateprocessor
Template Processor and Code Generation for HPPC.

%package javadoc
Summary:	Javadoc for HPPC

%description javadoc
This package contains javadoc for HPPC.

%prep
%setup -qn %{pkg_name}-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Unavailable deps
%pom_disable_module %{pkg_name}-benchmarks
%pom_remove_plugin :junit4-maven-plugin
%pom_remove_plugin -r :forbiddenapis
%pom_remove_plugin :junit4-maven-plugin hppc
# Unneeded task
%pom_remove_plugin -r :maven-assembly-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
# helpmojo extraction fails in RHEL, fix based on:
# http://maven.apache.org/plugin-tools/maven-plugin-plugin/examples/using-annotations.html#POM_configuration
%{?scl:%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[2]/pom:configuration" "
    <skipErrorNoDescriptorsFound>true</skipErrorNoDescriptorsFound>" %{pkg_name}-template-processor/pom.xml}

# Convert from dos to unix line ending
for file in CHANGES.txt; do
  sed -i.orig 's|\r||g' $file
  touch -r $file.orig $file
  rm $file.orig
done

%mvn_file :%{pkg_name} %{pkg_name}
%mvn_package :%{pkg_name}::esoteric:
%mvn_file :%{pkg_name}-template-processor %{pkg_name}-templateprocessor
%mvn_package :%{pkg_name}-template-processor %{pkg_name}-templateprocessor
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Disable test for now. Unavailable test deps
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc CHANGES.txt README.txt
%license LICENSE.txt NOTICE.txt

%files templateprocessor -f .mfiles-%{pkg_name}-templateprocessor
%license LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt NOTICE.txt

%changelog
* Wed Dec 14 2016 Tomas Repik <trepik@redhat.com> - 0.7.1-4
- scl conversion

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 gil cattaneo <puntogil@libero.it> 0.7.1-2
- install "esoteric" artifact

* Wed Jan 20 2016 Alexander Kurtakov <akurtako@redhat.com> 0.7.1-1
- Update to upstream 0.7.1 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 05 2015 gil cattaneo <puntogil@libero.it> 0.6.1-2
- introduce license macro

* Wed Dec 17 2014 gil cattaneo <puntogil@libero.it> 0.6.1-1
- update to 0.6.1

* Tue Jun 17 2014 gil cattaneo <puntogil@libero.it> 0.5.3-4
- fix BR list

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 29 2013 gil cattaneo <puntogil@libero.it> 0.5.3-2
- add templateprocessor sub-package

* Thu Dec 05 2013 gil cattaneo <puntogil@libero.it> 0.5.3-1
- 0.5.3

* Sun Aug 25 2013 gil cattaneo <puntogil@libero.it> 0.5.2-1
- initial rpm
