import { fireEvent, render, screen } from "@testing-library/react";
import TransactionTable from "../components/TransactionTable";

const rows = [
  { id: 1, instrument: "SCOM", type: "BUY", quantity: 1000, unit_price: 17.5, total: 17500, trade_date: "2026-01-05" },
  { id: 2, instrument: "KCB", type: "SELL", quantity: 200, unit_price: 40, total: 8000, trade_date: "2026-02-10" },
];

function setup(props = {}) {
  const onSort = vi.fn();
  const onDelete = vi.fn();
  render(
    <TransactionTable transactions={rows} currency="KES" sort="trade_date" order="desc" onSort={onSort} onDelete={onDelete} {...props} />,
  );
  return { onSort, onDelete };
}

describe("TransactionTable", () => {
  it("renders currency-formatted totals", () => {
    setup();
    expect(screen.getByText("KES 17,500.00")).toBeInTheDocument();
    expect(screen.getByText("KES 8,000.00")).toBeInTheDocument();
  });

  it("exposes the active sort order to assistive tech", () => {
    setup();
    expect(screen.getByRole("columnheader", { name: /date/i })).toHaveAttribute("aria-sort", "descending");
    expect(screen.getByRole("columnheader", { name: /instrument/i })).toHaveAttribute("aria-sort", "none");
  });

  it("calls onSort when a header button is clicked", () => {
    const { onSort } = setup();
    fireEvent.click(screen.getByRole("button", { name: /instrument/i }));
    expect(onSort).toHaveBeenCalledWith("instrument");
  });

  it("calls onDelete with the row", () => {
    const { onDelete } = setup();
    fireEvent.click(screen.getByRole("button", { name: /delete sell kcb/i }));
    expect(onDelete).toHaveBeenCalledWith(rows[1]);
  });
});
