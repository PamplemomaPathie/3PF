/*
** EPITECH PROJECT, 2025
** my_stringlib_tests.c
** File description:
** test each functions of the strings functions
*/

#include "criterion/criterion.h"
#include "criterion/redirect.h"
#include "../../include/header_main.h"

//**********************************
// -------- STRING FUNCTION --------
//**********************************

Test(my_strlen, full_covr)
{
    char str[7] = "cbbcbb\0";

    cr_assert_eq(my_strlen(str), 6);
}

Test(my_strlen_error, full_covr)
{
    char *str = NULL;

    cr_assert_eq(my_strlen(str), 0);
}

Test(my_strdup, full_covr, .init = cr_redirect_stdout)
{
    char *dup = my_strdup("Hello");

    mini_printf("%s\n", dup);
    cr_assert_stdout_eq_str("Hello\n");
}

Test(my_strcpy, full_covr, .init = cr_redirect_stdout)
{
    char *dup = my_strdup("Hello");
    char *cpy;

    mini_printf("%s\n", my_strcpy(cpy, dup));
    cr_assert_stdout_eq_str("Hello\n");
}

Test(my_strcmp, full_covr)
{
    char str[7] = "cbbcbb\0";
    char src[7] = "caacaa\0";

    cr_assert_eq(my_strcmp(str, str), 0);
    cr_assert_eq(my_strcmp(str, src), 1);
    cr_assert_eq(my_strcmp(src, str), -1);
}

Test(my_strncmp, full_covr)
{
    char str[7] = "cbbcbb\0";
    char src[7] = "caacaa\0";

    cr_assert_eq(my_strncmp(str, str, 1), 0);
    cr_assert_eq(my_strncmp(str, src, 1), 0);
    cr_assert_eq(my_strncmp(str, src, 6), 1);
    cr_assert_eq(my_strncmp(src, str, 6), -1);
}
