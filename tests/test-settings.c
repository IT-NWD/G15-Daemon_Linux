#include <assert.h>
#include <stddef.h>

#include "settings.h"

static void accepts_valid_levels(void) {
	unsigned int level = 99;

	assert(g15daemon_parse_backlight_level("0", &level) == 0);
	assert(level == 0);
	assert(g15daemon_parse_backlight_level("1", &level) == 0);
	assert(level == 1);
	assert(g15daemon_parse_backlight_level("2", &level) == 0);
	assert(level == 2);
}

static void rejects_invalid_levels(void) {
	unsigned int level = 99;

	assert(g15daemon_parse_backlight_level(NULL, &level) == -1);
	assert(g15daemon_parse_backlight_level("", &level) == -1);
	assert(g15daemon_parse_backlight_level("-1", &level) == -1);
	assert(g15daemon_parse_backlight_level("3", &level) == -1);
	assert(g15daemon_parse_backlight_level("2x", &level) == -1);
	assert(g15daemon_parse_backlight_level(" 2", &level) == 0);
	assert(level == 2);
	assert(g15daemon_parse_backlight_level("2 ", &level) == -1);
	assert(g15daemon_parse_backlight_level("1", NULL) == -1);
}

int main(void) {
	accepts_valid_levels();
	rejects_invalid_levels();
	return 0;
}
