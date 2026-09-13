#!/usr/bin/env bash
# loop 套件统一 lint：black（110 列）+ flake8（F 类必须为 0；E203/W503 与 black 冲突忽略；E501 交给 black）
# 用法：loop/lint.sh [--fix] [paths...]   默认检查 loop/ 下全部 .py
set -u
cd "$(dirname "$0")/.." || exit 1
FIX=0; [ "${1:-}" = "--fix" ] && { FIX=1; shift; }
PATHS=("$@"); [ ${#PATHS[@]} -eq 0 ] && PATHS=(loop)
if [ $FIX = 1 ]; then black -q -l 110 "${PATHS[@]}"; else black -l 110 --check "${PATHS[@]}" || exit 1; fi
flake8 --max-line-length 120 --extend-ignore E203,W503,E501 --exclude __pycache__,.pytest_cache,loop/work "${PATHS[@]}"
