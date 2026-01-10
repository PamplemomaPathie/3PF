/*
** EPITECH PROJECT, 2026
** c_functions.c
** File description:
** The C functions.
*/

#include "../../include/header_lib.h"
#include <stdarg.h>

int bst_getnbr(char const *str, char c, int *pos)
{
    int i = *pos;
    int res = 0;
    int is_neg = 1;

    if (str == NULL)
        return FALSE;
    while (str[i] != c && str[i] != '\0' && !(str[i] >= '0' && str[i] <= '9'))
        i++;
    while (str[i] != c && str[i] != '\0' && str[i] >= '0' && str[i] <= '9') {
        if (i > 0 && str[i - 1] == '-')
            is_neg = -1;
        res = res * 10 + (str[i] - '0');
        i++;
    }
    *pos = i + 1;
    return res * is_neg;
}

int char_in_str(char ch, char const *str)
{
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ch)
            return TRUE;
    }
    return FALSE;
}

int my_getnbr(char const *str)
{
    int i = 0;
    int res = 0;
    int is_neg = 1;

    if (str == NULL)
        return FALSE;
    while (str[i] != '\0' && !(str[i] >= '0' && str[i] <= '9')) {
        if (str[i] == '-') {
            is_neg *= -1;
        }
        i++;
    }
    while (str[i] != '\0' && str[i] >= '0' && str[i] <= '9') {
        res = res * 10 + (str[i] - '0');
        i++;
    }
    return res * is_neg;
}

static int my_putstr(char const *str)
{
    int length = my_strlen(str);

    write(1, &str[0], length);
    return length;
}

static void my_putchar(char c)
{
    write(1, &c, 1);
}

static void my_put_nbr(int nb)
{
    if (nb < 0) {
        my_putstr("-");
        nb = nb * (-1);
    }
    if (nb == -2147483648) {
        my_putstr("2147483648");
    }
    if (nb <= 9 && nb >= 0) {
        my_putchar(nb + 48);
    } else if (nb > 9) {
        my_put_nbr(nb / 10);
        my_putchar(nb % 10 + 48);
    }
}

static int condition_flag(const char *s, int i, va_list arg)
{
    if (s[i + 1] == 's') {
        my_putstr(va_arg(arg, char *));
    }
    if (s[i + 1] == 'd' || s[i + 1] == 'i') {
        my_put_nbr(va_arg(arg, int));
    }
    if (s[i + 1] == 'c') {
        my_putchar(va_arg(arg, int));
    }
    if (s[i + 1] == '%') {
        my_putchar('%');
    }
    return i;
}

int mini_printf(const char *format, ...)
{
    va_list arg;

    va_start(arg, format);
    for (int i = 0; format[i] != '\0'; i++) {
        if (format[i] == '%') {
            i = condition_flag(format, i, arg);
            i += 1;
        } else {
            my_putchar(format[i]);
        }
    }
    va_end(arg);
    return TRUE;
}

int debug_print(char const *format, ...)
{
    va_list arg;

    va_start(arg, format);
    for (int i = 0; format[i] != '\0'; i++) {
        if (format[i] == '%') {
            i = condition_flag(format, i, arg);
            i += 1;
        } else {
            my_putchar(format[i]);
        }
    }
    va_end(arg);
    write(1, "\n", 1);
    return ERROR;
}
