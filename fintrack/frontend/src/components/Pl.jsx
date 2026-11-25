import { formatSignedMoney, formatSignedPercent, plClass } from "../utils/format";

/** Profit/loss. Colour is only ever an addition to the +/− sign. */
export default function Pl({ value, currency, percent }) {
  return (
    <span className={`pl ${plClass(value)}`}>
      {formatSignedMoney(value, currency)}
      {percent !== undefined && ` (${formatSignedPercent(percent)})`}
    </span>
  );
}
