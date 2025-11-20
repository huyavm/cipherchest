from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_accounts: int
    expiring_accounts: int
    without_two_fa: int
    by_category: dict[str, int]
