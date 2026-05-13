#!/usr/bin/awk -f
# Update Exodus RPM spec file version and changelog
# Usage: awk -v version="X.Y.Z" -v date="..." -v git_email="..." -v git_username="..." -f update_specfile.awk exodus.spec

BEGIN {
  version = ENVIRON["EXODUS_VERSION"]

  if (version == "") {
    print "Error: EXODUS_VERSION environment variable is not defined." > "/dev/stderr"
    exit 1
  }

  date = ENVIRON["GIT_DATE"]
  git_user = ENVIRON["GIT_USER"]
  git_email = ENVIRON["GIT_EMAIL"]
}

/^Version:/ {
  if ($2 != version) {
    update_changelog = 1
    printf "Version:        %s\n", version
  } else {
    print $0
  }
  next
}

/^Release:/ {
  if (update_changelog) {
    print "Release:        1%{?dist}"
  } else {
    print $0
  }
  next
}

/^%changelog/ {
  print $0
  if (update_changelog) {
    printf "* %s %s <%s> - %s-1\n", date, git_user, git_email, version
    printf "- Update Exodus to version %s\n", version
  }
  next
}

{ print $0 }
