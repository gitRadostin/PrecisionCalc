from decimal import Decimal, getcontext
import numpy as np
import mpmath
import cmath
import scipy
import sympy
from time import perf_counter
from sys import set_int_max_str_digits, exit

input_attemps: int = 0
precision: int = 100 # default value

while True:
    if input_attemps >= 3:
        print("[ERROR]   Too many invalid inputs, exiting.")
        exit()

    try:
        precision_input: str = input(f"Enter precision for constants and significands (default {precision}): ").strip()

        if precision_input == '':
            break

        precision_input_int: int = int(precision_input)

        if precision_input_int < 0:
            print("[ERROR]   Precision must be a positive integer.")
            input_attemps += 1

        elif precision_input_int == 0:
            print("[ERROR]   Precision must be 1 or greater.")
            input_attemps += 1

        else:
            precision = precision_input_int
            break

    except ValueError:
        print("[ERROR]   Enter a valid integer.")
        input_attemps += 1

set_int_max_str_digits(0)

ctx = getcontext()
ctx.prec = precision
ctx.Emax = 999_999_999_999_999_999
ctx.Emin = -999_999_999_999_999_999

mpmath.mp.dps = precision * 10

def main():
    print("\nEnter 'exit' or 'quit' to exit.")

    is_exit: bool = False

    while not is_exit:
        input_equation: str = input("\n[INPUT]   ").strip()

        if input_equation in ('exit', 'quit'):
            is_exit = True
            break

        if input_equation != '':
            user_confirm_eval: str = input("[CONFIRM] Do you want to run the evaluation/calculation? (Y/n): ").strip().lower()

            try:
                if user_confirm_eval in ('y', 'yes', ''):
                    start_time = Decimal(str(perf_counter())) # ensure no floating point inaccuracies with Decimal
                    output_number = Decimal(str(eval(input_equation)))
                    end_time = Decimal(str(perf_counter()))

                    total_time_sec = end_time - start_time

                    total_time_ns = total_time_sec * 1_000_000_000 # nanoseconds
                    total_time_min = total_time_sec / 60
                    total_time_hr = (total_time_sec / 60) / 60


                    if (Decimal(str(mpmath.fabs(output_number))) >= Decimal('1e+100')) or (Decimal(str(mpmath.fabs(output_number))) <= Decimal('1e-100')):
                        print(f"[OUTPUT]  {output_number:,.{precision}e}")
                    else:
                        print(f"[OUTPUT]  {output_number:,}")

                    print(f"\n              Calculation time: {total_time_ns:,.2f} ns")
                    print(f"                                {total_time_sec:,.10f} sec")
                    print(f"                                {total_time_min:,.2f} min")
                    print(f"                                {total_time_hr:,.2f} hr")

                elif user_confirm_eval in ('n', 'no', 'exit', 'quit'):
                    print("Exiting.")
                    is_exit = True
                    break

                else:
                    print(f"[ERROR]   Invalid option '{user_confirm_eval}'")

            except Exception as e:
                print(f"[ERROR]   {e}")

if __name__ == '__main__':
    main()
