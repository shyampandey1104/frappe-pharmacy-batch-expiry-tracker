"""Pharmaceutical Batch, Expiry & FEFO Inventory Engine for Frappe."""

from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class MedicineBatch(BaseModel):
    batch_no: str
    medicine_code: str
    medicine_name: str
    manufacturing_date: str
    expiry_date: str  # YYYY-MM-DD
    quantity: float
    mrp: float
    is_schedule_h: bool = False  # Prescription mandatory


class PharmaFEFOEngine:
    """Enforces First-Expiry-First-Out (FEFO) dispensing and expiry monitoring."""

    def __init__(self):
        self.inventory: Dict[str, List[MedicineBatch]] = {}

    def add_batch(self, batch: MedicineBatch):
        if batch.medicine_code not in self.inventory:
            self.inventory[batch.medicine_code] = []
        self.inventory[batch.medicine_code].append(batch)
        # Sort batches by expiry date (FEFO)
        self.inventory[batch.medicine_code].sort(key=lambda b: b.expiry_date)

    def allocate_fefo_stock(self, medicine_code: str, requested_qty: float) -> List[Dict[str, Any]]:
        """Allocate stock strictly using First-Expiry-First-Out."""
        if medicine_code not in self.inventory:
            raise ValueError(f"Medicine {medicine_code} not in stock")

        batches = self.inventory[medicine_code]
        allocated = []
        remaining_qty = requested_qty

        for b in batches:
            if b.quantity <= 0:
                continue
            take = min(b.quantity, remaining_qty)
            b.quantity -= take
            remaining_qty -= take

            allocated.append({
                "batch_no": b.batch_no,
                "expiry_date": b.expiry_date,
                "qty_allocated": take,
                "unit_price": b.mrp,
            })

            if remaining_qty <= 0:
                break

        if remaining_qty > 0:
            raise ValueError(f"Insufficient stock for {medicine_code}. Shortfall: {remaining_qty}")

        return allocated

    def get_near_expiry_alerts(self, reference_date_str: Optional[str] = None, alert_days: int = 90) -> List[Dict[str, Any]]:
        ref_dt = datetime.strptime(reference_date_str, "%Y-%m-%d").date() if reference_date_str else date.today()
        alerts = []

        for med_code, batch_list in self.inventory.items():
            for b in batch_list:
                if b.quantity <= 0:
                    continue
                exp_dt = datetime.strptime(b.expiry_date, "%Y-%m-%d").date()
                days_left = (exp_dt - ref_dt).days

                if days_left <= alert_days:
                    alerts.append({
                        "medicine_code": med_code,
                        "medicine_name": b.medicine_name,
                        "batch_no": b.batch_no,
                        "expiry_date": b.expiry_date,
                        "days_to_expiry": days_left,
                        "stock_quantity": b.quantity,
                        "status": "Expired" if days_left < 0 else "Near Expiry",
                    })

        return alerts
