/* Configuration value parsers which do not depend on daemon state. */

#include <errno.h>
#include <stdlib.h>

#include <libg15.h>

#include "settings.h"

int g15daemon_parse_backlight_level(const char *value, unsigned int *level) {
	char *end = NULL;
	long parsed;

	if (value == NULL || level == NULL)
		return -1;

	errno = 0;
	parsed = strtol(value, &end, 10);
	if (errno != 0 || end == value || *end != '\0' ||
		parsed < G15_BRIGHTNESS_DARK || parsed > G15_BRIGHTNESS_BRIGHT)
		return -1;

	*level = (unsigned int)parsed;
	return 0;
}
