#!/bin/sh
set -eu

source_dir=${srcdir:-.}
daemon_config="$source_dir/contrib/init/g15daemon.conf"
keyd_config="$source_dir/contrib/keyd/g15.conf"
daemon_main="$source_dir/g15daemon/main.c"
linked_lists="$source_dir/g15daemon/linked_lists.c"

grep -q '^Keyboard Backlight Level: 2$' "$daemon_config"
grep -q '^default_layout = m1$' "$keyd_config"

for profile in m1 m2 m3; do
    grep -q "^\[$profile:layout\]$" "$keyd_config"
done

noop_count=$(grep -Ec '^g([1-9]|1[0-8]) = noop$' "$keyd_config")
test "$noop_count" -eq 54

test "$(grep -Ec 'apply_startup_keyboard_state\((lcdlist|masterlist)\);' "$daemon_main")" -eq 3
test "$(grep -c 'mkey_state = G15_LED_M1;' "$linked_lists")" -eq 2

if command -v keyd >/dev/null 2>&1; then
    keyd check "$keyd_config"
fi

echo "Konfigurationsprüfungen erfolgreich."
