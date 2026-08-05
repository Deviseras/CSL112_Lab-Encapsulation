"""
institutional_system.py
CSL 112 Lab: Institutional User & Payroll Management System

Implements an abstract User contract plus three concrete roles:
StudentUser, LecturerUser, and ResearchAssistant (multi-level).
"""

from abc import ABC, abstractmethod

# Module-level constant, kept outside the class on purpose so it reads
# like a policy value rather than a magic number buried in a method.
WELFARE_DUES_PERCENT = 0.02


class User(ABC):
    """Abstract root of the institutional-user hierarchy.

    Because this inherits from ABC and carries an @abstractmethod,
    Python refuses to build a bare `User(...)` instance - trying to do
    so raises TypeError before __init__ ever really "completes".
    """

    def __init__(self, user_id, full_name, email):
        self._user_id = user_id
        self._full_name = full_name
        self._email = email

    def get_user_id(self):
        return self._user_id

    def get_full_name(self):
        return self._full_name

    def get_email(self):
        return self._email

    def __str__(self):
        role = type(self).__name__
        return f"{role} | id={self._user_id} | name={self._full_name} | email={self._email}"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def calculate_monthly_payout(self):
        """Contract: subclasses decide how they get paid."""
        ...


class StudentUser(User):
    """Students earn a stipend, reduced by a fixed welfare-dues percentage."""

    def __init__(self, user_id, full_name, email, stipend_rate, courses_enrolled):
        super().__init__(user_id, full_name, email)
        self.__stipend_rate = stipend_rate
        self.__courses_enrolled = courses_enrolled

    @property
    def stipend_rate(self):
        return self.__stipend_rate

    @property
    def courses_enrolled(self):
        return self.__courses_enrolled

    def calculate_monthly_payout(self):
        dues = self.__stipend_rate * WELFARE_DUES_PERCENT
        return round(self.__stipend_rate - dues, 2)


class LecturerUser(User):
    """Lecturers earn a flat base salary plus paid overtime hours."""

    def __init__(self, user_id, full_name, email, base_salary, overtime_hours, hourly_rate):
        super().__init__(user_id, full_name, email)
        self.__base_salary = base_salary
        self.__overtime_hours = overtime_hours
        self.__hourly_rate = hourly_rate

    @property
    def base_salary(self):
        return self.__base_salary

    @property
    def overtime_hours(self):
        return self.__overtime_hours

    @property
    def hourly_rate(self):
        return self.__hourly_rate

    def calculate_monthly_payout(self):
        overtime_pay = self.__overtime_hours * self.__hourly_rate
        return round(self.__base_salary + overtime_pay, 2)


class ResearchAssistant(StudentUser):
    """A StudentUser who additionally receives a research grant allowance.

    Two levels deep: User -> StudentUser -> ResearchAssistant.
    """

    def __init__(self, user_id, full_name, email, stipend_rate,
                 courses_enrolled, research_grant_allowance):
        super().__init__(user_id, full_name, email, stipend_rate, courses_enrolled)
        self.__research_grant_allowance = research_grant_allowance

    @property
    def research_grant_allowance(self):
        return self.__research_grant_allowance

    def calculate_monthly_payout(self):
        # Chain up to StudentUser's payout first, then top it up.
        stipend_after_dues = super().calculate_monthly_payout()
        return round(stipend_after_dues + self.__research_grant_allowance, 2)


def _demo_edge_cases():
    """Part 4 sanity checks, runnable standalone with `python institutional_system.py`."""

    print("Edge case 1: instantiating the abstract User class directly")
    try:
        User("EDGE-1", "Nobody", "nobody@fuep.edu.ng")
        print("  -> unexpectedly succeeded (this should not happen)")
    except TypeError as err:
        print(f"  -> correctly blocked: {err}")

    print("Edge case 2: a subclass that skips calculate_monthly_payout()")

    class HalfBakedUser(User):
        """Deliberately incomplete - no override provided."""
        pass

    try:
        HalfBakedUser("EDGE-2", "Nobody Else", "nobody2@fuep.edu.ng")
        print("  -> unexpectedly succeeded (this should not happen)")
    except TypeError as err:
        print(f"  -> correctly blocked: {err}")


if __name__ == "__main__":
    _demo_edge_cases()
