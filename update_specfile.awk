#!/usr/bin/awk -f
# update_specfile.awk — update Exodus RPM spec file version and changelog
# Usage: awk -v version="X.Y.Z" -v date="..." -v git_email="..." -v git_username="..." -f update_specfile.awk exodus.spec

/^Version:/ {
  if ($2 != version) {
    update_changelog = 1
    print "Version:        " version
  } else {
    print
  }
  next
}

/^Release:/ {
  # Reset release to 1 on version change
  if (update_changelog) {
    print "Release:        1%{?dist}"
  } else {
    print
  }
  next
}

/^%changelog/ {
  print $0
  if (update_changelog) {
    printf "* %s %s <%s> - %s-1\n", date, git_username, git_email, version
    printf "- Update Exodus to version %s\n", version
  }
  next
}

{ print }
