%global real_name httpd
%global ius_suffix 24u
%global apr apr15u
%global apu apu15u
%global aprver 1
%define apuver 1

%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define suexec_caller apache
%define mmn 20120211
%define oldmmnisa %{mmn}-%{__isa_name}-%{__isa_bits}
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}

%if 0%{?fedora}
%define vstring %(source /etc/os-release; echo ${REDHAT_SUPPORT_PRODUCT})
%else
%if 0%{?centos}
%define vstring CentOS
%else
%define vstring Red Hat
%endif # centos
%endif # fedora

%if 0%{?rhel} >= 7
%global with_systemd 1
%global _macrosdir %{_rpmconfigdir}/macros.d
%global _rundir /run
%global suexec_uidmin 1000
%global suexec_gidmin 1000
%else
%global with_systemd 0
%global _macrosdir %{_sysconfdir}/rpm
%global _rundir %{_localstatedir}/run
%global suexec_uidmin 500
%global suexec_gidmin 100
%endif

# Drop automatic provides for module DSOs
%{?filter_setup:
%filter_provides_in %{_libdir}/httpd/modules/.*\.so$
%filter_setup
}

Summary: Apache HTTP Server
Name: %{real_name}%{ius_suffix}
Version: 2.4.12
Release: 2.ius%{?dist}
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source2: httpd.logrotate
Source3: httpd.sysconf
Source4: httpd-ssl-pass-dialog
Source5: httpd.tmpfiles
Source6: httpd.service
Source7: action-graceful.sh
Source8: action-configtest.sh
Source9: httpd.init
Source10: httpd.conf
Source11: 00-base.conf
Source12: 00-mpm.conf
Source13: 00-lua.conf
Source14: 01-cgi.conf
Source15: 00-dav.conf
Source16: 00-proxy.conf
Source17: 00-ssl.conf
Source18: 01-ldap.conf
Source19: 00-proxyhtml.conf
Source20: userdir.conf
Source21: ssl.conf
Source22: welcome.conf
Source23: manual.conf
Source24: 00-systemd.conf
Source25: 01-session.conf
Source26: 10-listen443.conf
Source27: httpd.socket
Source28: 00-optional.conf
# Documentation
Source30: README.confd
Source31: README.confmod
Source40: htcacheclean.service
Source41: htcacheclean.sysconf
Source42: htcacheclean.init
# build/scripts patches
Patch1: httpd-2.4.1-apctl.patch
Patch2: httpd-2.4.9-apxs.patch
Patch3: httpd-2.4.1-deplibs.patch
Patch6: httpd-2.4.3-apctl-systemd.patch
Patch7: httpd-2.4.3-layout.patch
Patch8: httpd-2.4.3-layout-legacy.patch
# Needed for socket activation and mod_systemd patch
Patch19: httpd-2.4.10-detect-systemd.patch
# Features/functional changes
Patch23: httpd-2.4.4-export.patch
Patch24: httpd-2.4.1-corelimit.patch
Patch25: httpd-2.4.1-selinux.patch
Patch26: httpd-2.4.4-r1337344+.patch
Patch27: httpd-2.4.2-icons.patch
Patch29: httpd-2.4.10-mod_systemd.patch
Patch30: httpd-2.4.4-cachehardmax.patch
Patch31: httpd-2.4.6-sslmultiproxy.patch
Patch34: httpd-2.4.9-socket-activation.patch
# Bug fixes
Patch55: httpd-2.4.4-malformed-host.patch
Patch56: httpd-2.4.4-mod_unique_id.patch
Patch57: httpd-2.4.10-sigint.patch
# Security fixes

License: ASL 2.0
Group: System Environment/Daemons
BuildRequires: autoconf, perl, pkgconfig, findutils, xmlto
BuildRequires: zlib-devel, libselinux-devel, lua-devel
BuildRequires: %{apr}-devel >= 1.5.0, %{apr}-util-devel >= 1.5.0, pcre-devel >= 5.0
%if 0%{?with_systemd}
BuildRequires: systemd-devel
%endif
Requires: /etc/mime.types, system-logos >= 7.92.1-1
Obsoletes: httpd-suexec
Provides: webserver
Provides: mod_dav = %{version}-%{release}, httpd-suexec = %{version}-%{release}
Provides: httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}, httpd-mmn = %{oldmmnisa}
Requires: httpd-tools = %{version}-%{release}
Requires: httpd-filesystem = %{version}-%{release}
Requires(pre): httpd-filesystem = %{version}-%{release}
%if 0%{?with_systemd}
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
%else
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

# IUS-isms
Provides: %{real_name} = %{version}-%{release}
Provides: %{real_name}%{?_isa} = %{version}-%{release}
# not sure on this one, it is provided by the stock el6 package but not the
# el7 or fedora ones
#Provides: config(%{real_name}) = %{version}-%{release}
Conflicts: %{real_name} < %{version}


%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.


%package devel
Group: Development/Libraries
Summary: Development interfaces for the Apache HTTP server
Obsoletes: secureweb-devel, apache-devel, stronghold-apache-devel
Requires: %{apr}-devel >= 1.5.0, %{apr}-util-devel >= 1.5.0, pkgconfig
Requires: httpd = %{version}-%{release}
# IUS-isms
Provides: %{real_name}-devel = %{version}-%{release}
Provides: %{real_name}-devel%{?_isa} = %{version}-%{release}
Conflicts: %{real_name}-devel < %{version}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.


%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server
Requires: httpd = %{version}-%{release}
Obsoletes: secureweb-manual, apache-manual
BuildArch: noarch
# IUS-isms
Provides: %{real_name}-manual = %{version}-%{release}
Provides: %{real_name}-manual%{?_isa} = %{version}-%{release}
Conflicts: %{real_name}-manual < %{version}

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.2/.


%package filesystem
Group: System Environment/Daemons
Summary: The basic directory layout for the Apache HTTP server
BuildArch: noarch
Requires(pre): /usr/sbin/useradd
# IUS-isms
Provides: %{real_name}-filesystem = %{version}-%{release}
Provides: %{real_name}-filesystem%{?_isa} = %{version}-%{release}
Conflicts: %{real_name}-filesystem < %{version}

%description filesystem
The httpd-filesystem package contains the basic directory layout
for the Apache HTTP server including the correct permissions
for the directories.


%package tools
Group: System Environment/Daemons
Summary: Tools for use with the Apache HTTP Server
# IUS-isms
Provides: %{real_name}-tools = %{version}-%{release}
Provides: %{real_name}-tools%{?_isa} = %{version}-%{release}
Conflicts: %{real_name}-tools < %{version}

%description tools
The httpd-tools package contains tools which can be used with 
the Apache HTTP Server.


%package -n mod%{ius_suffix}_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(post): openssl >= 0.9.7f-4, /bin/cat, /bin/hostname
Requires(pre): httpd-filesystem
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Obsoletes: stronghold-mod_ssl
# IUS-isms
Provides: mod_ssl = %{version}-%{release}
Provides: mod_ssl%{?_isa} = %{version}-%{release}
Conflicts: mod_ssl < %{version}

%description -n mod%{ius_suffix}_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.


%package -n mod%{ius_suffix}_proxy_html
Group: System Environment/Daemons
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
Epoch: 1
# IUS-isms
Provides: mod_proxy_html = %{version}-%{release}
Provides: mod_proxy_html%{?_isa} = %{version}-%{release}
Conflicts: mod_proxy_html < %{version}

%description -n mod%{ius_suffix}_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.


%package -n mod%{ius_suffix}_ldap
Group: System Environment/Daemons
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: %{apr}-util-ldap >= 1.5.0
# IUS-isms
Provides: mod_ldap = %{version}-%{release}
Provides: mod_ldap%{?_isa} = %{version}-%{release}
Conflicts: mod_ldap < %{version}

%description -n mod%{ius_suffix}_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.


%package -n mod%{ius_suffix}_session
Group: System Environment/Daemons
Summary: Session interface for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
# IUS-isms
Provides: mod_session = %{version}-%{release}
Provides: mod_session%{?_isa} = %{version}-%{release}
Conflicts: mod_session < %{version}

%description -n mod%{ius_suffix}_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.


%prep
%setup -q -n %{real_name}-%{version}
%patch1 -p1 -b .apctl
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs
%patch6 -p1 -b .apctlsystemd

%if 0%{?rhel} >= 7
%patch7 -p1 -b .layout
%else
%patch8 -p1 -b .layout
%endif

%if 0%{?with_systemd}
%patch19 -p1 -b .detectsystemd
%endif

%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .r1337344+
%patch27 -p1 -b .icons
%if 0%{?with_systemd}
%patch29 -p1 -b .systemd
%endif
%patch30 -p1 -b .cachehardmax
%patch31 -p1 -b .sslmultiproxy
%if 0%{?with_systemd}
%patch34 -p1 -b .socketactivation
%endif

%patch55 -p1 -b .malformedhost
%patch56 -p1 -b .uniqueid
%patch57 -p1 -b .sigint

# Patch in the vendor string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

: Building with MMN %{mmn}, MMN-ISA %{mmnisa} and vendor string '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
	support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

# Build the daemon
./configure \
 	--prefix=%{_sysconfdir}/httpd \
 	--exec-prefix=%{_prefix} \
 	--bindir=%{_bindir} \
 	--sbindir=%{_sbindir} \
 	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--sysconfdir=%{_sysconfdir}/httpd/conf \
	--includedir=%{_includedir}/httpd \
	--libexecdir=%{_libdir}/httpd/modules \
	--datadir=%{contentdir} \
        --enable-layout=Fedora \
        --with-installbuilddir=%{_libdir}/httpd/build \
        --enable-mpms-shared=all \
        --with-apr=%{_bindir}/%{apr}-%{aprver}-config \
        --with-apr-util=%{_bindir}/%{apu}-%{apuver}-config \
	--enable-suexec --with-suexec \
        --enable-suexec-capabilities \
	--with-suexec-caller=%{suexec_caller} \
	--with-suexec-docroot=%{docroot} \
	--without-suexec-logfile \
	--with-suexec-syslog \
	--with-suexec-bin=%{_sbindir}/suexec \
	--with-suexec-uidmin=%{suexec_uidmin} --with-suexec-gidmin=%{suexec_gidmin} \
        --enable-pie \
        --with-pcre \
        --enable-mods-shared=all \
	--enable-ssl --with-ssl --disable-distcache \
	--enable-proxy \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi \
        --enable-authn-anon --enable-authn-alias \
        --disable-imagemap  \
	$*
make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install

%if 0%{?with_systemd}
# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
for s in httpd.service htcacheclean.service httpd.socket; do
  install -p -m 644 $RPM_SOURCE_DIR/${s} \
                    $RPM_BUILD_ROOT%{_unitdir}/${s}
done
%else
# install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 $RPM_SOURCE_DIR/httpd.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/httpd
install -m755 $RPM_SOURCE_DIR/htcacheclean.init \
	$RPM_BUILD_ROOT/etc/rc.d/init.d/htcacheclean
%endif

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d \
      $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
install -m 644 $RPM_SOURCE_DIR/README.confmod \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/README
for f in 00-base.conf 00-mpm.conf 00-lua.conf 01-cgi.conf 00-dav.conf \
         00-proxy.conf 00-ssl.conf 01-ldap.conf 00-proxyhtml.conf \
         01-ldap.conf 01-session.conf 00-optional.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

%if 0%{?with_systemd}
for f in 00-systemd.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

# install systemd override drop directory
# Web application packages can drop snippets into this location if
# they need ExecStart[pre|post].
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d

install -m 644 -p $RPM_SOURCE_DIR/10-listen443.conf \
      $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d/10-listen443.conf
%endif

for f in welcome.conf ssl.conf manual.conf userdir.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

%if 0%{?rhel} < 7
# el6 should use /var/run, not /run
sed -i '/^SSLSessionCache/s,/run,%{_rundir},' \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/ssl.conf
%endif

# Split-out extra config shipped as default in conf.d:
for f in autoindex; do
  mv docs/conf/extra/httpd-${f}.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/${f}.conf
done

# Extra config trimmed:
rm -v docs/conf/extra/httpd-{ssl,userdir}.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
for s in httpd htcacheclean; do
  install -m 644 -p $RPM_SOURCE_DIR/${s}.sysconf \
                    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/${s}
done

%if 0%{?with_systemd}
# tmpfiles.d configuration
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d 
install -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
   $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd.conf
%endif

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/dav \
         $RPM_BUILD_ROOT/%{_rundir}/httpd/htcacheclean

# Substitute in defaults which are usually done (badly) by "make install"
sed -i \
   "s,@@ServerRoot@@/var,%{_localstatedir}/lib/dav,;
    s,@@ServerRoot@@/user.passwd,/etc/httpd/conf/user.passwd,;
    s,@@ServerRoot@@/docs,%{docroot},;
    s,@@ServerRoot@@,%{docroot},;
    s,@@Port@@,80,;" \
    docs/conf/extra/*.conf

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/ssl

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn
mkdir -p $RPM_BUILD_ROOT/%{_macrosdir}
cat > $RPM_BUILD_ROOT/%{_macrosdir}/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_bindir}/apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
EOF

# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex
install -m 644 -p docs/docroot/index.html \
        $RPM_BUILD_ROOT%{contentdir}/noindex/index.html
rm -rf %{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s ../../pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s %{_rundir}/httpd $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# install http-ssl-pass-dialog
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m755 $RPM_SOURCE_DIR/httpd-ssl-pass-dialog \
	$RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-pass-dialog

%if 0%{?with_systemd}
# Install action scripts
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd
for f in graceful configtest; do
    install -p -m 755 $RPM_SOURCE_DIR/action-${f}.sh \
            $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/${f}
done
%endif

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
	$RPM_BUILD_ROOT/etc/logrotate.d/httpd

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/%{_rundir}/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}


%pre
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
    -s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%pre filesystem
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
	-s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%post
%if 0%{?with_systemd}
%systemd_post httpd.service htcacheclean.service httpd.socket
%else
/sbin/chkconfig --add httpd
/sbin/chkconfig --add htcacheclean
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun httpd.service htcacheclean.service httpd.socket
%else
if [ $1 = 0 ]; then
	/sbin/service httpd stop > /dev/null 2>&1
	/sbin/chkconfig --del httpd
	/sbin/service htcacheclean stop > /dev/null 2>&1
	/sbin/chkconfig --del htcacheclean
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun
%endif

%posttrans
test -f /etc/sysconfig/httpd-disable-posttrans || \
%if 0%{?with_systemd}
  /bin/systemctl try-restart httpd.service htcacheclean.service >/dev/null 2>&1 || :
%else
  /sbin/service httpd condrestart >/dev/null 2>&1 || :
  /sbin/service htcacheclean condrestart >/dev/null 2>&1 || :
%endif

%define sslcert %{_sysconfdir}/pki/tls/certs/localhost.crt
%define sslkey %{_sysconfdir}/pki/tls/private/localhost.key

%post -n mod%{ius_suffix}_ssl
umask 077

if [ -f %{sslkey} -o -f %{sslcert} ]; then
   exit 0
fi

%{_bindir}/openssl genrsa -rand /proc/apm:/proc/cpuinfo:/proc/dma:/proc/filesystems:/proc/interrupts:/proc/ioports:/proc/pci:/proc/rtc:/proc/uptime 2048 > %{sslkey} 2> /dev/null

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
   FQDN=localhost.localdomain
fi

cat << EOF | %{_bindir}/openssl req -new -key %{sslkey} \
         -x509 -sha256 -days 365 -set_serial $RANDOM -extensions v3_req \
         -out %{sslcert} 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF

%check
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   : modules contain non-relocatable code
   exit 1
fi


%files
%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf

%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.d/ssl.conf
%exclude %{_sysconfdir}/httpd/conf.d/manual.conf

%dir %{_sysconfdir}/httpd/conf.modules.d
%{_sysconfdir}/httpd/conf.modules.d/README
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%config(noreplace) %{_sysconfdir}/sysconfig/ht*
%if 0%{?with_systemd}
%{_prefix}/lib/tmpfiles.d/httpd.conf
%dir %{_libexecdir}/initscripts/legacy-actions/httpd
%{_libexecdir}/initscripts/legacy-actions/httpd/*
%endif

%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%if 0%{?rhel} >= 7
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec
%else
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec
%endif

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%exclude %{_libdir}/httpd/modules/mod_session*.so

%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html

%attr(0710,root,apache) %dir %{_rundir}/httpd
%attr(0700,apache,apache) %dir %{_rundir}/httpd/htcacheclean
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/dav
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy

%{_mandir}/man8/*

%if 0%{?with_systemd}
%{_unitdir}/*.service
%{_unitdir}/*.socket
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%attr(755,root,root) %dir %{_unitdir}/httpd.socket.d
%else
# sysvinit
%{_sysconfdir}/rc.d/init.d/httpd
%{_sysconfdir}/rc.d/init.d/htcacheclean
%endif

%files filesystem
%dir %{_sysconfdir}/httpd
%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README
%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html
%dir %{contentdir}
%dir %{contentdir}/icons

%files tools
%{_bindir}/*
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files manual
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n mod%{ius_suffix}_ssl
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_libexecdir}/httpd-ssl-pass-dialog
%if 0%{?with_systemd}
%{_unitdir}/httpd.socket.d/10-listen443.conf
%endif

%files -n mod%{ius_suffix}_proxy_html
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n mod%{ius_suffix}_ldap
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n mod%{ius_suffix}_session
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files devel
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_macrosdir}/macros.httpd


%changelog
* Tue Feb 03 2015 Carl George <carl.george@rackspace.com> - 2.4.12-2.ius
- Use upstream noindex page instead of custom welcome page

* Wed Jan 28 2015 Carl George <carl.george@rackspace.com> - 2.4.12-1.ius
- Latest upstream
- Patch100 fixed upstream (CVE-2013-5704)
- Patch101 fixed upstream (CVE-2014-3581)
- Patch102 fixed upstream (CVE-2014-3583)
- Patch103 fixed upstream (CVE-2014-8109)

* Wed Jan 21 2015 Carl George <carl.george@rackspace.com> - 2.4.10-3.ius
- MPM is now a loadable module, make HTTPD static in init script
- Update comments in sysconf file for variables that are still valid

* Thu Jan 08 2015 Carl George <carl.george@rackspace.com> - 2.4.10-2.ius
- Require hostname command, not hostname package
- Don't install 00-systemd.conf on sysvinit systems
- Use /var/run on el6, /run on el7
- Explictly require the IUS versions of apr and apr-devel

* Fri Jan 02 2015 Carl George <carl.george@rackspace.com> - 2.4.10-1.ius
- Port from Fedora to IUS

* Wed Dec 17 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-15
- core: fix bypassing of mod_headers rules via chunked requests (CVE-2013-5704)
- mod_cache: fix NULL pointer dereference on empty Content-Type (CVE-2014-3581)
- mod_proxy_fcgi: fix a potential crash with long headers (CVE-2014-3583)
- mod_lua: fix handling of the Require line when a LuaAuthzProvider is used
  in multiple Require directives with different arguments (CVE-2014-8109)

* Tue Oct 14 2014 Joe Orton <jorton@redhat.com> - 2.4.10-14
- require apr-util 1.5.x

* Thu Sep 18 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-13
- use NoDelay and DeferAcceptSec in httpd.socket

* Mon Sep 08 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-12
- increase suexec minimum acceptable uid/gid to 1000 (#1136391)

* Wed Sep 03 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-11
- fix hostname requirement and conflict with openssl-libs

* Mon Sep 01 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-10
- use KillMode=mixed in httpd.service (#1135122)

* Fri Aug 29 2014 Joe Orton <jorton@redhat.com> - 2.4.10-9
- set vstring based on /etc/os-release (Pat Riehecky, #1114539)

* Fri Aug 29 2014 Joe Orton <jorton@redhat.com> - 2.4.10-8
- pull in httpd-filesystem as Requires(pre) (#1128328)
- fix cipher selection in default ssl.conf, depend on new OpenSSL (#1134348)
- require hostname for mod_ssl post script (#1135118)

* Fri Aug 22 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-7
- mod_systemd: updated to the latest version
- use -lsystemd instead of -lsystemd-daemon (#1125084)
- fix possible crash in SIGINT handling (#958934)

* Thu Aug 21 2014 Joe Orton <jorton@redhat.com> - 2.4.10-6
- mod_ssl: treat "SSLCipherSuite PROFILE=..." as special (#1109119)
- switch default ssl.conf to use PROFILE=SYSTEM (#1109119)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-4
- add /usr/bin/useradd dependency to -filesystem requires

* Thu Aug 14 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-3
- fix creating apache user in pre script (#1128328)

* Thu Jul 31 2014 Joe Orton <jorton@redhat.com> - 2.4.10-2
- enable mod_request by default for mod_auth_form
- move disabled-by-default modules from 00-base.conf to 00-optional.conf

* Mon Jul 21 2014 Joe Orton <jorton@redhat.com> - 2.4.10-1
- update to 2.4.10
- expand variables in docdir example configs

* Tue Jul 08 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-8
- add support for systemd socket activation (#1111648)

* Mon Jul 07 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-7
- remove conf.modules.d from httpd-filesystem subpackage (#1081453)

* Mon Jul 07 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-6
- add httpd-filesystem subpackage (#1081453)

* Fri Jun 20 2014 Joe Orton <jorton@redhat.com> - 2.4.9-5
- mod_ssl: don't use the default OpenSSL cipher suite in ssl.conf (#1109119)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-3
- add support for SetHandler + proxy (#1078970)

* Thu Mar 27 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-2
- move macros from /etc/rpm to macros.d (#1074277)
- remove unused patches

* Mon Mar 17 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-1
- update to 2.4.9

* Fri Feb 28 2014 Joe Orton <jorton@redhat.com> - 2.4.7-6
- use 2048-bit RSA key with SHA-256 signature in dummy certificate

* Fri Feb 28 2014 Stephen Gallagher <sgallagh@redhat.com> 2.4.7-5
- Create drop directory for systemd snippets

* Thu Feb 27 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.7-4
- remove provides of old MMN, because it contained double-dash (#1068851)

* Thu Feb 20 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.7-3
- fix graceful restart using legacy actions

* Thu Dec 12 2013 Joe Orton <jorton@redhat.com> - 2.4.7-2
- conflict with pre-1.5.0 APR
- fix sslsninotreq patch

* Wed Nov 27 2013 Joe Orton <jorton@redhat.com> - 2.4.7-1
- update to 2.4.7 (#1034071)

* Fri Nov 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-10
- switch to requiring system-logos-httpd (#1031288)

* Tue Nov 12 2013 Joe Orton <jorton@redhat.com> - 2.4.6-9
- change mmnisa to drop "-" altogether

* Tue Nov 12 2013 Joe Orton <jorton@redhat.com> - 2.4.6-8
- drop ambiguous invalid "-" in RHS of httpd-mmn Provide, keeping old Provide
  for transition

* Fri Nov  1 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-7
- systemd: use {MAINPID} notation to ensure /bin/kill has always the second arg

* Thu Oct 31 2013 Joe Orton <jorton@redhat.com> - 2.4.6-6
- mod_ssl: allow SSLEngine to override Listen-based default (r1537535)

* Thu Oct 24 2013 Jan kaluza <jkaluza@redhat.com> - 2.4.6-5
- systemd: send SIGWINCH signal without httpd -k in ExecStop

* Mon Oct 21 2013 Joe Orton <jorton@redhat.com> - 2.4.6-4
- load mod_macro by default (#998452)
- add README to conf.modules.d
- mod_proxy_http: add possible fix for threading issues (r1534321)
- core: add fix for truncated output with CGI scripts (r1530793)

* Thu Oct 10 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-3
- require fedora-logos-httpd (#1009162)

* Wed Jul 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-2
- revert fix for dumping vhosts twice

* Mon Jul 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-1
- update to 2.4.6
- mod_ssl: use revised NPN API (r1487772)

* Thu Jul 11 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-12
- mod_unique_id: replace use of hostname + pid with PRNG output (#976666)
- apxs: mention -p option in manpage

* Tue Jul  2 2013 Joe Orton <jorton@redhat.com> - 2.4.4-11
- add patch for aarch64 (Dennis Gilmore, #925558)

* Mon Jul  1 2013 Joe Orton <jorton@redhat.com> - 2.4.4-10
- remove duplicate apxs man page from httpd-tools

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.4.4-9
- remove zombie dbmmanage script

* Fri May 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-8
- return 400 Bad Request on malformed Host header

* Fri May 24 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-7
- ignore /etc/sysconfig/httpd and document systemd way of setting env variables
  in this file

* Mon May 20 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- htpasswd/htdbm: fix hash generation bug (#956344)
- do not dump vhosts twice in httpd -S output (#928761)
- mod_cache: fix potential crash caused by uninitialized variable (#954109)

* Thu Apr 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-5
- execute systemctl reload as result of apachectl graceful
- mod_ssl: ignore SNI hints unless required by config
- mod_cache: forward-port CacheMaxExpire "hard" option
- mod_ssl: fall back on another module's proxy hook if mod_ssl proxy
  is not configured.

* Tue Apr 16 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-4
- fix service file to not send SIGTERM after ExecStop (#906321, #912288)

* Tue Mar 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-3
- protect MIMEMagicFile with IfModule (#893949)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-2
- really package mod_auth_form in mod_session (#915438)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-1
- update to 2.4.4
- fix duplicate ownership of mod_session config (#914901)

* Fri Feb 22 2013 Joe Orton <jorton@redhat.com> - 2.4.3-17
- add mod_session subpackage, move mod_auth_form there (#894500)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 2.4.3-15
- add systemd service for htcacheclean

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-14
- drop patch for r1344712

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-13
- filter mod_*.so auto-provides (thanks to rcollet)
- pull in syslog logging fix from upstream (r1344712)

* Fri Oct 26 2012 Joe Orton <jorton@redhat.com> - 2.4.3-12
- rebuild to pick up new apr-util-ldap

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 2.4.3-11
- rebuild

* Wed Oct  3 2012 Joe Orton <jorton@redhat.com> - 2.4.3-10
- pull upstream patch r1392850 in addition to r1387633

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9
- define PLATFORM in os.h using vendor string

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-8
- use systemd script unconditionally (#850149)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-7
- use systemd scriptlets if available (#850149)
- don't run posttrans restart if /etc/sysconfig/httpd-disable-posttrans exists

* Mon Oct 01 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-6
- use systemctl from apachectl (#842736)

* Wed Sep 19 2012 Joe Orton <jorton@redhat.com> - 2.4.3-5
- fix some error log spam with graceful-stop (r1387633)
- minor mod_systemd tweaks

* Thu Sep 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-4
- use IncludeOptional for conf.d/*.conf inclusion

* Fri Sep 07 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-3
- adding mod_systemd to integrate with systemd better

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-2
- mod_ssl: add check for proxy keypair match (upstream r1374214)

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-1
- update to 2.4.3 (#849883)
- own the docroot (#848121)

* Mon Aug  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-23
- add mod_proxy fixes from upstream (r1366693, r1365604)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-21
- drop explicit version requirement on initscripts

* Thu Jul  5 2012 Joe Orton <jorton@redhat.com> - 2.4.2-20
- mod_ext_filter: fix error_log warnings

* Mon Jul  2 2012 Joe Orton <jorton@redhat.com> - 2.4.2-19
- support "configtest" and "graceful" as initscripts "legacy actions"

* Fri Jun  8 2012 Joe Orton <jorton@redhat.com> - 2.4.2-18
- avoid use of "core" GIF for a "core" directory (#168776)
- drop use of "syslog.target" in systemd unit file

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-17
- use _unitdir for systemd unit file
- use /run in unit file, ssl.conf

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-16
- mod_ssl: fix NPN patch merge

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-15
- move tmpfiles.d fragment into /usr/lib per new guidelines
- package /run/httpd not /var/run/httpd
- set runtimedir to /run/httpd likewise

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-14
- fix htdbm/htpasswd crash on crypt() failure (#818684)

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-13
- pull fix for NPN patch from upstream (r1345599)

* Thu May 31 2012 Joe Orton <jorton@redhat.com> - 2.4.2-12
- update suexec patch to use LOG_AUTHPRIV facility

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-11
- really fix autoindex.conf (thanks to remi@)

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-10
- fix autoindex.conf to allow symlink to poweredby.png

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-9
- suexec: use upstream version of patch for capability bit support

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-8
- suexec: use syslog rather than suexec.log, drop dac_override capability

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-7
- mod_ssl: add TLS NPN support (r1332643, #809599)

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-6
- add BR on APR >= 1.4.0

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-5
- use systemctl from logrotate (#221073)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-4
- pull from upstream:
  * use TLS close_notify alert for dummy_connection (r1326980+)
  * cleanup symbol exports (r1327036+)

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3
- really fix restart

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-2
- tweak default ssl.conf
- fix restart handling (#814645)
- use graceful restart by default

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.2-1
- update to 2.4.2

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-6
- fix macros

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-5
- add _httpd_moddir to macros

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-4
- fix symlink for poweredby.png
- fix manual.conf

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-3
- add mod_proxy_html subpackage (w/mod_proxy_html + mod_xml2enc)
- move mod_ldap, mod_authnz_ldap to mod_ldap subpackage

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-2
- clean docroot better
- ship proxy, ssl directories within /var/cache/httpd
- default config:
 * unrestricted access to (only) /var/www
 * remove (commented) Mutex, MaxRanges, ScriptSock
 * split autoindex config to conf.d/autoindex.conf
- ship additional example configs in docdir

* Tue Mar  6 2012 Joe Orton <jorton@redhat.com> - 2.4.1-1
- update to 2.4.1
- adopt upstream default httpd.conf (almost verbatim)
- split all LoadModules to conf.modules.d/*.conf
- include conf.d/*.conf at end of httpd.conf
- trim %%changelog

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-2
- fix build against PCRE 8.30

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 2.2.22-1
- update to 2.2.22

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.2.21-8
- Rebuild against PCRE 8.30

* Mon Jan 23 2012 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-7
- fix #783629 - start httpd after named

* Mon Jan 16 2012 Joe Orton <jorton@redhat.com> - 2.2.21-6
- complete conversion to systemd, drop init script (#770311)
- fix comments in /etc/sysconfig/httpd (#771024)
- enable PrivateTmp in service file (#781440)
- set LANG=C in /etc/sysconfig/httpd

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-4
- fix #751591 - start httpd after remote-fs

* Mon Oct 24 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.21-3
- allow change state of BalancerMember in mod_proxy_balancer web interface

* Thu Sep 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.2.21-2
- Make mmn available as %%{_httpd_mmn}.
- Add .svgz to AddEncoding x-gzip example in httpd.conf.

* Tue Sep 13 2011 Joe Orton <jorton@redhat.com> - 2.2.21-1
- update to 2.2.21

* Mon Sep  5 2011 Joe Orton <jorton@redhat.com> - 2.2.20-1
- update to 2.2.20
- fix MPM stub man page generation

* Wed Aug 10 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-5
- fix #707917 - add httpd-ssl-pass-dialog to ask for SSL password using systemd

* Fri Jul 22 2011 Iain Arnell <iarnell@gmail.com> 1:2.2.19-4
- rebuild while rpm-4.9.1 is untagged to remove trailing slash in provided
  directory names

* Wed Jul 20 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-3
- fix #716621 - suexec now works without setuid bit

* Thu Jul 14 2011 Jan Kaluza <jkaluza@redhat.com> - 2.2.19-2
- fix #689091 - backported patch from 2.3 branch to support IPv6 in logresolve

* Fri Jul  1 2011 Joe Orton <jorton@redhat.com> - 2.2.19-1
- update to 2.2.19
- enable dbd, authn_dbd in default config

* Thu Apr 14 2011 Joe Orton <jorton@redhat.com> - 2.2.17-13
- fix path expansion in service files

* Tue Apr 12 2011 Joe Orton <jorton@redhat.com> - 2.2.17-12
- add systemd service files (#684175, thanks to Jóhann B. Guðmundsson)

* Wed Mar 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-11
- minor updates to httpd.conf
- drop old patches

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 2.2.17-10
- rebuild

* Wed Feb 23 2011 Joe Orton <jorton@redhat.com> - 2.2.17-9
- use arch-specific mmn

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Joe Orton <jorton@redhat.com> - 2.2.17-7
- generate dummy mod_ssl cert with CA:FALSE constraint (#667841)
- add man page stubs for httpd.event, httpd.worker
- drop distcache support
- add STOP_TIMEOUT support to init script

* Sat Jan  8 2011 Joe Orton <jorton@redhat.com> - 2.2.17-6
- update default SSLCipherSuite per upstream trunk

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-5
- fix requires (#667397)

* Wed Jan  5 2011 Joe Orton <jorton@redhat.com> - 2.2.17-4
- de-ghost /var/run/httpd

* Tue Jan  4 2011 Joe Orton <jorton@redhat.com> - 2.2.17-3
- add tmpfiles.d configuration, ghost /var/run/httpd (#656600)

* Sat Nov 20 2010 Joe Orton <jorton@redhat.com> - 2.2.17-2
- drop setuid bit, use capabilities for suexec binary

* Wed Oct 27 2010 Joe Orton <jorton@redhat.com> - 2.2.17-1
- update to 2.2.17

* Fri Sep 10 2010 Joe Orton <jorton@redhat.com> - 2.2.16-2
- link everything using -z relro and -z now

* Mon Jul 26 2010 Joe Orton <jorton@redhat.com> - 2.2.16-1
- update to 2.2.16

* Fri Jul  9 2010 Joe Orton <jorton@redhat.com> - 2.2.15-3
- default config tweaks:
 * harden httpd.conf w.r.t. .htaccess restriction (#591293)
 * load mod_substitute, mod_version by default
 * drop proxy_ajp.conf, load mod_proxy_ajp in httpd.conf
 * add commented list of shipped-but-unloaded modules
 * bump up worker defaults a little
 * drop KeepAliveTimeout to 5 secs per upstream
- fix LSB compliance in init script (#522074)
- bundle NOTICE in -tools
- use init script in logrotate postrotate to pick up PIDFILE
- drop some old Obsoletes/Conflicts

* Sun Apr 04 2010 Robert Scheck <robert@fedoraproject.org> - 2.2.15-1
- update to 2.2.15 (#572404, #579311)

