"""
test_inheritance.py
CSL 112 Lab: Polymorphism & Dynamic Dispatch Verification

Builds a mixed-type payroll queue and proves that a single loop, written
against the abstract User interface, produces different behaviour per
object depending on its actual runtime class.
"""

from institutional_system import User, StudentUser, LecturerUser, ResearchAssistant


def make_payroll_queue():
    roster = [
        StudentUser(
            user_id="S-200",
            full_name="Chidinma Eze",
            email="c.eze@fuep.edu.ng",
            stipend_rate=40000.00,
            courses_enrolled=5,
        ),
        LecturerUser(
            user_id="L-100",
            full_name="Engr. Yusuf Bala",
            email="y.bala@fuep.edu.ng",
            base_salary=280000.00,
            overtime_hours=10,
            hourly_rate=4000.00,
        ),
        ResearchAssistant(
            user_id="RA-300",
            full_name="Ifeoma Nwachukwu",
            email="i.nwachukwu@fuep.edu.ng",
            stipend_rate=48000.00,
            courses_enrolled=3,
            research_grant_allowance=20000.00,
        ),
    ]
    return roster


def process_payroll(payroll_queue):
    """
    Walks payroll_queue and calls calculate_monthly_payout() on each entry.

    Dynamic dispatch, explained inline:
    --------------------------------------------------------------------
    `entry` is declared/typed as a plain User throughout this loop - the
    code never asks "is this a LecturerUser?" or "is this a StudentUser?".
    Yet entry.calculate_monthly_payout() still runs the RIGHT version of
    the method for whichever concrete object entry currently points to,
    because Python looks up the method on the object's actual class at
    call time (runtime), not on the declared/reference type. That
    late-binding behaviour is exactly what "polymorphism via dynamic
    dispatch" means.
    --------------------------------------------------------------------
    """
    grand_total = 0.0
    for entry in payroll_queue:
        pay = entry.calculate_monthly_payout()  # <- resolved at runtime
        grand_total += pay
        print(f"{entry} => NGN {pay:,.2f}")
    print(f"\nGrand total payout: NGN {grand_total:,.2f}")
    return grand_total


def check_abstract_instantiation_blocked():
    outcome = "FAIL"
    try:
        User("Z-1", "Blocked User", "blocked@fuep.edu.ng")
    except TypeError:
        outcome = "PASS"
    print(f"[{outcome}] Direct User(...) instantiation should raise TypeError")


def check_incomplete_subclass_blocked():
    class NotQuiteAUser(User):
        pass  # missing calculate_monthly_payout override

    outcome = "FAIL"
    try:
        NotQuiteAUser("Z-2", "Also Blocked", "blocked2@fuep.edu.ng")
    except TypeError:
        outcome = "PASS"
    print(f"[{outcome}] Subclass without calculate_monthly_payout() should raise TypeError")


def main():
    print("--- Payroll Run ---")
    process_payroll(make_payroll_queue())
    print("\n--- Contract Rule Checks ---")
    check_abstract_instantiation_blocked()
    check_incomplete_subclass_blocked()


if __name__ == "__main__":
    main()
