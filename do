#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# fmt -> fmt code
_fmt() {
	local retcode
	retcode=0
	if [ "$CI" -eq 0 ]; then
		isort -q "${ROOT}/adf" || retcode=$?
	else
		isort -q --check "${ROOT}/adf" || retcode=$?
	fi
	if [ "$CI" -eq 0 ]; then
		black -q "${ROOT}/adf" || retcode=$?
	else
		black -q --check --diff "${ROOT}/adf" || retcode=$?
	fi
	flake8 "${ROOT}/adf" || retcode=$?
	[ "$retcode" -eq 0 ] && echo "Great, all is ok !"
	return "$retcode"
}

help() {
	echo "Available commands :"
	grep "^#[^!]" "$0" | cut -d "#" -f 2
}

main() {
	[ $# -eq 0 ] && help >&2 && return 1
	local cmd
	cmd=$1
	shift
	"_$cmd" "$@"
}

main "$@"
