function formatMoney(value, currency = "KES") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(Number(value) || 0);
}

export default function TransactionTable({ transactions, onDelete, currency = "KES" }) {
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
            <th>Instrument</th>
            <th>Qty</th>
            <th>Price</th>
            <th>Total</th>
            {onDelete ? <th /> : null}
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.trade_date}</td>
              <td className="kind">{transaction.type}</td>
              <td>{transaction.instrument}</td>
              <td>{transaction.quantity}</td>
              <td>{formatMoney(transaction.unit_price, currency)}</td>
              <td className={transaction.type === "SELL" ? "negative" : "positive"}>
                {formatMoney(transaction.total, currency)}
              </td>
              {onDelete ? (
                <td>
                  <button type="button" className="text-button" onClick={() => onDelete(transaction.id)}>
                    Remove
                  </button>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
