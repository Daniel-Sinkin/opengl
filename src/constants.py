from enum import IntEnum, auto
from typing import TypeAlias

import pygame.constants
from glm import vec3


# fmt: off
###
# Enums
###
class MouseMode(IntEnum):
    FPS = auto()
    FREELOOK = auto()


###
# Quality of Life
###
vec3_0  = vec3(0.0, 0.0, 0.0)
vec3_1  = vec3(1.0, 1.0, 1.0)
vec3_x  = vec3(1.0, 0.0, 0.0)
vec3_y  = vec3(0.0, 1.0, 0.0)
vec3_z  = vec3(0.0, 0.0, 1.0)
vec3_xy = vec3(1.0, 1.0, 0.0)
vec3_xz = vec3(1.0, 0.0, 1.0)
vec3_yz = vec3(0.0, 1.0, 1.0)

SECOND_TO_MS = 1e-4
MS_TO_SECOND = 1000

###
# TypeDefs
###
POINT: TypeAlias = tuple[float, float, float]
VERTEX_IDX: TypeAlias = tuple[int, int, int]

###
# Key Mappings
###
MOUSE_BUTTON_ID_TO_NAME_MAP: dict[int, str] = {
    pygame.constants.BUTTON_LEFT:      "BUTTON_LEFT",
    pygame.constants.BUTTON_MIDDLE:    "BUTTON_MIDDLE",
    pygame.constants.BUTTON_RIGHT:     "BUTTON_RIGHT",
    pygame.constants.BUTTON_WHEELDOWN: "BUTTON_WHEELDOWN",
    pygame.constants.BUTTON_WHEELUP:   "BUTTON_WHEELUP",
    pygame.constants.BUTTON_X1:        "BUTTON_X1",
    pygame.constants.BUTTON_X2:        "BUTTON_X2",
}

KEYBOARD_ID_TO_NAME_MAP: dict[int, str] = {
    pygame.constants.K_0:               "0",
    pygame.constants.K_1:               "1",
    pygame.constants.K_2:               "2",
    pygame.constants.K_3:               "3",
    pygame.constants.K_4:               "4",
    pygame.constants.K_5:               "5",
    pygame.constants.K_6:               "6",
    pygame.constants.K_7:               "7",
    pygame.constants.K_8:               "8",
    pygame.constants.K_9:               "9",
    pygame.constants.K_AC_BACK:         "AC_BACK",
    pygame.constants.K_AMPERSAND:       "AMPERSAND",
    pygame.constants.K_ASTERISK:        "ASTERISK",
    pygame.constants.K_AT:              "AT",
    pygame.constants.K_BACKQUOTE:       "BACKQUOTE",
    pygame.constants.K_BACKSLASH:       "BACKSLASH",
    pygame.constants.K_BACKSPACE:       "BACKSPACE",
    pygame.constants.K_BREAK:           "BREAK",
    pygame.constants.K_CAPSLOCK:        "CAPSLOCK",
    pygame.constants.K_CARET:           "CARET",
    pygame.constants.K_CLEAR:           "CLEAR",
    pygame.constants.K_COLON:           "COLON",
    pygame.constants.K_COMMA:           "COMMA",
    pygame.constants.K_CURRENCYSUBUNIT: "CURRENCYSUBUNIT",
    pygame.constants.K_CURRENCYUNIT:    "CURRENCYUNIT",
    pygame.constants.K_DELETE:          "DELETE",
    pygame.constants.K_DOLLAR:          "DOLLAR",
    pygame.constants.K_DOWN:            "DOWN",
    pygame.constants.K_END:             "END",
    pygame.constants.K_EQUALS:          "EQUALS",
    pygame.constants.K_ESCAPE:          "ESCAPE",
    pygame.constants.K_EURO:            "EURO",
    pygame.constants.K_EXCLAIM:         "EXCLAIM",
    pygame.constants.K_F1:              "F1",
    pygame.constants.K_F10:             "F10",
    pygame.constants.K_F11:             "F11",
    pygame.constants.K_F12:             "F12",
    pygame.constants.K_F13:             "F13",
    pygame.constants.K_F14:             "F14",
    pygame.constants.K_F15:             "F15",
    pygame.constants.K_F2:              "F2",
    pygame.constants.K_F3:              "F3",
    pygame.constants.K_F4:              "F4",
    pygame.constants.K_F5:              "F5",
    pygame.constants.K_F6:              "F6",
    pygame.constants.K_F7:              "F7",
    pygame.constants.K_F8:              "F8",
    pygame.constants.K_F9:              "F9",
    pygame.constants.K_GREATER:         "GREATER",
    pygame.constants.K_HASH:            "HASH",
    pygame.constants.K_HELP:            "HELP",
    pygame.constants.K_HOME:            "HOME",
    pygame.constants.K_INSERT:          "INSERT",
    pygame.constants.K_KP0:             "KP0",
    pygame.constants.K_KP1:             "KP1",
    pygame.constants.K_KP2:             "KP2",
    pygame.constants.K_KP3:             "KP3",
    pygame.constants.K_KP4:             "KP4",
    pygame.constants.K_KP5:             "KP5",
    pygame.constants.K_KP6:             "KP6",
    pygame.constants.K_KP7:             "KP7",
    pygame.constants.K_KP8:             "KP8",
    pygame.constants.K_KP9:             "KP9",
    pygame.constants.K_KP_0:            "KP_0",
    pygame.constants.K_KP_1:            "KP_1",
    pygame.constants.K_KP_2:            "KP_2",
    pygame.constants.K_KP_3:            "KP_3",
    pygame.constants.K_KP_4:            "KP_4",
    pygame.constants.K_KP_5:            "KP_5",
    pygame.constants.K_KP_6:            "KP_6",
    pygame.constants.K_KP_7:            "KP_7",
    pygame.constants.K_KP_8:            "KP_8",
    pygame.constants.K_KP_9:            "KP_9",
    pygame.constants.K_KP_DIVIDE:       "KP_DIVIDE",
    pygame.constants.K_KP_ENTER:        "KP_ENTER",
    pygame.constants.K_KP_EQUALS:       "KP_EQUALS",
    pygame.constants.K_KP_MINUS:        "KP_MINUS",
    pygame.constants.K_KP_MULTIPLY:     "KP_MULTIPLY",
    pygame.constants.K_KP_PERIOD:       "KP_PERIOD",
    pygame.constants.K_KP_PLUS:         "KP_PLUS",
    pygame.constants.K_LALT:            "LALT",
    pygame.constants.K_LCTRL:           "LCTRL",
    pygame.constants.K_LEFT:            "LEFT",
    pygame.constants.K_LEFTBRACKET:     "LEFTBRACKET",
    pygame.constants.K_LEFTPAREN:       "LEFTPAREN",
    pygame.constants.K_LESS:            "LESS",
    pygame.constants.K_LGUI:            "LGUI",
    pygame.constants.K_LMETA:           "LMETA",
    pygame.constants.K_LSHIFT:          "LSHIFT",
    pygame.constants.K_LSUPER:          "LSUPER",
    pygame.constants.K_MENU:            "MENU",
    pygame.constants.K_MINUS:           "MINUS",
    pygame.constants.K_MODE:            "MODE",
    pygame.constants.K_NUMLOCK:         "NUMLOCK",
    pygame.constants.K_NUMLOCKCLEAR:    "NUMLOCKCLEAR",
    pygame.constants.K_PAGEDOWN:        "PAGEDOWN",
    pygame.constants.K_PAGEUP:          "PAGEUP",
    pygame.constants.K_PAUSE:           "PAUSE",
    pygame.constants.K_PERCENT:         "PERCENT",
    pygame.constants.K_PERIOD:          "PERIOD",
    pygame.constants.K_PLUS:            "PLUS",
    pygame.constants.K_POWER:           "POWER",
    pygame.constants.K_PRINT:           "PRINT",
    pygame.constants.K_PRINTSCREEN:     "PRINTSCREEN",
    pygame.constants.K_QUESTION:        "QUESTION",
    pygame.constants.K_QUOTE:           "QUOTE",
    pygame.constants.K_QUOTEDBL:        "QUOTEDBL",
    pygame.constants.K_RALT:            "RALT",
    pygame.constants.K_RCTRL:           "RCTRL",
    pygame.constants.K_RETURN:          "RETURN",
    pygame.constants.K_RGUI:            "RGUI",
    pygame.constants.K_RIGHT:           "RIGHT",
    pygame.constants.K_RIGHTBRACKET:    "RIGHTBRACKET",
    pygame.constants.K_RIGHTPAREN:      "RIGHTPAREN",
    pygame.constants.K_RMETA:           "RMETA",
    pygame.constants.K_RSHIFT:          "RSHIFT",
    pygame.constants.K_RSUPER:          "RSUPER",
    pygame.constants.K_SCROLLLOCK:      "SCROLLLOCK",
    pygame.constants.K_SCROLLOCK:       "SCROLLOCK",
    pygame.constants.K_SEMICOLON:       "SEMICOLON",
    pygame.constants.K_SLASH:           "SLASH",
    pygame.constants.K_SPACE:           "SPACE",
    pygame.constants.K_SYSREQ:          "SYSREQ",
    pygame.constants.K_TAB:             "TAB",
    pygame.constants.K_UNDERSCORE:      "UNDERSCORE",
    pygame.constants.K_UNKNOWN:         "UNKNOWN",
    pygame.constants.K_UP:              "UP",
    pygame.constants.K_a:               "a",
    pygame.constants.K_b:               "b",
    pygame.constants.K_c:               "c",
    pygame.constants.K_d:               "d",
    pygame.constants.K_e:               "e",
    pygame.constants.K_f:               "f",
    pygame.constants.K_g:               "g",
    pygame.constants.K_h:               "h",
    pygame.constants.K_i:               "i",
    pygame.constants.K_j:               "j",
    pygame.constants.K_k:               "k",
    pygame.constants.K_l:               "l",
    pygame.constants.K_m:               "m",
    pygame.constants.K_n:               "n",
    pygame.constants.K_o:               "o",
    pygame.constants.K_p:               "p",
    pygame.constants.K_q:               "q",
    pygame.constants.K_r:               "r",
    pygame.constants.K_s:               "s",
    pygame.constants.K_t:               "t",
    pygame.constants.K_u:               "u",
    pygame.constants.K_v:               "v",
    pygame.constants.K_w:               "w",
    pygame.constants.K_x:               "x",
    pygame.constants.K_y:               "y",
    pygame.constants.K_z:               "z",
}

CONTROLLER_ID_TO_NAME_MAP: dict[int, str] = {
    pygame.constants.CONTROLLER_BUTTON_A:             "A",
    pygame.constants.CONTROLLER_BUTTON_B:             "B",
    pygame.constants.CONTROLLER_BUTTON_BACK:          "BACK",
    pygame.constants.CONTROLLER_BUTTON_DPAD_DOWN:     "DPAD_DOWN",
    pygame.constants.CONTROLLER_BUTTON_DPAD_LEFT:     "DPAD_LEFT",
    pygame.constants.CONTROLLER_BUTTON_DPAD_RIGHT:    "DPAD_RIGHT",
    pygame.constants.CONTROLLER_BUTTON_DPAD_UP:       "DPAD_UP",
    pygame.constants.CONTROLLER_BUTTON_GUIDE:         "GUIDE",
    pygame.constants.CONTROLLER_BUTTON_INVALID:       "INVALID",
    pygame.constants.CONTROLLER_BUTTON_LEFTSHOULDER:  "LEFTSHOULDER",
    pygame.constants.CONTROLLER_BUTTON_LEFTSTICK:     "LEFTSTICK",
    pygame.constants.CONTROLLER_BUTTON_MAX:           "MAX",
    pygame.constants.CONTROLLER_BUTTON_RIGHTSHOULDER: "RIGHTSHOULDER",
    pygame.constants.CONTROLLER_BUTTON_RIGHTSTICK:    "RIGHTSTICK",
    pygame.constants.CONTROLLER_BUTTON_START:         "START",
    pygame.constants.CONTROLLER_BUTTON_X:             "X",
    pygame.constants.CONTROLLER_BUTTON_Y:             "Y",
}
# fmt: on
