"""Unit tests for PharmaFEFOEngine."""

from pharma.engine import PharmaFEFOEngine, MedicineBatch


def test_fefo_allocation():
    engine = PharmaFEFOEngine()
    # Batch A expires earlier than Batch B
    batch_a = MedicineBatch(batch_no="B-001", medicine_code="MED-PARA", medicine_name="Paracetamol 650", manufacturing_date="2026-01-01", expiry_date="2026-12-31", quantity=50.0, mrp=30.0)
    batch_b = MedicineBatch(batch_no="B-002", medicine_code="MED-PARA", medicine_name="Paracetamol 650", manufacturing_date="2026-03-01", expiry_date="2027-06-30", quantity=100.0, mrp=30.0)

    engine.add_batch(batch_b)
    engine.add_batch(batch_a)

    # Allocate 70 units: Should take 50 from Batch A, 20 from Batch B
    alloc = engine.allocate_fefo_stock("MED-PARA", 70.0)
    assert len(alloc) == 2
    assert alloc[0]["batch_no"] == "B-001"
    assert alloc[0]["qty_allocated"] == 50.0
    assert alloc[1]["batch_no"] == "B-002"
    assert alloc[1]["qty_allocated"] == 20.0
