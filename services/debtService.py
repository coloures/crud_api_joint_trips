from collections import defaultdict
from repositories import (
    ExpenseRepository,
    ExpenseAllocationRepository,
    TripMemberRepository
)


class DebtService:
    def __init__(self, expense_repo: ExpenseRepository,
                 allocation_repo: ExpenseAllocationRepository,
                 member_repo: TripMemberRepository):
        self.expense_repo = expense_repo
        self.allocation_repo = allocation_repo
        self.member_repo = member_repo

    async def calculate_balances(self, trip_id: int):
        expenses = await self.expense_repo.get_by_trip(trip_id)

        balances = defaultdict(float)

        for exp in expenses:
            allocations = await self.allocation_repo.get_by_expense(exp.id)

            for alloc in allocations:
                if alloc.is_paid:
                    continue

                balances[alloc.user_id] -= alloc.amount
                balances[exp.user_id_pay] += alloc.amount

        return balances

    async def calculate_debts(self, trip_id: int):
        balances = await self.calculate_balances(trip_id)

        debtors = []
        creditors = []

        for user_id, balance in balances.items():
            if balance < 0:
                debtors.append([user_id, -balance])
            elif balance > 0:
                creditors.append([user_id, balance])

        result = []

        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            d_user, d_amount = debtors[i]
            c_user, c_amount = creditors[j]

            amount = min(d_amount, c_amount)

            result.append({
                "fromUserId": d_user,
                "toUserId": c_user,
                "amount": round(amount, 2)
            })

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

        return result