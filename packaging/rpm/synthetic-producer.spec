Name:     synthetic-producer
Version:  %{__version}
Release:  %{__release}%{?dist}

License:  GNU AGPLv3
URL:  https://github.com/redBorder/synthetic-producer
Source0: %{name}-%{version}.tar.gz

BuildRequires: maven java-devel

%global debug_package %{nil}

Summary: synthetic-producer module
Requires: java

%description
%{summary}

%prep
%setup -qn %{name}-%{version}

%build
export MAVEN_OPTS="-Xmx512m -Xms256m -Xss10m -XX:MaxPermSize=512m" && mvn clean package

%install
mkdir -p %{buildroot}/usr/share/%{name}
mkdir -p %{buildroot}/etc/%{name}/config
install -D -m 644 target/%{name}-*-selfcontained.jar %{buildroot}/usr/share/%{name}/%{name}.jar
install -D -m 644 yamls/*.yml %{buildroot}/etc/%{name}/config

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d / -s /sbin/nologin \
    -c "User of %{name} service" %{name}
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root)
/usr/share/%{name}
%defattr(644,root,root)
/usr/share/%{name}/%{name}.jar
/etc/%{name}/config/rb_flow.yml
/etc/%{name}/config/rb_state.yml
/etc/%{name}/config/rb_event.yml

%changelog
* Mon Jul 15 2024 Luis Blanco <ljblanco@redborder.com> - 1.5.0-1
- add all yamls in directory to include rb_event 
* Wed Oct 4 2023 David Vanhoucke <dvanhoucke@redborder.com> - 1.5.0-1
- sped update
* Wed Jan 26 2022 Eduardo Reyes <eareyes@redborder.com> - 0.0.1
- first spec version
