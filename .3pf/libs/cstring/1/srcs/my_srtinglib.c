/*
** EPITECH PROJECT, 2024
** my_stringlib.c
** File description:
** The string.h functions.
*/
#include "../../include/header_lib.h"

int my_strlen(char const *str)
{
    int i = 0;

    if (str == NULL)
        return 0;
    while (str[i] != '\0')
        i++;
    return i;
}

char *my_strdup(char const *src)
{
    int i = 0;
    char *str;

    str = malloc(sizeof(char) * (my_strlen(src) + 1));
    if (str == NULL)
        return NULL;
    while (src[i] != '\0') {
        str[i] = src[i];
        i++;
    }
    str[i] = '\0';
    return str;
}

char *my_strcpy(char *dest, char const *src)
{
    int i = 0;

    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
    return dest;
}

int my_strcmp(char const *s1, char const *s2)
{
    int i = 0;

    if (s1 == NULL || s2 == NULL)
        return 1;
    while (s1[i] != '\0' && s2[i] != '\0') {
        if (s1[i] != s2[i])
            return s1[i] - s2[i];
        i++;
    }
    return s1[i] - s2[i];
}

int my_strncmp(char const *s1, char const *s2, int n)
{
    int i = 0;

    while (s1[i] != '\0' && s2[i] != '\0' && n > 1) {
        if (s1[i] != s2[i])
            return s1[i] - s2[i];
        i++;
        n--;
    }
    return s1[i] - s2[i];
}
