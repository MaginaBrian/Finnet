function formatMoney(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number(value) || 0);
}

function signedAmount(transaction) {
  const amount = Number(transaction.amount) || 0;
  if (transaction.kind === "buy" || transaction.kind === "withdrawal") {
    return -amount;
  }
  return amount;
}

export default function TransactionTable({ transactions, onDelete }) {
  if (!transactions?.length) {
    return <p className="empty">No transactions yet.</p>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Type</th>
            <th>Symbol</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Amount</th>
            {onDelete ? <th /> : null}
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => {
            const amount = signedAmount(transaction);
            return (
              <tr key={transaction.id}>
                <td>{transaction.occurred_at.slice(0, 10)}</td>
                <td className="kind">{transaction.kind}</td>
                <td>{transaction.symbol || "—"}</td>
                <td>{transaction.quantity ?? "—"}</td>
                <td>{transaction.price == null ? "—" : formatMoney(transaction.price)}</td>
                <td className={amount < 0 ? "negative" : "positive"}>{formatMoney(amount)}</td>
                {onDelete ? (
                  <td>
                    <button type="button" className="text-button" onClick={() => onDelete(transaction.id)}>
                      Remove
                    </button>
                  </td>
                ) : null}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
