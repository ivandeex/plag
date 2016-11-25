#!/bin/bash
# PRAG development script
action="$1"
shift
extra_args="$*"

project_dir=$(dirname $(dirname $(readlink -f $0)))
cd $project_dir
[ -e .env ] && . .env


run_ansible()
{
  playbook="$1"
  ./bin/update-secrets.sh
  cd ansible
  ansible-playbook plays/$playbook.yml $extra_args
  cd ..
}

migrate_db()
{
  python manage.py makemigrations --noinput --exit
  python manage.py migrate --noinput
}

run_linters()
{
  flake8
}


set -x
case "$action" in
  prepare)
    migrate_db
    # Use `-v0` to silence verbose whitenoise messages:
    python manage.py collectstatic --noinput -v0
    ;;
  prod)
    run_linters
    ;;
  devel)
    pip -q install -r requirements/devel.txt
    migrate_db
    ;;
  test)
    # We do not let django create test database for security reasons.
    # Database is created manually by ansible, and here we supply the
    # `--keep` option telling django to skip creating and dropping.
    python manage.py check && \
    python manage.py test --keep --reverse --failfast --verbosity 2 $extra_args
    ;;
  cover)
    coverage run --source=. manage.py test -k $extra_args
    coverage report
    ;;
  lint)
    run_linters
    ;;
  live)
    TEST_LIVESERVER=1 python manage.py test --keep --liveserver=0.0.0.0:8000 --tag liveserver $extra_args
    ;;
  setup-devel|backup-db|install-server)
    run_ansible $action
    ;;
  *)
    set +x
    echo "usage: $0 ACTION|PLAYBOOK"
    echo "  ACTIONS:   prepare prod devel test cover lint live"
    echo "  PLAYBOOKS: setup-devel backup-db install-server"
    exit 1
esac
