# TODO
# - package socketserver config (separate package)
%include	/usr/lib/rpm/macros.perl
Summary:	Zmanda MySQL Backup and Recovery Manager for MySQL
Name:		mysql-zrm
Version:	3.0
Release:	0.5
License:	GPL v2
Group:		Applications/Databases
Source0:	http://www.zmanda.com/downloads/community/ZRM-MySQL/%{version}/Source/MySQL-zrm-%{version}-release.tar.gz
# Source0-md5:	dbc09406c04f5a21c09d582af6b1fe34
Patch0:		tar-options.patch
URL:		http://www.zmanda.com/backup-mysql.html
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	%{name}-client = %{version}-%{release}
Requires:	bash
Suggests:	gnupg
Suggests:	lvm2
Suggests:	mailx
Suggests:	mysql-client
Suggests:	sudo
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib

%description
Zmanda Recovery Manager (ZRM) for MySQL simplifies the life of a
Database Administrator who needs an easy-to-use yet flexible and
robust backup and recovery solution for MySQL server. With ZRM for
MySQL you can:
- Schedule full and incremental backups of your MySQL database.
- Start immediate backup or postpone scheduled backups based on
  thresholds defined by you.
- Choose to do more flexible logical or faster raw backups of your
  database.
- Perform backup that is the best match for your storage engine and
  your MySQL configuration.
- Backup your remote MySQL database through a firewall.
- Configure on-the-fly compression and/or encryption of your MySQL
  backups to meet your storage and security needs.
- Get e-mail notification about the status of your backups and receive
  MySQL backup reports via RSS feed.
- Monitor and browse your backups.
- Define retention policies and delete backups that have expired.
- Recover a database easily to any point in time or to any particular
  transaction, e.g. just before a user made an error.
- Parse binary logs to search and filter MySQL logs for operational
  and security reasons.

%package client
Summary:	Zmanda Recovery Manager for MySQL client
Group:		Applications/Databases

%description client
Zmanda Recovery Manager (ZRM) for MySQL is a backup and recovery
manager for MySQL databases with enterprise features.

ZRM client must be installed on MySQL servers that are backed up ZRM
for MySQL remotely.

%prep
%setup -qc
%patch0 -p1

mv .%{_docdir}/MySQL-zrm-%{version} doc
mv doc/* .

# solaris inetd
mv .%{_datadir}/%{name}/plugins/xinetd.smf .

# TODO: package later
mv .%{_sysconfdir}/xinetd.d/mysql-zrm-socket-server .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
cp -a etc usr var $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL README
%doc README-plugin-*
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/mysql-zrm-release
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/RSS.header
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mysql-zrm-reporter.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/mysql-zrm.conf
%attr(755,root,root) %{_bindir}/mysql-zrm
%attr(755,root,root) %{_bindir}/mysql-zrm-abort-backup
%attr(755,root,root) %{_bindir}/mysql-zrm-backup
%attr(755,root,root) %{_bindir}/mysql-zrm-check
%attr(755,root,root) %{_bindir}/mysql-zrm-extract-backup
%attr(755,root,root) %{_bindir}/mysql-zrm-getconf
%attr(755,root,root) %{_bindir}/mysql-zrm-list
%attr(755,root,root) %{_bindir}/mysql-zrm-manage-backup
%attr(755,root,root) %{_bindir}/mysql-zrm-migrate-file-ownership
%attr(755,root,root) %{_bindir}/mysql-zrm-parse-binlogs
%attr(755,root,root) %{_bindir}/mysql-zrm-purge
%attr(755,root,root) %{_bindir}/mysql-zrm-reporter
%attr(755,root,root) %{_bindir}/mysql-zrm-restore
%attr(755,root,root) %{_bindir}/mysql-zrm-scheduler
%attr(755,root,root) %{_bindir}/mysql-zrm-verify-backup
%attr(755,root,root) %{_bindir}/zrm-pre-scheduler
%{_mandir}/man1/mysql-zrm-abort-backup.1*
%{_mandir}/man1/mysql-zrm-backup.1*
%{_mandir}/man1/mysql-zrm-check.1*
%{_mandir}/man1/mysql-zrm-extract-backup.1*
%{_mandir}/man1/mysql-zrm-list.1*
%{_mandir}/man1/mysql-zrm-manage-backup.1*
%{_mandir}/man1/mysql-zrm-parse-binlogs.1*
%{_mandir}/man1/mysql-zrm-purge.1*
%{_mandir}/man1/mysql-zrm-reporter.1*
%{_mandir}/man1/mysql-zrm-restore.1*
%{_mandir}/man1/mysql-zrm-scheduler.1*
%{_mandir}/man1/mysql-zrm-verify-backup.1*
%{_mandir}/man1/mysql-zrm.1*
%{_mandir}/man5/mysql-zrm-reporter.conf.5*
%{_mandir}/man5/mysql-zrm.conf.5*
%{_libdir}/%{name}/Data
%{_libdir}/%{name}/XML
%{_libdir}/%{name}/ZRM/Common.pm
%{_libdir}/%{name}/ZRM/MySQL.pm
%{_libdir}/%{name}/ZRM/Replication.pm
%attr(755,root,root) %{_datadir}/%{name}/plugins/encrypt.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/parse-binlogs.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/post-backup.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/post-restore.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/pre-backup.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/pre-restore.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/pre-scheduler-plugin.pl

%files client
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/ZRM
%{_libdir}/%{name}/ZRM/SnapshotCommon.pm
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/plugins
%attr(755,root,root) %{_datadir}/%{name}/plugins/lvm-snapshot.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/socket-copy.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/socket-server.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/ssh-copy.pl
%attr(755,root,root) %{_datadir}/%{name}/plugins/zfs-snapshot.pl
%dir /var/lib/%{name}
%dir /var/log/%{name}
%ghost /var/log/%{name}/%{name}.log
