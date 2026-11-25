import { formatMoney, formatPrice, formatQuantity } from "../utils/format";
import Pl from "./Pl";
import { EmptyState } from "./StateViews";

export default function HoldingsTable({ holdings, currency }) {
  if (holdings.length === 0) {
    return (
      <EmptyState title="No open holdings">
        Holdings appear here once you record a buy. Fully sold positions drop off this list.
      </EmptyState>
    );
  }
  return (
    <div className="table-wrap">
      <table className="table">
        <caption className="visually-hidden">Current holdings by instrument, in {currency}</caption>
        <thead>
          <tr>
            <th scope="col">Instrument</th>
            <th scope="col" className="num">Net qty</th>
            <th scope="col" className="num">Avg cost</th>
            <th scope="col" className="num">Invested</th>
            <th scope="col" className="num">Last price</th>
            <th scope="col" className="num">Value</th>
            <th scope="col" className="num">Unrealised P/L</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => (
            <tr key={h.instrument}>
              <th scope="row">{h.instrument}</th>
              <td className="num">{formatQuantity(h.net_quantity)}</td>
              <td className="num">{formatPrice(h.average_cost)}</td>
              <td className="num">{formatMoney(h.total_invested, currency)}</td>
              <td className="num">{formatPrice(h.last_price)}</td>
              <td className="num">{formatMoney(h.total_value, currency)}</td>
              <td className="num">
                <Pl value={h.unrealized_pl} currency={currency} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
