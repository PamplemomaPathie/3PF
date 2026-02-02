/*
** EPITECH PROJECT, 2025
** lib_test.c
** File description:
** test each function of lib
*/

#include "criterion/criterion.h"
#include "criterion/redirect.h"
#include "../../include/header_main.h"

//**********************************
// ------ MINI_PRINTF FUNCTION------
//**********************************

Test(mini_printf_str, full_covr, .init = cr_redirect_stdout)
{
    char *str = "hello";

    mini_printf("%s\n", str);
    cr_assert_stdout_eq_str("hello\n");
}

Test(mini_printf_char, full_covr, .init = cr_redirect_stdout)
{
    mini_printf("%c %%", '\n');
    cr_assert_stdout_eq_str("\n %");
}

Test(mini_printf_num, full_covr, .init = cr_redirect_stdout)
{
    mini_printf("%d %d\n", 2, -25);
    cr_assert_stdout_eq_str("2 -25\n");
}

Test(mini_printf_overflow, full_covr, .init = cr_redirect_stdout)
{
    mini_printf("%d\n", -2147483647 - 1);
    cr_assert_stdout_eq_str("-2147483648\n");
}

//**********************************
// ------ DEBUG_PRINT FUNCTION------
//**********************************

Test(debug_print_test, full_covr, .init = cr_redirect_stdout)
{
    char *str = "hello";

    debug_print("\n %s\n", str);
}

//**********************************
// --------- LIB FUNCTIONS ---------
//**********************************

Test(my_getnbr, full_covr)
{
    char str[7] = "c-1bbc\0";
    char src[7] = "caac45\0";

    cr_assert_eq(my_getnbr(str), -1);
    cr_assert_eq(my_getnbr(src), 45);
}

Test(my_getnbr_error, full_covr)
{
    char *str = NULL;

    cr_assert_eq(my_getnbr(str), 0);
}

Test(char_in_str_true, full_covr)
{
    cr_assert_eq(char_in_str('o', "bonjour"), TRUE);
}

Test(char_in_str_false, full_covr)
{
    cr_assert_eq(char_in_str('z', "bonjour"), FALSE);
}
Test(bst_getnbr_valid_input, full_covr)
{
    char str[] = "abc-123,456";
    int pos = 0;

    cr_assert_eq(bst_getnbr(str, ',', &pos), -123);
    cr_assert_eq(pos, 8);
}

Test(bst_getnbr_multiple_numbers, full_covr)
{
    char str[] = "123,456,789";
    int pos = 0;

    cr_assert_eq(bst_getnbr(str, ',', &pos), 123);
    cr_assert_eq(pos, 4);
    cr_assert_eq(bst_getnbr(str, ',', &pos), 456);
    cr_assert_eq(pos, 8);
    cr_assert_eq(bst_getnbr(str, ',', &pos), 789);
    cr_assert_eq(pos, 12);
}

Test(bst_getnbr_no_numbers, full_covr)
{
    char str[] = "abc,def";
    int pos = 0;

    cr_assert_eq(bst_getnbr(str, ',', &pos), 0);
    cr_assert_eq(pos, 4);
    cr_assert_eq(bst_getnbr(str, ',', &pos), 0);
    cr_assert_eq(pos, 8);
}

Test(bst_getnbr_null_string, full_covr)
{
    int pos = 0;

    cr_assert_eq(bst_getnbr(NULL, ',', &pos), FALSE);
    cr_assert_eq(pos, 0);
}

Test(bst_getnbr_empty_string, full_covr)
{
    char str[] = "";
    int pos = 0;

    cr_assert_eq(bst_getnbr(str, ',', &pos), 0);
    cr_assert_eq(pos, 1);
}

Test(bst_getnbr_negative_number, full_covr)
{
    char str[] = "-42,100";
    int pos = 0;

    cr_assert_eq(bst_getnbr(str, ',', &pos), -42);
    cr_assert_eq(pos, 4);
    cr_assert_eq(bst_getnbr(str, ',', &pos), 100);
    cr_assert_eq(pos, 8);
}
